import os
import random
import threading
import time
import uuid
from enum import Enum

import vlc

MEDIA_ROOT = "/home/user/Music/"

RepeatMode = Enum("RepeatMode", "OFF ALL ONE")

def _check_name_start(name, num_dig):
    return name[0:num_dig].isdigit() and name[num_dig] == ' '

def _get_track_name(name):
    name = name[2:] if _check_name_start(name, 1) else \
           name[3:] if _check_name_start(name, 2) else \
           name[4:] if _check_name_start(name, 3) else \
           name
    return name.rsplit(".", 1)[0]


class MediaPlayer:
    root = None
    paused = True
    repeat = RepeatMode.OFF
    shuffle = False
    current_track = None
    current_track_index = -1
    current_track_uuid = None
    current_tracks = []
    albums = []
    playlists = []
    artists = []

    def __init__(self, music_path, shuffle, repeat):
        global MEDIA_ROOT

        MEDIA_ROOT   = music_path
        music        = os.listdir(MEDIA_ROOT)
        self.shuffle = shuffle
        self.repeat  = RepeatMode.ALL if repeat == "ALL" else \
                       RepeatMode.OFF if repeat == "OFF" else \
                       RepeatMode.ONE
        for name in music:
            if os.path.isdir(MEDIA_ROOT + name):
                self.albums.append(name)
                continue
            file = name.rsplit(".", 1)
            if len(file) > 1:
                if file[1] == "playlist":
                    self.playlists.append(name)
                elif file[1] == "artist":
                    self.artists.append(name)
        self.albums.sort()
        self.playlists.sort()
        self.artists.sort()

    def _play_checker(self):
        current_uuid = self.current_track_uuid
        while (not self.paused) and (current_uuid == self.current_track_uuid) and (self.current_track_index != -1):
            if self.current_track is None:
                self._next_track()
                self._play()
            time.sleep(.1)

    def _kill_playing(self):
        self.current_track.stop()
        self.current_track = None
        self.current_track_index = -1

    def _play(self):
        self.paused = False
        if self.current_track is None:
            self.current_track = vlc.MediaPlayer(MEDIA_ROOT + self.current_tracks[self.current_track_index][0] +
                                                        "/" + self.current_tracks[self.current_track_index][1])
        self.current_track.play()
        self.current_track_uuid = uuid.uuid1()
        threading.Thread(target=self._play_checker).start()

    def _new_play(self):
        self.current_track.stop()
        self.current_track = None
        self._play()

    def _pause(self):
        self.paused = True
        if self.current_track is not None:
            self.current_track.pause()

    def _next_track(self):
        if self.repeat == RepeatMode.ONE:
            self.current_track.stop()
            self.current_track.play()
        else:
            self.current_track_index += 1
            if self.current_track_index < len(self.current_tracks):
                self._new_play()
            else:
                if self.repeat == RepeatMode.ALL:
                    self.current_track_index = 0
                    self._new_play()
                else:
                    self._kill_playing()

    def _prev_track(self):
        if self.repeat == RepeatMode.ONE:
            self.current_track.stop()
            self.current_track.play()
        else:
            self.current_track_index -= 1
            if self.current_track_index == -1:
                if self.repeat == RepeatMode.ALL:
                    self.current_track_index = len(self.current_tracks) - 1
                    self._new_play()
                else:
                    self._kill_playing()
            elif self.current_track_index > -1:
                self._new_play()
            else:
                self.current_track_index = -1

    def _play_init(self):
        self.current_tracks = []
        self.current_track_index = 0

    def _init_album(self, album):
        track_names = os.listdir(MEDIA_ROOT + album)
        track_indexes = random.sample(range(0, len(track_names)), len(track_names)) if self.shuffle else \
                        list(range(0, len(track_names)))
        for i in track_indexes:
            self.current_tracks.append((album, track_names[i]))

    def _init_playlist(self, playlist, is_artist):
        playlist_file = open(MEDIA_ROOT + playlist + (".artist" if is_artist else ".playlist"), 'r').readlines()
        track_indexes = random.sample(range(0, len(playlist_file) // 3), len(playlist_file) // 3) if self.shuffle else \
                        list(range(0, len(playlist_file) // 3))
        for i in track_indexes:
            self.current_tracks.append((playlist_file[3 * i].strip(" \n"), playlist_file[3 * i + 1].strip(" \n")))

    def play(self):
        if self.current_track_index > -1:
            self._play()

    def pause(self):
        self._pause()

    def skip(self):
        if self.current_track_index > -1:
            self._next_track()

    def prev(self):
        if self.current_track_index > -1:
            self._prev_track()

    def play_track(self, album, track):
        self._play_init()
        # FIXME:  Add case for album == None
        self.current_tracks[0] = album + "/" + track
        self._play()

    def play_album(self, album):
        self._play_init()
        self._init_album(album)
        self._play()

    def play_playlist(self, playlist, is_artist=False):
        self._play_init()
        self._init_playlist(playlist, is_artist)
        self._play()

    def play_all(self):
        self._play_init()
        for album in self.albums:
            self._init_album(album)
        self._play()

    def get_albums(self):
        return self.albums

    def get_playlists(self, is_artist=False):
        return list(map(_get_track_name, self.artists if is_artist else self.playlists))

    def get_all_tracks(self):
        all_tracks = []
        for track_list in list(map(lambda album: os.listdir(MEDIA_ROOT + album), self.albums)):
            for track in track_list:
                all_tracks.append(_get_track_name(track))
        all_tracks.sort()
        return all_tracks

    @staticmethod
    def get_album_tracks(name):
        return list(map(_get_track_name, sorted(os.listdir(MEDIA_ROOT + name))))

    @staticmethod
    def get_playlist_tracks(name, is_artist=False):
        playlist_tracks = []
        playlist_file = list(open(MEDIA_ROOT + name + "." + ("artist" if is_artist else "playlist"), 'r'))
        for i in range(1, len(playlist_file), 3):
            playlist_tracks.append(playlist_file[i])
        return list(map(lambda track: _get_track_name(track), sorted(playlist_tracks)))

    def get_track_info(self):
        return "" if self.current_track_index == -1 else self.current_tracks[self.current_track_index][1], \
               "" if self.current_track_index == -1 else self.current_tracks[self.current_track_index][0], \
               ""
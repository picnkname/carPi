import os
import vlc

MEDIA_ROOT = "/home/user/Music/"

def check_name_start(name, num_dig):
    return name[0:num_dig].isdigit() and name[num_dig] == ' '

def get_track_name(name):
    name = name[2:] if check_name_start(name, 1) else \
           name[3:] if check_name_start(name, 2) else \
           name[4:] if check_name_start(name, 3) else \
           name
    return name.rsplit(".", 1)[0]


class MediaPlayer:
    root = None
    paused = False
    current_track = None
    albums = []
    playlists = []
    artists = []

    def __init__(self, music_path, start_playing):
        global MEDIA_ROOT

        MEDIA_ROOT = music_path
        music = os.listdir(MEDIA_ROOT)
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

    def play(self):
        self.paused = False
        # self.current_track.play()

    def pause(self):
        self.paused = True
        # self.current_track.pause()

    def play_track(self, album, track):
        print(album + " -> " + track)

    def play_album(self, album):
        print(album)

    def play_playlist(self, playlist, is_artist=False):
        print(playlist)

    def skip(self):
        return

    def prev(self):
        return

    def get_albums(self):
        return self.albums

    def get_playlists(self, is_artist=False):
        return list(map(get_track_name, self.artists if is_artist else self.playlists))

    def get_all_tracks(self):
        all_tracks = []
        for track_list in list(map(lambda album: os.listdir(MEDIA_ROOT + album), self.albums)):
            for track in track_list:
                all_tracks.append(get_track_name(track))
        all_tracks.sort()
        return all_tracks

    @staticmethod
    def get_album_tracks(name):
        return list(map(get_track_name, sorted(os.listdir(MEDIA_ROOT + name))))

    @staticmethod
    def get_playlist_tracks(name, is_artist=False):
        return list(map(lambda track: get_track_name(track),
                        sorted(list(map(lambda n: n.rsplit("/", 1)[1],
                                        open(MEDIA_ROOT + name + "." + ("artist" if is_artist else "playlist"), 'r'))))))

    def get_track_info(self):
        title, album, artist = "", "", ""
        title, album, artist = str(title).strip(" \n"), str(album).strip(" \n"), str(artist).strip(" \n")
        return title, album, artist

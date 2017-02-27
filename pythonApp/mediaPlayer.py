import vlc

MEDIA_ROOT = "/home/user/Music/"


class MediaPlayer:
    root = None
    current_track = None
    paused = False


    def __init__(self, music_path, start_playing):
        global MEDIA_ROOT
        MEDIA_ROOT = music_path

    def play(self):
        self.paused = False
        # self.current_track.play()

    def pause(self):
        self.paused = True
        # self.current_track.pause()

    def skip(self):
        return

    def prev(self):
        return

    def get_track_info(self):
        title, album, artist = "", "", ""
        title, album, artist = str(title).strip(" \n"), str(album).strip(" \n"), str(artist).strip(" \n")
        return title, album, artist


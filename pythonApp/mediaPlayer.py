import vlc


BACKGROUND_COLOR = "#2b2b2b"
FOREGROUND_COLOR = "#d9d9d9"
MEDIA_ROOT = "/home/user/Music/"
IMAGE_PATH = "images/mediaPlayer/"


class MediaPlayer:
    root = None
    current_track = None
    paused = False


    def __init__(self):
        return


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


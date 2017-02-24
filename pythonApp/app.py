from tkinter import *
import subprocess as sp
import time

import mediaPlayer as mediaPlayer


BACKGROUND_COLOR = "#2b2b2b"
FOREGROUND_COLOR = "#d9d9d9"
IMAGE_PATH = "images/"


class RootApp:
    root = None
    mp = None
    song_info = None
    clock_time = None
    volume = 0
    hotspot = False
    mp_controls = True
    aux = False

    status_frame = None
    hotspot_image = None
    hotspot_button = None
    clock_label = None
    power_off_image = None
    power_button = None

    media_control_frame = None
    toggle_mp_button_image = None
    toggle_mp_button = None
    prev_button_image = None
    prev_button = None
    play_pause_button_image = None
    play_pause_button = None
    skip_button_image = None
    skip_button = None
    aux_button_image = None
    aux_button = None

    mp_control_frame = None
    mp_buttons_controls_frame = None
    mp_pst_button_image = None
    mp_pst_button = None
    mp_psaapp_button_image = None
    mp_psaapp_button = None
    mp_sr_frame = None
    mp_shuffle_button_image = None
    mp_shuffle_button = None
    mp_repeat_button_image = None
    mp_repeat_button = None
    mp_artwork = None
    mp_aap_frame1 = None
    mp_aap_frame2 = None
    mp_aap_all_button_image = None
    mp_aap_all_button = None
    mp_aap_album_button_image = None
    mp_aap_album_button = None
    mp_aap_playlist_button_image = None
    mp_aap_playlist_button = None
    mp_aap_artist_button_image = None
    mp_aap_artist_button = None


    def __init__(self):
        self.root = Tk()
        self.mp = mediaPlayer.MediaPlayer()
        self.song_info = StringVar()
        self.clock_time = StringVar()
        self.draw_everything(True)

    def toggle_hotspot(self):
        self.hotspot = not self.hotspot
        self.draw_status_frame()

    def update_clock(self):
        self.clock_time.set(time.strftime("%I:%M:%S"))
        self.root.after(1000, self.update_clock)

    @staticmethod
    def power_off():
        sp.call(["sudo", "shutdown", "-h", "now"])

    def change_vol(self, new_vol):
        self.volume = new_vol
        # Note that my USB sound card doesn't output sound until 25%
        # The sound slider is on a 0-63 scale
        new_vol = 0 if int(new_vol) == 0 else (int(new_vol) - 1) * 1.22 + 25
        sp.call(["amixer", "-D", "pulse", "sset", "Master", str(new_vol) + "%"])

    def update_track_info(self):
        (title, album, artist) = self.mp.get_track_info()
        self.song_info.set("\n" +
                           ("[No Title Data]\n" if title == "" else title + "\n") +
                           ("[No Album Data]\n" if album == "" else album + "\n") +
                           ("[No Artist Data]\n" if artist == "" else artist + "\n"))
        self.root.after(250, self.update_track_info)

    def toggle_mp_controls(self):
        self.mp_controls = not self.mp_controls

    def prev(self):
        self.mp.prev()

    def play_pause(self):
        self.play_pause_button.config(image=PhotoImage(file=IMAGE_PATH + ("pause.gif" if self.mp.paused else "play.gif")))
        if self.mp.paused:
            self.mp.play()
        else:
            self.mp.pause()
        self.draw_media_control_frame()

    def skip(self):
        self.mp.skip()

    def toggle_aux(self):
        self.aux = not self.aux
        self.aux_button.config(image=PhotoImage(file=IMAGE_PATH + ("aux-on.gif" if self.aux else "aux-off.gif")))
        self.draw_media_control_frame()

    def play_selected_track(self):
        return

    def play_selected_aap(self):
        return

    def shuffle(self):
        return

    def repeat(self):
        return

    def aap_all(self):
        return

    def aap_album(self):
        return

    def aap_playlist(self):
        return

    def aap_artist(self):
        return

    def draw_status_frame(self, first_draw=False):
        if not first_draw:
            self.hotspot_button.pack_forget()
            self.hotspot_button.destroy()
            self.clock_label.pack_forget()
            self.clock_label.destroy()
            self.power_button.pack_forget()
            self.power_button.destroy()
        self.hotspot_image = PhotoImage(file=IMAGE_PATH + ("hotspot-on.gif" if self.hotspot else "hotspot-off.gif"))
        self.power_off_image = PhotoImage(file=IMAGE_PATH + "power.gif")
        self.hotspot_button = Button(self.status_frame, command=self.toggle_hotspot, image=self.hotspot_image)
        self.clock_label = Label(self.status_frame, textvariable=self.clock_time, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=("Arial", 52))
        self.power_button = Button(self.status_frame, command=self.power_off, image=self.power_off_image)
        self.hotspot_button.pack(side=LEFT)
        self.clock_label.pack(side=LEFT)
        self.power_button.pack(side=RIGHT)

    def draw_media_control_frame(self, first_draw=False):
        if not first_draw:
            self.toggle_mp_button.pack_forget()
            self.toggle_mp_button.destroy()
            self.prev_button.pack_forget()
            self.prev_button.destroy()
            self.play_pause_button.pack_forget()
            self.play_pause_button.destroy()
            self.skip_button.pack_forget()
            self.skip_button.destroy()
            self.aux_button.pack_forget()
            self.aux_button.destroy()
        self.toggle_mp_button_image = PhotoImage(file=IMAGE_PATH + "media.gif")
        self.prev_button_image = PhotoImage(file=IMAGE_PATH + "prev.gif")
        self.play_pause_button_image = PhotoImage(file=IMAGE_PATH + ("pause.gif" if self.mp.paused else "play.gif"))
        self.skip_button_image = PhotoImage(file=IMAGE_PATH + "skip.gif")
        self.aux_button_image = PhotoImage(file=IMAGE_PATH + ("aux-on.gif" if self.aux else "aux-off.gif"))
        self.toggle_mp_button = Button(self.media_control_frame, command=self.toggle_mp_controls, image=self.toggle_mp_button_image)
        self.prev_button = Button(self.media_control_frame, command=self.prev, image=self.prev_button_image)
        self.play_pause_button = Button(self.media_control_frame, command=self.play_pause, image=self.play_pause_button_image)
        self.skip_button = Button(self.media_control_frame, command=self.skip, image=self.skip_button_image)
        self.aux_button = Button(self.media_control_frame, command=self.toggle_aux, image=self.aux_button_image)
        self.toggle_mp_button.pack(side=LEFT)
        self.prev_button.pack(side=LEFT)
        self.play_pause_button.pack(side=LEFT)
        self.skip_button.pack(side=LEFT)
        self.aux_button.pack(side=LEFT)

    def draw_mp_buttons_controls_frame(self, first_draw=False):
        self.mp_buttons_controls_frame = Frame(self.mp_control_frame, bg=BACKGROUND_COLOR)
        self.mp_buttons_controls_frame.pack(side=LEFT)
        self.mp_pst_button_image    = PhotoImage(file=IMAGE_PATH + "playSelectedTrack.gif")
        self.mp_psaapp_button_image = PhotoImage(file=IMAGE_PATH + "playSelectedPlaylist.gif")
        self.mp_pst_button    = Button(self.mp_buttons_controls_frame, command=self.play_selected_track, image=self.mp_pst_button_image)
        self.mp_psaapp_button = Button(self.mp_buttons_controls_frame, command=self.play_selected_aap,   image=self.mp_psaapp_button_image)
        self.mp_pst_button.pack(fill=X)
        self.mp_psaapp_button.pack(fill=X)
        self.mp_sr_frame = Frame(self.mp_buttons_controls_frame, bg=BACKGROUND_COLOR)
        self.mp_sr_frame.pack(fill=X)
        # self.mp_shuffle_button_image = PhotoImage(file=IMAGE_PATH + "shuffle.gif")
        # self.mp_repeat_button_image  = PhotoImage(file=IMAGE_PATH + "repeat.gif")
        self.mp_shuffle_button = Button(self.mp_sr_frame, command=self.shuffle, text="Shuffle")
        self.mp_repeat_button  = Button(self.mp_sr_frame, command=self.repeat,  text="Repeat")
        self.mp_shuffle_button.pack(side=LEFT, fill=X, expand=True)
        self.mp_repeat_button.pack(side=LEFT, fill=X, expand=True)
        self.mp_artwork = Label(self.mp_buttons_controls_frame, text="\n[insert]\n[artwork]\n[here]\n")
        self.mp_artwork.pack()
        self.mp_aap_frame1 = Frame(self.mp_buttons_controls_frame, bg=BACKGROUND_COLOR)
        self.mp_aap_frame2 = Frame(self.mp_buttons_controls_frame, bg=BACKGROUND_COLOR)
        self.mp_aap_frame1.pack()
        self.mp_aap_frame2.pack()
        self.mp_aap_all_button_image      = PhotoImage(file=IMAGE_PATH + "aap-all.gif")
        self.mp_aap_album_button_image    = PhotoImage(file=IMAGE_PATH + "aap-album.gif")
        self.mp_aap_playlist_button_image = PhotoImage(file=IMAGE_PATH + "aap-playlist.gif")
        self.mp_aap_artist_button_image   = PhotoImage(file=IMAGE_PATH + "aap-artist.gif")
        self.mp_aap_all_button      = Button(self.mp_aap_frame1, command=self.aap_all,      image=self.mp_aap_all_button_image)
        self.mp_aap_album_button    = Button(self.mp_aap_frame1, command=self.aap_album,    image=self.mp_aap_album_button_image)
        self.mp_aap_playlist_button = Button(self.mp_aap_frame2, command=self.aap_playlist, image=self.mp_aap_playlist_button_image)
        self.mp_aap_artist_button   = Button(self.mp_aap_frame2, command=self.aap_artist,   image=self.mp_aap_artist_button_image)
        self.mp_aap_all_button.pack(side=LEFT)
        self.mp_aap_album_button.pack(side=LEFT)
        self.mp_aap_playlist_button.pack(side=LEFT)
        self.mp_aap_artist_button.pack(side=LEFT)


    def draw_everything(self, first_draw=False):
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.minsize(width=796, height=200)
        self.root.resizable(width=False, height=True)
        self.root.title("carPi GUI")

        root_frame = Frame(self.root, bg=BACKGROUND_COLOR)
        root_frame.pack()

        self.status_frame = Frame(root_frame, bg=BACKGROUND_COLOR)
        self.status_frame.pack(fill=X)
        self.draw_status_frame(first_draw)

        volume_slider = Scale(root_frame, command=self.change_vol, orient=HORIZONTAL, bg=BACKGROUND_COLOR, length=794, sliderlength=100, width=75, fg=FOREGROUND_COLOR, to=63, repeatdelay=250, repeatinterval=1, font=("Arial", 12))
        volume_slider.set(self.volume)
        volume_slider.pack()
        self.change_vol(self.volume)

        Label(root_frame, textvariable=self.song_info, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=("Arial", 16)).pack()
        if first_draw:
            self.update_clock()
            self.update_track_info()
        # TODO:  Add some kind of progress bar

        self.media_control_frame = Frame(root_frame, bg=BACKGROUND_COLOR)
        self.media_control_frame.pack()
        self.draw_media_control_frame(first_draw)

        if self.mp_controls:
            self.mp_control_frame = Frame(self.root, bg=BACKGROUND_COLOR)
            self.mp_control_frame.pack(fill=Y)
            Listbox(self.mp_control_frame, width=36, height=100, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(side=RIGHT, fill=Y)
            Listbox(self.mp_control_frame, width=36, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(side=RIGHT, fill=Y)
            self.draw_mp_buttons_controls_frame(first_draw)

        self.root.mainloop()

if __name__ == "__main__":
    RootApp()

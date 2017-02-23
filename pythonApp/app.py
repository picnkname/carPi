from tkinter import *
import subprocess as sp
import time

import mediaPlayer as mediaPlayer


IMAGE_PATH = "images/"
BACKGROUND_COLOR = "#2b2b2b"
FOREGROUND_COLOR = "#d9d9d9"


class RootApp:
    root = Tk()
    mp = mediaPlayer.MediaPlayer()
    song_info = StringVar()
    clock_time = StringVar()
    volume = 0
    hotspot = False
    aux = False
    play = False
    hotspot_button = None
    aux_button = None
    play_pause_button = None


    def __init__(self):
        self.draw_everything(True)


    def toggle_hotspot(self):
        self.hotspot = not self.hotspot
        self.hotspot_button.config(image=PhotoImage(file=IMAGE_PATH + ("hotspot-on.gif" if self.hotspot else "hotspot-off.gif")))
        self.draw_everything()


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


    def show_mp(self):
        return


    def prev(self):
        self.mp.prev()


    def play_pause(self):
        self.play = not self.play
        self.play_pause_button.config(image=PhotoImage(file=IMAGE_PATH + ("play.gif" if self.play else "pause.gif")))
        if self.play:
            self.mp.play()
        else:
            self.mp.pause()
        self.draw_everything()


    def skip(self):
        self.mp.skip()


    def toggle_aux(self):
        self.aux = not self.aux
        self.aux_button.config(image=PhotoImage(file=IMAGE_PATH + ("aux-on.gif" if self.aux else "aux-off.gif")))
        self.draw_everything()


    def draw_everything(self, first_draw=False):
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.minsize(width=796, height=472)
        self.root.resizable(width=False, height=False)
        self.root.title("carPi GUI")

        status_frame = Frame(self.root, bg=BACKGROUND_COLOR)
        status_frame.grid(row=0, column=0)
        status_frame.columnconfigure(1, minsize=552)
        hotspot_image = PhotoImage(file=IMAGE_PATH + ("hotspot-on.gif" if self.hotspot else "hotspot-off.gif"))
        power_off_image = PhotoImage(file=IMAGE_PATH + "power.gif")

        self.hotspot_button = Button(status_frame, command=self.toggle_hotspot, image=hotspot_image)
        self.hotspot_button.grid(row=0, column=0)
        Label(status_frame, textvariable=self.clock_time, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=("Arial", 52)).grid(row=0, column=1)
        Button(status_frame, command=self.power_off, image=power_off_image).grid(row=0, column=2)

        scale = Scale(self.root, command=self.change_vol, orient=HORIZONTAL, bg=BACKGROUND_COLOR, length=794, sliderlength=100, width=75, fg=FOREGROUND_COLOR, to=63, repeatdelay=250, repeatinterval=1, font=("Arial", 12))
        scale.set(self.volume)
        scale.grid(row=1, column=0)
        self.change_vol(self.volume)

        Label(self.root, textvariable=self.song_info, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=("Arial", 16)).grid(row=2, column=0)
        if first_draw:
            self.update_clock()
            self.update_track_info()
        # TODO:  Add some kind of progress bar

        control_frame = Frame(self.root, bg=BACKGROUND_COLOR)
        control_frame.grid(row=3, column=0)

        media_image = PhotoImage(file=IMAGE_PATH + "media.gif")
        prev_image = PhotoImage(file=IMAGE_PATH + "rewind.gif")
        skip_image = PhotoImage(file=IMAGE_PATH + "fast-forward.gif")
        play_image = PhotoImage(file=IMAGE_PATH + ("play.gif" if self.play else "pause.gif"))
        aux_image = PhotoImage(file=IMAGE_PATH + ("aux-on.gif" if self.aux else "aux-off.gif"))
        Button(control_frame, command=self.show_mp, image=media_image).grid(row=0, column=0)
        Button(control_frame, command=self.prev, image=prev_image).grid(row=0, column=1)
        Button(control_frame, command=self.skip, image=skip_image).grid(row=0, column=3)
        self.play_pause_button = Button(control_frame, command=self.play_pause, image=play_image)
        self.aux_button = Button(control_frame, command=self.toggle_aux, image=aux_image)
        self.play_pause_button.grid(row=0, column=2)
        self.aux_button.grid(row=0, column=4)

        self.root.mainloop()

if __name__ == "__main__":
    RootApp()

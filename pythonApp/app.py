from Tkinter import *
from subprocess import call, Popen, PIPE
import time


DAY_IMAGE_PATH = "images-day/"
NIGHT_IMAGE_PATH = "images-night/"

night_mode = False
root = Tk()
song_info = StringVar()
clock_time = StringVar()


def change_vol(new_vol):
    call(["amixer", "-D", "pulse", "sset", "Master", str(new_vol) + "%"])


def play():
    call(["rhythmbox-client", "--play"])


def pause():
    call(["rhythmbox-client", "--pause"])


def next():
    call(["rhythmbox-client", "--next"])


def prev():
    call(["rhythmbox-client", "--previous"])


def power_off():
    call(["sudo", "shutdown", "-h", "now"])


def night_mode_toggle():
    global night_mode
    global root
    night_mode = not night_mode
    root.destroy()
    root = Tk()
    draw_everything()


def update_song_info():
    (title, x) = Popen(["rhythmbox-client", "--print-playing-format=%tt"], stdout=PIPE).communicate()
    (album, x) = Popen(["rhythmbox-client", "--print-playing-format=%at"], stdout=PIPE).communicate()
    (artist, x) = Popen(["rhythmbox-client", "--print-playing-format=%ta"], stdout=PIPE).communicate()
    song_info.set(str(title) + "\n" + str(album) + "\n" + str(artist))
    root.after(100, update_song_info)


def run_clock():
    clock_time.set(time.strftime("%I:%M:%S"))
    root.after(1000, run_clock)


def draw_everything():
    global night_mode
    global root

    bgc = "#2b2b2b" if night_mode else "#d9d9d9"
    fgc = "#d9d9d9" if night_mode else "#2b2b2b"
    image_path = NIGHT_IMAGE_PATH if night_mode else DAY_IMAGE_PATH
    root.configure(bg=bgc)
    root.minsize(width=800, height=600)
    root.resizable(width=False, height=False)

    status_frame = Frame(root, bg=bgc)
    status_frame.grid(row=0, column=0)
    status_frame.columnconfigure(1, minsize=556)
    night_mode_image = PhotoImage(file=image_path + "night-mode.gif")
    power_off_image = PhotoImage(file=image_path + "power.gif")
    Button(status_frame, command=night_mode_toggle, image=night_mode_image).grid(row=0, column=0)
    time_label = Label(status_frame, textvariable=clock_time, bg=bgc, fg=fgc)
    time_label.config(font=("Monospace", 48))
    time_label.grid(row=0, column=1)
    Button(status_frame, command=power_off, image=power_off_image).grid(row=0, column=2)
    run_clock()  # FIXME:  breaks on night mode switch

    scale = Scale(root, command=change_vol, orient=HORIZONTAL, bg=bgc, length=798, sliderlength=75, width=50, fg=fgc)
    scale.grid(row=1, column=0)

    # TODO:  Add track info/shuffle/repeat
    # Label(root, textvariable=song_info, bg=bgc, fg=fgc, width=50).pack(side=BOTTOM)
    # root.after(100, update_song_info)

    control_frame = Frame(root, bg=bgc)
    control_frame.grid(row=3, column=0)
    prev_image = PhotoImage(file=image_path + "rewind.gif")
    play_image = PhotoImage(file=image_path + "play.gif")
    pause_image = PhotoImage(file=image_path + "pause.gif")
    next_image = PhotoImage(file=image_path + "fast-forward.gif")
    Button(control_frame, command=prev, image=prev_image).grid(row=0, column=0)
    Button(control_frame, command=play, image=play_image).grid(row=0, column=1)
    Button(control_frame, command=pause, image=pause_image).grid(row=0, column=2)
    Button(control_frame, command=next, image=next_image).grid(row=0, column=3)

    root.mainloop()


draw_everything()

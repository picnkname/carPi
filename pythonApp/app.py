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
    draw_everything(True)


def update_clock():
    clock_time.set(time.strftime("%I:%M:%S"))
    root.after(1000, run_clock)


def update_track_info():
    (title, x) = Popen(["rhythmbox-client", "--print-playing-format=%tt"], stdout=PIPE).communicate()
    (album, x) = Popen(["rhythmbox-client", "--print-playing-format=%at"], stdout=PIPE).communicate()
    (artist, x) = Popen(["rhythmbox-client", "--print-playing-format=%ta"], stdout=PIPE).communicate()
    title, album, artist = str(title).strip(" \n"), str(album).strip(" \n"), str(artist).strip(" \n")
    song_info.set("\n\n[No Data]\n\n"
                  if title == "" and album == "" and artist == ""
                  else "\n" + title + "\n" + album + "\n" + artist + "\n")
    root.after(250, update_track_info)


def draw_everything():
    global night_mode
    global root

    bgc = "#2b2b2b" if night_mode else "#d9d9d9"
    fgc = "#d9d9d9" if night_mode else "#2b2b2b"
    image_path = NIGHT_IMAGE_PATH if night_mode else DAY_IMAGE_PATH
    root.configure(bg=bgc)
    root.minsize(width=800, height=472)
    root.resizable(width=False, height=False)
    root.title("carPi GUI")

    status_frame = Frame(root, bg=bgc)
    status_frame.grid(row=0, column=0)
    status_frame.columnconfigure(1, minsize=556)
    night_mode_image = PhotoImage(file=image_path + "night-mode.gif")
    power_off_image = PhotoImage(file=image_path + "power.gif")
    Button(status_frame, command=night_mode_toggle, image=night_mode_image).grid(row=0, column=0)
    Label(status_frame, textvariable=clock_time, bg=bgc, fg=fgc, font=("Arial", 52)).grid(row=0, column=1)
    Button(status_frame, command=power_off, image=power_off_image).grid(row=0, column=2)
    update_clock()  # FIXME:  breaks on night mode switch

    scale = Scale(root, command=change_vol, orient=HORIZONTAL, bg=bgc, length=798, sliderlength=75, width=50, fg=fgc, font=("Arial", 12))
    scale.grid(row=1, column=0)

    Label(root, textvariable=song_info, bg=bgc, fg=fgc, font=("Arial", 16)).grid(row=2, column=0)
    update_track_info()  # FIXME:  breaks on night mode switch
    # TODO:  Add some kind of progress bar

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


draw_everything(False)

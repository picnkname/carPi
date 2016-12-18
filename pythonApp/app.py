from Tkinter import *
from subprocess import call, Popen, PIPE


DAY_IMAGE_PATH = "images-day/"
NIGHT_IMAGE_PATH = "images-night/"
MEDIA_SUB_PATH = "mediacontrols/"

night_mode = False
root = Tk()
song_info = StringVar()


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
    global song_info
    (title, x) = Popen(["rhythmbox-client", "--print-playing-format=%tt"], stdout=PIPE).communicate()
    (album, x) = Popen(["rhythmbox-client", "--print-playing-format=%at"], stdout=PIPE).communicate()
    (artist, x) = Popen(["rhythmbox-client", "--print-playing-format=%ta"], stdout=PIPE).communicate()
    song_info.set(str(title) + "\n" + str(album) + "\n" + str(artist))
    root.after(100, update_song_info)


def draw_everything():
    global night_mode
    global root

    bgc = "#2b2b2b" if night_mode else "#d9d9d9"
    fgc = "#d9d9d9" if night_mode else "#2b2b2b"
    root.configure(bg=bgc)

    status_frame = Frame(root, bg=bgc)
    status_frame.pack(anchor=CENTER)
    night_mode_image = PhotoImage(file=(NIGHT_IMAGE_PATH if night_mode else DAY_IMAGE_PATH) + "night-mode.gif").subsample(9, 9)
    power_off_image = PhotoImage(file=(NIGHT_IMAGE_PATH if night_mode else DAY_IMAGE_PATH) + "power.gif").subsample(9, 9)
    Button(status_frame, command=night_mode_toggle, image=night_mode_image).pack(side=LEFT)
    Button(status_frame, command=power_off, image=power_off_image).pack(side=RIGHT)
    Label(status_frame, textvariable=song_info, bg=bgc, fg=fgc, width=50).pack(side=LEFT)
    root.after(100, update_song_info)

    scale = Scale(root, command=change_vol, orient=HORIZONTAL, bg=bgc, length=800, sliderlength=75, width=50, fg=fgc)
    scale.pack(anchor=CENTER)

    bottom_frame = Frame(root, bg=bgc)
    bottom_frame.pack(anchor=CENTER)
    z = 6  # Just some scaling number for the images
    media_image_path = (NIGHT_IMAGE_PATH if night_mode else DAY_IMAGE_PATH) + MEDIA_SUB_PATH
    prev_image = PhotoImage(file=media_image_path + "rewind.gif").subsample(z, z)
    play_image = PhotoImage(file=media_image_path + "play.gif").subsample(z, z)
    pause_image = PhotoImage(file=media_image_path + "pause.gif").subsample(z, z)
    next_image = PhotoImage(file=media_image_path + "fast-forward.gif").subsample(z, z)
    Button(bottom_frame, command=prev, image=prev_image).pack(side=LEFT)
    Button(bottom_frame, command=play, image=play_image).pack(side=LEFT)
    Button(bottom_frame, command=pause, image=pause_image).pack(side=LEFT)
    Button(bottom_frame, command=next, image=next_image).pack(side=LEFT)

    root.mainloop()


draw_everything()

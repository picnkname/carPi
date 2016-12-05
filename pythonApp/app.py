from tkinter import *
from subprocess import call


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


root = Tk()
scale = Scale(root, command=change_vol, orient=HORIZONTAL, length=800, sliderlength=75, width=50)
scale.pack(anchor=CENTER)

bottom_frame = Frame(root)
bottom_frame.pack(anchor=CENTER)

z = 5
prev_image = PhotoImage(file="prev.gif").subsample(z, z)
play_image = PhotoImage(file="play.gif").subsample(z, z)
pause_image = PhotoImage(file="pause.gif").subsample(z, z)
next_image = PhotoImage(file="next.gif").subsample(z, z)
prev_button = Button(bottom_frame, command=prev, image=prev_image)
play_button = Button(bottom_frame, command=play, image=play_image)
pause_button = Button(bottom_frame, command=pause, image=pause_image)
next_button = Button(bottom_frame, command=next, image=next_image)
prev_button.pack(side=LEFT)
play_button.pack(side=LEFT)
pause_button.pack(side=LEFT)
next_button.pack(side=LEFT)


root.mainloop()

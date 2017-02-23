from tkinter import *
import subprocess as sp
import time

import mediaPlayer as mp


IMAGE_PATH = "images/"
BACKGROUND_COLOR = "#2b2b2b"
FOREGROUND_COLOR = "#d9d9d9"

root = Tk()
song_info = StringVar()
clock_time = StringVar()
hotspot = False
aux = False
play = False
hotspot_button = None
aux_button = None
play_pause_button = None


def toggle_hotspot():
    global hotspot
    global hotspot_button
    hotspot = not hotspot
    hotspot_button.config(image=PhotoImage(file=IMAGE_PATH + ("hotspot-on.gif" if hotspot else "hotspot-off.gif")))
    draw_everything()


def update_clock():
    clock_time.set(time.strftime("%I:%M:%S"))
    root.after(1000, update_clock)


def power_off():
    sp.call(["sudo", "shutdown", "-h", "now"])


def change_vol(new_vol):
    # The USB sound card for my pi does not output sound if it is below 25%
    # This scales it so there's a still a 0%-100% available to the user
    new_vol = int(new_vol) * 0.75 + 25 if int(new_vol) > 0 else 0
    sp.call(["amixer", "-D", "pulse", "sset", "Master", str(new_vol) + "%"])


def update_track_info():
    (title, album, artist) = mp.get_track_info()
    song_info.set("\n" +
                  ("[No Title Data]\n" if title == "" else title + "\n") +
                  ("[No Album Data]\n" if album == "" else album + "\n") +
                  ("[No Artist Data]\n" if artist == "" else artist + "\n"))
    root.after(250, update_track_info)


def show_mp():
    return


def prev():
    mp.prev()


def play_pause():
    global play
    global play_pause_button
    play = not play
    play_pause_button.config(image=PhotoImage(file=IMAGE_PATH + ("play.gif" if play else "pause.gif")))
    if play:
        mp.play()
    else:
        mp.pause()
    draw_everything()


def skip():
    mp.skip()


def toggle_aux():
    global aux
    global aux_button
    aux = not aux
    aux_button.config(image=PhotoImage(file=IMAGE_PATH + ("aux-on.gif" if aux else "aux-off.gif")))
    draw_everything()


def draw_everything(first_draw=False):
    global root
    global hotspot
    global aux
    global play
    global hotspot_button
    global aux_button
    global play_pause_button

    root.configure(bg=BACKGROUND_COLOR)
    root.minsize(width=796, height=472)
    root.resizable(width=False, height=False)
    root.title("carPi GUI")

    status_frame = Frame(root, bg=BACKGROUND_COLOR)
    status_frame.grid(row=0, column=0)
    status_frame.columnconfigure(1, minsize=552)
    hotspot_image = PhotoImage(file=IMAGE_PATH + ("hotspot-on.gif" if hotspot else "hotspot-off.gif"))
    power_off_image = PhotoImage(file=IMAGE_PATH + "power.gif")

    hotspot_button = Button(status_frame, command=toggle_hotspot, image=hotspot_image)
    hotspot_button.grid(row=0, column=0)
    Label(status_frame, textvariable=clock_time, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=("Arial", 52)).grid(row=0, column=1)
    Button(status_frame, command=power_off, image=power_off_image).grid(row=0, column=2)

    scale = Scale(root, command=change_vol, orient=HORIZONTAL, bg=BACKGROUND_COLOR, length=794, sliderlength=100, width=75, fg=FOREGROUND_COLOR, font=("Arial", 12))
    scale.grid(row=1, column=0)

    Label(root, textvariable=song_info, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=("Arial", 16)).grid(row=2, column=0)
    if first_draw:
        update_clock()
        update_track_info()
    # TODO:  Add some kind of progress bar

    control_frame = Frame(root, bg=BACKGROUND_COLOR)
    control_frame.grid(row=3, column=0)

    media_image = PhotoImage(file=IMAGE_PATH + "media.gif")
    prev_image = PhotoImage(file=IMAGE_PATH + "rewind.gif")
    skip_image = PhotoImage(file=IMAGE_PATH + "fast-forward.gif")
    play_image = PhotoImage(file=IMAGE_PATH + ("play.gif" if play else "pause.gif"))
    aux_image = PhotoImage(file=IMAGE_PATH + ("aux-on.gif" if aux else "aux-off.gif"))
    Button(control_frame, command=show_mp, image=media_image).grid(row=0, column=0)
    Button(control_frame, command=prev, image=prev_image).grid(row=0, column=1)
    Button(control_frame, command=skip, image=skip_image).grid(row=0, column=3)
    play_pause_button = Button(control_frame, command=play_pause, image=play_image)
    aux_button = Button(control_frame, command=toggle_aux, image=aux_image)
    play_pause_button.grid(row=0, column=2)
    aux_button.grid(row=0, column=4)

    root.mainloop()


draw_everything(True)

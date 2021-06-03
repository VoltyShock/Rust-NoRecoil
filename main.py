import win32api
import time
import ctypes
from tkinter import *
from tkinter import ttk
import threading

sensitivity = 0.288
guns = ['AssaultRifle', 'AssaultRifleHolo', 'AssaultRifle8X', 'LR300', 'LR300-Holo', 'MP5A4', 'MP5A4-Holo', 'M249']

# ~~AK RecoilTable~~ #
AssaultRifle = [[-38, 52.3906], [15, 46], [-40, 42], [-57, 37], [0, 34], [0, 28], [30, 25], [20, 22], [46, 15],
                [38, 11], [38, 10], [35, 18], [38, 18], [25, 25], [0, 29], [-17, 32], [-22, 33], [-34, 32], [-38, 29],
                [-45, 24], [-45, 17], [-45, 8], [-42, 5], [-36, 14], [-25, 21], [0, 25], [0, 28], [40, 28], [53, 26],
                [48, 15], [38, 21]]
AssaultRifleTime = 0.013

# ~~LR RecoilTable~~ #
LR300AssaultRifle = [[-2, 25], [-8, 31], [-10, 33], [-14, 31], [-18, 25], [-16, 20], [-14, 12], [-10, 12], [12, 8],
                     [19, 8], [24, 8], [17, 7], [10, 5], [0, 4], [-5, 4], [-9, 4], [-12, 3], [-17, 3], [-18, 3],
                     [-18, 2], [-16, 2], [-16, 2], [-15, 2], [-7, 2], [-3, 2], [13, 2], [30, 2], [36, 3], [30, 3]]
LR300AssaultRifleTime = 0.011

# ~~MP5 RecoilTable~~ #
MP5A4 = [[2, 40], [-5, 29], [18, 33], [25, 33], [42, 34], [25, 32], [-15, 24], [-15, 8], [-10, 9], [-8, 3], [-2, 8],
         [0, 8], [12, 8], [12, 4], [10, 2], [5, 0], [8, 1], [5, 5], [-15, 5], [-18, 5], [-18, 5], [-18, 2],
         [-18, 2], [-10, 2], [-15, 0], [-15, 0], [-15, 10], [-2, -10], [35, 0], [10, 0]]
MP5A4Time = 0.005


# ~~M2 RecoilTable~~ #
# M249 recoil pattern is mostly down so I just have a loop for it instead of an 2D array for [x,y] co-ords
M249Time = 0.125


def choosegun():
    if gun_type.get() == 1:
        gun = AssaultRifle
        timer = AssaultRifleTime
    if gun_type.get() == 2:
        gun = LR300AssaultRifle
        timer = LR300AssaultRifleTime
    if gun_type.get() == 3:
        gun = MP5A4
        timer = MP5A4Time
    return gun, timer


# Is mouse button 1 and 2 pressed
def ispressed():
    a = win32api.GetKeyState(0x01)
    b = win32api.GetKeyState(0x02)
    if a < 0 and b < 0:
        return True


# Moves mouse X amount
def move(x, y):
    ctypes.windll.user32.mouse_event(0x0001, x, y, 0, 0)


def godown(gun, timer, attachments):
    if gun == 'M249':
        for i in range(0, 100):
            # Crouched
            if win32api.GetKeyState(0x11) < 0:
                # Crouched Strafing
                if win32api.GetKeyState(0x58) < 0 or win32api.GetKeyState(0x41) < 0 or win32api.GetKeyState(0x44) < 0 or win32api.GetKeyState(0x53) < 0:
                    move(0, int(28/sensitivity))
                # Crouched Still
                else:
                    move(0, int(16/sensitivity))
            # Stood up M249
            else:
                move(0, int(32/sensitivity))
            time.sleep(timer/8)
            if not ispressed():
                return
    else:
        for i in gun:
            if attachments == 1:
                truex = (((i[0]*1.2) / 2) / sensitivity)
                truey = (((i[1]*1.2) / 2) / sensitivity)
            elif attachments == 2:
                truex = (((i[0] * 3.6) / 2) / sensitivity)
                truey = (((i[1] * 3.6) / 2) / sensitivity)
            elif attachments == 0:
                truex = ((i[0]/2)/sensitivity)
                truey = ((i[1]/2)/sensitivity)
            for x in range(8):
                movex = (truex/8)
                movey = (truey/8)
                move(int(movex), int(movey))
                time.sleep(timer/8)
            if not ispressed():
                return


def loop():
    while True:
        while gun_type.get() != 0:
            if ispressed():
                godown(choosegun()[0], choosegun()[1], attachment.get())


def start():
    thrd = threading.Thread(target=loop)
    thrd.start()


def update_sens(*args):
    global sensitivity
    sensitivity = round(float(sens_mul.get()), 3)
    if sensitivity == 0:
        sensitivity = 0.001


# UI
root = Tk()
root.title("Rust No-Recoil")
root.resizable(0, 0)

gun_type = IntVar()
attachment = IntVar()
sens_mul = StringVar()

guns = [ttk.Radiobutton(root, text="None", variable=gun_type, value=0),
        ttk.Radiobutton(root, text="AK-47", variable=gun_type, value=1),
        ttk.Radiobutton(root, text="LR300", variable=gun_type, value=2),
        ttk.Radiobutton(root, text="MP5A4", variable=gun_type, value=3)]

attachments = [ttk.Radiobutton(root, text="None", variable=attachment, value=0),
               ttk.Radiobutton(root, text="Holo", variable=attachment, value=1),
               ttk.Radiobutton(root, text="8x", variable=attachment, value=2)]


sens_title = ttk.Label(root, text="Sensitivity:")
sens = ttk.Entry(root, textvariable=sens_mul)
sens_submit = ttk.Button(root, text="Set Sensitivity", command=update_sens)
sens.grid(column=3, row=2)
sens_title.grid(column=3, row=1)
sens_submit.grid(column=3, row=3)


var = 2

label1 = ttk.Label(root, text="Guns:")
label1.grid(column=0, row=1, ipadx="8px")
for x in guns:
    x.grid(column=0, row=var)
    var = var + 1

var = 2
label2 = ttk.Label(root, text="Attachments:")
label2.grid(column=1, row=1, ipadx="8px")
for x in attachments:
    x.grid(column=1, row=var)
    var = var+1

watermark = ttk.Label(root, text="Rust No-Recoil Made By Voltyshock.")
watermark.grid(column=3, row=len(guns)+2, sticky=SW)
root.grid_rowconfigure(len(guns)+2, weight=5)
root.grid_columnconfigure(3, weight=5)


start()

root.geometry("400x300")
root.mainloop()


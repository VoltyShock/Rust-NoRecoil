import win32api
import time
import ctypes
from tkinter import *
import threading

sensitivity = 0.288
guns = ['AssaultRifle', 'AssaultRifleHolo', 'AssaultRifle8X', 'LR300', 'LR300-Holo', 'MP5A4', 'MP5A4-Holo', 'M249']

# ~~AK RecoilTable~~ #
AssaultRifle = [[-35, 52.3906], [15, 46], [-40, 42], [-55, 37], [0, 34], [0, 28], [30, 25], [20, 22], [46, 15],
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
MP5A4 = [[0, 40], [0, 29], [0, 33], [25, 33], [45, 34], [47, 32], [-12, 24], [-43, 8], [-23, 9], [-18, 3], [-2, -8],
         [0, 8], [12, 8], [15, 4], [20, 2], [22, 0], [28, 1], [30, 2], [-27, 1], [-26, 4], [-26, 2], [-32, -2],
         [-32, 2], [-30, -2], [-28, 0], [-28, 0], [-26, 10], [-22, -10], [-20, 0], [-10, 0]]
MP5A4Time = 0.005


# ~~M2 RecoilTable~~ #
# M249 recoil pattern is mostly down so I just have a loop for it instead of an 2D array for [x,y] co-ords
M249Time = 0.125


def choosegun():
    gun = 0
    timer = 0
    if gun_type.get() == 1:
        gun = AssaultRifle
        timer = AssaultRifleTime
    elif gun_type.get() == 2:
        gun = LR300AssaultRifle
        timer = LR300AssaultRifleTime
    elif gun_type.get() == 3:
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
                truex = (((i[0] * 3.8) / 2) / sensitivity)
                truey = (((i[1] * 3.8) / 2) / sensitivity)
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
    while gun_type.get() != 0:
        if ispressed():
            godown(choosegun()[0], choosegun()[1], attachment.get())


def start():
    thrd = threading.Thread(target=loop)
    thrd.start()


# UI
root = Tk()


gun_type = IntVar()
attachment = IntVar()


guns = [Radiobutton(root, text="None", command=start, variable=gun_type, value=0),
        Radiobutton(root, text="AK-47", command=start, variable=gun_type, value=1),
        Radiobutton(root, text="LR300", command=start, variable=gun_type, value=2),
        Radiobutton(root, text="MP5A4", command=start, variable=gun_type, value=3)]

attachments = [Radiobutton(root, text="None", variable=attachment, value=0),
               Radiobutton(root, text="Holo", variable=attachment, value=1),
               Radiobutton(root, text="8x", variable=attachment, value=2)]

label1 = Label(root, text="Guns:")
label1.pack(anchor=NW)
for x in guns:
    x.pack(anchor=NW)

label2 = Label(root, text="Attachments:")
label2.pack(anchor=NW)
for x in attachments:
    x.pack(anchor=NW)


root.geometry("400x300")
root.mainloop()


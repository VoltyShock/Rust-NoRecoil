import win32api
import time
import ctypes
from tkinter import *
from tkinter import ttk
import threading


sensitivity = 0.288
stop = False
# ~~AK RecoilTable~~ #
AssaultRifle = [[-38, 52.3906], [15, 46], [-42, 42], [-59, 37], [0, 34], [0, 28], [34, 25], [22, 26], [46, 18],
                [38, 14], [38, 15], [38, 18], [38, 18], [25, 28], [0, 29], [-22, 32], [-26, 33], [-32, 32], [-36, 29],
                [-45, 24], [-45, 17], [-45, 8], [-42, 5], [-38, 14], [-14, 21], [0, 25], [10, 28], [40, 28], [53, 26],
                [48, 15], [38, 21]]
AssaultRifleTime = 0.013

# ~~LR RecoilTable~~ #
LR300AssaultRifle = [[-2, 25], [-8, 31], [-10, 33], [-14, 31], [-18, 25], [-16, 20], [-14, 12], [-10, 12], [12, 8],
                     [19, 8], [17, 8], [15, 7], [10, 5], [0, 4], [-10, 4], [-9, 4], [-12, 3], [-17, 3], [-18, 3],
                     [-18, 2], [-16, 2], [-16, 2], [-15, 2], [-7, 2], [-3, 2], [13, 2], [30, 2], [36, 3], [30, 3]]
LR300AssaultRifleTime = 0.011

# ~~MP5 RecoilTable~~ #
MP5A4 = [[3, 40], [-5, 29], [18, 36], [28, 36], [34, 34], [34, 32], [-23, 24], [-14, 8], [-17, 9], [-18, 3], [-2, 8],
         [20, 8], [18, 8], [25, 4], [12, 2], [7, 0], [7, 1], [5, 5], [-45, 5], [-40, 5], [-30, 5], [-25, 2],
         [-15, 2], [-10, 2], [-15, 0], [15, 0], [-5, 10], [-2, -10], [25, 0], [10, 0]]
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
    if gun_type.get() == 4:
        gun = "M249"
        timer = M249Time
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
                    move(0, int(17/sensitivity))
            # Stood up M249
            else:
                move(0, int(33/sensitivity))
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
    global stop
    while True:
        while gun_type.get() != 0:
            if gun_type.get() == 4:
                attachment.set(2)
            if ispressed():
                godown(choosegun()[0], choosegun()[1], attachment.get())


def check_input():
    while True:
        none = win32api.GetKeyState(0x60)
        if none < 0 and win32api.GetKeyState(0x11) < 0:
            gun_type.set(0)
        ak = win32api.GetKeyState(0x61)
        if ak < 0 and win32api.GetKeyState(0x11) < 0:
            gun_type.set(1)
        lr = win32api.GetKeyState(0x62)
        if lr < 0 and win32api.GetKeyState(0x11) < 0:
            gun_type.set(2)
        mp5 = win32api.GetKeyState(0x63)
        if mp5 < 0 and win32api.GetKeyState(0x11) < 0:
            gun_type.set(3)
        m2 = win32api.GetKeyState(0x64)
        if m2 < 0 and win32api.GetKeyState(0x11) < 0:
            gun_type.set(4)
        iron = win32api.GetKeyState(0x67)
        if iron < 0 and win32api.GetKeyState(0x11) < 0:
            attachment.set(0)
        holo = win32api.GetKeyState(0x68)
        if holo < 0 and win32api.GetKeyState(0x11) < 0:
            attachment.set(1)
        eight = win32api.GetKeyState(0x69)
        if eight < 0 and win32api.GetKeyState(0x11) < 0:
            attachment.set(2)


def start():
    thrd1 = threading.Thread(target=loop)
    thrd2 = threading.Thread(target=check_input)
    thrd2.start()
    thrd1.start()


def update_sens(*args):
    global sensitivity
    try:
        sensitivity = round(float(sens_mul.get()), 3)
        if sensitivity < 0:
            sensitivity = 0.001
            sens_mul.set("0")
        if sensitivity > 1:
            sensitivity = 1
            sens_mul.set("1")
    except ValueError:
        sens_mul.set("")


# UI
root = Tk()
root.title("Rust No-Recoil")
root.resizable(0, 0)

gun_type = IntVar()
attachment = IntVar()
sens_mul = StringVar()
sens_mul.set(str(sensitivity))

guns = [ttk.Radiobutton(root, text="None", variable=gun_type, value=0),
        ttk.Radiobutton(root, text="AK-47", variable=gun_type, value=1),
        ttk.Radiobutton(root, text="LR300", variable=gun_type, value=2),
        ttk.Radiobutton(root, text="MP5A4", variable=gun_type, value=3),
        ttk.Radiobutton(root, text="M249", variable=gun_type, value=4)]

attachments = [ttk.Radiobutton(root, text="None", variable=attachment, value=0),
               ttk.Radiobutton(root, text="Holo", variable=attachment, value=1),
               ttk.Radiobutton(root, text="8x", variable=attachment, value=2)]


# Presents the sensitivity adjuster
sens_title = ttk.Label(root, text="Sensitivity:")
sens = ttk.Entry(root, textvariable=sens_mul)
sens_submit = ttk.Button(root, text="Set Sensitivity", command=update_sens)
sens.grid(column=3, row=2)
sens_title.grid(column=3, row=1)
sens_submit.grid(column=3, row=3)


# Presents Guns
row = 2
gun_title = ttk.Label(root, text="Guns:")
gun_title.grid(column=0, row=1, ipadx="4px", sticky=W)
for x in guns:
    x.grid(column=0, row=row, sticky=W, ipadx="4px")
    row = row + 1

# Presents Attachments
row = 2
attachment_title = ttk.Label(root, text="Attachments:")
attachment_title.grid(column=1, row=1, ipadx="18px", sticky=W)
for x in attachments:
    x.grid(column=1, row=row, sticky=W, ipadx="18px")
    row = row+1

# Instructions on keybinds
info = ttk.Label(root, text="Gun Keybinds (ctrl + numpad):\n"
                            "0 = None, 1 = AK-47, 2 = LR300, 3 = MP5A4, 4 = M249\n"
                            "Attachment Keybinds (ctrl + numpad):\n"
                            "7 = None, 8 = Holographic Site, 9 = 8x Scope")
info.grid(column=0, row=len(guns)+2, sticky=SW, columnspan=4)
root.grid_rowconfigure(len(guns)+2, weight=5)
# Starts the scripts
start()

root.geometry("325x275")
root.mainloop()


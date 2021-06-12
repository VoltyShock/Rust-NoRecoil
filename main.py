import win32api
import time
from tkinter import *
from tkinter import ttk
import gc
import json


sensitivity = 0.288


gun_dict = json.load(open("Rust-NoRecoil/RecoilTables", "r"))

# ~~Gun Timers ~~ #
AssaultRifleTime = 0.001
LR300AssaultRifleTime = 0.011
MP5A4Time = 0.005
M249Time = 0.125


def start():
    import threading
    thrd1 = threading.Thread(target=loop)
    thrd2 = threading.Thread(target=check_input)
    thrd2.start()
    thrd1.start()


def choose_gun():
    global gun_dict

    if gun_type.get() == 1:
        gun = "AssaultRifle"
        timer = AssaultRifleTime
    if gun_type.get() == 2:
        gun = "LR300AssaultRifle"
        timer = LR300AssaultRifleTime
    if gun_type.get() == 3:
        gun = "MP5A4"
        timer = MP5A4Time
    if gun_type.get() == 4:
        gun = "M249"
        timer = M249Time
        return gun, timer

    if attachment.get() == 0:
        gun = gun_dict[gun + "Iron"]
    elif attachment.get() == 1:
        gun = gun_dict[gun + "Holo"]
    elif attachment.get() == 2:
        gun = gun_dict[gun + "Eight"]

    return gun, timer


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
        gc.collect(0)


# Is mouse button 1 and 2 pressed
def is_pressed():
    a = win32api.GetKeyState(0x01)
    b = win32api.GetKeyState(0x02)
    if a < 0 and b < 0:
        return True


def loop():
    while True:
        while gun_type.get() != 0:
            if gun_type.get() == 4:
                attachment.set(2)
            if is_pressed():
                go_down(choose_gun()[0], choose_gun()[1])


def go_down(gun, timer):
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
            if not is_pressed():
                gc.collect(0)
                return
    else:
        for i in gun:
            truex = ((i[0]/2)/sensitivity)
            truey = ((i[1]/2)/sensitivity)
            for x in range(8):
                movex = (truex/8)
                movey = (truey/8)
                move(int(movex), int(movey))
                time.sleep(timer/8)
            if not is_pressed():
                gc.collect(0)
                return
            
            
# Moves mouse X amount
def move(x, y):
    import ctypes
    ctypes.windll.user32.mouse_event(0x0001, x, y, 0, 0)


def update_sens():
    global sensitivity
    try:
        sensitivity = round(float(sens_mul.get()), 3)
        if sensitivity < 0.001:
            sensitivity = 0.001
            sens_mul.set("0")
        if sensitivity > 1:
            sensitivity = 1
            sens_mul.set("1")
    except ValueError:
        sens_mul.set("")
    gc.collect(0)


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

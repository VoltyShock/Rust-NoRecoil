import win32api
import time
import ctypes

guntype = 0
attachment = 0
timer = 0
sensitivity = 0.288
guns = ['AssaultRifle', 'AssaultRifleHolo', 'AssaultRifle8X', 'LR300AssaultRifle', 'MP5A4', 'MP5A4Holo', 'M249']

# ~~AK RecoilTable~~ #
AssaultRifle = [[-35, 52.3906], [10, 46], [-40, 42], [-55, 37], [-5, 33], [0, 28], [30, 24], [20, 19], [48, 14],
                [38, 9], [38, 9], [34, 18], [38, 18], [25, 25], [0, 29], [-15, 32], [-22, 33], [-32, 32], [-38, 29],
                [-43, 24], [-45, 17], [-45, 8], [-42, 5], [-35, 14], [-25, 21], [0, 25], [0, 28], [40, 28], [50, 26],
                [45, 15], [38, 21]]
AssaultRifleTime = 0.013

# ~~LR RecoilTable~~ #
LR300AssaultRifle = [[-2, 25], [-8, 31], [-10, 33], [-14, 31], [-15, 25], [-14, 20], [-9, 17], [-2, 15], [9, 12],
                     [17, 10], [20, 8], [17, 7], [10, 5], [0, 4], [-5, 4], [-9, 4], [-12, 3], [-14, 3], [-15, 3],
                     [-15, 2], [-14, 2], [-13, 2], [-10, 2], [-7, 2], [-3, 2], [13, 2], [30, 2], [36, 3], [30, 3]]
LR300AssaultRifleTime = 0.110

# ~~MP5 RecoilTable~~ #
MP5A4 = [[0, 40], [0, 29], [0, 33], [25, 33], [40, 34], [42, 32], [40, 24], [-55, 8], [-23, 9], [-23, 3], [-23, -8],
         [0, 8], [0, 8], [19, 4], [20, 4], [22, 0], [28, 1], [25, 2], [25, 1], [-22, 1], [-22, 0], [-30, 0],
         [-32, 0], [-28, 0], [-28, 0], [-28, 0], [-26, 0], [-22, 0], [-20, 0], [-10, 0]]
MP5A4Time = 0.001


# ~~M2 RecoilTable~~ #
# M249 recoil pattern is mostly down so I just have a loop for it instead of an 2D array for [x,y] co-ords
M249Time = 0.125


# Checks what keys are pressed to enable guns
def ispressedchangenum():
    global guntype
    global timer
    global attachment
    a = win32api.GetKeyState(0x61)
    if a < 0:
        guntype = AssaultRifle
        attachment = "Ironsights"
        timer = AssaultRifleTime
    b = win32api.GetKeyState(0x62)
    if b < 0:
        guntype = AssaultRifle
        attachment = "Holo"
        timer = AssaultRifleTime
    c = win32api.GetKeyState(0x63)
    if c < 0:
        guntype = AssaultRifle
        attachment = "8x"
        timer = AssaultRifleTime
    d = win32api.GetKeyState(0x64)
    if d < 0:
        guntype = LR300AssaultRifle
        attachment = "Ironsights"
        timer = LR300AssaultRifleTime
    e = win32api.GetKeyState(0x65)
    if e < 0:
        guntype = MP5A4
        attachment = "Ironsights"
        timer = MP5A4Time
    f = win32api.GetKeyState(0x66)
    if f < 0:
        guntype = MP5A4
        attachment = "Holo"
        timer = MP5A4Time
    g = win32api.GetKeyState(0x67)
    if g < 0:
        guntype = 'M249'
        timer = M249Time
    return


# Menu, only visual
def menu():
    i = 1
    for x in guns:
        print(f'{i} - {x}')
        i += 1
    print("0 - None")
    print("0 + any other key on numpad - Close")


# Is mouse button 1 and 2 pressed
def ispressed():
    a = win32api.GetKeyState(0x01)
    b = win32api.GetKeyState(0x02)
    if a < 0 and b < 0:
        return True


# Disables scripts
def ispressednumber():
    global guntype
    global attachment
    a = win32api.GetKeyState(0x60)
    if a < 0:
        guntype = 0
        attachment = 0
        loop()


# Moves mouse X amount
def move(x, y):
    ctypes.windll.user32.mouse_event(0x0001, x, y, 0, 0)


def godown(guntype, attachment, timer):
    if guntype == 'M249':
        for i in range(0, 100):
            # Crouched
            if win32api.GetKeyState(0x11) < 0:
                # Crouched Strafing
                if win32api.GetKeyState(0x58) < 0 or win32api.GetKeyState(0x41) < 0 or win32api.GetKeyState(0x44) < 0 or win32api.GetKeyState(0x53) < 0:
                    move(0, int(20/sensitivity))
                # Crouched Still
                else:
                    move(0, int(12/sensitivity))
            # Stood up M249
            else:
                move(0, int(28/sensitivity))
            time.sleep(timer/8)
            if not ispressed():
                return
    else:
        for x in guntype:
            if attachment == "Holo":
                truex = (((x[0]*1.2) / 2) / sensitivity)
                truey = (((x[1]*1.2) / 2) / sensitivity)
            elif attachment == "8x":
                truex = (((x[0] * 3.8) / 2) / sensitivity)
                truey = (((x[1] * 3.8) / 2) / sensitivity)
            elif attachment == "Ironsights":
                truex = ((x[0]/2)/sensitivity)
                truey = ((x[1]/2)/sensitivity)
            for x in range(8):
                movex = (truex/8)
                movey = (truey/8)
                move(int(movex), int(movey))
                time.sleep(timer/8)
            if not ispressed():
                return


def loop():
    while guntype == 0:
        ispressedchangenum()
    while guntype != 0:
        try:
            ispressedchangenum()
            ispressednumber()
            if ispressed():
                godown(guntype, attachment, timer)
        except RecursionError:
            exit()


menu()
loop()

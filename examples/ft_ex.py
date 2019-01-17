from ft import ftclient
import time

f = ftclient()

white = [255, 255, 255]
black = [1,1,1]
color = [0, 200, 0]

PAL = [[165, 0, 38], [215, 48, 39], [244, 109, 67], [253, 174, 97], [254, 224, 144], [224, 243, 248], [171, 217, 233], [116, 173, 209], [69, 117, 180], [49, 54, 149]]
PAL_MAX = 35
def interpolate_int(a, b, flt):
    return int(a + (b - a) * flt)
def interpolated_color(val):
    flt = (val / PAL_MAX) * (len(PAL) - 1)
    idx = int(flt)
    flt = flt - idx
    a = PAL[idx]
    b = PAL[idx + 1]
    return [
        interpolate_int(a[0], b[0], flt),
        interpolate_int(a[1], b[1], flt),
        interpolate_int(a[2], b[2], flt)
    ]

delta = 0.1

def fill_slow():
    for col in range(45):
        for row in range(35):
            f.set(col, row, interpolated_color(row))
            f.show()
        time.sleep(delta)

while True:
    color = [0, 200, 0]
    fill_slow()
    color = [1, 1, 2]
    fill_slow()

def show_dot(x, y):
    f.set(x, y, white)
    f.show()
    time.sleep(delta)
    f.set(x, y, black)

for i in range(35):
    show_dot(i, i)

for i in range(10):
    show_dot(35 + i, 33 - i)

for i in range(25):
    show_dot(44 - i, 24 - i)

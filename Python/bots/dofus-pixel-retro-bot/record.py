from PIL import Image
from pynput.mouse import Controller
from pynput import keyboard
import pyscreenshot as ImageGrab

import sys, time, random, os

if len(sys.argv) > 1:
    arg1 = sys.argv[1]
else:
    arg1 = ""

mouse = Controller()
keyinput = keyboard.Controller()
path = os.path.dirname(os.path.abspath(__file__)) + "/record"

if arg1 != "stream":
    time.sleep(3)
    im = ImageGrab.grab()



def on_press(key):
    if arg1 != "stream":
        global im
    else:
        im = ImageGrab.grab()
    if key == keyboard.KeyCode(char="z"):
        x, y = mouse.position
        r,g,b = im.getpixel((x, y))
        # im.save( os.path.join(path , 'ss.jpg'), "JPEG")
        if arg1 == "pos":
            print("({}, {}) ({}, {}, {}),".format(x, y, r,g,b), end="\n")
        else:
            print("({}, {}, {}),".format(r,g,b), end=" ")
        

try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    pass






        


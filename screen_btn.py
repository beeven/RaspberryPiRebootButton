#!/usr/bin/env python3

from gpiozero import Button
import time
import sys
import os
import fileinput


btn22 = Button(22, hold_time=5)
btn27 = Button(27, hold_time=10)



def when_btn_held(btn):
    print("Button {0} is held for {1} seconds".format(btn.pin.number, btn.active_time))
    if btn is btn22:
        if btn27.is_pressed:
            print("Switching output device in /boot/config")
            switch_display_config()
        print("Rebooting system...")
        os.system("shutdown -r now")
    elif btn is btn27:
        if btn22.is_pressed:
            return
        else:
            print("Shuting down system...")
            os.system("shutdown -h now")


def switch_display_config():
    with fileinput.FileInput("/boot/config.txt", inplace=True) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("display_default_lcd="):
                value = line[-1]
                if value == "1":
                    print("display_default_lcd=0")
                else:
                    print("display_default_lcd=1")
            else:
                print(line)



if __name__=="__main__":

    btn22.when_held = when_btn_held
    btn27.when_held = when_btn_held

    print("Waiting for screen button...")

    while True:
        time.sleep(100)


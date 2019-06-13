#!/usr/bin/env python3

from gpiozero import Button
import time
import datetime
import sys
import os
import fileinput
import fcntl, struct, socket
import subprocess


class DButton(Button):
    def __init__(self,pin, *args, **kwargs):
        super().__init__(pin, *args, **kwargs)
        self.last_pressed = None


btn22 = DButton(22, hold_time=5)
btn27 = DButton(27, hold_time=10)



def when_btn_held(btn):
    print("Button {0} is held for {1} seconds".format(btn.pin.number, btn.active_time))
    if btn is btn22:
        if btn27.is_pressed:
            print("Switching output device in /boot/config")
            switch_display_config()
        print("Rebooting system...")
        subprocess.run(["shutdown", "-r", "now"])
    elif btn is btn27:
        if btn22.is_pressed:
            return
        else:
            print("Shuting down system...")
            subprocess.run(["shutdown", "-h", "now"])


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


def when_pressed(btn):
    if btn.last_pressed is None:
        btn.last_pressed = datetime.datetime.now()
        return
    else:
        delta = datetime.datetime.now() - btn.last_pressed
        if delta.total_seconds() > 0.8:
            btn.last_pressed = datetime.datetime.now()
            return
        else:
            toggle_wifi()


def toggle_wifi():
    if is_wifi_on():
        print("Turing wifi off ...")
        subprocess.run(["iwconfig","wlan0", "txpower", "off"])
    else:
        print("Turning wifi on ...")
        subprocess.run(["iwconfig", "wlan0", "txpower", "auto"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        subprocess.run(["iwconfig", "wlan0", "txpower", "auto"])

def is_wifi_on():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    result = fcntl.ioctl(s.fileno(), 0x8913, 'wlan0'+'\0'*256)
    flags, = struct.unpack('H', result[16:18])
    up = flags & 1
    s.close()
    del s
    return up == 1
    


if __name__=="__main__":

    btn22.when_held = when_btn_held
    btn27.when_held = when_btn_held
    btn22.when_pressed = when_pressed

    print("Waiting for screen button...")

    while True:
        time.sleep(100)


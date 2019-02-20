# RaspberryPiRebootButton

## How to install
1. Place `screen_btn.py` and `screen-btn.service` file to somewhere like `/usr/share/screen-btn/`.
2. Update `screen-btn.service`, replace `ExecStart` with the correct path.
3. Link `screen-btn.service` to `/etc/systemd/system/`.
4. Enable `screen-btn.service` with systemctl.

## How to use
* Press button on BCM22 for 5 seconds to reboot.
* Press button on BCM27 for 10 seconds to shutdown.
* Press buttons on BCM22 and BCM27 simultaneously for 5 seconds to switch output between LCD and HDMI and reboot.


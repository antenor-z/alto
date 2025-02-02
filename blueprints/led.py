from flask import Blueprint, session
from notlogged import try_logged, NotLoggedError
import atexit
import time
import os
led = Blueprint('led', __name__)

from arduinoInterface import send_color

def get_current_color_from_file():
    if os.path.exists("currentColor"):
        with open("currentColor", "r") as fp:
            color = fp.read().strip()
            if len(color) == 6 and all(c in "0123456789abcdefABCDEF" for c in color):
                return color
    return "000000"

def write_color_to_file(color):
    with open("currentColor", "w") as fp:
        fp.write(color)

def _write_color(color: str, save=True):
    if color.startswith("#"):
        color = color[1:]
    if len(color) != 6 or not all(c in "0123456789abcdefABCDEF" for c in color):
        raise ValueError("Invalid color code")

    print("Hex color:", color)
    #fade_color(get_current_color(), color)
    send_color(color)
    if save:
        write_color_to_file(color)

    return "ok"

@led.get("/currentColor")
def get_current_color():
    try_logged(session)
    return get_current_color_from_file()

@led.get("/writeColor/<string:color>")
def write_color(color: str):
    try_logged(session)
    return _write_color(color)

def linear(start, end, steps, i):
    diff = end - start
    steps = steps - 1
    alpha = diff / steps
    return int(start + alpha * i)

def fade_color(start_color, end_color):
    n_steps = 15
    for i in range(n_steps):
        r = linear(int(start_color[0:2], 16), int(end_color[0:2], 16), n_steps, i)
        g = linear(int(start_color[2:4], 16), int(end_color[2:4], 16), n_steps, i)
        b = linear(int(start_color[4:6], 16), int(end_color[4:6], 16), n_steps, i)
        send_color("{:02x}{:02x}{:02x}".format(r, g, b))
        time.sleep(1 / 30)

def clean_exit():
    _write_color("000000", save=False)

_write_color(get_current_color_from_file())
atexit.register(clean_exit)


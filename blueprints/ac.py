from flask import Blueprint, session
from notlogged import NotLoggedError, try_logged
import atexit
import time
import os
ac = Blueprint('ac', __name__)

from arduinoInterface import *


@ac.get("/ac/temperature/<int:temperature>")
def ac_temperature(temperature):
    try_logged(session)
    write_ac_temperature(temperature)
    return "ok"

@ac.get("/ac/fan/<int:speed>")
def ac_fan(speed):
    try_logged(session)
    write_ac_fan(speed)
    return "ok"

@ac.get("/ac/light")
def ac_toggle_light():
    try_logged(session)
    write_ac_toggle_light()
    return "ok"

@ac.get("/ac/on")
def ac_on():
    try_logged(session)
    write_ac_on()
    return "ok"

@ac.get("/ac/off")
def ac_off():
    try_logged(session)
    write_ac_off()
    return "ok"




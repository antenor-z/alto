from flask import Blueprint, session
from notlogged import NotLoggedError, try_logged
import atexit
import time
import os
temperature = Blueprint('temperature', __name__)

from arduinoInterface import get_temperature

@temperature.get("/temperature")
def get_current_color():
    try_logged(session)
    return str(get_temperature())




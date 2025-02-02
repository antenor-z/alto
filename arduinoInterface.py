import time
import json
from serial import Serial
from config import Config, get_config
from datetime import datetime

config: Config = get_config()

if not config.deactivate_serial:
    ser = Serial(config.serial_port, baudrate=115200, timeout=1)

def send_color(hex_color):
    if not config.deactivate_serial:
        if ser.is_open == False:
            ser.open()

        if len(hex_color) != 6:
            raise ValueError("Hex color must be 6 characters long.")
        for i in hex_color:
            if i not in "0123456789ABCDEFabcdef":
                raise ValueError("Invalid color code")

        message = "#" + hex_color

        print(ser.write(message.encode()))


CACHE_FILE = "temperature.json"

def read_cache():
    try:
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_read": 0, "temperature": 0}

def write_cache(data):
    with open(CACHE_FILE, "w") as file:
        json.dump(data, file)

def get_temperature():
    cache = read_cache()
    current_unix = int(datetime.now().timestamp())

    if not config.deactivate_serial:
        if current_unix < cache["last_read"] + 3:
            return cache["temperature"]

        if not ser.is_open:
            ser.open()

        message = "T"
        ser.write(message.encode())
        time.sleep(0.05)
        temp_str = ser.read_until(expected="\n", size=10).decode()

        try:
            temp = float(temp_str) / 10
        except ValueError:
            return 0.0

        cache["last_read"] = current_unix
        cache["temperature"] = temp

        write_cache(cache)

        return temp

if __name__ == "__main__":
    while(True):
        last_color = "000000"
        to_send = input("#000000 or T: ")
        if to_send.startswith("#"):
            send_color(to_send[1:])
        elif to_send == "T":
            get_temperature()


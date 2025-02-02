import time
from serial import Serial
from config import Config, get_config

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

def get_temperature():
    if not config.deactivate_serial:
        if ser.is_open == False:
            ser.open()
        
        message = "T"

        ser.write(message.encode())
        time.sleep(0.05)
        temp_str = ser.read_until(expected="\n", size=10).decode()
        try:
            temp = float(temp_str) / 10
        except ValueError:
            return 0.0
        return float(temp_str) / 10

if __name__ == "__main__":
    while(True):
        last_color = "000000"
        to_send = input("#000000 or T: ")
        if to_send.startswith("#"):
            send_color(to_send[1:])
        elif to_send == "T":
            get_temperature()


from serial import Serial
from config import Config, get_config

config: Config = get_config()

ser = Serial(config.serial_port, 115200)

def send_color(hex_color):
    if ser.is_open == False:
        ser.open()
    
    if len(hex_color) != 6:
        raise ValueError("Hex color must be 6 characters long.")
    for i in hex_color:
        if i not in "0123456789ABCDEFabcdef":
            raise ValueError("Invalid color code")
    
    message = "#" + hex_color

    print(ser.write(message.encode()))

if __name__ == "__main__":
    while(True):
        color = input("Color: #")
        send_color(color)


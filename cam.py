from json import load
from time import sleep
from dvrip import DVRIPCam

from config import Config, get_config

class CameraController:
    def __init__(self, config_path="config.json"):
        config: Config = get_config(config_path)

        host_ip = config.cam_ip
  
        self.cam = DVRIPCam(host_ip, user=config.cam_user, password=config.cam_password)
        self.cam.login()

    def move(self, direction, step=1):
        if direction == "Left":
            direction = "Right"
            step = 5
        elif direction == "Right":
            direction = "Left"
            step = 5

        self.cam.ptz(f"Direction{direction}", step=step, preset=0)
        sleep(0.5)
        self.cam.ptz(f"Direction{direction}", step=5, preset=-1)
        

# Example usage
# controller = CameraController()
# controller.move("Up")

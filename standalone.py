from json import load
from config import Config, get_config
from dvrip import DVRIPCam

config: Config = get_config()

host_ip = config.cam_ip

with open("config.json") as fp:
    auth = load(fp)
    cam = DVRIPCam(host_ip, user=config.cam_user, password=config.cam_password)
    if cam.login():
        print(f"{host_ip} OK")
    else:
        print("FAIL")
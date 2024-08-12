from dataclasses import dataclass
from json import load


@dataclass
class Config():
    user: str
    password: str
    cam_user: str
    cam_password: str
    RTSP_URL: str
    session_key: str
    totp_token: str
    cam_ip: str
    serial_port: str

def get_config(file: str="config.json") -> Config:
    with open(file) as fp:
        auth = load(fp)
        config = Config(**auth)
        return config
import time
import traceback as tb
import sys

def custom_exception_hook(exctype, value, traceback):
    tb.print_exc(traceback)
    print(f"Exception Type: {exctype}\nValue: {value}")
sys.excepthook = custom_exception_hook

import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '3p'))
from onvif import ONVIFCamera
from config import Config, get_config

class CameraController:
    def __init__(self, config_path="config.json"):    
        # Initialize camera connection and PTZ setup
        config: Config = get_config(config_path)

        ip = config.cam_ip
        port = 80
        user = config.cam_user
        password = config.cam_password
        self.camera = ONVIFCamera(ip, port, user, password)
        self.media = self.camera.create_media_service()
        self.ptz = self.camera.create_ptz_service()
        self.media_profile = self.media.GetProfiles()[0]

        # Create continuous move request
        self.request = self.ptz.create_type('ContinuousMove')
        self.request.ProfileToken = self.media_profile.token

        # Determine velocity ranges
        self._init_velocity_ranges()
        self.request.Velocity = self._get_default_velocity()
        self.active = False

    def _init_velocity_ranges(self):
        # Retrieve PTZ configuration options
        cfg_req = self.ptz.create_type('GetConfigurationOptions')
        cfg_req.ConfigurationToken = self.media_profile.PTZConfiguration.token
        opts = self.ptz.GetConfigurationOptions(cfg_req)

        pan_space = opts.Spaces.ContinuousPanTiltVelocitySpace[0]
        self.x_min, self.x_max = pan_space.XRange.Min / 2, pan_space.XRange.Max / 2
        self.y_min, self.y_max = pan_space.YRange.Min / 2, pan_space.YRange.Max / 2

    def _get_default_velocity(self):
        # Create a default velocity object if needed
        if self.request.Velocity is None:
            status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
            vel = status.Position
            vel.PanTilt.space = self.ptz.GetConfigurationOptions(
                {'ConfigurationToken': self.media_profile.PTZConfiguration.token}
            ).Spaces.ContinuousPanTiltVelocitySpace[0].URI
            return vel
        return self.request.Velocity

    def _do_move(self):
        # Execute and immediately stop continuous move
        if self.active:
            self.ptz.Stop({'ProfileToken': self.request.ProfileToken})
        self.active = True
        self.ptz.ContinuousMove(self.request)
        self.ptz.Stop({'ProfileToken': self.request.ProfileToken})

    def _move(self, x, y):
        # Set pan-tilt velocity and perform move
        self.request.Velocity.PanTilt.x = x
        self.request.Velocity.PanTilt.y = y
        self._do_move()

    def move(self, direction):
        if direction == "Up":
            self._move(0, self.y_max)
        elif direction == "Down":
            self._move(0,   self.y_min)
        elif direction == "Left":
            self._move(self.x_min, 0)
        elif direction == "Right":
            self._move(self.x_max, 0)


if __name__ == '__main__':    
    controller = CameraController('192.168.86.21', 80, 'admin', 't-d1gp9BLVYKzGhB2T*^STQqIMd9NFPV')
    controller.move("Right")


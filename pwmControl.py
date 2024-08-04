import pigpio
import time

red_pin = 17
green_pin = 27
blue_pin = 22

pi = pigpio.pi()
if not pi.connected:
    print("pigpiod: no conection")
    exit(1)


def setPWM(red, green, blue):
    pi.set_PWM_dutycycle(red_pin, red)
    pi.set_PWM_dutycycle(green_pin, green)
    pi.set_PWM_dutycycle(blue_pin, blue)

def testPWM(level, wait):
    setPWM(level, 0, 0)
    time.sleep(wait)
    setPWM(0, level, 0)
    time.sleep(wait)
    setPWM(0, 0, level)
    time.sleep(wait)
    setPWM(0, 0, 0)

def stop():
    print("Releasing pigpio resources")
    pi.stop()
    print("Released pigpio resources")
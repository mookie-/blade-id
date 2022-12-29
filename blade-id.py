from time import sleep
from os.path import exists
import board
import neopixel
import psutil
import RPi.GPIO as GPIO
import configparser
import signal

g, r, b = 0, 0, 0
flag = 0

if exists('/etc/blade-id.conf'):
    config = configparser.RawConfigParser()
    config_path = r'/etc/blade-id.conf'
    config.read(config_path)

    mintemp = config['main'].getint('mintemp', 30)
    maxtemp = config['main'].getint('maxtemp', 50)
    brightness = config['main'].getfloat('brightness', 0.2)
    brightness_id_active = config['main'].getfloat('brightness_id_active', 1)
    button = config['main'].getint('button_gpio', 20)
else:
    mintemp = 30
    maxtemp = 50
    brightness = 0.2
    brightness_id_active = 1
    button = 20


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pixels = neopixel.NeoPixel(
    board.D18, 2, brightness=brightness, auto_write=False, pixel_order=neopixel.GRB
)


def signal_handler(signum, frame):
    signame = signal.Signals(signum).name
    print(f'signal ${signame}')
    global flag
    if signame == 'SIGUSR1':
        flag = 1
    elif signame == 'SIGUSR2':
        flag = 0


signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)


def show(percent, pixel):
    a = int(round((510 / 100) * percent))
    if a > 255:
        r = 255
        g = 510 - a
    else:
        r = a
        g = 255
    pixels[pixel] = (g, r, b)
    pixels.show()


while True:
    temp = int(round(psutil.sensors_temperatures()["cpu_thermal"][0].current))
    button_state = GPIO.input(button)
    if mintemp <= temp <= maxtemp:
        temp = temp - mintemp
        mtemp = maxtemp - mintemp
        c = int(round((temp / mtemp) * 100))
        show(c, 0)
    elif temp < mintemp:
        pixels[0] = (255, 0, 0)
    else:
        pixels[0] = (0, 255, 0)

    sleep(0.1)

    load = psutil.cpu_percent()
    show(load, 1)
    sleep(0.1)

    if button_state == 0:
        sleep(0.5)
        if flag == 0:
            flag = 1
        else:
            flag = 0
    if flag == 1:
        pixels[1] = (0, 0, 255)
        pixels.brightness = brightness_id_active
        pixels.show()
    else:
        pixels.brightness = brightness

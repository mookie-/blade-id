from time import sleep
import board
import neopixel
import psutil
import RPi.GPIO as GPIO

g,r,b = 0,0,0
mintemp = 40 #Temperature Boundaries. Closer to this is green
maxtemp = 70 #Temperature Boundaries. Closer to this is red
LEDbrightness = 0.2 #Yes, you can change the brightness here
Button = 20
flag = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
pixels = neopixel.NeoPixel(
    board.D18, 2, brightness=LEDbrightness, auto_write=False, pixel_order=neopixel.GRB
)

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
#    return print('showed', a, 'on', pixel)

while True:
    temp = int(round(psutil.sensors_temperatures()["cpu_thermal"][0].current))
#    print('temp = ', temp)
    button_state = GPIO.input(Button)
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
 #   print('load = ', load)
    show(load, 1)
    sleep(0.1)

    if button_state == 0:
        sleep(0.5)
        if flag == 0:
            flag = 1
        else:
            flag = 0
    if flag == 1:
        print('Blade ID is active')
        pixels[1] = (0, 0, 255)

    else:
        print('Blade ID isn\'t active')

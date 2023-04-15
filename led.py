from machine import Pin
import utime

onboard = Pin('LED', Pin.OUT)
led = Pin(15, Pin.OUT)

onboard.value(1)
led.value(0)
while True:
    onboard.value(0)
    led.value(1)
    utime.sleep(0.3)
    onboard.value(1)
    led.value(0)
    utime.sleep(0.3)
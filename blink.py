from machine import Pin
import utime

led = Pin('LED', Pin.OUT)

led.value(0)
while True:
    led.value(1)
    utime.sleep(0.3)
    led.value(0)
    utime.sleep(0.3)
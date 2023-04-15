from machine import Pin, ADC
import utime

potPin = 28
pot = ADC(potPin)
low_clip= 400
high_clip = 65200
scale = 100

while True:
    raw = pot.read_u16()
    value = (scale / (high_clip - low_clip)) * (raw - low_clip)
    value = max(value, 0)
    value = min(value, scale)
    value = 100 - value
    print(value)
    utime.sleep(0.2)
    
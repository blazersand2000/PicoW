from machine import Pin, ADC, PWM
import utime

potPin = 28
pot = ADC(potPin)
led = PWM(Pin(11, Pin.OUT))
led.freq(1000)

low_clip= 400
high_clip = 65200
scale = 100

#for brightness in range(0, 65535, 50):
#    led.duty_u16(brightness)
#    utime.sleep_ms(10)
#led.duty_u16(0)

while True:
    raw = pot.read_u16()
    led.duty_u16(raw)
    utime.sleep_ms(10)
    
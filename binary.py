from machine import Pin
import utime

def main():
    pins = ( Pin(15, Pin.OUT),
             Pin(14, Pin.OUT),
             Pin(18, Pin.OUT),
             Pin(19, Pin.OUT)  )

    n = 0
    while True:
        set_leds(pins, n)
        print(bin(n))
        n = n + 1
        n = n % 16
        utime.sleep(1)

def set_leds(pins, n):
    for power in range(4):
        if 2**power & n > 0:
            pins[power].value(1)
        else:
            pins[power].value(0)

if __name__ == "__main__":
    main()
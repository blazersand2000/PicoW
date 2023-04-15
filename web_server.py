import network
import socket
import time

from machine import Pin

led = Pin(11, Pin.OUT)
led.value(0)

ssid = 'Tom Brady - G.O.A.T.'
password = 'ripcityforever'
hostname = 'Andrew_PicoW'

network.hostname(hostname)
network.country('US')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body>
        <h1>Pico W</h1>
        <p>%s</p>
        <div>
            <form action="/light/on" method="GET">
                <input type="submit" value="Turn LED on">
            </form>
        </div>
        <div>
            <form action="/light/off" method="GET">
                <input type="submit" value="Turn LED off">
            </form>
        </div>
    </body>
</html>
"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))

        if led_on == 6:
            led.value(1)

        if led_off == 6:
            led.value(0)
            
        if led.value() == 1:
            stateis = "LED is ON"
            print("led on")
        else:
            stateis = "LED is OFF"
            print("led off")
            
        response = html % stateis

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')

    
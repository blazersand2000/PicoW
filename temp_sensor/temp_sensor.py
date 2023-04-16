import network
import urequests
import time
import uasyncio as asyncio
from machine import Pin

led = Pin(15, Pin.OUT)
onboard = Pin("LED", Pin.OUT, value=0)

template = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> 
        <h1>Pico W</h1>
        <p>%s</p>
    </body>
</html>
"""

temperatures = []

def connect_to_network():
    ssid = 'Tom Brady - G.O.A.T.'
    password = 'ripcityforever'
    hostname = 'Andrew_PicoW'
    
    network.hostname(hostname)
    network.country('US')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power-save mode
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        log('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        log('connected')
        status = wlan.ifconfig()
        log('ip = ' + status[0])
        
    return wlan

async def serve_client(reader, writer):
    log("Client connected")
    request_line = await reader.readline()
    log("Request:" + str(request_line))
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    html = '\n'.join(f'<p>{temp}</p>' for temp in list(reversed(temperatures))) if len(temperatures) > 0 else ''
    response = template % html
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    log("Client disconnected")

async def main():
    log('Connecting to network...')
    wlan = connect_to_network()

    log('Setting up web server...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    
    asyncio.create_task(heartbeat())
    
    while True:
        try:
            log('Fetching weather for Tampa...')
            url = 'https://api.open-meteo.com/v1/forecast?latitude=27.95&longitude=-82.46&hourly=temperature_2m&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
            r = urequests.get(url)
            data = r.json()
            r.close()
            temp = data['current_weather']['temperature']
            message = f'Current temperature in Tampa is {temp} F.'
            global temperatures
            temperatures.append(log(message, False))
            temperatures = temperatures[-100:]
            log(message)
        except Exception as ex:
            # print(ex)
            log("could not connect (status =" + str(wlan.status()) + ")")
            log("trying to reconnect...")
            wlan.disconnect()
            wlan = connect_to_network()
        await asyncio.sleep(60)
        
async def heartbeat():
    while True:
        onboard.on()
        # log("heartbeat")
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(5)
        
def log(s, shouldPrint = True):
    f = lambda n : f'0{n}' if n < 10 else f'{n}'
    t = time.localtime()
    log = f'{t[0]}-{f(t[1])}-{f(t[2])} {f(t[3])}:{f(t[4])}:{f(t[5])}\t{s}'
    if shouldPrint:
        print(log)
    return log

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
import network
import urequests
import uasyncio
import queue
import output
import temp_sensor
from machine import Pin, ADC
from state import State
from logger import log
from wifi import wifi_loop

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

async def handle_request(reader, writer):
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
    wifi_status_q = queue.Queue()
    log('Connecting to network...')
    uasyncio.create_task(wifi_loop(wifi_status_q))

    log('Setting up web server...')
    uasyncio.create_task(uasyncio.start_server(handle_request, "0.0.0.0", 80))
    
    uasyncio.create_task(heartbeat())
    
    output_q = queue.Queue()
    temperature_q = queue.Queue()

    out = output.Output()
    uasyncio.create_task(out.output_loop(output_q))

    uasyncio.create_task(temp_sensor.read_temp_loop(temperature_q))

    state = State(output_q)

    while True:
        if not temperature_q.empty():
            temperature = await temperature_q.get()
            await state.set_temperature(temperature)
        if not wifi_status_q.empty():
            wifi_status = await wifi_status_q.get()
            await state.set_wifi_status(wifi_status)
        await uasyncio.sleep_ms(0)
    
    # while True:
    #     try:
    #         log('Fetching weather for Tampa...')
    #         url = 'https://api.open-meteo.com/v1/forecast?latitude=27.95&longitude=-82.46&hourly=temperature_2m&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
    #         r = urequests.get(url)
    #         data = r.json()
    #         r.close()
    #         temp = data['current_weather']['temperature']
    #         message = f'Current temperature in Tampa is {temp} F.'
    #         global temperatures
    #         temperatures.append(log(message, False))
    #         temperatures = temperatures[-100:]
    #         log(message)
    #     except Exception as ex:
    #         # print(ex)
    #         log("could not connect (status =" + str(wlan.status()) + ")")
    #         log("trying to reconnect...")
    #         wlan.disconnect()
    #         wlan = connect_to_network()
    #     await uasyncio.sleep(60)
        
async def heartbeat():
    while True:
        onboard.on()
        # log("heartbeat")
        await uasyncio.sleep(0.25)
        onboard.off()
        await uasyncio.sleep(5)

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()
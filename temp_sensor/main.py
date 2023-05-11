from json import load
import network
import urequests
import uasyncio
import queue
import output
import temp_sensor
from settings import load_settings
from machine import Pin, ADC
from state import State
from temp_publisher import TempPublisher
from logger import log_info
from phew.logging import *
from wifi import wifi_loop
import web_server

async def main():
    #set_log_levels()

    uasyncio.create_task(State.state_loop())

    wifi_status_q = queue.Queue()
    uasyncio.create_task(wifi_loop(wifi_status_q))

    web_server.run()

    temperature_q = queue.Queue()

    uasyncio.create_task(temp_sensor.read_temp_loop(temperature_q))

    settings = load_settings()
    await State.state_q.put((State.set_settings, settings))

    publisher = TempPublisher()
    uasyncio.create_task(publisher.publish_temp_loop())

    while True:
        if not temperature_q.empty():
            temperature = await temperature_q.get()
            await State.state_q.put((State.set_temperature, temperature))
        if not wifi_status_q.empty():
            wifi_status = await wifi_status_q.get()
            await State.state_q.put((State.set_wifi_status, wifi_status))
        await uasyncio.sleep_ms(0)

def set_log_levels():
    disable_logging_types(LOG_INFO | LOG_DEBUG)

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()
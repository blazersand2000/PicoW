import uasyncio
import queue
from machine import Pin
import onewire
import ds18x20
import time
from phew.logging import info, error

SensorPin = Pin(26, Pin.IN)
sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))
roms = sensor.scan()
if len(roms) != 1:
    error(f'Detected {len(roms)} temperature sensors but expected 1')
rom = roms[0]

async def read_temp_loop(q: queue.Queue):
    while True:
        sensor.convert_temp()
        await uasyncio.sleep(2)
        try:
            celsius = sensor.read_temp(rom)
            if celsius >= 85.0:
                error('Received maximum temperature reading which likely indicates a connection issue with the temperature sensor probe')
        except Exception as ex:
            error(f'Temperature read failed. Exception: {str(ex)}')
        else:
            fahrenheit = celsius * 9 / 5 + 32
            info(f'Temperature reading (F): {fahrenheit}')
            await q.put(fahrenheit)

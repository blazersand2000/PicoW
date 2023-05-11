import uasyncio
import queue
from machine import ADC
from phew.logging import info

   
async def read_temp_loop(q: queue.Queue):
    temp_sensor = ADC(4)
    while True:
        voltage = temp_sensor.read_u16() * 3.3 / 65535
        celsius = 27 - (voltage - 0.706) / 0.001721
        fahrenheit = celsius * 9 / 5 + 32
        info(f'Temperature reading (F): {fahrenheit}')
        await q.put(fahrenheit)
        await uasyncio.sleep(1)


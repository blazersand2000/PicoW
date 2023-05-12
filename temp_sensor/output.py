import uasyncio
import queue
from state import State, OutputState
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332
from pimoroni import RGBLED
import gc
import my_time

class Output:
    def __init__(self) -> None:
        self._current_state = None
        self._screen_on = False
        self._screenOnHour = 0
        self._screenOnMinute = 0
        self._screenOffHour = 0
        self._screenOffMinute = 0
        self._rotated = False
        self._display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332)
        self._width, self.height = self._display.get_bounds()
        self._current_y_offset = 0
        self._bg_pen = self._display.create_pen(0, 0, 0)
        self._is_temp_within_range = True
        self._temp_pen_within_range = self._display.create_pen(100, 255, 100)
        self._temp_pen_outside_range = self._display.create_pen(255, 0, 100)
        self._label_pen = self._display.create_pen(255, 255, 255)
        self._value_pen = self._display.create_pen(200, 200, 255)
    
    async def output_loop(self, q: queue.Queue):
        led = RGBLED(6, 7, 8)
        while True:
            await self.__check_if_screen_should_be_turned_on_or_off(q)
            if not q.empty():
                output: OutputState = await q.get()
                self._current_state = output
                self.__update_screen_on_and_off_time(output)
                self.__set_rotation(output.rotated)
                self.__set_temp_within_range(output)

                self._current_y_offset = 0
                self.__set_background(output.brightness)
                self.__write_temp(output.temperature)
                self.__write_value(output.hostname, 'Name: ')
                self.__write_value(output.status, 'WiFi: ')
                self.__write_value(output.ip, 'IP: ')
                self._display.update()

            self.__set_led(led)
            await uasyncio.sleep(1.0 / 60)

    def __update_screen_on_and_off_time(self, output: OutputState):
        self._screenOnHour = output.screenOnHour
        self._screenOnMinute = output.screenOnMinute
        self._screenOffHour = output.screenOffHour
        self._screenOffMinute = output.screenOffMinute
    
    async def __check_if_screen_should_be_turned_on_or_off(self, q: queue.Queue):
        current_time = my_time.localtime()
        current_hour = current_time[3]
        current_minute = current_time[4]
        should_be_on = (current_hour > self._screenOnHour or (current_hour == self._screenOnHour and current_minute >= self._screenOnMinute)) and (current_hour < self._screenOffHour or (current_hour == self._screenOffHour and current_minute < self._screenOffMinute))
        if self._screen_on != should_be_on:
            self._screen_on = should_be_on
            await q.put(self._current_state)
    
    def __set_led(self, led):
        if not self._is_temp_within_range and my_time.localtime()[5] % 2 == 0:
            led.set_rgb(255, 0, 0)
        elif not self._current_state.connected if self._current_state is not None else True:
            led.set_rgb(255, 255, 0)
        else:
            led.set_rgb(0, 0, 0)

    def __set_rotation(self, rotated):
        if rotated != self._rotated:
            self._display = None
            gc.collect()
            rotation = 180 if rotated else 0
            self._display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332, rotate=rotation)
            self._rotated = rotated

    def __set_background(self, brightness):
        self._display.set_backlight(0 if not self._screen_on else brightness)
        self._display.set_pen(self._bg_pen)
        self._display.clear()

    def __write_temp(self, temp):
        pen = self._temp_pen_within_range if self._is_temp_within_range else self._temp_pen_outside_range
        def __write_f(f_offset):
            self._display.set_pen(pen)
            self._display.set_font('sans')
            thickness = 2
            self._display.set_thickness(thickness)
            scale = 1
            y_offset = 12 * scale + thickness
            self._display.text('F', f_offset, y_offset + 1, scale=scale)
        self._display.set_pen(pen)
        self._display.set_font('sans')
        thickness = 6
        self._display.set_thickness(thickness)
        scale = 4
        y_offset = 12 * scale + thickness
        text = str(f'{temp:.1f}') if temp is not None else ''
        self._display.text(text, 0, y_offset + 1, scale=scale)
        x_offset = self._display.measure_text(text, scale)
        if text is not None:
          __write_f(x_offset)
        self._current_y_offset = self._current_y_offset + 111

    def __write_value(self, value_text, label_text = None):
        self._display.set_font('bitmap8')
        thickness = 2
        self._display.set_thickness(thickness)
        scale = 2
        x_offset = 0
        if label_text is not None:
            self._display.set_pen(self._label_pen)
            self._display.text(label_text, 0, self._current_y_offset, scale=scale)
            x_offset = self._display.measure_text(label_text, scale)
        self._display.set_pen(self._value_pen)
        self._display.text(value_text, x_offset, self._current_y_offset, scale=scale)
        self._current_y_offset = self._current_y_offset + 20

    def __set_temp_within_range(self, output: OutputState):
        self._is_temp_within_range = output.temperature is None or output.min_temp <= output.temperature <= output.max_temp


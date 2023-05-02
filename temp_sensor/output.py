import uasyncio
import queue
from state import State, OutputState
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332

class Output:
    def __init__(self) -> None:
        self._display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332)
        self._width, self.height = self._display.get_bounds()
        self._current_y_offset = 0
        self._bg_pen = self._display.create_pen(0, 0, 0)
        self._temp_pen = self._display.create_pen(100, 255, 100)
        self._label_pen = self._display.create_pen(255, 255, 255)
        self._value_pen = self._display.create_pen(200, 200, 255)
    
    async def output_loop(self, q: queue.Queue):
        while True:
            if not q.empty():
                output: OutputState = await q.get()

                self._current_y_offset = 0
                self.__set_background()
                self.__write_temp(output.temperature)
                self.__write_value(output.hostname, 'Name: ')
                self.__write_value(output.status, 'WiFi: ')
                self.__write_value(output.ip, 'IP: ')
                self._display.update()

            await uasyncio.sleep_ms(0)

    def __set_background(self):
        self._display.set_backlight(0.4)    
        self._display.set_pen(self._bg_pen)
        self._display.clear()

    def __write_temp(self, temp):
        def __write_f(f_offset):
            self._display.set_pen(self._temp_pen)
            self._display.set_font('sans')
            thickness = 2
            self._display.set_thickness(thickness)
            scale = 1
            y_offset = 12 * scale + thickness
            self._display.text('F', f_offset, y_offset + 1, scale=scale)
        self._display.set_pen(self._temp_pen)
        self._display.set_font('sans')
        thickness = 6
        self._display.set_thickness(thickness)
        scale = 4
        y_offset = 12 * scale + thickness
        text = str(f'{temp:.1f}')
        self._display.text(text, 0, y_offset + 1, scale=scale)
        x_offset = self._display.measure_text(text, scale)
        __write_f(x_offset)
        self._current_y_offset = self._current_y_offset + 111

    def __write_value(self, value_text, label_text = None):
        # TODO: handle unimplemented characters
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


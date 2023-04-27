import uasyncio
import queue
from state import State, OutputState
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332

class Output:
    def __init__(self) -> None:
        self._display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332)
        self._width, self.height = self._display.get_bounds()
        self._bg_pen = self._display.create_pen(40, 40, 40)
        self._temp_pen = self._display.create_pen(100, 255, 100)
        self._text_pen = self._display.create_pen(255, 255, 255)
    
    async def output_loop(self, q: queue.Queue):
        while True:
            if not q.empty():
                output: OutputState = await q.get()

                self._display.set_backlight(0.4)    
                self._display.set_pen(self._bg_pen)
                self._display.clear()

                f_offset = self.__write_temp(output._temperature)

                self._display.set_pen(self._temp_pen)
                self._display.set_font('sans')
                thickness = 2
                self._display.set_thickness(thickness)
                scale = 1
                y_offset = 12 * scale + thickness
                self._display.text('F', f_offset, y_offset + 1, scale=scale)


                self._display.set_pen(self._text_pen)
                self._display.set_font('sans')
                thickness = 2
                self._display.set_thickness(thickness)
                scale = 1
                y_offset = 110
                self._display.text('Test', 0, y_offset + 1, scale=scale)
                
                self._display.update()

            await uasyncio.sleep_ms(0)

    def __write_temp(self, temp):
        self._display.set_pen(self._temp_pen)
        self._display.set_font('sans')
        thickness = 6
        self._display.set_thickness(thickness)
        scale = 4
        y_offset = 12 * scale + thickness
        text = str(f'{temp:.1f}')
        self._display.text(text, 0, y_offset + 1, scale=scale)
        return self._display.measure_text(text, scale)

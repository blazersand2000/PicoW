import time
import random
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332)
display.set_backlight(0.4)

WIDTH, HEIGHT = display.get_bounds()
BG = display.create_pen(40, 40, 40)
TEXT = display.create_pen(100, 255, 100)
WHITE = display.create_pen(255, 255, 255)
    
display.set_pen(BG)
display.clear()

def write_temp(display):
    display.set_pen(TEXT)
    display.set_font('sans')
    thickness = 6
    display.set_thickness(thickness)
    scale = 4
    y_offset = 12 * scale + thickness
    text = '38.2'
    display.text(text, 0, y_offset + 1, scale=scale)
    return display.measure_text(text, scale)

f_offset = write_temp(display)

display.set_pen(TEXT)
display.set_font('sans')
thickness = 2
display.set_thickness(thickness)
scale = 1
y_offset = 12 * scale + thickness
display.text('F', f_offset, y_offset + 1, scale=scale)


display.set_pen(WHITE)
display.set_font('sans')
thickness = 2
display.set_thickness(thickness)
scale = 1
y_offset = 110
display.text('Test', 0, y_offset + 1, scale=scale)



display.update()



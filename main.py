from ble_peripheral import LEDGridPeripheral
from led import Grid
import time

grid = Grid()
peripheral = LEDGridPeripheral("TedsGrid", grid.set_colours, grid.set_delay)

while True:
    grid.draw()
    time.sleep(0.1)


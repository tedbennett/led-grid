import machine
from neopixel import NeoPixel

import time 
LED_COUNT = 64
LED_PIN = 5

class Grid(NeoPixel):
  def __init__(self):
    super().__init__(machine.Pin(LED_PIN), LED_COUNT)
    self.colours = [(0, 0, 0)] * 64

  def set_colours(self, colours):
    self.colours = colours

  def draw(self):
    for index, colour in enumerate(self.colours):
      self[index] = colour
    self.write()

if __name__ == "__main__":
  grid = Grid()
  grid.colours = [(10,10,10)] * 64
  grid.draw()
  time.sleep(10)
  grid.colours = [(0,0,0)] * 64
  grid.draw()
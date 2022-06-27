import machine
from neopixel import NeoPixel

LED_COUNT = 64
LED_PIN = 5


class Grid(NeoPixel):
    def __init__(self):
        super().__init__(machine.Pin(LED_PIN), LED_COUNT)
        self.colours = [(0, 0, 0)] * 64
        self.delay = 5
        self.timer = machine.Timer(1)

    def set_delay(self, delay):
        self.delay = delay

    def set_colours(self, colours):
        self.timer.deinit()
        self.colours = colours
        self.timer.init(
            mode=machine.Timer.ONE_SHOT, period=self.delay * 1000, callback=self.clear
        )

    def draw(self):
        for index, colour in enumerate(self.colours):
            self[index] = colour
        self.write()

    def clear(self, timer):
        self.colours = [(0, 0, 0)] * 64
        self.timer.deinit()

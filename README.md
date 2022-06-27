# LED Grid

LED Grid is a repositiory for an ESP32 microcontroller powering an 8x8 LED grid and is the companion to my
LED Grid iOS app.

## Installation

### Board Setup

The components for this are very simple, all that is needed is an ESP32 board, an 8x8 LED grid and 3 cables.
The LED Grid is connected to the boards 5V, Ground and G5 pins.

### Flashing the ESP32

The Python scripts in this repo need to flashed to the ESP32. I used Thonny for this, and tutorials can be
found online describing how to get started with that.

Once the files have been copied to the ESP32, the Bluetooth server can be started by running the `main.py`
from the REPL or by adding the line `import main` to `boot.py` so that the server is started whenever the
ESP32 is powered on.

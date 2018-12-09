# Wiring
# ItsyBitsy        NeoTrellis
#   SDA      <—>      SDA
#   SCL      <—>      SCL
#   Vin      <—>      Vin
#   Ground   <—>      Ground
#   10       <—>      Interrupt

import time
import random
import board
from board import SCL, SDA
import digitalio
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

# create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

# create the trellis
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x30)],
    [NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x31)]
    ]
 
trellis = MultiTrellis(trelli)

button_pin = board.D10

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# some color definitions
OFF = (0, 0, 0)
RED = (25, 0, 0)
ORANGE = (25, 10, 0)
YELLOW = (25, 25, 0)
GREEN = (0, 25, 0)
CYAN = (0, 25, 25)
BLUE = (0, 0, 25)
MAGENTA = (25, 0, 25)
PURPLE = (10, 0, 25)
WHITE = (127, 127, 127)

PUSH_COLOR = WHITE
ANIM_COLOR = WHITE

COLORS = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, MAGENTA, PURPLE, WHITE]
buttons = []

# this will be called when button events are received
def blink(xcoord, ycoord, edge):
    # turn the LED on when a rising edge is detected
    if edge == NeoTrellis.EDGE_RISING:
        trellis.color(xcoord, ycoord, PUSH_COLOR)

    # turn the LED off when a rising edge is detected
    elif edge == NeoTrellis.EDGE_FALLING:
        if buttons[xcoord][ycoord] == OFF or buttons[xcoord][ycoord] == COLORS[len(COLORS) - 1]:
            trellis.color(xcoord, ycoord, RED)
            buttons[xcoord][ycoord] = RED
        else:
            trellis.color(xcoord, ycoord, COLORS[COLORS.index(buttons[xcoord][ycoord]) + 1])
            buttons[xcoord][ycoord] = COLORS[COLORS.index(buttons[xcoord][ycoord]) + 1]
            
for y in range(8):
    for x in range(8):
        #activate rising edge events on all keys
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        #activate falling edge events on all keys
        trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
        trellis.set_callback(x, y, blink)
        trellis.color(x, y, ANIM_COLOR)
        time.sleep(.02)
 
for y in range(8):
    row = []
    for x in range(8):
        trellis.color(x, y, OFF)
        row.append(OFF)
        time.sleep(.02)
    buttons.append(row);

while True:
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(.02)

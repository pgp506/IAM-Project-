
"""This code is taken from the IAM labs and
modified to fit the Selene Looper Pedal.
Alterations include the addition of writing
saying "SELENE LOOPER" and a star picture showing
when the microbit is turned on.

midiNoteOn(0, BUTTON_A_NOTE, 127) lines were changed
to fit the seperate channels in MAX 7.
"""

from microbit import *
import math

def midiNoteOn(chan, n, vel):
    MIDI_NOTE_ON = 0x90
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_ON | chan, n, vel])
    uart.write(msg)

def midiNoteOff(chan, n, vel):
    MIDI_NOTE_OFF = 0x80
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_OFF | chan, n, vel])
    uart.write(msg)

def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15:
        return
    if n > 127:
        return
    if value > 127:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)

def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

Start()
lastA = False
lastB = False
lastC = False
BUTTON_A_NOTE = 36
BUTTON_B_NOTE = 39
BUTTON_C_NOTE = 43
last_tilt = 0
last_pot = 0
while True:
    pot = pin2.read_analog()
    if last_pot != pot:
        velocity = math.floor(pot / 1024 * 127)
        midiControlChange(0, 23, velocity)
    last_pot = pot

    a = button_a.was_pressed()
    b = button_b.was_pressed()
    c = pin1.is_touched()
    display.scroll("SELENE LOOPER")
    sleep(5000)
    display.show(Image(
        "90909:"
        "09990:"
        "99999:"
        "09990:"
        "90909"))
    sleep(5000)
    if a is True and lastA is False:
        midiNoteOn(0, BUTTON_A_NOTE, 127)
    elif a is False and lastA is True:
        midiNoteOff(0, BUTTON_A_NOTE, 127)
    if b is True and lastB is False:
        midiNoteOn(1, BUTTON_B_NOTE, 127)
    elif b is False and lastB is True:
        midiNoteOff(1, BUTTON_B_NOTE, 127)
    if c is True and lastC is False:
        midiNoteOn(2, BUTTON_C_NOTE, 127)
    elif c is False and lastC is True:
        midiNoteOff(2, BUTTON_C_NOTE, 127)

    lastA = a
    lastB = b
    lastC = c
    current_tilt = accelerometer.get_y()
    if current_tilt != last_tilt:
        mod_y = math.floor(math.fabs(((current_tilt + 1024) / 2048 * 127)))
        midiControlChange(0, 22, mod_y)
        last_tilt = current_tilt
    sleep(10)
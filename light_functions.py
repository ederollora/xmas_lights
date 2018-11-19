import RPi.GPIO as GPIO
from collections import deque
from itertools import permutations
import time
import random


# Turn off warnings
GPIO.setwarnings(False)

# Set pin mapping to board, use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)


class Pin(object):
    def __init__(self, pin_number, jumper_color, relay_number):
        self.pin_number = pin_number
        self.jumper_color = jumper_color
        self.relay_number = relay_number

pin1 = Pin(pin_number=17, jumper_color="blue", relay_number=1)
pin2 = Pin(pin_number=18, jumper_color="yellow", relay_number=2)
pin3 = Pin(pin_number=27, jumper_color="purple", relay_number=3)
pin4 = Pin(pin_number=22, jumper_color="green", relay_number=4)

pins = [
    pin1, pin2, pin3, pin4,
]

pin_numbers = [pin.pin_number for pin in pins]
relay_numbers = [pin.relay_number for pin in pins]
relay_pin_map = dict(zip(relay_numbers, pin_numbers))

# GPIO.LOW = relay on, GPIO.HIGH = relay off
on = lambda pin: GPIO.output(pin, GPIO.LOW)
off = lambda pin: GPIO.output(pin, GPIO.HIGH)


# "any" function executes the function on the iterator but doesn't return anything
# This is the same as "for pin in pins: GPIO.setup"
for pin in pin_numbers:
    GPIO.setup(pin, GPIO.OUT)

######################
#    GPIO FUNCTIONS  #
######################

def reverse_light(pin_number):
    it_is_on = GPIO.input(pin_number)

    if it_is_on:
        off(pin_number)
    else:
        on(pin_number)

def super_blink(*, pin_numbers: list, iterations=1, sleep=1) -> None:
    while iterations > 0:
        any(on(pin_number) for pin_number in pin_numbers)
        time.sleep(sleep)
        any(off(pin_number) for pin_number in pin_numbers)
        time.sleep(sleep)
        iterations -= 1

def blink(*, pin_numbers: list, iterations=1, sleep=2) -> None:
    """Turn all pins on, sleep, turn all pins off"""
    while iterations > 0:
        any(on(pin_number) for pin_number in pin_numbers)
        time.sleep(sleep)
        any(off(pin_number) for pin_number in pin_numbers)
        time.sleep(sleep)
        iterations -= 1

def step(*, pin_numbers: list, iterations=1, sleep=1.5) -> None:
    """Turn a pin on then off then move onto the next pin"""
    while iterations > 0:
        for pin in pin_numbers:
            on(pin)
            time.sleep(sleep)
            off(pin)
        iterations -= 1

def climb(*, pin_numbers: list, iterations=1, sleep=2) -> None:
    """Turn the pins on in order then off in reverse"""
    climb_number = len(pin_numbers)
    reversed_pin_numbers = reversed(pin_numbers)

    while iterations > 0:
        for index, pin in enumerate(pin_numbers):
            if index <= climb_number:
                on(pin)
                time.sleep(sleep)
        for pin in reversed_pin_numbers:
            off(pin)
            time.sleep(sleep)
        iterations -= 1

def randomshow(*, pin_numbers: list, iterations=1, sleep=2) -> None:

    FIRST_GROUP = 0
    SECOND_GROUP = 1
    FIRST_LIGHT = 0
    SECOND_LIGHT = 1

    #random_pins = pin_numbers
    #random.shuffle(random_pins)

    random_pins = round_robin_even(len(pin_numbers))
    random.shuffle(random_pins)

    for kb in random_pins:
        while iterations > 0:
            if iterations % 2 == 0:
                on(kb[FIRST_GROUP][FIRST_LIGHT])
                on(kb[FIRST_GROUP][SECOND_LIGHT])
                off(kb[SECOND_GROUP][FIRST_LIGHT])
                off(kb[SECOND_GROUP][SECOND_LIGHT])
            else:
                off(kb[FIRST_GROUP][FIRST_LIGHT])
                off(kb[FIRST_GROUP][SECOND_LIGHT])
                on(kb[SECOND_GROUP][FIRST_LIGHT])
                on(kb[SECOND_GROUP][SECOND_LIGHT])

            time.sleep(sleep)
            iterations -= 1

def allonshow(*, pin_numbers: list, iterations=1, sleep=1) -> None:
    any(on(pin_number) for pin_number in pin_numbers)
    time.sleep(sleep)

def simpleshow(*, pin_numbers: list, iterations=10, sleep=1) -> None:
    while iterations > 0:
        if (iterations % 2 == 0):
            on(pin_numbers[0])
            on(pin_numbers[2])
            off(pin_numbers[1])
            off(pin_numbers[3])
        else:
            off(pin_numbers[0])
            off(pin_numbers[2])
            on(pin_numbers[1])
            on(pin_numbers[3])

        time.sleep(sleep)
        iterations -= 1

def light_show():
    """
    Choose a random light function
    Execute it for a random number of iterations between 1-5
    Sleep for a random time during function between .1 and .5 seconds
    """
    all_pins = pin_numbers
    even_pins = pin_numbers[0:][::2]
    odd_pins = pin_numbers[1:][::2]
    random_pin = [random.choice(pin_numbers)]
    first_half_pins = pin_numbers[:int(len(pin_numbers) / 2)]
    second_half_pins = pin_numbers[int(len(pin_numbers) / 2):]
    random_sleep = float(str(random.uniform(1, 2))[:4])
    random_iterations = random.choice(list(range(5)))

    functions = [super_blink, step, climb]
    pin_configs = [
        all_pins, even_pins, odd_pins,
        first_half_pins, second_half_pins, random_pin
    ]

    random.choice(functions)(
        pin_numbers=random.choice(pin_configs),
        iterations=random_iterations,
        sleep=random_sleep)

def random_show():
    randomshow(pin_numbers=pin_numbers)

def allon_show():
    allonshow(pin_numbers=pin_numbers)

def simple_show():
    simpleshow(pin_numbers=pin_numbers)

def ojeblink():
    super_blink(pin_numbers=pin_numbers)

def cycle_all():
    """Turn all pins on in order, sleep, turn all pins off in reverse order"""
    climb(pin_numbers=pin_numbers)

def all_pins_off():
    """Turn off all pins"""
    any(off(pin) for pin in pin_numbers)
    time.sleep(1)

def round_robin_even(n):
    d = deque(range(n))
    for i in range(n - 1):
        yield [[d[j], d[-j-1]] for j in range(n//2)]
        d[0], d[-1] = d[-1], d[0]
        d.rotate()

def cleanup():
    GPIO.cleanup()

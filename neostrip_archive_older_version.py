import time
import machine
import neopixel
import json
from machine import Pin, PWM, Timer
import random

NUMBER_OF_PIXELS = 144
# https://roger-random.github.io/RGB332_color_wheel_three.js/

NEO_PIXEL_PINS = [15, 16]


# Hilfsfunktion zur Farbberechnung
def extract_and_scale(value, mask, scale_factor):
    return (value * 255) // scale_factor


def byte_to_rgb2222(byte_value):
    r = (byte_value >> 4) & 0b11  # Extrahiere die oberen 2 Bits (Rot)
    g = (byte_value >> 2) & 0b11  # Extrahiere die Bits 5-4 (Grün)
    b = byte_value & 0b11  # Extrahiere die Bits 3-2 (Blau)
    brightness = (((byte_value >> 6) & 0b11) + 1) * 16
    return r * brightness, g * brightness, b * brightness  # Rückgabe als Tupel


def rgb2222_to_byte(brightness, rgb):
    r, g, b = rgb
    r = r & 0b00000011
    g = g & 0b00000011
    b = b & 0b00000011
    brightness = brightness & 0b00000011
    return (brightness << 6) | (r << 4) | (g << 2) | b


# Beispiel
# rgb_value = (128, 64, 255)  # Beispiel-RGB-Tuple
# color_byte = rgb_to_byte(rgb_value)
# print(f"RGB {rgb_value} → Byte: {color_byte} (0x{color_byte:02X})")

class Neostrip:
    def __init__(self, neo_pin, timer_id, period=50):
        self.MODES = ["off", "on", "rotate_left", "rotate_right"]
        self.neo_pin = neo_pin
        self.pixels = neopixel.NeoPixel(Pin(neo_pin), NUMBER_OF_PIXELS)
        # self.timer = Timer(timer_id)
        # self.timer.init(period=period, mode=Timer.PERIODIC, callback=self.timer_callback)
        self.mode = self.MODES[0]

    def set_mode(self, mode: str) -> None:
        if mode in self.MODES:
            self.mode = mode

    # def set_period(self, period: int) -> None:
    #    self.timer.init(period=period, mode=Timer.PERIODIC, callback=self.timer_callback)

    def set_pattern(self, pattern: list[int]) -> None:
        print(f"set_pattern: {pattern}")

        for i in range(0, NUMBER_OF_PIXELS):
            self.pixels[i] = byte_to_rgb2222(pattern[i % len(pattern)])
        self.mode = self.MODES[1]
        # self.pixels.fill((0, 3, 0))
        self.pixels.write()

    def timer_callback(self, timer: Timer) -> None:
        #if self.mode == self.MODES[0]:
        #    self.pixels.fill((0, 0, 0))
        #elif self.mode == self.MODES[1]:
        #    pass
        #    # self.pixels.fill((255, 255, 255))
        #elif self.mode == self.MODES[2]:
        #    self.rotate_left()
        #elif self.mode == self.MODES[3]:
        #    self.rotate_right()
        # self.pixels.write()
        pass

    def rotate_right(self) -> None:
        temp = self.pixels[-1]
        self.pixels[1:] = self.pixels[:-1]
        self.pixels[0] = temp

    def rotate_left(self) -> None:
        temp = self.pixels[0]
        self.pixels[0:-1] = self.pixels[1:]
        self.pixels[-1] = temp

    def process_input(self, input_data: str) -> None:
        try:
            input_data = json.loads(input_data)
            print(f"process_input: {input_data}")
            if "pattern" in input_data:
                self.set_pattern(input_data["pattern"])
        except ValueError as e:
            print(f"exception process_input: {e}")
            return

    def __del__(self) -> None:
        pass
        # self.timer.deinit()


strip15 = Neostrip(14, 0, period=50)
strip16 = Neostrip(15, 1, period=100)

if __name__ == "__main__":
    strip14 = Neostrip(14, 0, period=50)
    # strip14.process_input('{"pattern":[1,2,3,4,5,6,7,8,9,15,20,40,80,100], "start":0, "repeat":0}')
    while True:
        # Erzeuge eine Liste von 10 zufälligen Integer-Werten zwischen 0 und 100
        pattern = [random.randint(0, 63) for _ in range(NUMBER_OF_PIXELS)]
        # pattern = [rgb2222_to_byte(3, (3, 0, 3))]
        # print(pattern)
        for i in range(0, len(pattern)):
            # strip14.pixels[i] = byte_to_rgb222(pattern[i] & 0b00111111)
            strip14.pixels[i] = byte_to_rgb2222(pattern[i])
            # strip14.pixels[i] = byte_to_rgb(pattern[i])
        strip14.pixels.write()
        time.sleep(0.05)

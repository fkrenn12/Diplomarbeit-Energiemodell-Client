import neopixel
from machine import Pin, PWM, Timer

NUMBER_OF_PIXELS = 144
# https://roger-random.github.io/RGB332_color_wheel_three.js/

NEO_PIXEL_PINS = [14, 15]
# Konstanten für Bitmasken und Skalierungsfaktoren
RED_MASK = 0b111
GREEN_MASK = 0b111
BLUE_MASK = 0b11
RED_SCALE = 7
GREEN_SCALE = 7
BLUE_SCALE = 3


# Hilfsfunktion zur Farbberechnung
def extract_and_scale(value, mask, scale_factor):
    return (value * 255) // scale_factor


def byte_to_rgb(rgb332):
    # Farbbits extrahieren
    red = (rgb332 >> 5) & RED_MASK  # Extrahiere die obersten 3 Bits (R)
    green = (rgb332 >> 2) & GREEN_MASK  # Extrahiere die mittleren 3 Bits (G)
    blue = rgb332 & BLUE_MASK  # Extrahiere die untersten 2 Bits (B)

    # Hochskalieren auf den Bereich 0–255
    red = extract_and_scale(red, RED_MASK, RED_SCALE)
    green = extract_and_scale(green, GREEN_MASK, GREEN_SCALE)
    blue = extract_and_scale(blue, BLUE_MASK, BLUE_SCALE)

    return green, red, blue


# Beispiel
# color_byte = 139  # Beispielwert (0x8B)
# rgb_value = byte_to_rgb(color_byte)
# print(f"Byte {color_byte} (0x{color_byte:02X}) → RGB: {rgb_value}")


def rgb_to_byte(rgb):
    r, g, b = rgb
    # Rot auf 3 Bits skalieren (0–7)
    r = r >> 5  # Rechtsverschiebung um 5 Bits (255 → 7 bei max)
    # Grün auf 3 Bits skalieren (0–7)
    g = g >> 5
    # Blau auf 2 Bits skalieren (0–3)
    b = b >> 6  # Rechtsverschiebung um 6 Bits (255 → 3 bei max)

    # Kombiniere die Werte zu einem Byte
    return (r << 5) | (g << 2) | b


# Beispiel
# rgb_value = (128, 64, 255)  # Beispiel-RGB-Tuple
# color_byte = rgb_to_byte(rgb_value)
# print(f"RGB {rgb_value} → Byte: {color_byte} (0x{color_byte:02X})")

class Neostrip:
    def __init__(self, neo_pin, timer_id, period=100):
        self.MODES = ["off", "on", "rotate_left", "rotate_right"]
        self.neo_pin = neo_pin
        self.pixels = neopixel.NeoPixel(Pin(neo_pin), NUMBER_OF_PIXELS)
        self.timer = Timer(timer_id)
        self.timer.init(period=period, mode=Timer.PERIODIC, callback=self.timer_callback)
        self.mode = self.MODES[0]

    def set_mode(self, mode: str) -> None:
        if mode in self.MODES:
            self.mode = mode

    def set_period(self, period: int) -> None:
        self.timer.init(period=period, mode=Timer.PERIODIC, callback=self.timer_callback)

    def set_pattern(self, pattern: list[int]) -> None:
        for i in range(0, NUMBER_OF_PIXELS):
            self.pixels[i] = byte_to_rgb(pattern[i % len(pattern)])

    def timer_callback(self, timer: Timer) -> None:
        if self.mode == self.MODES[0]:
            self.pixels.fill((0, 0, 0))
        elif self.mode == self.MODES[1]:
            pass
            # self.pixels.fill((255, 255, 255))
        elif self.mode == self.MODES[2]:
            self.rotate_left()
        elif self.mode == self.MODES[3]:
            self.rotate_right()
        self.pixels.write()

    def rotate_right(self) -> None:
        temp = self.pixels[-1]
        self.pixels[1:] = self.pixels[:-1]
        self.pixels[0] = temp

    def rotate_left(self) -> None:
        temp = self.pixels[0]
        self.pixels[0:-1] = self.pixels[1:]
        self.pixels[-1] = temp

    def __del__(self) -> None:
        self.timer.deinit()


strip14 = Neostrip(14, 0, period=50)
strip15 = Neostrip(15, 1, period=100)

import neopixel
from machine import Pin, PWM, Timer

NUMBER_OF_PIXELS = 144
# https://roger-random.github.io/RGB332_color_wheel_three.js/

NEO_PIXEL_PINS = [14, 15]


def byte_to_rgb(rgb332):
    # Farbbits extrahieren
    r = (rgb332 >> 5) & 0b111  # Extrahiere die obersten 3 Bits (R)
    g = (rgb332 >> 2) & 0b111  # Extrahiere die mittleren 3 Bits (G)
    b = rgb332 & 0b11  # Extrahiere die untersten 2 Bits (B)

    # Hochskalieren auf den Bereich 0–255
    r = (r * 255) // 7  # Von 0–7 auf 0–255 skalieren
    g = (g * 255) // 7  # Von 0–7 auf 0–255 skalieren
    b = (b * 255) // 3  # Von 0–3 auf 0–255 skalieren

    return (r, g, b)


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
        self.neo_pin = neo_pin
        self.pixels = neopixel.NeoPixel(Pin(neo_pin), NUMBER_OF_PIXELS)
        self.timer = Timer(timer_id)
        self.timer.init(period=period, mode=Timer.PERIODIC, callback=self.timer_callback)

    def timer_callback(self, timer):
        # self.pixels.fill((0, 0, 0))
        self.pixels.write()

    def __del__(self):
        self.timer.deinit()


strip14 = Neostrip(14, 0, period=50)
strip15 = Neostrip(15, 1, period=100)


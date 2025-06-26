import neopixel
from machine import Pin, PWM, Timer

NEO_PIXEL_PINS = [14, 15]
neo14 = neopixel.NeoPixel(Pin(14), 144)
neo15 = neopixel.NeoPixel(Pin(15), 144)


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


# Callback-Funktion, die beim Timer-Interrupt ausgeführt wird
def callback(timer):
    # print("Timer ausgelöst")
    # neo14.fill((0, 0, 0))
    neo14.write()


# Timer erstellen (Software- oder Hardware-Timer je nach Board)
timer = Timer(0)  # Timer 0 auswählen

# Timer konfigurieren 100 -> 50ms ???!!!!
timer.init(period=100, mode=Timer.PERIODIC, callback=callback)

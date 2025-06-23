from machine import Pin, ADC
import time

# ADC Setup
adc_pin = 0  # ADC an GPIO0 (oder den verfügbaren freien Pin)
adc = ADC(Pin(adc_pin))
adc.width(ADC.WIDTH_12BIT)  # 12-Bit-Auflösung (0–4095)
adc.atten(ADC.ATTN_11DB)  # Spannung bis 3,3 V

# Spannungsbereiche für Adressen (berechnet aus den Widerstandswerten)
ADDRESS_RANGES = [
    (2.90, 3.10),  # Spannung für Adresse 1 (ca. 3,00 V ± Toleranz)
    (2.65, 2.85),  # Spannung für Adresse 2 (ca. 2,75 V ± Toleranz)
    (2.30, 2.50),  # Spannung für Adresse 3 (ca. 2,36 V ± Toleranz)
    (1.75, 1.95),  # Spannung für Adresse 4 (ca. 1,83 V ± Toleranz)
]


def get_address():
    raw_value = adc.read()  # ADC-Wert auslesen (0–4095)
    voltage = (raw_value / 4095) * 3.3  # Spannung berechnen (0–3,3 V Bereich)
    print(f"Gemessene Spannung: {voltage:.2f} V")

    # Adresse bestimmen
    for i, (low, high) in enumerate(ADDRESS_RANGES):
        if low <= voltage <= high:
            return i + 1  # Adresse ist 1-basiert
    return None  # Keine gültige Adresse erkannt


# Hauptprogramm
while True:
    address = get_address()
    if address:
        print(f"Meine Adresse: {address}")
    else:
        print("Unbekannte Adresse!")
    time.sleep(1)

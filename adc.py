from machine import Pin, ADC
import time

# ADC-Pin und Konfiguration
adc_pin = 2  # GPIO2 (oder anderer ADC-Pin)
adc = ADC(Pin(adc_pin))  # ADC-Objekt erstellen
adc.width(ADC.WIDTH_12BIT)  # Auflösung einstellen (12 Bit -> Wertebereich: 0–4095)
adc.atten(ADC.ATTN_11DB)  # Eingangsspannungsbereich konfigurieren (bis ~3,3 V)


# Funktion zur Spannungsmessung
def read_voltage():
    raw_value = adc.read()  # Unkalibrierter Wert vom ADC (0–4095)
    voltage = (raw_value / 4095) * 3.3  # Konvertiere zu Spannung in Volt (0–3,3 V Bereich)
    return voltage


# Messwerte ausgeben
while True:
    voltage = read_voltage()
    print(f"Gemessene Spannung: {voltage:.2f} V")  # Ausgabe auf 2 Dezimalstellen
    time.sleep(1)  # 1 Sekunde Pause

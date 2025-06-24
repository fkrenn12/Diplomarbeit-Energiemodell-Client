from machine import Pin, PWM
from adc import get_voltage
import neopixel

NEO_PIXEL_PIN = 8
ADC_PINS = [2, 3, 4, 5]
PWM_PINS = [14, 15, 18, 19, 20, 21, 22]
DIGITAL_PINS = [14, 15, 18, 19, 20, 21, 22]

rgb = neopixel.NeoPixel(Pin(NEO_PIXEL_PIN), 1)
rgb[0] = (0, 0, 0)
rgb.write()


def set_pin(pin, value):
    pin = Pin(pin, Pin.OUT)
    pin.value(value)


def get_pin(pin):
    pin = Pin(pin, Pin.IN)
    return pin.value()


def read_adc(pin):
    return f"{get_voltage(pin):.2f}"


def set_pwm(pin, freq=500, duty_percent=0):
    duty = duty_percent * 65535 // 100
    PWM(Pin(pin), freq=freq, duty_u16=duty)


def execute(pin=None, typ=None, direction=None, value=None, freq=None, duty_percent=None):
    try:
        pin = int(pin) if pin else None
        value = int(value) if value else None
        freq = int(freq) if freq else None
        duty_percent = int(duty_percent) if duty_percent else None

        if typ == "pwm" and pin in PWM_PINS:
            set_pwm(pin, freq, duty_percent)
        elif typ == "adc" and pin in ADC_PINS:
            return read_adc(pin)
        elif typ == "digital" and pin in DIGITAL_PINS:
            if direction is None:
                print(f"set_pin({pin}, {value})")
                set_pin(pin, value)
            if direction == "?":
                return str(int(get_pin(pin)))
        return str()
    except Exception as e:
        return f"{e}"

import network
import time
import machine
from umqtt.simple import MQTTClient
import time
from ubinascii import hexlify
from machine import unique_id
from adc import get_address
from gpio import execute
from gpio import rgb

# General
MAC = hexlify(unique_id(), ":").decode("utf-8")
UID = (int(MAC.replace(":", "")[-6:], 16) % 100000)
CLIENT_ADDRESS = get_address()
# WiFi-Konfiguration
SSID = "LAWIG14-FlexBox"
PASSWORD = "wiesengrund14"

# MQTT-Konfiguration
MQTT_BROKER = "192.168.0.132"  # IP-Adresse oder Domain des MQTT-Brokers
MQTT_PORT = 8883
MQTT_TOPIC_ROOT_IN = "to-client"
MQTT_TOPIC_ROOT_OUT = "from-client"
MQTT_CLIENT_ID = f"ESP32-C6-Client_{UID}"
MQTT_USER = "admin"  # Benutzername für MQTT-Auth
MQTT_PASSWORD = "admin"  # Passwort für MQTT-Auth


def connect_mqtt():
    try:
        print(f"Verbinde mit MQTT-Broker {MQTT_BROKER}...")
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, ssl=True, port=MQTT_PORT, user=MQTT_USER,
                            password=MQTT_PASSWORD)
        client.connect()
        print("Mit MQTT-Broker verbunden!")
        return client
    except Exception as e:
        print(f"MQTT-Verbindung fehlgeschlagen: {e}")
        return None


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # WLAN-Interface im Station-Modus
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)
    if not wlan.isconnected():  # Prüfen ob bereits verbunden
        print(f"Verbinde mit WiFi {SSID}...")
        wlan.connect(SSID, PASSWORD)
        retries = 0
        while not wlan.isconnected():  # Warten, bis Verbindung hergestellt wird
            retries += 1
            print(retries)
            if retries >= 20:  # Abbruch nach 20 Versuchen (~20 Sekunden)
                print("Verbindung fehlgeschlagen.")
                return False
            rgb[0] = (0, 20, 0)
            rgb.write()
            time.sleep(0.1)
            rgb[0] = (0, 0, 0)
            rgb.write()
            time.sleep(0.9)

    print(f"Mit WiFi verbunden! IP-Adresse: {wlan.ifconfig()[0]}")
    return True


def handle_mqtt(topic, msg) -> str | None:
    try:
        topic = topic.replace(f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/", "")
        topic_count = len(topic.split("/"))
        duty_percent = None
        freq = None
        direction = None
        if topic_count == 4 and "pwm" in topic:
            pin, typ, freq, duty_percent = topic.split("/")[-4:]
        elif topic_count == 3 and "digital" in topic:
            pin, typ, direction = topic.split("/")[-3:]
        elif topic_count == 2 and ("adc" in topic or "digital" in topic):
            pin, typ = topic.split("/")[-2:]
        else:
            raise Exception('Invalid Topic')
        print(f"Pin: {pin}, Typ: {typ}, Direction: {direction}, Freq: {freq}, Duty: {duty_percent}")
        return execute(pin=pin, typ=typ, value=msg, direction=direction, freq=freq, duty_percent=duty_percent)

    except Exception as e:
        # return None
        return str(e)


def main():
    def mqtt_callback(topic, msg):
        rgb[0] = (0, 0, 20)
        rgb.write()
        try:
            print(f"Empfangene Nachricht: {topic.decode()} -> {msg.decode()}")
            topic = topic.decode()
            response = handle_mqtt(topic, msg.decode())
            if response is not None:
                topic = topic.replace(MQTT_TOPIC_ROOT_IN, MQTT_TOPIC_ROOT_OUT)
                topic = topic.replace("/?", "")
                print(f"Nachricht an den Broker: {topic} {response}")
                mqtt_client.publish(topic, response)
                print(f"Nachricht gesendet: {topic} -> {response}")
        finally:
            rgb[0] = (0, 0, 0)
            rgb.write()

    # Versuchen, eine Verbindung aufzubauen
    if not connect_wifi():
        print("Keine Verbindung möglich. Neustart...")
        machine.reset()  # Neustart bei Verbindungsproblemen

    mqtt_client = connect_mqtt()
    if not mqtt_client:
        print("Keine Verbindung mit MQTT-Broker möglich. Neustart...")
        machine.reset()

    rgb[0] = (20, 0, 0)
    rgb.write()
    mqtt_client.set_callback(mqtt_callback)
    subscribe_topic = f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/+/digital/#"
    print(f"Abonniere auf Topic: {subscribe_topic}")
    mqtt_client.subscribe(subscribe_topic.encode())
    subscribe_topic = f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/+/adc/#"
    print(f"Abonniere auf Topic: {subscribe_topic}")
    mqtt_client.subscribe(subscribe_topic.encode())
    subscribe_topic = f"{MQTT_TOPIC_ROOT_IN}/{CLIENT_ADDRESS}/+/pwm/#"
    print(f"Abonniere auf Topic: {subscribe_topic}")
    mqtt_client.subscribe(subscribe_topic.encode())
    rgb[0] = (0, 0, 0)
    rgb.write()
    counter = 0
    while True:
        try:
            counter += 1
            if counter % 600 == 0:  # every minute
                mqtt_client.ping()
                continue
            mqtt_client.check_msg()
            if counter % 10 == 0:  # every second
                time.sleep(0.09)
                rgb[0] = (5, 0, 0)
                rgb.write()
                time.sleep(0.01)
                rgb[0] = (0, 0, 0)
                rgb.write()
            else:
                time.sleep(0.1)

        except Exception as e:
            print(f"Fehler beim Senden der MQTT-Nachricht: {e}")
            machine.reset()


if __name__ == "__main__":
    main()

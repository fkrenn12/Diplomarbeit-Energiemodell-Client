import network
import time
from umqtt.simple import MQTTClient
import time

# WiFi-Konfiguration
SSID = "LAWIG14-FlexBox"  # Ersetze mit deinem WLAN-Namen
PASSWORD = "wiesengrund14"  # Ersetze mit deinem WLAN-Passwort

# MQTT-Konfiguration
MQTT_BROKER = "192.168.0.132"  # IP-Adresse oder Domain des MQTT-Brokers
MQTT_PORT = 8883
MQTT_TOPIC = "object/1/coil/1"
MQTT_CLIENT_ID = "XIAO_ESP32_1234"
MQTT_USER = "admin"  # Optional: Benutzername für MQTT-Auth
MQTT_PASSWORD = "admin"  # Optional: Passwort für MQTT-Auth

def mqtt_callback(topic, msg):
    print(f"Empfangene Nachricht: {topic.decode('utf-8')} -> {msg.decode('utf-8')}")
    
def connect_mqtt():
    try:
        print(f"Verbinde mit MQTT-Broker {MQTT_BROKER}...")
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, ssl=True, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
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
            if retries >= 20:  # Abbruch nach 20 Versuchen (~10 Sekunden)
                print("Verbindung fehlgeschlagen.")
                return False
            time.sleep(1)
    print(f"Mit WiFi verbunden! IP-Adresse: {wlan.ifconfig()[0]}")
    return True 


def main():
    # Versuchen, eine Verbindung aufzubauen
    if not connect_wifi():
        print("Keine Verbindung möglich. Neustart...")
        machine.reset()  # Neustart bei Verbindungsproblemen

    mqtt_client = connect_mqtt()
    # if not mqtt_client:
    #    return
    
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.subscribe(b"esp32/subscription")

    # Beispiel: Senden von Nachrichten an den Broker
    while True:
        try:
            message = "Hallo von XIAO ESP32"
            mqtt_client.publish(MQTT_TOPIC, message)
            print(f"Nachricht gesendet: {MQTT_TOPIC} -> {message}")
            time.sleep(5)  # Nach 5 Sekunden neue Nachricht senden
        except Exception as e:
            print(f"Fehler beim Senden der MQTT-Nachricht: {e}")
            mqtt_client.disconnect()
            break


if __name__ == "__main__":
    main()
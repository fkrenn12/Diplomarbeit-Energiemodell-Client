## Remote Peripheral Control MQTT-Client (ESP32-C6)
### Overview
A MQTT client is used to control peripherals by publishing messages to an MQTT broker.   
The messages are received by this client.   
This allows for remote control and automation of devices connected to the network. 
## Limitations
After using pin as gpio output it cannot be used as pwm pin  
(workaround: use pin always as pwm and change duty between 0 and 100)
MQTT send topics

PWM: 
to-client/<ADDRESS>/pwm/<PIN>/<FREQUENCY> : <DUTYCYCLE>
Response: None
ADC: 
to-client/<ADDRESS>/adc/<PIN> : Empty Payload
Response: Decimal voltage level on pin
SET GPIO: 
to-client/<ADDRESS>/gpio/<PIN> : <STATUS>
Response: None
READ GPIO: 
to-client/<ADDRESS>/gpio/<PIN>/? : Empty Payload
Response: Digital level 0 or 1
UART: 
to-client/<ADDRESS>/uart : <DATA>
Response: None

![alt text](Client-Waveshare-ESP32C6.png "Title")

<ADDRESS> Client address which is defined with resistors R1 to R4 on the board
<PIN> Pin number 2,3,4,5 (for adc) and 15,18,19,20,21,22 (for pwm and gpio)
<FREQUENCY> integer value between 1 and 1000000
<DUTYCYCLE> integer value between 0 and 100
<STATUS> 0 or 1
<DATA> string of characters


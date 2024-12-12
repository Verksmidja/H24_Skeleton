# Skeletor
Skýrsla fyrir VESM lokaverkefni

---

![Snapchat-1713000634](https://github.com/user-attachments/assets/f642eef2-2bdd-4620-946a-3cdc0e96daa1)


## Prop (Havoc Staff):

### tilbúin hauskúpa:
![skull_Complete](https://github.com/user-attachments/assets/64579127-3733-49df-8e7a-f805896f02e4)

### ljós hjá augum:
https://github.com/user-attachments/assets/19f32ba3-851b-4b0d-a1e5-0e3f28e418a2

### Kóði fyrir hauskúpu:
```
import machine
import neopixel
import time

LED_PIN1 = 1
LED_PIN2 = 2

NUM_LEDS = 16

np1 = neopixel.NeoPixel(machine.Pin(LED_PIN1), NUM_LEDS)
np2 = neopixel.NeoPixel(machine.Pin(LED_PIN2), NUM_LEDS)

def set_color1(r, g, b):
    for i in range(NUM_LEDS):
        np1[i] = (r, g, b)
    np1.write()
    
def set_color2(r, g, b):
    for i in range(NUM_LEDS):
        np2[i] = (r, g, b)
    np2.write()
    
while True:
    set_color1(100,0,0)
    set_color2(100,0,0)
    time.sleep(1)
```

## Skeletor (fígúra)

### myndbönd af fígúru virknu

https://github.com/user-attachments/assets/d8022402-78b4-43cd-b6e8-e1e72eb1d855



https://github.com/user-attachments/assets/20c9660d-340b-40fa-b989-ced6a5d2ed37



https://github.com/user-attachments/assets/535539dd-973e-4e56-8a5a-453d14cdaa2b



https://github.com/user-attachments/assets/0325df02-2720-4f0e-bba4-5e11e1350630



https://github.com/user-attachments/assets/024257ca-923d-4af8-86b0-559020ef86cf

### Kóða1 fyrir fígurin
```
from machine import Pin, PWM
import network
import time
from umqtt.simple import MQTTClient
import machine
import math

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('TskoliVESM', 'Fallegurhestur')  # Replace with your WiFi credentials
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to WiFi:', wlan.ifconfig())

# MQTT setup
def setup_mqtt():
    client = MQTTClient("esp32", "10.201.48.85")  # Replace with Raspberry Pi's IP address
    try:
        print("Attempting to connect to MQTT broker...")
        client.connect()
        print("Connected to MQTT Broker")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        time.sleep(5)  # Retry after 5 seconds
        setup_mqtt()  # Retry connection
    client.set_callback(sub_cb)
    client.subscribe("animatronic/UpDown")
    client.subscribe("animatronic/LeftRight")
    client.subscribe("animatronic/jaw")
    client.subscribe("animatronic/lefthand")
    client.subscribe("animatronic/righthand")
    client.subscribe("animatronic/Eyes")

    print("Subscribed to topics")
    return client

# Servo class definition
class Servo:
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.pwm = machine.PWM(machine.Pin(pin), freq=freq, duty=0)  # Correcting the Pin definition

    def write_us(self, us):
        if us == 0:
            self.pwm.duty(0)
            return
        us = min(self.max_us, max(self.min_us, us))
        duty = us * 1024 * self.freq // 1000000
        self.pwm.duty(duty)

    def write_angle(self, degrees=None, radians=None):
        if degrees is None:
            degrees = math.degrees(radians)
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)

# Initialize servos on the pins
neck1 = Servo(11)  # Pin 11 for neck1
neck2 = Servo(13)  # Pin 13 for neck2
lefthand = Servo(14)  # Pin 14 for left hand
righthand = Servo(10)  # Pin 10 for right hand
led1_green = Pin(5, Pin.OUT)  # Green for LED 1
led2_green = Pin(2, Pin.OUT)


def sub_cb(topic, msg):
    try:
        print(f"Message received: Topic={topic}, Message={msg}")
        if topic == b"animatronic/UpDown":
            angle = int(msg)
            if 0 <= angle <= 180:
                neck2.write_angle(angle)
                print(f"Moving neck2 to angle: {angle}")
            else:
                print(f"Invalid angle: {angle}. Must be between 0 and 180.")
                
        elif topic == b"animatronic/LeftRight":
            angle = int(msg)
            if 0 <= angle <= 180:
                neck1.write_angle(angle)
                print(f"Moving neck1 to angle: {angle}")
            else:
                print(f"Invalid angle: {angle}. Must be between 0 and 180.")
                
        elif topic == b"animatronic/lefthand":
            angle = int(msg)
            if 0 <= angle <= 180:
                lefthand.write_angle(angle)
                print(f"Moving left hand to angle: {angle}")
            else:
                print(f"Invalid angle: {angle}. Must be between 0 and 180.")
                
        elif topic == b"animatronic/righthand":
            angle = int(msg)
            if 0 <= angle <= 180:
                righthand.write_angle(angle)
                print(f"Moving right hand to angle: {angle}")
            else:
                print(f"Invalid angle: {angle}. Must be between 0 and 180.")
        elif topic == b"animatronic/Eyes":
            if msg == b"ON":
                led1_green.value(1)
                led2_green.value(1)
                print("Lights turned ON")
            elif msg == b"OFF":
                led1_green.value(0)
                led2_green.value(0)
                print("Lights turned OFF")
            else:
                print(f"Invalid lights command: {msg}")

        else:
            print(f"Unknown topic: {topic}")
    except ValueError:
        print(f"Invalid message: {msg}. Could not convert to integer.")

# Main loop
connect_wifi()
mqtt_client = setup_mqtt()

while True:
    mqtt_client.check_msg()  # Listen for incoming messages
    time.sleep(1)




```
### Kóða2 fyrir fígurin - MP3 - Asyncio
```

from machine import Pin, PWM, UART
import network
import time
import asyncio
from umqtt.simple import MQTTClient
import machine
import math
from lib.dfplayer import DFPlayer

Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('TskoliVESM', 'Fallegurhestur')  # Replace with your WiFi credentials
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to WiFi:', wlan.ifconfig())

MQTT setup
def setup_mqtt():
    client = MQTTClient("esp32", "10.201.48.85")  # Replace with Raspberry Pi's IP address
    try:
        print("Attempting to connect to MQTT broker...")
        client.connect()
        print("Connected to MQTT Broker")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        time.sleep(5)  # Retry after 5 seconds
        setup_mqtt()  # Retry connection
    client.set_callback(sub_cb)

    client.subscribe("animatronic/Laugh")
    print("Subscribed to topics")
    return client

Set up UART communication and DFPlayer
uart = UART(2, baudrate=9600, tx=17, rx=16)  # TX=17, RX=16
busy_pin = Pin(15, Pin.IN)  # GPIO 15, change if necessary
df = DFPlayer(2)
df.init(tx=17, rx=16)

async def play_laugh():
    print("Playing Laugh audio...")
    await df.wait_available()
    await df.volume(30)
    await df.play(1, 2)  # Adjust folder and file number as needed

def sub_cb(topic, msg):
    print(f"Message received: Topic={topic}, Message={msg}")  # Debugging output

    if topic == b"animatronic/Laugh":
        asyncio.create_task(play_laugh())  # Play laugh audio asynchronously

Main loop
connect_wifi()
mqtt_client = setup_mqtt()

async def main_loop():
    while True:
        mqtt_client.check_msg()  # Listen for incoming messages
        await asyncio.sleep(1)

asyncio.run(main_loop())Red.py…]()

```

---

### Node Red Dashboard
![Screenshot 2024-12-11 164705](https://github.com/user-attachments/assets/25230648-b10f-483f-80cf-91164458878f)
![Screenshot 2024-12-11 164641](https://github.com/user-attachments/assets/7aee1ce0-efe3-402c-b1c6-befec8a143f7)

ssh pi@10.201.48.85

password: Verksm1dja

---

### Myndir
![20241211_163923](https://github.com/user-attachments/assets/125b22c9-9f70-4644-b3f7-9cc935404fb6)
![20241211_163946](https://github.com/user-attachments/assets/5684ca9a-b3a1-40ef-a3ca-73e87cc7d6a9)
![20241211_163928](https://github.com/user-attachments/assets/0f75f317-0248-4deb-8602-898b3ef0abd0)
![20241211_163919](https://github.com/user-attachments/assets/fca6aa9c-d055-4198-aa58-e43778e33046)




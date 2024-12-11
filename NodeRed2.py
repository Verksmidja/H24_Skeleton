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

asyncio.run(main_loop())
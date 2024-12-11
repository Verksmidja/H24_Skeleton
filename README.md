# VESM2V-05CU-VERK5
Skýrsla fyrir VESM loka verkefni Skeletor

## Prop (Havoc Staff):
Hornin:
![horn2](https://github.com/user-attachments/assets/e1255b2a-f9e9-4a9c-84a6-65668f7f99c8)
![horn1](https://github.com/user-attachments/assets/90559643-ff0a-4ea8-985c-10225d9cfbfe)
## Hauskúpan og augun:
![hauskupa](https://github.com/user-attachments/assets/17bd8379-b5f3-4c81-9589-6efeb64a0566)
![auga1](https://github.com/user-attachments/assets/86918624-4f54-40e2-9fd8-8931cb737b06)

## tilbúin hauskúpa:
![skull_Complete](https://github.com/user-attachments/assets/64579127-3733-49df-8e7a-f805896f02e4)
### ljós hjá augum:
https://github.com/user-attachments/assets/19f32ba3-851b-4b0d-a1e5-0e3f28e418a2

### Kóði fyrir hauskúpu:
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



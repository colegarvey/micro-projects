from machine import Pin
import time

time.sleep(3)  # grace period so you can always interrupt after a reset

PINS = {"GreenBtn": 13, "RedBtn": 27, "BlueBtn": 14}
buttons = {name: Pin(p, Pin.IN, Pin.PULL_UP) for name, p in PINS.items()}
down = {name: False for name in PINS}

while True:
    for name, b in buttons.items():
        pressed = b.value() == 0
        if pressed and not down[name]:
            time.sleep_ms(20)              # debounce
            if b.value() == 0:
                down[name] = True
                print(name)                # this is what the PC receives
        elif not pressed and down[name]:
            time.sleep_ms(20)
            if b.value() == 1:
                down[name] = False
    time.sleep_ms(5)


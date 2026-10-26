import os
import serial
import pyautogui

PORT = "COM4"

ACTIONS = {
    "BTN1": lambda: pyautogui.press("playpause"),            # media play/pause
    "BTN2": lambda: pyautogui.hotkey("ctrl", "shift", "m"),  # any hotkey combo
    "BTN3": lambda: os.startfile("calc.exe"),                # launch a program
    "BTN4": lambda: os.startfile("https://www.youtube.com"), # open a website
}

with serial.Serial(PORT, 115200, timeout=1) as ser:
    print("Listening...")
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line in ACTIONS:
            ACTIONS[line]()
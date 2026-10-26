from machine import Pin, I2C
from time import sleep
import dht, ssd1306, network, json
import config
import urequests as requests


dht_sensor = dht.DHT11(Pin(14))
sleep(2)
# Display setup (the script keeps going if the screen fails)
# oled = None
# try:
#     i2c = I2C(0, sda=Pin(12), scl=Pin(13), freq=400000)
#     oled = ssd1306.SSD1306_I2C(128, 64, i2c)
# except OSError as e:
#     print("Display init failed:", e)
# 
# def show_lines(lines):
#     if oled is None:
#         return
#     try:
#         oled.fill(0)
#         for text, y in lines:
#             oled.text(text, 0, y)
#         oled.show()
#     except OSError as e:
#         print("Display write failed:", e)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(config.SSID, config.PSKY)
        for _ in range(20):
            if wlan.isconnected():
                break
            sleep(1)
    return wlan.isconnected()

def read_sensor():
    for _ in range(3):
        try:
            dht_sensor.measure()
            return dht_sensor.temperature(), dht_sensor.humidity()
        except OSError:
            sleep(1)
    return None

def send_reading(temp_f, humidity):
    r = requests.post(
        config.PI_SERVER_URL,
        data=json.dumps({"node": "Bedroom Rack", "temp_f": temp_f, "humidity": humidity}),
        headers={"Content-Type": "application/json",
                 "X-Api-Key": config.API_KEY})
    ok = (r.status_code == 200)
    r.close()
    return ok

while True:
    result = read_sensor()
    if result:
        temp_f = result[0] * 9 / 5 + 32
#         show_lines([("Bedroom Rack", 0),
#                     ("Temp: {:.0f} F".format(temp_f), 24),
#                     ("Hum:  {} %".format(result[1]), 40)])
        try:
            if not connect_wifi():
                raise OSError("no wifi")
            if not send_reading(temp_f, result[1]):
                print("Server rejected reading")
        except OSError as e:
            print("Upload failed:", e)
#     else:
#         show_lines([("Sensor error", 24)])
    sleep(600)

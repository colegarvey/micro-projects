from machine import Pin, ADC
from time import sleep, sleep_ms
import dht, ssd1306, network, json
import config
import urequests as requests


dht11 = dht.DHT11(Pin(14))
ldr = ADC(Pin(26))
sleep(2)

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

def read_dht():
    for _ in range(3):
        try:
            dht11.measure()
            return dht11.temperature(), dht11.humidity()
        except OSError:
            sleep(1)
    return None

def read_light():
    total = 0
    for _ in range(10):
        total += ldr.read_u16()
        sleep_ms(5)
    return round(total / 10 / 65535 * 100)   # 0 to 100 percent

def send_reading(temp_f, humidity, light_lvl):
    r = requests.post(
        config.PI_SERVER_URL,
        data=json.dumps({"node": "Bedroom Rack", "temp_f": temp_f, "humidity": humidity, "light_lvl": light_lvl}),
        headers={"Content-Type": "application/json",
                 "X-Api-Key": config.API_KEY})
    ok = (r.status_code == 200)
    r.close()
    return ok



while True:

     result_dht11 = read_dht()
     result_light = read_light()
     if result_dht11 is not None and result_light is not None:
         temp_f = result_dht11[0] * 9 / 5 + 32
         print(temp_f, result_dht11[1],result_light)
         try:
             if not connect_wifi():
                 raise OSError("no wifi")
             if not send_reading(temp_f, result_dht11[1],result_light):
                 print("Server rejected reading")
         except OSError as e:
             print("Upload failed:", e)
 
     sleep(600)

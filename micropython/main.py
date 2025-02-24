import time, ujson, urequests
from machine import Pin
from dht import DHT11

DEVICE_LABEL = "temperature-device"
UBIDOTS_BROKER = "industrial.api.ubidots.com"
UBIDOTS_PORT = 1883
UBIDOTS_USER = "BBUS-mudojHhzScIws0HZMme865CI0cziE0"
UBIDOTS_TOPIC = "/v2.0/devices/"+DEVICE_LABEL

print("Menyambungkan ke MQTT server... ", end="")
client = MQTTClient(DEVICE_LABEL, UBIDOTS_BROKER, UBIDOTS_PORT, user=UBIDOTS_USER, password="")
client.connect()
print("Tersambung!")

temp_sensor = DHT11(Pin(4))
led = Pin(2, Pin.OUT)
button = Pin(25, Pin.IN, Pin.PULL_UP)

pressed = False
state = 0

while True:
    print("Status: "+("Nyala" if state == 1 else "Mati"))
    if button.value() == 0 and not pressed:
        state = 0 if state == 1 else 1
        print("ON" if state == 1 else "OFF")
        led.value(state)
        pressed = True
    elif button.value() == 1 and pressed:
        pressed = False

    try:
        data = {
            "state": {
                "value": state,
                "context": {
                    "status": "Nyala" if state == 1 else "Mati"
                }
            },
            "temperature": {
                "value": 0,
                "context": {
                    "status": "-"
                }
            },
            "humidity": {
                "value": 0,
                "context": {
                    "status": "-"
                }
            }
        }
        
        if state == 1:
            temp_sensor.measure()
            temp = temp_sensor.temperature()
            hum = temp_sensor.humidity()
            temp_status = "-"
            hum_status = "-"

            if temp <= 0:
                temp_status = "Sangat Dingin"
            elif 1 <= temp <= 15:
                temp_status = "Dingin"
            elif 16 <= temp <= 25:
                temp_status = "Normal"
            elif 26 <= temp <= 35:
                temp_status = "Panas"
            else:
                temp_status = "Sangat Panas"

            if hum <= 30:
                hum_status = "Kering"
            elif 31 <= hum <= 60:
                hum_status = "Normal"
            else:
                hum_status = "Lembab"
            data.update({
                "temperature": {
                    "value": temp,
                    "context": {
                        "status": temp_status
                    }
                },
                "humidity": {
                    "value": hum,
                    "context": {
                        "status": hum_status
                    }
                }
            })
            print(f"Suhu: {temp}°C - Status: {temp_status}, Kelembapan: {hum}% - Status: {hum_status}")
            
        client.publish(UBIDOTS_TOPIC, ujson.dumps(data))
        response = urequests.post("http://192.168.1.6:5000/temperature", json=data)
        print(response.json().get('message'))
    except OSError:
        print("Error measuring...")
    except ValueError:
        print("Fail to sending request...")
    
    time.sleep(3)
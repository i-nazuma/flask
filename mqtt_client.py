import paho.mqtt.client as mqtt
import json

sensor_data = {'temperature': None, 'humidity': None}


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/sensors/#")


def on_message(client, userdata, msg):
    global sensor_data
    try:
        payload = json.loads(msg.payload)
        if 'temperature' in payload and 'humidity' in payload:
            sensor_data['temperature'] = payload['temperature']
            sensor_data['humidity'] = payload['humidity']
    except json.JSONDecodeError:
        print("Failed to decode JSON payload")


def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(ca_certs="client_certs/ca.crt",
                   certfile="client_certs/client.crt",
                   keyfile="client_certs/client.key")
    client.connect("iotgw.local", 8883, 60)
    client.loop_start()


if __name__ == "__main__":
    start_mqtt_client()

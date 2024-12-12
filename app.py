from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = '192.168.8.106'
app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
# app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
topic = '/sensors/#'

mqtt_client = Mqtt(app)

messages = []

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    messages.append(data)  
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
    
@app.route('/')
def index():
    return '''
        <h1>Welcome to the Flask MQTT application!</h1>
        <p><a href="/publish">Go to Publish</a></p>
    '''

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    messages.append(data)  
    print(f"Received message: {data}")

@app.route('/publish', methods=['GET'])
def view_messages():
    messages_html = ''.join(
        f'<tr><td>{msg["topic"]}</td><td>{msg["payload"]}</td></tr>' for msg in messages
    )
    html = f'''
        <h1>Subscribed Data</h1>
        <table border="1">
            <tr>
                <th>Topic</th>
                <th>Payload</th>
            </tr>
            {messages_html if messages else '<tr><td colspan="2">No messages yet</td></tr>'}
        </table>
        <p><a href="/">Back to Home</a></p>
    '''
    return html

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)
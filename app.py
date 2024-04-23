#MQTT subscriber with RabbitMQ & MongoDB (MongoEngine) Integration
import paho.mqtt.client as mqtt
import pika
import json
import logging
from mongoengine import connect
from constants import RABBITMQ_HOST, RABBITMQ_QUEUE, MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MQTT_HOST, MQTT_PORT, MQTT_TOPIC
from models import SensorData
from datetime import datetime

#logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#MongoDB configuration
try:
    connect(db=MONGODB_DB, host=MONGODB_HOST, port=MONGODB_PORT)
    logging.info('Successfully Connected to MongoDB!')
except Exception as e:
    logging.error(f'Error connecting to MongoDB: {e}')
    exit()
#RabbitMQ configuration
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    logging.info('Successfully Connected to RabbitMQ!')
except Exception as e:
    logging.error(f'Error connecting to RabbitMQ: {e}')
    exit()

#MQTT configuration
def on_connect(self,client, userdata, flags, rc):
    logging.info(f'Connected with result code {rc}')

def on_message(client, userdata, msg):
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=msg.payload)
    logging.info(f'Message sent to RabbitMQ: {msg.payload}')
    data = json.loads(msg.payload)
    sensor_data = SensorData(data=data['data'])
    sensor_data.save()
    logging.info(f'Message saved to MongoDB: {sensor_data.to_json()}')

def publish_to_mqtt(msg):
    try:
        client.publish(MQTT_TOPIC, msg, qos=0)
    except Exception as e:
        logging.error(f'Error publishing to MQTT: {e}')

    
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    logging.error(f'Error connecting to MQTT: {e}')
    exit()

#main logic to subscribe to MQTT topic & publish to RabbitMQ
try:
    logging.info(f'Subscribing to topic: {MQTT_TOPIC}')
    client.subscribe(MQTT_TOPIC)
    #publish to RabbitMQ
    while True:
        print()
        data = input('Enter data or press enter to exit: ')
        print()
        if data :
            msg = json.dumps({'data': data})
            publish_to_mqtt(msg)
        else:
            logging.error('Data cannot be empty')
            client.disconnect()
            connection.close()
            exit()
except Exception as e:
    logging.error(f'Error:{e}')
    logging.info('Exiting...')
    client.disconnect()
    connection.close()
    exit()
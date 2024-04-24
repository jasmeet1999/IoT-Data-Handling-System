#MQTT subscriber with RabbitMQ & MongoDB

#Importing required libraries
import paho.mqtt.client as mqtt
import pika
import json
import logging
from mongodb_config import connect_to_mongodb
from constants import RABBITMQ_HOST, RABBITMQ_QUEUE, MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MQTT_HOST, MQTT_PORT, MQTT_TOPIC
from models import SensorData
from datetime import datetime
from logging_config import debug_mode
import sys


#Enable debug mode
debug_mode(sys.argv)

#MongoDB connection

connect_to_mongodb()

#RabbitMQ configuration
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    logging.info('Successfully Connected to RabbitMQ!')
except Exception as e:
    logging.error(f'Error connecting to RabbitMQ: {e}\n')
    exit()

#MQTT configuration
def on_connect(self,client, userdata, flags, rc):
    logging.info(f'Connected with result code {rc}')

def on_message(client, userdata, msg):
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=msg.payload)
    logging.info(f'Message sent to RabbitMQ: {msg.payload}\n')
    data = json.loads(msg.payload)
    sensor_data = SensorData(temperature=data['data'])
    sensor_data.save()
    logging.info(f'Message saved to MongoDB')
    print(sensor_data.to_json())

def publish_to_mqtt(msg):
    try:
        client.publish(MQTT_TOPIC, msg, qos=0)
    except Exception as e:
        logging.error(f'Error publishing to MQTT: {e}\n')

def get_data_from_mongodb(id):
    try:
        data = SensorData.objects.get(id=id).to_json()
        print(data)
        return data
    except Exception as e:
        logging.error(f'Error getting data from MongoDB: {e}\n')
        return None

    
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    logging.error(f'Error connecting to MQTT: {e}\n')
    exit()

#main logic to subscribe to MQTT topic & publish to RabbitMQ
try:
    logging.info(f'Subscribing to topic: {MQTT_TOPIC}\n')
    client.subscribe(MQTT_TOPIC)
    #publish to RabbitMQ
    print('Select an option:\n1. Publish data to MQTT\n2. Retrive data from MongoDB with id\n3. Publish Hello RabbitMQ\n')
    option = input('Select an option or type exit to stop: ')
    while option.lower() != 'exit':
        match option:
            case '1':
                data = input('\nEnter temperature to publish to MQTT:')
                if data:
                    #checking if data is a number through unicode
                    if int(ord((data[0]))>= 48 and int(ord(data[0])) <= 57):
                        msg = json.dumps({'data': float(data)})
                        publish_to_mqtt(msg)
                    else:
                        print('Invalid data!\n')
                        logging.error('Invalid data!\n')
                    break
                else:
                    print('Data cannot be empty!\n')
                    logging.error('Data cannot be empty!\n')
                    break
            case '2':
                data = input('\nEnter id to retrieve data from MongoDB:')
                if data:
                    #checking if data is valid objectid
                    if len(data) == 24:
                        get_data_from_mongodb(data)
                        break
                else:
                    print('Id cannot be empty!\n')
                    logging.error('Id cannot be empty!\n')
            case 'exit':
                    logging.info('Exiting...\n')
                    client.disconnect()
                    connection.close()
                    exit()
            case _:
                print('Invalid option!\n')
                logging.error('Invalid option!\n')
                break
except Exception as e:
    logging.error(f'Error:{e}\n')
    logging.info('Exiting...\n')
    client.disconnect()
    connection.close()
    exit()
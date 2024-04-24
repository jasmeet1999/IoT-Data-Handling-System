from mongoengine import connect
import logging
from constants import MONGODB_DB, MONGODB_HOST, MONGODB_PORT

def connect_to_mongodb():
    try:
        connect(db=MONGODB_DB, host=MONGODB_HOST, port=MONGODB_PORT)
        logging.info('Successfully Connected to MongoDB!\n')
    except Exception as e:
        logging.error(f'Error connecting to MongoDB: {e}\n')
        exit()
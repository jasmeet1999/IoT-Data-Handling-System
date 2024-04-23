from mongoengine import Document, StringField, DateTimeField
from datetime import datetime
class SensorData(Document):
    data = StringField(required=True)
    timestamp = DateTimeField(default=datetime.now())

    meta = {
        'collection': 'sensor_data'
    }

    def to_json(self):
        return {
            'data': self.data,
            'timestamp': self.timestamp
        }
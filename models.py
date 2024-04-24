import mongoengine as me
from datetime import datetime
class SensorData(me.Document):
    temperature = me.FloatField(required=True)
    day = me.StringField(default=datetime.today().strftime('%A'))
    timestamp = me.DateTimeField(default=datetime.now())

    meta = {
        'collection': 'sensor_data'
    }

    def to_json(self):
        return {
            '_id': str(self.id),
            'temperature': str(self.temperature) + '°C',
            'day': self.day,
            'timestamp': self.timestamp
        }
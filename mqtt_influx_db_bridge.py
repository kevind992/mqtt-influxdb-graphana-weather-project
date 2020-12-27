import re

import weather_stations_pb2
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient


INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'weather_stations'

MQTT_ADDRESS = '0.0.0.0'
MQTT_USER = 'kdelassus'
MQTT_PASSWORD = 'kdelassus'
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'Influx-Client'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    response = weather_stations_pb2.SensorData()
    if match:
        response.ParseFromString(payload)
        response.location = match.group(1)
        if response.measurement == 'status':
            return None
        return response
    else:
        return None

def _send_sensor_data_to_influxdb(response):
    json_body = [
        {
            'measurement': response.measurement,
            'tags': {
                'location': response.location
            },
            'fields': {
                'value': response.value
            }
        }
    ]
    print(json_body)
    influxdb_client.write_points(json_body)

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    response = _parse_mqtt_message(msg.topic, msg.payload)
    if response is not None:
        _send_sensor_data_to_influxdb(response)

def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)
    print('DB setup')

def main():
    print('In main')
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()

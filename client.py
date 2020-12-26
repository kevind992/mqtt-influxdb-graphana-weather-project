import re
from typing import NamedTuple
import paho.mqtt.client as mqtt

class SensorData(NamedTuple):
    measurement: str
    value: float

MQTT_ADDRESS = '0.0.0.0'
MQTT_USER = 'kdelassus'
MQTT_PASSWORD = 'kdelassus'
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'Data-Client'
HUMIDITY_TOPIC = "home/livingroom/humidity"
TEMP_TOPIC = "home/livingroom/temperature"

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def read_file():

    list = []

    with open("sample_data.txt", "r") as filestream:
        for line in filestream:
            currentline = line.split(",")
            list.append(SensorData(str(currentline[0]), float(currentline[1])))
    
    return list


def main():
    data = read_file()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish

    mqtt_client.connect(MQTT_ADDRESS, 1883)

    for d in data:
        if d.measurement == 'temp':
            print('[INFO ] SENDING: ' + TEMP_TOPIC + ' '+ str(d.value))
            mqtt_client.publish(TEMP_TOPIC, str(d.value))
        else:
            print('[INFO ] SENDING: ' + HUMIDITY_TOPIC + ' '+ str(d.value))
            mqtt_client.publish(HUMIDITY_TOPIC, str(d.value))

    mqtt_client.loop_forever()
    print('[INFO ] Data Sent - Closing Client')


if __name__ == '__main__':
    print('[INFO ] Starting Client')
    main()
            
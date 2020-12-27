import weather_stations_pb2
import paho.mqtt.client as mqtt

MQTT_ADDRESS = '0.0.0.0'
MQTT_USER = 'weather'
MQTT_PASSWORD = 'weather'
MQTT_TOPIC = 'home/+/+'
MQTT_CLIENT_ID = 'Data-Client'
HUMIDITY_TOPIC = "home/livingroom/humidity"
TEMP_TOPIC = "home/livingroom/temperature"

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('[INFO ] Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_publish(client,userdata,result):
    print("[INFO ] data published")
    pass

def read_file():
    list = []
    with open("sample_data.txt", "r") as filestream:
        for line in filestream:
            currentline = line.split(",")
            value = weather_stations_pb2.SensorData()
            value.measurement = str(currentline[0])
            value.value = float(currentline[1])
            list.append(value)
    return list

def main():
    # Read Sample data
    data = read_file()

    # Conenct to broker
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.connect(MQTT_ADDRESS, 1883)

    # Send sample data to MQTT Broker. 
    for d in data:
        if d.measurement == 'temp':
            print('[INFO ] SENDING: ' + TEMP_TOPIC + ' '+ str(d.value))
            mqtt_client.publish(TEMP_TOPIC, d.SerializeToString())
        else:
            print('[INFO ] SENDING: ' + HUMIDITY_TOPIC + ' '+ str(d.value))
            mqtt_client.publish(HUMIDITY_TOPIC, d.SerializeToString())

    mqtt_client.loop_forever()
    print('[INFO ] Data Sent - Closing Client')


if __name__ == '__main__':
    print('[INFO ] Starting Client')
    main()
            
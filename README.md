# Introduction
The following weather station projects primary objective was to introduce new upcomming technologies.
These technologies are
 - MQTT
 - InfluxDB
 - Protobuf
 - Graphana

## Prerequisites
The following is need to run this project

### Python3
This project requires python 3
Follow this [step by step guide](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu) to install

### MQTT
First the mosquitto broker needs to be installed and setup
```
$ sudo apt-get install mosquitto
```

```
$ sudo apt-get install mosquitto-clients
```

Now start the service
```
$ sudo service mosquitto start
```

Next the defualt configuration needs to be modified
```
$ sudo vi /etc/mosquitto/mosquitto.conf
```

Overwrite with the following
```
# Place your local configuration in /etc/mosquitto/conf.d/
#
# A full description of the configuration file is at
# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

# include_dir /etc/mosquitto/conf.d

allow_anonymous = false
password_file /etc/mosquitto/pwfile
listener 1883
```

save and exit

To setup username and password for the broker enter the following
```
$ sudo mosquitto_passwd -c /etc/mosquitto/pwfile weather
```

You should be asked to enter a password. Enter "weather"

Restart the mosquitto service
```
$ sudo service mosquitto restart
```

Finally you will need to install the mqtt python dependencies 
```
$ sudo pip3 install paho-mqtt
```

Mqtt should now be ready to go

### InfluxDB
To install influxDB enter the following commands
```
$ sudo apt install influxdb
```
```
$ sudo apt install influxdb-client
```

Next you will need to change some options within the influxdb.conf file
Open the configuration file
```
sudo vi /etc/influxdb/influxdb.conf
```

Once opened uncomment "enabled = true" and save and exit.

Restart the influxdb service 
```
$ sudo service influxdb restart
```

Next open influxdb by typing "influx" in your terminal. Once opened enter the following to create your database
```
CREATE DATABASE weather_stations
```
```
CREATE USER mqtt WITH PASSWORD ‘mqtt’
GRANT ALL ON weather_stations TO mqtt
```

Finally you will need to install the python influx dependencies
```
$ sudo pip3 install influxdb
```

Influx is now ready to go.
### Protobuf
To install protoc compiler and protobuf follow these [instructions](https://developers.google.com/protocol-buffers/docs/pythontutorial) . Once protoc and protobuf have been installed you can compile the weather_stations proto file by either running the compile_proto script or running this command from the root proto directory
```
$ protoc -I=./ --python_out=./ ./weather_stations.proto
```
you should see a new python file after running the above command.
 
### Graphana
To install and setup graphana run the following commands
```
$ wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```
Next, add the Grafana repository to your APT sources:
```
$ sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
```
Refresh your APT cache to update your package lists:
```
$ sudo apt update
```
Install grafana
```
$ sudo apt install grafana
```
Start grafana service
```
$ sudo service grafana-server start
```
Once the service has been started open a browser and go to the following url
```
http://localhost:3000
```
Default username and password should be **admin**.

Next you will need to setup the data source. Select InfuxDB as our default data source and enter the rest of the options. Once entered click the "connect and test" button and the bottom the the page. You should get a success message if connection was successful. 

## Instructions
To run this project ensure that the MQTT broker, influxdb and graphana services are up and running. If the services are not running run the following
```
$ sudo service grafana-server start
$ sudo service influxdb start
$ sudo service mosquitto start
```

Nexe in one terminal window run the following command
```
$ python3 mqtt_influx_db_bridge.py
```

In a second terminal window run the following command to send the sample data to the broker
```
$ python3 sample_data_client.py
```
After running the above sample_data_client data script you should see outputs from both terminal windows. Open your brower where you had set up graphana and click the explore tab. You should now see the sample data on one of the graphs. 



## Useful Links
 - [visualize-mqtt-data-with-influxdb-and-grafana](https://diyi0t.com/visualize-mqtt-data-with-influxdb-and-grafana/)
 - [microcontroller-to-raspberry-pi-wifi-mqtt-communication](https://diyi0t.com/microcontroller-to-raspberry-pi-wifi-mqtt-communication/)
 - [Gettting-started-with-graphana](https://docs.influxdata.com/influxdb/v1.8/introduction/get-started/)
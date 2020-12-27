#!/usr/bin/env bash

PROTO_FILE="weather_stations.proto"

protoc -I=../ --python_out=../ ../$PROTO_FILE

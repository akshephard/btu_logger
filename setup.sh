#!/bin/bash

sudo apt-get install influxdb
sudo apt-get install influxdb-client
pip3 install influxdb
pip3 install pymodbus
sudo apt-get install python3-pandas
sudo apt-get install python3-pip
pip3 install configparser
pip3 install PyYaml
pip3 install influxdb
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update
sudo apt-get install telegraf
sudo apt-get install chronograf
sudo systemctl start chronograf telegraf
influx -execute "create database local_btu"
influx -execute "create database remote_btu"

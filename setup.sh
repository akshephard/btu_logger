#!/bin/bash

sudo apt-get install influxdb
sudo apt-get install influxdb-client
pip3 install influxdb
pip3 install pandas
sudo apt-get install python3-pandas
sudo apt-get install python3-pip
pip3 install configparser
pip3 install PyYaml
pip3 install influxdb
influx -execute "create database local_btu"

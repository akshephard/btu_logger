#!/bin/bash

sudo apt-get install influxdb  >> /home/pi/install.log 2>&1
sudo apt-get install influxdb-client >> /home/pi/install.log 2>&1
pip3 install influxdb   >> /home/pi/install.log 2>&1
pip3 install pymodbus >> /home/pi/install.log 2>&1
sudo apt-get install python3-pandas >> /home/pi/install.log 2>&1
sudo apt-get install python3-pip >> /home/pi/install.log 2>&1
pip3 install configparser >> /home/pi/install.log 2>&1
pip3 install PyYaml >> /home/pi/install.log 2>&1
pip3 install influxdb >> /home/pi/install.log 2>&1
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list >> /home/pi/install.log 2>&1
sudo apt-get update >> /home/pi/install.log 2>&1
sudo apt-get install telegraf >> /home/pi/install.log 2>&1
sudo apt-get install chronograf >> /home/pi/install.log 2>&1
sudo systemctl start chronograf telegraf >> /home/pi/install.log 2>&1
influx -execute "create database local_btu" >> /home/pi/install.log 2>&1
influx -execute "create database remote_btu" >> /home/pi/install.log 2>&1

# btu_logger
This project contains a modbus driver and a class to push data pulled from the modbus device
to a local and remote instance of instance of influxDB. 

#setup.sh
This is a shell script that will install all of the necessary things to make the project run 
on a fresh Raspberry Pi. After cloning the repo, run the command: 
chmod +x setup.sh && ./setup.sh

After running the shell script, 

#Influx_Dataframe_Client.py
This is a wrapper around the influx python client which supports writing dataframes with specified tags.

#local_db.py

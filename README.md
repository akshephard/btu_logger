# btu_logger
This project contains a modbus driver and a class to push data pulled from the modbus device
to a local and remote instance of instance of influxDB. 

## setup.sh
This is a shell script that will install all of the necessary things to make the project run 
on a fresh Raspberry Pi. After cloning the repo, run the command: 
```chmod +x setup.sh && ./setup.sh```

## config_template.yaml 
Modify this file to correspond to the settings of your modbus device and the local and remote 
instance of influxDB.

## run_script.py
This python script runs a loop that pulls information from the modbus device and puts it into 
the local database and remote database. Use this file to quickly test if everything is working.
To run this script:
```
python3 run_script.py config_template.yaml
```

## cron_script.py
Use this script to add a cron job that will run on a given interval. To do this use the command:
crontab -e

This will allow you to edit the cron jobs. Add the following lines to your crontab:
```
*/1 * * * * python3 /home/pi/btu_logger/cron_script.py  /home/pi/btu_logger/config_template.yaml >> /home/pi/log_cron_script.txt 2>&1
*/1 * * * * date >> /home/pi/cron_test.log
```
The output of cron_script.py will be placed in:
```~/log_cron_script.txt```

The second line isn't necessary to run the script but is useful to make sure cron is working by
placing a timestamp in:
```~/cron_test.log```

You can change the 1 to the interval that you are interested in. Example to run every 15 minutes:
```
*/15 * * * * python3 /home/pi/btu_logger/cron_script.py  >> /home/pi/log_cron_script.txt 2>&1
```
This will run the script at 12:00, 12:15, 12:30, 12:45, 1:00...etc 

## Influx_Dataframe_Client.py
This is a wrapper around the influx python client which supports writing dataframes with specified tags.

## local_db.py
Instantiates a connection the local and remote instance of influxDB




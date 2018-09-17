from local_db import Influx_Database_class
from modbus_driver import Modbus_Driver
import time
import argparse
#TODO Add error handling for the case where there is a network outage


def main():
    # read arguments passed at .py file call
    # only argument is the yaml config file which specifies all the details
    # for connecting to the modbus device as well the local and remote
    # influx databases
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file")

    args = parser.parse_args()
    config_file = args.config

    #config_file = 'config_template.yaml'

    #setup connection to modbus device
    obj = Modbus_Driver(config_file)
    obj.initialize_modbus()

    #setup connection to the local and remote database
    local_db = Influx_Database_class(config_in=config_file, config_type="local")
    remote_db = Influx_Database_class(config_in=config_file, config_type="remote")

    # request all of the data from the holding registers specified in config file
    data = obj.get_data()
    print(data)

    # push data to local database
    local_db.push_json_to_db(data=data)


    time_now = time.time()
    local_data = local_db.read_from_db(time_now=time_now)
    print("length of data in local db:", len(local_data))

    remote_db.push_df_to_db(df=local_data)
    local_db.successful_push()
    remote_data = remote_db.read_from_db(time_now=time_now)
    print("length after remote push = ",len(remote_data))

    #local_db.delete_from_db(time_now=time_now)
    #local_data2 = local_db.read_from_db(time_now=time_now)
    #print("length after deleting from local = ", len(local_data2))



    return

if __name__ == "__main__":
    main()

from local_db import Influx_Database_class
from modbus_driver import Modbus_Driver
import time

obj = Modbus_Driver('config_template.yaml')
obj.initialize_modbus()

local_db = Influx_Database_class(config_in='config_template.yaml',config_type="local")
remote_db = Influx_Database_class(config_in='config_template.yaml',config_type="remote")

i=0
while True:
    data = obj.get_data()
    print(data)
    local_db.push_json_to_db(data=data)
    time.sleep(1)

    if i%10 == 0 and i!=0:
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
    i+=1

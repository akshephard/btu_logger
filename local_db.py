import logging
from logging.handlers import TimedRotatingFileHandler
import os
import json
import datetime
from influxdb import InfluxDBClient
from Influx_Dataframe_Client import Influx_Dataframe_Client
import time
import yaml

# @author : Marco Pritoni <mpritoni@lbl.gov>
# @author : Anand Prakash <akprakash@lbl.gov>


class Influx_Database_class(object):
    """
    This class saves the data from pandas dataframe to a local db (currently sqlite3 on disk) as buffer while pushing data
    to another DB/API.
    """

    def __init__(self, config_in,config_type="local"):


        try:
            if config_type == "local":
                db_config_name = "local_database_config"
                #db_config = Config["local_database_config"]
            else:
                db_config_name = "remote_database_config"
                #db_config = Config["remote_database_config"]

            self.influx_obj=Influx_Dataframe_Client(config_file=config_in, db_section=db_config_name)
            #self.influx_obj=Influx_Dataframe_Client(config_file="config_template.yaml", db_section=db_config_name)
            self.client=self.influx_obj.expose_influx_client()

        except Exception as e:
            # self.logger.error("unexpected error while setting configuration from config_file=%s, error=%s"%(self.config_file, str(e)))
            raise e

        db_section = db_config_name
        with open('config_template.yaml') as f:
            # use safe_load instead load
            dbConfig = yaml.safe_load(f)




        self.measurement_name = dbConfig[db_section]['measurement_name']
        self.tag_dict = dbConfig[db_section]['tag_dict']
        self.tag_names = dbConfig[db_section]['tag_list']
        self.tag_values = dbConfig[db_section]['tag_values']
        self.database_name = dbConfig[db_section]['database']
        self.field_names = dbConfig[db_section]['fields']



    def push_json_to_db(self, data):
        for key in self.tag_dict:
            print(self.tag_dict[key])
            output[key] = self.read_discrete(self.discrete_register_dict[key][0])

        '''
        tags = {}
        for i in range(len(self.tag_names)):
            tags[self.tag_names[i]] = self.tag_values[i]
        '''

        tags = self.tag_dict
        fields = data
        pushData = [
                    {
                        "measurement": self.measurement_name,
                        "tags": tags,
                        "fields": fields
                    }
                ]
        print(pushData)
        self.influx_obj.write_json(json=pushData, database=self.database_name)

    def successful_push(self):
        '''
        Args:
            None
        Returns:
            Nothing
        This function adds a timestamp of a successful push to the measurement
        "Push_to_remote". This can be used to select data from to delete.
        '''
        tags = {}
        #tags.append("127.0.0.1")
        #tags.update({'ip':"127.0.0.1"})

        pushData = [
                    {
                        "measurement": "Push_to_remote",
                        "tags": {},
                        "fields": {"success": 1}
                    }
                ]
        print(self.database_name)
        print(pushData)
        self.influx_obj.write_json(json=pushData, database=self.database_name)

    def push_df_to_db(self, df):
        '''
        Args:
            df: Pandas dataframe in format specified

        Returns:
            Nothing
        '''
        self.influx_obj.write_dataframe(data=df,
            tags=self.tag_names,
            fields=self.field_names,
            measurement=self.measurement_name,
            database=self.database_name)

    # Enter time in seconds
    def read_from_db(self, time_now=None):
        '''
        Args:
            time_now (optional):the time to read data until from database. Default is
            current time

        Returns:
            Pandas dataframe in format specified.
        '''
        if time_now == None:
            time_now=time.time()*1000000000

        # print("end_time = ", time_now)
        df = self.influx_obj.specific_query(database=self.database_name,
                measurement=self.measurement_name,
                end_time=int(time_now*1000000000)
            )
        return df

    # Enter time in seconds
    def delete_from_db(self, time_now=None):
        '''
        Args:
            time_now (optional): The time to delete data until from database.
            Default is current time

        Returns:
            Nothing
        '''
        if time_now == None:
            time_now=time.time()*1000000000

        self.influx_obj.delete_based_on_time(database=self.database_name,
                measurement=self.measurement_name,
                end_time=int(time_now*1000000000)
            )

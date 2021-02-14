"""
Convert Realtime source data folder parquet files into realtime records in app data folder real time data

Only preserve the following fields: 
code <str>
hour <int>
minute <int>
second <int>
turnover <int>
volume <float>

Maintain the code_to_partition_map.json
"""
import json 
import os 
import sys 
from shutil import copyfile

from data_source.postprocessing.schema import create_app_realtime_data_record_dict
from data_source.postprocessing.utils import save_record_dict_to_parquet, load_parquet_to_dataframe

class RealtimeSourceDataToAppSourceData(object):
    def __init__(self, source_data_folder, app_data_folder, data_date):
        self._source_data_folder = source_data_folder
        self._app_data_folder = app_data_folder
        self._data_date = data_date
    
        self.verify_folder_structure()
    
    def verify_folder_structure(self):
        assert os.path.exists(self.source_data_folder)
        assert os.path.exists(self.app_data_folder)
        # setup folders in the app_data_folder
        astock_folder = os.path.join(self.app_data_folder, "astock")
        if not os.path.exists(self.astock_folder):
            os.mkdir(astock_folder)
        
        record_folder = os.path.join(astock_folder, "record_data")
        if not os.path.exists(astock_folder):
            os.mkdir(record_folder)
        
        realtime_folder = os.path.join(record_folder, "realtime_data")
        if not os.path.exists(realtime_folder):
            os.mkdir(realtime_folder)
        
        data_date_folder = os.path.join(realtime_folder, self.data_date)
        if not os.path.exists(data_date_folder):
            os.mkdir(data_date_folder)
        
    def run(self):
        cur_partition = 0
        source_partition_path = self.get_source_partition_path(cur_partition)
        while (os.path.exists(source_partition_path)):
            records_dict = create_app_realtime_data_record_dict()
            app_data_partition_path = self.get_app_data_partition_path(cur_partition)

            dataframe = load_parquet_to_dataframe(app_data_partition_path)
            for row in dataframe.rows:
                records_dict["code"].append(row["code"])
                records_dict["hour"].append(row["hour"])
                records_dict["minute"].append(row["minute"])
                records_dict["second"].append(row["second"])
                records_dict["turnover"].append(row["turnover"])
                records_dict["volume"].append(row["volume"])
            
            save_record_dict_to_parquet(records_dict, app_data_partition_path)

            cur_partition += 1
        # copy the code_to_partition_map.json to the destination path
        copyfile(
            self.get_source_code_to_partition_map_json_path(),
            self.get_app_code_to_partition_map_json_path()
        )
    
    def get_source_code_to_partition_map_json_path(self):
        return os.path.join(self.source_data_folder, self.data_date, "code_to_partition_map.json")
    
    def get_app_code_to_partition_map_json_path(self):
        return os.path.join(
            self.app_data_folder,
            "astock",
            "record_data",
            "realtime_data",
            self.data_date,
            "code_to_partition_map.json"
        )

    def get_source_partition_path(self, partition):
        return os.path.join(self.source_data_folder, self.data_date, "{}.parquet".format(partition))
    
    def get_app_data_partition_path(self, partition):
        return os.path.join(
            self.app_data_folder,
            "astock",
            "record_data",
            "realtime_data",
            self.data_date,
            "{}.parquet".format(partition)
        )
    
    @property
    def source_data_folder(self):
        return self._source_data_folder

    @property
    def app_data_folder(self):
        return self._app_data_folder
    
    @property 
    def data_date(self):
        return self._app_data_folder
    

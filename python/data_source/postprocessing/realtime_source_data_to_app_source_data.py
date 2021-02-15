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

from data_source.postprocessing.postprocessor import Postprocessor
from data_source.postprocessing.schema import create_app_realtime_data_record_dict
from data_source.postprocessing.utils import save_record_dict_to_parquet, load_parquet_to_dataframe

class RealtimeSourceDataToAppSourceData(Postprocessor):
    def __init__(self, source_data_folder, app_data_folder, data_date):
        super().__init__(source_data_folder, app_data_folder)
        self._data_date = data_date
        self.verify_date_folder_structure()
    
    def verify_date_folder_structure(self):
        
        data_date_folder = os.path.join(self.app_astock_record_data_realtime_folder, self.data_date)
        if not os.path.exists(data_date_folder):
            os.mkdir(data_date_folder)
        
    def run(self):
        cur_partition = 0
        source_partition_path = self.get_source_date_partition(self.data_date, cur_partition)
        while (os.path.exists(source_partition_path)):
            records_dict = create_app_realtime_data_record_dict()
            app_data_partition_path = self.get_app_astock_record_data_realtime_date_partition(self.data_date, cur_partition)

            dataframe = load_parquet_to_dataframe(source_partition_path)
            for _, row in dataframe.iterrows():
                records_dict["code"].append(row["code"])
                records_dict["hour"].append(row["hour"])
                records_dict["minute"].append(row["minute"])
                records_dict["second"].append(row["second"])
                records_dict["turnover"].append(row["turnover"])
                if (row["turnover"] == 0):
                    records_dict["avg_price"].append(0.0)
                else:
                    records_dict["avg_price"].append(row["volume"] / row["turnover"])
            
            save_record_dict_to_parquet(records_dict, app_data_partition_path)

            cur_partition += 1
            source_partition_path = self.get_source_date_partition(self.data_date, cur_partition)
        # copy the code_to_partition_map.json to the destination path
        copyfile(
            self.get_source_date_code_to_partition_map(self.data_date),
            self.get_app_astock_record_data_realtime_date_code_to_partition_map(self.data_date)
        )
    
    @property 
    def data_date(self):
        return self._data_date
    

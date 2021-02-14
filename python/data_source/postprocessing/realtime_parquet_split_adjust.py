"""
!!! Assume:
app data has already been processed into realtime data


Including following duties:

- Shrink the real time data into the following columnar
0. code <str>
1. hour <int>
2. minute <int>
3. second <int>
4. handover <int>
5. price <float>

- Adjust the price according to the split adjust factor

- Store the adjusted parquet data into app_data folder

- update the split adjust metadata json
"""

import json 
import os 
from datetime import date
from data_source.postprocessing.utils import (
    save_record_dict_to_parquet, 
    load_parquet_to_dataframe
)
from data_source.lib.split_adjust import SplitAdjust

class RealTimeParquetDataSplitAdjust(object):

    def __init__(self, source_data_folder, app_data_folder, realtime_record_date, split_adjust_record_date):
        self._source_data_folder = source_data_folder
        self._app_data_folder = app_data_folder
        self._realtime_record_date = realtime_record_date 
        self._split_adjust_record_date = split_adjust_record_date
        self._split_adjust = SplitAdjust()

    def run(self):
        """
        Perform split adjust for a given date's data according to loaded split adjust data

        Args:
            app_data_path <str>: app_data_path as of config 
            realtime_record_date <str>: date of realtime data to be processed in app_data_folder in yyyy-MM-dd format
            split_adjust_record_date <str>: date of the split adjust record used to adjust
        """
        pass

    def load_split_adjust_record_parquet(self, parquet_path):
        dataframe = load_parquet_to_dataframe(parquet_path)
        for row in dataframe.rows:
            self.split_adjust.add_record(
                row["code"], 
                date(row["year"], row["month"], row["day"]),
                row["backward_split_adjust_factor"],
                row["forward_split_adjust_factor"]
            )
        self.split_adjust.sort_backward_split_adjust_list_dict_desc()
    
    def verify_folder_structure(self):
        assert os.path.exists(self.source_data_folder)
        assert os.path.exists(self.app_data_folder)

        astock_path

    @property
    def source_data_folder(self):
        return self._source_data_folder

    @property
    def app_data_folder(self):
        return self._app_data_folder

    @property 
    def realtime_record_date(self):
        return self._realtime_record_date

    @property
    def split_adjust_record_date(self):
        return self._split_adjust_record_date
    
    @property
    def split_adjust(self):
        return self._split_adjust

    


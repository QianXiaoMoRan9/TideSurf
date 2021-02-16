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
from data_source.lib.date import parse_iso_date
from data_source.postprocessing.utils import (
    save_record_dict_to_parquet,
    load_parquet_to_dataframe
)
from data_source.postprocessing.postprocessor import Postprocessor
from data_source.lib.split_adjust import SplitAdjust
from data_source.postprocessing.schema import create_app_realtime_data_record_dict

class RealTimeParquetDataSplitAdjust(Postprocessor):

    def __init__(self, source_data_folder, app_data_folder, realtime_record_date, split_adjust_record_date):
        super().__init__(source_data_folder, app_data_folder)
        self._realtime_record_date = realtime_record_date
        self._split_adjust_record_date = split_adjust_record_date
        self.verify_date_folder_structure()
        self._split_adjust = SplitAdjust()

    def run(self):
        """
        Perform split adjust for a given date's data according to loaded split adjust data
        """
        self.load_split_adjust_record_parquet()
        record_date = parse_iso_date(self.realtime_record_date)

        "code<str> -> date<datetime.date>"
        latest_adjust_record_dict = dict()
        latest_adjust_record_path = self.get_app_astock_data_realtime_date_latest_adjust_record(
            self.realtime_record_date)
        if os.path.exists(latest_adjust_record_path):
            with open(latest_adjust_record_path, "r") as json_f:
                latest_adjust_record_raw_dict = json.load(json_f)
                for code, iso_date in latest_adjust_record_raw_dict.items():
                    latest_adjust_record_dict[code] = parse_iso_date(iso_date)

        "code<str> -> date<datetime.date>"
        new_adjust_record_dict = dict()

        # load all the partitions, and change each of them
        cur_partition = 0
        partition_path = self.get_app_astock_record_data_realtime_date_partition(
            self.realtime_record_date, cur_partition)
        while (os.path.exists(partition_path)):
            new_records_dict = create_app_realtime_data_record_dict()
            dataframe = load_parquet_to_dataframe(partition_path)
            for _, row in dataframe.iterrows():
                code = row["code"]
                hour = row["hour"]
                minute = row["minute"]
                second = row["second"]
                avg_price = row["avg_price"]
                turnover = row["turnover"]

                prev_adjusted_date = record_date
                if code in latest_adjust_record_dict:
                    prev_adjusted_date = latest_adjust_record_dict[code]
                factor = self.split_adjust.get_stock_backward_adjust_factor_for_date(code, prev_adjusted_date)
                
                # update the newly adjusted date for the code
                if code not in new_adjust_record_dict:
                    new_adjust_record_dict[code] = self.split_adjust_record_date
                
                new_records_dict["code"].append(code)
                new_records_dict["hour"].append(hour)
                new_records_dict["minute"].append(minute)
                new_records_dict["second"].append(second)
                new_records_dict["avg_price"].append(avg_price * factor)
                new_records_dict["turnover"].append(turnover)
            
            realtime_parquet_partition_path = self.get_app_astock_record_data_realtime_date_partition(
                self.realtime_record_date,
                cur_partition
            )

            cur_partition += 1
            partition_path = self.get_app_astock_record_data_realtime_date_partition(
                self.realtime_record_date, cur_partition)

        # store the new aplit adjust record into the app's realtime data
        new_split_adjust_path = self.get_app_astock_data_realtime_date_latest_adjust_record(
            self.realtime_record_date)
        with open(new_split_adjust_path, "w") as json_f:
            json.dump(new_adjust_record_dict, json_f)

    def load_split_adjust_record_parquet(self):
        parquet_path = self.get_source_date_split_adjust(
            self.split_adjust_record_date)
        dataframe = load_parquet_to_dataframe(parquet_path)
        for _, row in dataframe.iterrows():
            self.split_adjust.add_record(
                row["code"],
                date(row["year"], row["month"], row["day"]),
                row["backward_split_adjust_factor"],
                row["forward_split_adjust_factor"]
            )
        self.split_adjust.sort_backward_split_adjust_list_dict_desc()

    def verify_date_folder_structure(self):
        split_adjust_path = self.get_source_date_split_adjust(
            self.split_adjust_record_date)
        assert os.path.exists(split_adjust_path)

        realtime_record_folder = self.get_app_astock_record_data_realtime_date_folder(
            self.realtime_record_date)
        assert os.path.exists(realtime_record_folder)

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

import unittest
from unittest import TestCase 
import os 
import json
import shutil 
import time
import random
import pathlib
from data_source.lib.enum_types import AStockExchange, AssetType
from data_source.postprocessing.utils import save_record_dict_to_parquet, load_parquet_to_dataframe
from data_source.postprocessing.postprocessor import Postprocessor
from data_source.postprocessing.schema import create_app_realtime_data_record_dict
from data_source.postprocessing.realtime_parquet_split_adjust import RealTimeParquetDataSplitAdjust

class RealTimeParquetDataSplitAdjustTest():

    def setUp(self):
        
        self.source_data_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), "source_data_folder")
        self.app_data_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), "app_data_folder")
        
        if not os.path.exists(self.source_data_folder):
            os.mkdir(self.source_data_folder)
        if not os.path.exists(self.app_data_folder):
            os.mkdir(self.app_data_folder)

        self.dates = ["2020-12-21", "2020-12-22", "2020-12-23", "2020-12-24", "2020-12-25", "2020-12-28"]
        self.postprocessor = Postprocessor(self.source_data_folder, self.app_data_folder)
        self.codes = [
            "sz000001", "sh600450", "sz000002", "sz003456","sz000003", "sh603456"
        ]

        self.date_to_record_dict_dict = dict()
        self.num_records = 10
        for i in range(len(self.codes)):
            date = self.dates[i]
            record_dict = create_app_realtime_data_record_dict()
            for code in self.codes:
                record_dict["code"] += [code for _ in range(self.num_records)]
                record_dict["hour"] += [random.randint(9, 12) for _ in range(self.num_records)]
                record_dict["minute"] += [random.randint(0, 60) for _ in range(self.num_records)]
                record_dict["second"] += [random.randint(0, 60) for _ in range(self.num_records)]
                record_dict["avg_price"] += [random.uniform(10.0, 12.0) for _ in range(self.num_records)]
                record_dict["turnover"] += [random.randint(100, 5000) for _ in range(self.num_records)]
            os.mkdir(self.postprocessor.get_app_astock_record_data_realtime_date_folder(date))
            save_record_dict_to_parquet(
                record_dict,
                self.postprocessor.get_app_astock_record_data_realtime_date_partition(date, 0)
            )
            self.date_to_record_dict_dict[date] = record_dict

        self.latest_split_adjust_20201221 = {
            "sz000002": "2020-12-24"
        }
        with open(self.postprocessor.get_app_astock_data_realtime_date_latest_adjust_record("2020-12-21"), "w") as json_f:
            json.dump(self.latest_split_adjust_20201221, json_f)

        self.split_adjust_record_20201228 = {
            "code": ["sz000001", "sz000001", "sz000002"],
            "type": [AssetType.STOCK, AssetType.STOCK, AssetType.STOCK],
            "exchange": [AStockExchange.SHENZHEN, AStockExchange.SHENZHEN, AStockExchange.SHENZHEN],
            "year": [2020, 2020, 2020],
            "month": [12, 12, 12],
            "day": [22, 28, 23],
            "price_day_before_yesterday": [0.0, 0.0, 0.0],
            "close_price_before_split": [0.0, 0.0, 0.0],
            "split_day_cur_price": [0.0, 0.0, 0.0],
            "split_day_percentage_increase": [0.0, 0.0, 0.0],
            "split_day_handover": [0, 0, 0],
            "split_day_volume": [0, 0, 0],
            "backward_split_adjust_factor": [0.45, 0.55, 0.4],
            "forward_split_adjust_factor": [1/0.45, 1/0.55, 1/0.4]
        }
        os.mkdir(self.postprocessor.get_source_date_folder("2020-12-28"))
        save_record_dict_to_parquet(
            self.split_adjust_record_20201228,
            self.postprocessor.get_source_date_split_adjust("2020-12-28")
        )

        for adjust_date in self.dates:
            self.split_adjust_processor = RealTimeParquetDataSplitAdjust(
                self.source_data_folder, 
                self.app_data_folder,
                adjust_date,
                "2020-12-28"
            )

            self.split_adjust_processor.run()

    def tearDown(self):
        shutil.rmtree(self.source_data_folder)
        shutil.rmtree(self.app_data_folder)

    def perform_adjust(self, code, data_date, discount_factor, partition = 0):
        adjusted_parquet_path = self.postprocessor.get_app_astock_record_data_realtime_date_partition(
            data_date,
            partition
        )
        dataframe = load_parquet_to_dataframe(adjusted_parquet_path)
        cur_index = 0

        for _, row in dataframe.iterrows():
            if (row["code"] == code):
                self.assertAlmostEqual(
                    row["avg_price"], 
                    discount_factor * self.date_to_record_dict_dict[data_date]["avg_price"][cur_index]
                )
            cur_index += 1

    def test_multiple_split_adjust(self):
        
        # test if the split adjust on multiple time scale is effective

        "Verify sz000001 price at 2020-12-28 does not change"
        self.perform_adjust("sz000001", "2020-12-28", 1.0)

        "Verify sz000001 price at 2020-12-25 changes by 0.55"
        self.perform_adjust("sz000001", "2020-12-25", 0.55)

        "Verify sz000001 price at 2020-12-22 changes by 0.55"
        self.perform_adjust("sz000001", "2020-12-22", 0.55)

        "Verify sz000001 price at 2020-12-21 changes by 0.55*0.45"
        self.perform_adjust("sz000001", "2020-12-21", 0.55 * 0.45)

        "Verify sz000002 price at 2020-12-23 does not change"
        self.perform_adjust("sz000002", "2020-12-23", 1.0)

        "Verify sz000002 price at 2020-12-22 changes by 0.4"
        self.perform_adjust("sz000002", "2020-12-22", 0.4)

        "Verify sz000002 price at 2020-12-21 does not change"
        self.perform_adjust("sz000002", "2020-12-21", 1.0)

        # test if the split adjust on timestamp that has already been adjusts is effective

    def assertAlmostEqual(self, a, b):
        if not (abs(a-b) < 1e-5):
            print("Got two diferent value {}, {}".format(a, b))
            self.tearDown()
            assert False 

    def run(self):
        t.setUp() 
        t.test_multiple_split_adjust()
        t.tearDown()


if __name__ == "__main__":
    t = RealTimeParquetDataSplitAdjustTest()
    t.run()


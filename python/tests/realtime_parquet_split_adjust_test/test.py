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

class RealTimeParquetDataSplitAdjustTest(TestCase):

    def setUp(self):
        
        self.source_data_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), "source_data_folder")
        self.app_data_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), "app_data_folder")
        
        if not os.path.exists(self.source_data_folder):
            os.mkdir(self.source_data_folder)
        if not os.path.exists(self.app_data_folder):
            os.mkdir(self.app_data_folder)

        self.postprocessor = Postprocessor(self.source_data_folder, self.app_data_folder)
        self.codes = [
            "sz000001", "sh600450", "sz000002", "sz003456","sz000003", "sh603456"
        ]
        self.num_records = 10

        

        self.records_dict_20201221 = create_app_realtime_data_record_dict()
        for code in self.codes:
            self.records_dict_20201221["code"] += [code for _ in range(self.num_records)]
            self.records_dict_20201221["hour"] += [random.randint(9, 12) for _ in range(self.num_records)]
            self.records_dict_20201221["minute"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201221["second"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201221["avg_price"] += [random.uniform(10.0, 12.0) for _ in range(self.num_records)]
            self.records_dict_20201221["turnover"] += [random.randint(100, 5000) for _ in range(self.num_records)]
        os.mkdir(self.postprocessor.get_app_astock_record_data_realtime_date_folder("2020-12-21"))
        save_record_dict_to_parquet(
            self.records_dict_20201221,
            self.postprocessor.get_app_astock_record_data_realtime_date_partition("2020-12-21", 0)
        )

        self.records_dict_20201222 = create_app_realtime_data_record_dict()
        for code in self.codes:
            self.records_dict_20201222["code"] += [code for _ in range(self.num_records)]
            self.records_dict_20201222["hour"] += [random.randint(9, 12) for _ in range(self.num_records)]
            self.records_dict_20201222["minute"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201222["second"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201222["avg_price"] += [random.uniform(10.0, 12.0) for _ in range(self.num_records)]
            self.records_dict_20201222["turnover"] += [random.randint(100, 5000) for _ in range(self.num_records)]
        os.mkdir(self.postprocessor.get_app_astock_record_data_realtime_date_folder("2020-12-22"))
        save_record_dict_to_parquet(
            self.records_dict_20201222,
            self.postprocessor.get_app_astock_record_data_realtime_date_partition("2020-12-22", 0)
        )


        self.records_dict_20201224 = create_app_realtime_data_record_dict()
        for code in self.codes:
            self.records_dict_20201224["code"] += [code for _ in range(self.num_records)]
            self.records_dict_20201224["hour"] += [random.randint(9, 12) for _ in range(self.num_records)]
            self.records_dict_20201224["minute"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201224["second"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201224["avg_price"] += [random.uniform(10.0, 12.0) for _ in range(self.num_records)]
            self.records_dict_20201224["turnover"] += [random.randint(100, 5000) for _ in range(self.num_records)]
        os.mkdir(self.postprocessor.get_app_astock_record_data_realtime_date_folder("2020-12-24"))
        save_record_dict_to_parquet(
            self.records_dict_20201224,
            self.postprocessor.get_app_astock_record_data_realtime_date_partition("2020-12-24", 0)
        )

        self.records_dict_20201225 = create_app_realtime_data_record_dict()
        for code in self.codes:
            self.records_dict_20201225["code"] += [code for _ in range(self.num_records)]
            self.records_dict_20201225["hour"] += [random.randint(9, 12) for _ in range(self.num_records)]
            self.records_dict_20201225["minute"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201225["second"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201225["avg_price"] += [random.uniform(10.0, 12.0) for _ in range(self.num_records)]
            self.records_dict_20201225["turnover"] += [random.randint(100, 5000) for _ in range(self.num_records)]
        os.mkdir(self.postprocessor.get_app_astock_record_data_realtime_date_folder("2020-12-25"))
        save_record_dict_to_parquet(
            self.records_dict_20201225,
            self.postprocessor.get_app_astock_record_data_realtime_date_partition("2020-12-25", 0)
        )
        
        self.records_dict_20201223 = create_app_realtime_data_record_dict()
        for code in self.codes:
            self.records_dict_20201223["code"] += [code for _ in range(self.num_records)]
            self.records_dict_20201223["hour"] += [random.randint(9, 12) for _ in range(self.num_records)]
            self.records_dict_20201223["minute"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201223["second"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201223["avg_price"] += [random.uniform(10.0, 12.0) for _ in range(self.num_records)]
            self.records_dict_20201223["turnover"] += [random.randint(100, 5000) for _ in range(self.num_records)]
        os.mkdir(self.postprocessor.get_app_astock_record_data_realtime_date_folder("2020-12-23"))
        save_record_dict_to_parquet(
            self.records_dict_20201223,
            self.postprocessor.get_app_astock_record_data_realtime_date_partition("2020-12-23", 0)
        )
        
        self.records_dict_20201228 = create_app_realtime_data_record_dict()
        for code in self.codes:
            self.records_dict_20201228["code"] += [code for _ in range(self.num_records)]
            self.records_dict_20201228["hour"] += [random.randint(9, 12) for _ in range(self.num_records)]
            self.records_dict_20201228["minute"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201228["second"] += [random.randint(0, 60) for _ in range(self.num_records)]
            self.records_dict_20201228["avg_price"] += [random.uniform(10.0, 12.0) for _ in range(self.num_records)]
            self.records_dict_20201228["turnover"] += [random.randint(100, 5000) for _ in range(self.num_records)]
        os.mkdir(self.postprocessor.get_app_astock_record_data_realtime_date_folder("2020-12-28"))
        save_record_dict_to_parquet(
            self.records_dict_20201228,
            self.postprocessor.get_app_astock_record_data_realtime_date_partition("2020-12-28", 0)
        )

        dates = [
            "2020-12-21", "2020-12-22", "2020-12-23", "2020-12-24", "2020-12-25", "2020-12-28"
        ]

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

        self.processor = RealTimeParquetDataSplitAdjust(
            self.source_data_folder, 
            self.app_data_folder,
            "2020-12-28",
            "2020-12-28"
        )

        self.processor.run()

    def tearDown(self):
        shutil.rmtree(self.source_data_folder)
        shutil.rmtree(self.app_data_folder)

    def test_multiple_split_adjust(self):
        time.sleep(10)

    def test_split_adjust_already_done(self):
        pass


if __name__ == "__main__":
    unittest.main()

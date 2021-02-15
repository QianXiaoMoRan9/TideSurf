from unittest import TestCase 
import os 
import shutil 
import random
from data_source.postprocessing.realtime_source_data_to_app_source_data import RealtimeSourceDataToAppSourceData

class RealtimeSourceDataToAppSourceDataTest(TestCase):

    def setUp(self):
        self.source_data_folder = "./source_data_folder"
        self.app_data_folder = "./app_data_folder"
        
        if not os.path.exists(self.source_data_folder):
            os.mkdir(self.source_data_folder)
        if not os.path.exists(self.app_data_folder):
            os.mkdir(self.app_data_folder)

        codes = [
            "sz000001", "sh600450", "sz000002", "sz003456", "sh603456"
        ]
        self.num_records = 100
        self.records_dict_20201221 = {
            "ask1": [random.uniform(10.0, 12.0) for _ in range(self.num_records)],
            "ask1_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "ask2": [random.uniform(10.0, 13.0) for _ in range(self.num_records)],
            "ask2_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "ask3": [random.uniform(10.0, 14.0) for _ in range(self.num_records)],
            "ask3_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "ask4": [random.uniform(10.0, 15.0) for _ in range(self.num_records)],
            "ask4_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "ask5": [random.uniform(10.0, 16.0) for _ in range(self.num_records)],
            "ask5_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "bid1": [random.uniform(10.0, 16.0) for _ in range(self.num_records)],
            "bid1_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "bid2": [random.uniform(10.0, 15.0) for _ in range(self.num_records)],
            "bid2_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "bid3": [random.uniform(10.0, 14.0) for _ in range(self.num_records)],
            "bid3_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "bid4": [random.uniform(10.0, 13.0) for _ in range(self.num_records)],
            "bid4_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "bid5": [random.uniform(10.0, 12.0) for _ in range(self.num_records)],
            "bid5_volume": [random.randint(30, 1000) for _ in range(self.num_records)],
            "buy": [random.uniform(11.0, 12.0) for _ in range(self.num_records)],
            "close": [random.uniform(10.0, 15.0) for _ in range(self.num_records)],
            "high": [random.uniform(15.0, 19.0) for _ in range(self.num_records)],
            "low": [random.uniform(9.0, 11.0) for _ in range(self.num_records)],
            "now": [random.uniform(10.0, 12.0) for _ in range(self.num_records)],
            "open": [random.uniform(10.0, 12.0) for _ in range(self.num_records)],
            "sell": [random.uniform(10.0, 12.0) for _ in range(self.num_records)],
            "hour": [random.randint(9, 12) for _ in range(self.num_records)],
            "minute": [random.randint(0, 60) for _ in range(self.num_records)],
            "second": [random.randint(0, 60) for _ in range(self.num_records)],
            "turnover": [random.randint(100, 5000) for _ in range(self.num_records)],
            "volume": [random.uniform(10000.0, 500000.0) for _ in range(self.num_records)],
            "code": [random.choice(codes) for _ in range(self.num_records)]
        }

    def tearDown(self):
        shutil.rmtree(self.source_data_folder)
        shutil.rmtree(self.app_data_folder)






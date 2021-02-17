import json 
import os
import shutil 
import random
import pathlib
from testing.test_case import TestCase 
from data_source.lib.price import PriceTwoDecimal
from data_source.postprocessing.schema import create_sina_record_dict, SINA_RECORD_FLOAT_ENTRIES
from data_source.postprocessing.utils import save_record_dict_to_parquet, load_parquet_to_dataframe
from data_source.postprocessing.postprocessor import Postprocessor
from data_source.postprocessing.realtime_source_data_to_daily_price_breakdown import RealtimeSourceDataToDailyPriceBreakdown

class RealtimeSourceDataToDailyPriceBreakdownTest(TestCase):

    def setUp(self):
        self.source_data_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), "source_data_folder")
        self.app_data_folder = os.path.join(pathlib.Path(__file__).parent.absolute(), "app_data_folder")
        if not os.path.exists(self.source_data_folder):
            os.mkdir(self.source_data_folder)
        if not os.path.exists(self.app_data_folder):
            os.mkdir(self.app_data_folder)
        self.date = "2020-12-21"
        self.num_entry = 10
        self.postprocessor = Postprocessor(self.source_data_folder, self.app_data_folder)
        self.p0_codes = ["sz000001", "sz000002"]
        self.p1_codes = ["sz000003", "sz000002"]

        # create the record folders
        source_date_folder = self.postprocessor.get_source_date_folder(self.date)
        if not os.path.exists(source_date_folder):
            os.mkdir(source_date_folder)
        
        breakdown_date_folder = self.postprocessor.get_app_astock_data_daily_breakdown_date_folder(self.date)
        if not os.path.exists(breakdown_date_folder):
            os.mkdir(breakdown_date_folder)
        
        self.p0_path = self.postprocessor.get_source_date_partition(self.date, 0)
        self.p1_path = self.postprocessor.get_source_date_partition(self.date, 1)

        self.p0_data = self.add_record(self.p0_codes)
        self.p1_data = self.add_record(self.p1_codes)

        save_record_dict_to_parquet(self.p0_data, self.p0_path)
        save_record_dict_to_parquet(self.p1_data, self.p1_path)

        self.data_processor = RealtimeSourceDataToDailyPriceBreakdown(
            self.source_data_folder,
            self.app_data_folder,
            self.date
        )
        self.data_processor.run()
    
    def tearDown(self):
        shutil.rmtree(self.source_data_folder)
        shutil.rmtree(self.app_data_folder)

    def add_record(self, codes):
        record_dict = create_sina_record_dict()
        for code in self.p0_codes:
            record_dict["ask1"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["ask2"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["ask3"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["ask4"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["ask5"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["bid1"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["bid2"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["bid3"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["bid4"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["bid5"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["ask1_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["ask2_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["ask3_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["ask4_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["ask5_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["bid1_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["bid2_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["bid3_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["bid4_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["bid5_volume"] += [random.randint(0, 10) for _ in range(self.num_entry)]
            record_dict["buy"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["close"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["high"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["low"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["now"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["open"] += [random.randrange(10, 12) for _ in range(self.num_entry)]
            record_dict["sell"] += [random.randrange(10, 12) for _ in range(self.num_entry)]

            record_dict["volume"] += [random.randrange(10000, 120000) for _ in range(self.num_entry)]
            record_dict["code"] += [code for _ in range(self.num_entry)]
            record_dict["hour"] += [random.randint(9, 12) for _ in range(self.num_entry)]
            record_dict["minute"] += [random.randint(0, 60) for _ in range(self.num_entry)]
            record_dict["second"] += [random.randint(0, 60) for _ in range(self.num_entry)]
            record_dict["turnover"] += [random.randint(0, 120) for _ in range(self.num_entry)]
        return record_dict

    def test_daily_price_breakdown(self):
        total_tunover_dict = dict() 
        for i in range(len(self.p0_data["turnover"])):
            code = self.p0_data["code"][i]
            if code not in total_tunover_dict:
                total_tunover_dict[code] = 0
            total_tunover_dict[code] += self.p0_data["turnover"][i]
        
        for i in range(len(self.p1_data["turnover"])):
            code = self.p1_data["code"][i]
            if code not in total_tunover_dict:
                total_tunover_dict[code] = 0
            total_tunover_dict[code] += self.p1_data["turnover"][i]
    
    def run_test_cases(self):
        self.test_daily_price_breakdown()

if __name__ == "__main__":
    t  = RealtimeSourceDataToDailyPriceBreakdownTest()
    t.run()


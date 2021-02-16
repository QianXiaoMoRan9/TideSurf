"""
Depending on the source data for that particular date

Input:
    source data folder, realtime records for a particular date
Output
    breakdown of the price/turnover for each stock/funds

"""
import os 

from data_source.postprocessing.utils import load_parquet_to_dataframe, save_record_dict_to_parquet
from data_source.lib.price import PriceTwoDecimal
from data_source.postprocessing.postprocessor import Postprocessor
from data_source.postprocessing.schema import create_app_daily_price_breakdown_record_dict

class RealtimeSourceDataToDailtPriceBreakdown(Postprocessor):
    def __init__(self, source_data_folder, app_data_folder, data_date):
        super().__init__(source_data_folder, app_data_folder)
        self._data_date = data_date

    @property 
    def data_date(self):
        return self._data_date

    def run(self):
        "code <str> -> price <Price> -> share amount"
        breakdown_dict = dict()
        "code <str> -> share amount"
        total_turnover_dict = dict()
        # iterate through all thr partitions
        cur_partition = 0
        partition_path = self.get_source_date_partition(self.data_date, cur_partition)
        while (os.path.exists(partition_path)):
            dataframe = load_parquet_to_dataframe(partition_path)
            for _, row in dataframe.iterrows():
                code = row["code"]
                turnover = row["turnover"]
                volume = row["volume"]

                avg_price = 0.0
                if turnover != 0:
                    avg_price = volume / turnover

                price = PriceTwoDecimal(avg_price)

                if code not in breakdown_dict:
                    breakdown_dict[code] = dict()
                if price not in breakdown_dict[code]:
                    breakdown_dict[code][price] = 0
                breakdown_dict[code][price] += turnover 

                if code not in total_turnover_dict:
                    total_turnover_dict[code] = 0
                total_turnover_dict[code] += turnover
            
            cur_partition += 1
            partition_path = self.get_source_date_partition(self, data_date, cur_partition)
        # accumulate: each 
        record_dict = create_app_daily_price_breakdown_record_dict()
        for code, price_dict in breakdown_dict.items(): 
            for price, turnover in price_dict.items():
                record_dict["code"].append(code)
                record_dict["price_int"].append(price.int_num)
                record_dict["price_float"].append(price.float_num)
                record_dict["num_share"].append(turnover)
                record_dict["share_percentage"].append(turnover / total_turnover_dict[code])
        # save this into app_data_folder
        price_breakdown_path = self.get_app_astock_data_daily_breakdown_date_price_breakdown(self.data_date)
        save_record_dict_to_parquet(record_dict, price_breakdown_path)

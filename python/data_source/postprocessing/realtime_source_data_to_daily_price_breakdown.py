"""
Depending on the source data for that particular date

Input:
    source data folder, realtime records for a particular date
Output
    breakdown of the price/turnover for each stock/funds

"""
from data_source.lib.price import PriceTwoDecimal
from data_source.postprocessing.postprocessor import Postprocessor

class RealtimeSourceDataToDailtPriceBreakdown(PostProcessor):
    def __init__(self, source_data_folder, app_data_folder, data_date):
        super().__init__(source_data_folder, app_data_folder)
        self._data_date = data_date

    @property 
    def data_date(self):
        return self._data_date

    def run(self):
        # iterate through all thr partitions

        # accumulate:
        pass


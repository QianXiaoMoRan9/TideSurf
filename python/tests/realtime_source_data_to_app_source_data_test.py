import json
import os
from data_source.postprocessing.realtime_source_data_to_app_source_data import RealtimeSourceDataToAppSourceData

SOURCE_DATA_FOLDER = "/home/steven/Desktop/Fast500/astock_parquet"
APP_DATA_FOLDER = "/home/steven/Desktop/Fast500/tidesurf_data"
DATA_DATE = "2020-12-22"
obj = RealtimeSourceDataToAppSourceData(
    SOURCE_DATA_FOLDER,
    APP_DATA_FOLDER,
    DATA_DATE
)

# obj.run()

with open(obj.get_source_date_code_to_partition_map(DATA_DATE), "r") as json_f:
    source_code_to_partition_dict = json.load(json_f)
    with open(obj.get_app_astock_record_data_realtime_date_code_to_partition_map(DATA_DATE)) as json_ff:
        app_code_to_partition_dict = json.load(json_ff)
        assert source_code_to_partition_dict == app_code_to_partition_dict

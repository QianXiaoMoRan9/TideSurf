"""
CMD ARGV:
engine config JSON path
cur_date

For A Stocks

Main driver entry for calling python part of the engine for retrieving data for today
This must be done before the C++ engine gets launched

Initialized data include:

- retrieve today's stock list
- retrieve today's stock split adjust factors

"""
import json
import argparse
import os

from config.app_config import AppConfig
from data_source.stock.split_share_juchao import get_split_share_from_stock_list_to_parquet

def get_args():
    parser = argparse.ArgumentParser(
        description='Args for launching initialize_data_today_astock_main')
    parser.add_argument(
        '--config-json',
        dest='config_json',
        type=str,
        required=True,
        metavar="config-json",
        help='Engine config json file path'
    )
    parser.add_argument(
        '--cur-date',
        dest='cur_date',
        type=str,
        required=True,
        metavar="cur-date",
        help='Current Beijing time Date in yyyy-MM-dd'
    )

    args = parser.parse_args()
    return args

def save_split_adjust_factors_to_app_folder(app_folder, cur_date):
    pass

if __name__ == "__main__":
    args = get_args()
    app_config = AppConfig(args.config_json)


    
    
    


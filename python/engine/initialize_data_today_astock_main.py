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

from logger.logger import Logger 
from logger.enums import MarketType
from config.app_config import AppConfig
from data_source.stock.get_stock_codes import StockCodeSHDJT
from data_source.stock.split_share_juchao import retrieve_all_stocks_from_stock_list

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

def get_current_date_stock_list(app_folder, cur_date):
    temp_folder = os.path.join(app_folder, "temp")
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    day_folder = os.path.join(temp_folder, cur_date)
    if not os.path.exists(day_folder):
        os.mkdir(day_folder)
    
    with open(os.path.join(day_folder, "data", "stock_list.json"), "w") as json_f:
        getter = StockCodeSHDJT()
        res_list = getter.get_list()
        json.dump(res_list, json_f)
    


def get_split_adjust_factors_to_app_folder(app_folder, cur_date):
    temp_folder = os.path.join(app_folder, "temp")
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    day_folder = os.path.join(temp_folder, cur_date)
    if not os.path.exists(day_folder):
        os.mkdir(day_folder)
    split_adjust_json = retrieve_all_stocks_from_stock_list(
        temp_folder,
        cur_date,
        cur_date,
        cur_date
    )
    with open(os.path.join(day_folder, "data", "split_adjust_factor.json"), "w") as json_f:
        json.dump(split_adjust_json, json_f)
    

if __name__ == "__main__":
    
    args = get_args()
    app_config = AppConfig(args.config_json)
    logger = Logger(app_config.app_data_folder, args.cur_date, MarketType.A_STOCK, "initialize_data_today_astock_main")
    
    logger.info("Begin getting stock list for date {}".format(args.cur_date))
    get_current_date_stock_list(app_config.app_data_folder, args.cur_date)
    logger.info("End getting stock list for date {}".format(args.cur_date))

    logger.info("Begin getting split share adjust factor for date {}".format(args.cur_date))
    get_split_adjust_factors_to_app_folder(app_config.app_data_folder, args.cur_date)
    logger.info("End getting split share adjust factor for date {}".format(args.cur_date))



    
    
    


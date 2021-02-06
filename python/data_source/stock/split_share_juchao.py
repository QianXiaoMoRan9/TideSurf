import json
import urllib
import os, sys
import requests
import time
import datetime
from pprint import pprint
from data_source.postprocessing.utils import save_record_dict_to_parquet, has_prefix, add_stock_prefix
from data_source.lib.enum_types import AssetType, AStockExchange
from data_source.lib.date import parse_iso_date

"""
Get the stocks according to the code
"""

####用于获取token
def gettoken(client_id,client_secret):
    url='http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token'
    post_data="grant_type=client_credentials&client_id=%s&client_secret=%s"%(client_id,client_secret)
    post_data={"grant_type":"client_credentials",
               "client_id":client_id,
               "client_secret":client_secret
               }
    req = requests.post(url, data=post_data)
    tokendic = json.loads(req.text)
    return tokendic['access_token']

####用于解析接口返回内容
def getPage(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

def get_split_share_json(stock_code_list, start_date = None, end_date = None):
    """
    Args:
        stock_code_list list<str>: code list without prefix: [000002, 000001, 688152]
    Returns:
        [
            {
                "raw_code": "000002",
                "type": AssetType.STOCK / AssetType.FUND,
                "exchange": AStockExchange.SHANGHAI / AStockExchange.SHENZHEN
                "split_date": 2020-08-14
                "price_day_before_yesterday": 28.60
                "close_price_before_split": 27.58
                "split_day_cur_price": 27.68
                "split_day_percentage_increase": 0.3626
                "split_day_handover": 94094734,
                "split_day_volume": 2592380291.0
                "pre_split_adjust_factor": 0.96433566
                "post_split_adjust_factor": 1.03698332
            }
        ]
    
    """
    assert len(stock_code_list) <= 50, "one request must have no more than 50 stocks, got: {}".format(len(stock_code_list))
    if len(stock_code_list) == 0:
        return []
    codes = ','.join(stock_code_list)
    param = "&scode={}".format(codes)
    if start_date is not None:
        param += "&sdate={}".format(start_date)
    if end_date is not None:
        param += "&edate={}".format(end_date)
    
    token = gettoken('I1qrKDSzMTV8Iqm9vKomdXVJ7As3yeD0','raA6BEZoYZ9KrmVu0AJ4QXbDJUDUi0oD') ##请在平台注册后并填入个人中心-我的凭证中的Access Key，Access Secret
    url = 'http://webapi.cninfo.com.cn/api/stock/p_stock2406?subtype=002&access_token='+token + param
    print(url)
    result = json.loads(getPage(url))
    
    res = []
    if 'records' not in result:
        return res
    raw_list = result['records']
    for record in raw_list:
        entry = dict()
        entry["raw_code"] = record["SECCODE"]

        asset_type = record["F001V"] 
        if (asset_type == "股票"):
            entry["type"] = AssetType.STOCK
        elif (asset_type == "基金"):
            entry["type"] = AssetType.FUND
        else:
            assert False, "split adjust encountered unknown asset type {}".format(asset_type)
        
        exchange = record["F002V"]
        if (exchange == "深交所"):
            entry["exchange"] = AStockExchange.SHENZHEN
        elif (exchange == "上交所"):
            entry["exchange"] = AStockExchange.SHANGHAI
        else:
            assert False, "split adjust encountered unknown exchange {}".format(exchange)
        
        entry["split_date"] = record["F003D"]
        entry["price_day_before_yesterday"] = record["F004N"]
        entry["close_price_before_split"] = record["F005N"]
        entry["split_day_cur_price"] = record["F006N"]
        entry["split_day_percentage_increase"] = record["F007N"]
        entry["split_day_handover"] = record["F008N"]
        entry["split_day_volume"] = record["F009N"]
        entry["pre_split_adjust_factor"] = record["F010N"]
        entry["post_split_adjust_factor"] = record["F011N"]
        res.append(entry)

    return res

def raw_code_to_astock_code(record):
    """ 
    Args:
        record dict: a record get_split_share_json() outputs
    Returns:
        proper A stock code with prefix
    """
    return add_stock_prefix(code)


def save_records_to_parquet(record_list, output_path):
    records_dict = {
                "code": [],
                "type": [],
                "exchange": [],
                "year": [],
                "month": [],
                "day": [],
                "price_day_before_yesterday": [],
                "close_price_before_split": [],
                "split_day_cur_price": [],
                "split_day_percentage_increase": [],
                "split_day_handover": [],
                "split_day_volume": [],
                "pre_split_adjust_factor": [],
                "post_split_adjust_factor": []
    }
    for record in record_list:
        for key, value in record.items():
            if (key == "code"):
                records_dict["code"].append(raw_code_to_astock_code(record))
            elif (key == "split_date"):
                date = parse_iso_date(record["split_date"])
                records_dict["year"] = date.year
                records_dict["month"] = date.month
                records_dict["day"] = date.day
            else:
                records_dict[key] = value 
    save_record_dict_to_parquet(records_dict, output_path)

if __name__ == "__main__":

    """
    Get all split records for the stock list from aicai stock lists, those codes without prefix
    Sys.argvs:
    
    data_folder
    cur_date
    output_folder

    example:
    /home/steven/Desktop/Fast500/sina-raw
    2020-12-22
    /home/steven/Desktop/Fast500/astock_parquet/
    """
    assert len(sys.argv) == 4, "Must have two arguments, data_folder_path, cur_date, destination_folder"
    MAX_NUM_STOCK_PER_REQUEST = 49
    stock_list_path = "{}/{}/data/stock_list_{}.json".format(sys.argv[1], sys.argv[2], sys.argv[2]) 
    with open(stock_list_path, "r") as json_f:
        record_list = []
        stock_list = json.load(json_f)["stocks"]
        for start_index in range(0, len(stock_list), MAX_NUM_STOCK_PER_REQUEST):
            code_list = []
            for stock in stock_list[start_index: start_index + MAX_NUM_STOCK_PER_REQUEST]:
                code = stock[0]
                if not has_prefix(code):
                    code_list.append(code)
            record_list += get_split_share_json(code_list)
            print("stepped {}, {}".format(start_index, start_index + MAX_NUM_STOCK_PER_REQUEST))
            time.sleep(2)
            
        parent_folder = os.path.join(sys.argv[3], sys.argv[2])
        if not os.path.exists(parent_folder):
            os.mkdir(parent_folder)
        output_path = "{}/{}/split_share.parquet".format(sys.argv[3], sys.argv[2])
        save_records_to_parquet(record_list, output_path)

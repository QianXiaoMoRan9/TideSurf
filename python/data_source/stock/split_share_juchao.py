import json
import urllib
import requests
import datetime

from data_source.postprocessing.utils import save_record_dict_to_parquet
from data_source.lib.enum_types import AssetType, AStockExchange
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
    raw_list = result['records']
    res = []
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
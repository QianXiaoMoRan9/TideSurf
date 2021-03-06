LATIN_CHAR_START = 65281
ASCII_CHAR_START = 33
# 'Ａ' -> 'A'
ASCII_TO_LATIN_CHAR_DICT = {chr(ASCII_CHAR_START + x) : chr(LATIN_CHAR_START + x) for x in range(94)}

A_STOCK_PREFIX = {
    'sh60',
    'sh688',
    'sz00',
    'sz30'
}

SH_HEAD = ("50", "51", "60", "90", "110", "113",
            "132", "204", "5", "6", "9", "7")

SINA_RECORD_FLOAT_ENTRIES = {
    "ask1",
    "ask2",
    "ask3",
    "ask4",
    "ask5",
    "bid1",
    "bid2",
    "bid3",
    "bid4",
    "bid5",
    "buy",
    "close",
    "high",
    "low",
    "now",
    "open",
    "sell",
    "volume"
}




def create_sina_record_dict():
    return {
        "ask1": [],
        "ask1_volume": [],
        "ask2": [],
        "ask2_volume": [],
        "ask3": [],
        "ask3_volume": [],
        "ask4": [],
        "ask4_volume": [],
        "ask5": [],
        "ask5_volume": [],
        "bid1": [],
        "bid1_volume": [],
        "bid2": [],
        "bid2_volume": [],
        "bid3": [],
        "bid3_volume": [],
        "bid4": [],
        "bid4_volume": [],
        "bid5": [],
        "bid5_volume": [],
        "buy": [],
        "close": [],
        "high": [],
        "low": [],
        "now": [],
        "open": [],
        "sell": [],
        "hour": [],
        "minute": [],
        "second": [],
        "turnover": [],
        "volume": [],
        "code": []
}

def create_sina_stock_list_record_dict():
    return {
        "code": [],
        "name": []
    }

def create_junchao_split_adjust_record_dict():
    return {
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
        "backward_split_adjust_factor": [],
        "forward_split_adjust_factor": []
    }

def create_app_realtime_data_record_dict():
    return {
        "code": [],
        "hour": [],
        "minute": [],
        "second": [],
        "avg_price": [],
        "turnover": []
    }

def create_app_daily_price_breakdown_record_dict():
    return {
        "code": [],
        "price_int": [],
        "price_float": [],
        "num_share": [],
        "share_percentage": []
    }

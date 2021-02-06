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
        "name": [],
        "abbreviation": []
    }



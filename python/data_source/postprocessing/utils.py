import pandas as pd 
import pyarrow.parquet as pq
import pyarrow as pa

from data_source.postprocessing.schema import SH_HEAD

def has_prefix(stock_code):
    return ord('a') <= ord(stock_code[0]) <= ord('z')

def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert type(stock_code) is str, "stock code need str type"
    
    if stock_code.startswith(("sh", "sz", "zz")):
        return stock_code[:2]
    else:
        return "sh" if stock_code.startswith(SH_HEAD) else "sz"

def add_stock_prefix(stock_code):
    return get_stock_type(stock_code) + stock_code[-6:]

def save_record_dict_to_parquet(result_record_dict, output_path):
    dataframe = pd.DataFrame.from_dict(result_record_dict)
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, output_path)
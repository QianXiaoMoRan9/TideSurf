"""
Read the stock_list_yyyy_mm_dd.json and convert it into a parquet

Args:

source_data_folder, cur_date, target_data_folder

example:
/home/steven/Desktop/Fast500/sina-raw/2020-12-22/data
2020-12-22
/home/steven/Dessktop/Fast500/astock_parquet/2020-12-22

"""

import json 
import pyarrow as pa  
import pandas as pd 
import pyarrow.parquet as pq 
from data_source.postprocessing.schema import create_sina_stock_list_record_dict

def load_stock_list_json_to_pandas_table(json_path):
    with open(json_path, "r") as file:
        json_object = json.load(file)
        record_dict = create_sina_stock_list_record_dict()
        for stock_object in json_object["stocks"]:
            record_dict["code"].append(stock_object[0])
            record_dict["name"].append(stock_object[1])
            record_dict["abbreviation"].append(stock_object[2])
        return pd.DataFrame.from_dict(record_dict)

def save_stock_list_to_parquet(dataframe, output_path):
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, output_path)
    print("Stock list parquet table written in: {}".format(output_path))


def json_to_parquet(json_path, output_path):
    pd_dataframe = load_stock_list_json_to_pandas_table(json_path)
    save_stock_list_to_parquet(pd_dataframe, output_path)

if __name__ == "__main__":
    import os, sys
    assert len(sys.argv) == 4, "Must have three arguments"
    source_path = os.path.join(
        sys.argv[1],
        "stock_list_{}.json".format(sys.argv[2])
    )

    output_path = os.path.join(
        sys.argv[3],
        "stock_list.parquet"
    )
    json_to_parquet(source_path, output_path)



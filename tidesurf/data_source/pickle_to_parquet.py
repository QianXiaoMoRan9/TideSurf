import pickle 
import pandas as pd 
import pyarrow as pa 
import pyarrow.parquet as pq


"""
Implement the sina post processing for a given date crawled data
Deduplicate the data from the same date
Store then into proper parquet file format

Driver args:
data_folder, destination_parent_folder, date


Post process schema:

Assume that no missing gaps between time stamp.
Divide the amount traded by the number of seconds from the difference between prev and current
Divide the number traded by the price range

For example if for a stock with label 600001:

prev:
timestamp: 02:00:00, close: 12.00

Current:
timestampe: 2:00:03, high: 12.04, low: 11.99, volumn(股) 60000

Then for each second we have 60000 / 3 / (12.04 - 11.99) we assign:
timestamp: 2:00:01, price: 11.99 volumn: 40000
timestamp: 2:00:02, price: 11.99 volumn: 40000
timestamp: 2:00:03, price: 11.99 volumn: 40000
timestamp: 2:00:01, price: 12.00 volumn: 40000
timestamp: 2:00:02, price: 12.00 volumn: 40000
timestamp: 2:00:03, price: 12.00 volumn: 40000
....

Input:
Folder structure:
.
|---<year>-<month>-<day>_<process>-<part>.pkl
|---stock_list_<year>-<month>-<day>.json

pkl:
[
    {
        'code': {'ask1': 18.07,
             'ask1_volume': 92900,
             'ask2': 18.08,
             'ask2_volume': 15760,
             'ask3': 18.09,
             'ask3_volume': 14900,
             'ask4': 18.1,
             'ask4_volume': 9200,
             'ask5': 18.11,
             'ask5_volume': 1000,
             'bid1': 18.06,
             'bid1_volume': 1100,
             'bid2': 18.05,
             'bid2_volume': 77200,
             'bid3': 18.04,
             'bid3_volume': 75200,
             'bid4': 18.03,
             'bid4_volume': 155201,
             'bid5': 18.02,
             'bid5_volume': 150100,
             'buy': 18.06,
             'close': 18.36,
             'date': '2020-12-21',
             'high': 18.3,
             'low': 18.03,
             'name': '平安银行',
             'now': 18.06,
             'open': 18.3,
             'sell': 18.07,
             'time': '09:44:21',
             'turnover': 12563538,
             'volume': 227526419.67
        },
        ...
    },
    ...
]

"""

import json
import pickle
import os, sys
from multiprocessing import Process
import pandas as pd
import datetime

FLOAT_ENTRIES = {
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

def create_record_dict():
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
    }

def get_process_file_name(cur_date, process, part):
    return "{}_{}-{}.pkl".format(cur_date, process, part)

def get_destination_file_name(code):
    return "{}.parquet".format(code)


def add_record(record, cur_date, code, records_dict, prev_time_dict,
               prev_turnover_dict, prev_volume_dict):
    # if this stock does not trade then add only one row with 0 on volume arguments
    if cur_date != record["date"]:
        if len(records_dict[code]["hour"]) == 1:
            return 
        else:
            for key, lst in records_dict[code].items():
                if key == "hour":
                    lst.append(9)
                elif key == "minute":
                    lst.append(15)
                else:
                    lst.append(0)
            return 
    # check if time overlaps, if not, update time
    if (prev_time_dict[code] == record["time"]):
        return 
    for key, value in record.items():
        if key in FLOAT_ENTRIES:
            parsed_value = float(record[key])
            if (key == "volume"):
                delta = parsed_value - prev_volume_dict[code]
                prev_volume_dict[code] = parsed_value
                parsed_value = delta
            records_dict[code][key].append(parsed_value)
        else:
            if (key == "date"):
                continue 
            elif (key == "name"):
                continue
            elif (key == "time"):
                prev_time_dict[code] = record[key]
                time_list = list(map(int, record[key].split(":")))
                records_dict[code]["hour"].append(time_list[0])
                records_dict[code]["minute"].append(time_list[1])
                records_dict[code]["second"].append(time_list[2])
            elif (key == "turnover"):
                turnover = int(record[key])
                delta = turnover - prev_turnover_dict[code]
                records_dict[code][key].append(delta) 
                prev_turnover_dict[code] = turnover
            else:
                records_dict[code][key].append(int(record[key]))

def job(data_folder, destination_folder, cur_date, process):
    """
    Args:
        data_folder (str): the folder where data is stored
        destination_folder (str): folder with cur_date, example: /some_folder/2020-12-23
        cur_date (str): in form of yyyy-MM-dd
        process (int): the process number
    """
    records_dict = dict()
    prev_time_dict = dict()
    prev_turnover_dict = dict()
    prev_volume_dict = dict()

    part_0_name = os.path.join(data_folder, get_process_file_name(cur_date, process, 0))
    
    # initialize the empty entries for each stock
    with open(part_0_name, "rb") as part_0_file:
        part_0_pickle = pickle.load(part_0_file)
        for code, record in part_0_pickle[0].items():
            records_dict[code] = create_record_dict()
            prev_time_dict[code] = "00:00:00"
            prev_turnover_dict[code] = 0
            prev_volume_dict[code] = 0.0
    
    cur_part = 0
    while True:
        part_file_name = os.path.join(
                data_folder, 
                get_process_file_name(cur_date, process, cur_part)
        )
        if not os.path.exists(part_file_name):
            break 
        with open(part_file_name, "rb") as part_file:
            pickle_file = pickle.load(part_file)
            for record_dict in pickle_file:
                for code, record in record_dict.items():
                    add_record(
                        record, 
                        cur_date, 
                        code, 
                        records_dict, 
                        prev_time_dict, 
                        prev_turnover_dict, 
                        prev_volume_dict
                    )
        cur_part += 1
        print(cur_part)

    for code, record_dict in records_dict.items():
        output_path = os.path.join(destination_folder, get_destination_file_name(code))
        dataframe = pd.DataFrame.from_dict(record_dict)
        table = pa.Table.from_pandas(dataframe)
        pq.write_table(table, output_path)

if __name__ == "__main__":
    assert len(sys.argv) == 4, "There must be 4 arguments"
    [
        data_folder,
        destination_parent_folder,
        cur_date
    ] = sys.argv[1:]

    process = 0 
    destination_folder = os.path.join(destination_parent_folder, cur_date)
    if (not os.path.exists(destination_folder)):
        os.mkdir(destination_folder)
    job(data_folder, destination_folder, cur_date, process)
    print("done")

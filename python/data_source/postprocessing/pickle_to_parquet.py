"""
Implement the sina post processing for a given date crawled data
Deduplicate the data from the same date
Store then into proper parquet file format

Driver args:
data_folder <str>
destination_folder <str> 
date <yyyy-MM-dd>
num_stocks_per_folder <int> optional

Example:
/home/steven/Desktop/Fast500/sina-raw
/home/steven/Desktop/Fast500/astock_parquet
2020-12-21
50 

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
import os
import sys
from multiprocessing import Process
import pandas as pd
import datetime
import pyarrow as pa
import pyarrow.parquet as pq
from data_source.postprocessing.schema import (
    SINA_RECORD_FLOAT_ENTRIES,
    ASCII_TO_LATIN_CHAR_DICT,
    create_sina_record_dict
)

from data_source.stock.easy_quotation_sina_real import add_stock_prefix

DEFAULT_NUM_STOCKS_PER_PARTITION = 50


def get_process_file_name(cur_date, process, part):
    return "{}_{}-{}.pkl".format(cur_date, process, part)


def get_destination_file_name(code):
    return "{}.parquet".format(code)


def add_record(
        record,
        cur_date,
        records_dict,
        prev_time_dict,
        prev_turnover_dict,
        prev_volume_dict,
        name_to_code_dict):
    code = name_to_code_dict[record["name"]]
    # if records_dict does not have current code then initialize it
    if code not in records_dict:
        records_dict[code] = create_sina_record_dict()
        prev_time_dict[code] = "00:00:00"
        prev_turnover_dict[code] = 0
        prev_volume_dict[code] = 0.0

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
                elif key == "code":
                    lst.append(code)
                else:
                    lst.append(0)
            return
    # check if time overlaps, if not, update time
    if (prev_time_dict[code] == record["time"]):
        return
    for key, value in record.items():
        if key in SINA_RECORD_FLOAT_ENTRIES:
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
    records_dict[code]["code"].append(code)


def dump_partition(
        data_folder,
        destination_folder,
        cur_date, partition,
        records_dict,
        stock_partition_dict,
        min_num_stock_in_partition):
    """
    pop min_num_stock_in_partition number of stocks, concatenate then into 
    one single dictionary of records, dump them into one parquet partition

    Returns:
        The next partition number if current partition number is dumped
    """
    if len(records_dict) < min_num_stock_in_partition:
        return partition

    # concatenate records from different code into one
    num_keys_concatenated = 0
    result_record_dict = create_sina_record_dict()
    pop_key_list = []
    for code, record_dict in records_dict.items():
        for column, lst in record_dict.items():
            result_record_dict[column] = result_record_dict[column] + \
                records_dict[code][column]
        # remove the processed stock from the records dict
        # if reaches the number of stocks per partition, then terminate
        pop_key_list.append(code)
        
        num_keys_concatenated += 1
        if (num_keys_concatenated == min_num_stock_in_partition):
            break
    for code in pop_key_list:
        assert code not in stock_partition_dict, "Code {} should not be in partition {} as it has already in partition {}".format(partition, stock_partition_dict[code])
        stock_partition_dict[code] = partition
        records_dict.pop(code)

    output_path = os.path.join(
        destination_folder, cur_date, "{}.parquet".format(partition))
    dataframe = pd.DataFrame.from_dict(result_record_dict)
    table = pa.Table.from_pandas(dataframe)
    pq.write_table(table, output_path)
    return partition + 1

def replace_ascii_to_latin(string):
    d = {
        "启迪古汉": "启迪药业"
    }
    # res = []
    # for c in string:
    #     if c in ASCII_TO_LATIN_CHAR_DICT:
    #         res.append(ASCII_TO_LATIN_CHAR_DICT[c])
    #     else:
    #         res.append(c)

    # return ''.join(res)
    if (string in d):
        return d[string]
    
    return string.replace("A", "Ａ")

def construct_name_to_code_dict(source_data_folder, cur_date, name_to_code_dict):
    json_path = os.path.join(source_data_folder, "stock_list_{}.json".format(cur_date))
    with open(json_path, "r") as json_f:
        stock_list = json.load(json_f)
        for stock_elem in stock_list["stocks"]:
            name_to_code_dict[replace_ascii_to_latin(stock_elem[1])] = add_stock_prefix(stock_elem[0])
            name_to_code_dict[stock_elem[1]] = add_stock_prefix(stock_elem[0])
    print(name_to_code_dict)

def job(data_folder, destination_folder, cur_date, min_num_stocks_per_partition):
    """
    Args:
        data_folder (str): the folder where data is stored
        destination_folder (str): folder without date separation example: /some_folder
        cur_date (str): in form of yyyy-MM-dd
    """
    # create destination folder with date as sub-folder
    subfolder = os.path.join(destination_folder, cur_date)
    if (not os.path.exists(subfolder)):
        os.mkdir(subfolder)

    source_data_folder = os.path.join(data_folder, cur_date, "data")
    assert os.path.exists(source_data_folder), \
        "Source data folder {} must exists".format(source_data_folder)

    cur_process = 0
    cur_partition = 0

    records_dict = dict()
    prev_time_dict = dict()
    prev_turnover_dict = dict()
    prev_volume_dict = dict()
    stock_partition_dict = dict()
    name_to_code_dict = dict()

    construct_name_to_code_dict(source_data_folder, cur_date, name_to_code_dict)

    # iterate through all processes, until process number no longer exists
    # add records into the
    while (True):
        part_0_name = os.path.join(
            source_data_folder, get_process_file_name(cur_date, cur_process, 0))
        if (not os.path.exists(part_0_name)):
            break
        print("Start processing cur process: {}".format(cur_process))

        cur_part = 0
        # iterate through all the possible parts of records
        # until there is no part that exists
        part_file_name = os.path.join(
            source_data_folder,
            get_process_file_name(cur_date, cur_process, cur_part)
        )
        while os.path.exists(part_file_name):
            with open(part_file_name, "rb") as part_file:
                pickle_file = pickle.load(part_file)
                for record_dict in pickle_file:
                    for code, record in record_dict.items():
                        add_record(
                            record,
                            cur_date,
                            records_dict,
                            prev_time_dict,
                            prev_turnover_dict,
                            prev_volume_dict,
                            name_to_code_dict
                        )
            cur_part += 1
            part_file_name = os.path.join(
                source_data_folder,
                get_process_file_name(cur_date, cur_process, cur_part)
            )
        # after getting all the records in the current process
        # dump the partitions into parquet files
        if (len(records_dict) >= min_num_stocks_per_partition):

            next_partition = dump_partition(
                source_data_folder,
                destination_folder,
                cur_date,
                cur_partition,
                records_dict,
                stock_partition_dict,
                min_num_stocks_per_partition)
            while(next_partition != cur_partition):
                cur_partition = next_partition
                next_partition = dump_partition(
                    source_data_folder,
                    destination_folder,
                    cur_date,
                    cur_partition,
                    records_dict,
                    stock_partition_dict,
                    min_num_stocks_per_partition)
        print("Finished processing cur process: {}".format(cur_process))
        cur_process += 1
    # dump the remaining records into a single partition
    next_partition = dump_partition(
        source_data_folder,
        destination_folder,
        cur_date,
        cur_partition,
        records_dict,
        stock_partition_dict,
        0)

    # dump the stock_partition_map
    code_to_partition_json_path = os.path.join(
        destination_folder, cur_date, "code_to_partition_map.json")
    with open(code_to_partition_json_path, "w") as json_f:
        json.dump(stock_partition_dict, json_f)


if __name__ == "__main__":
    assert len(sys.argv) >= 4, "There must be at least 3 arguments"
    data_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    cur_date = sys.argv[3]
    min_num_stocks_per_partition = DEFAULT_NUM_STOCKS_PER_PARTITION
    if len(sys.argv) > 4:
        min_num_stocks_per_partition = int(sys.argv[4])

    job(data_folder, destination_folder, cur_date, min_num_stocks_per_partition)
    print("done")

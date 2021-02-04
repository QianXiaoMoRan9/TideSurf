
import pickle
import json
import os
import pyarrow as pa
import pyarrow.parquet as pq
from data_source.postprocessing.pickle_to_parquet import get_process_file_name

SOURCE_DATA_FOLDER = "/home/steven/Desktop/Fast500/sina-raw/2020-12-21/data"
DESTINATION_FOLDER = "/home/steven/Desktop/Fast500/astock_parquet/2020-12-21"
CUR_DATE = "2020-12-21"

print("Start testing")

print(""" Load the pickle files """)

"code -> count of non-repeating record"
expect_records_dict = dict()
"code ->previous time stamp"
expect_prev_time_dict = dict()

for cur_process in range(16):
    cur_part = 0
    part_file_name = os.path.join(
        SOURCE_DATA_FOLDER,
        get_process_file_name(CUR_DATE, cur_process, cur_part)
    )
    while os.path.exists(part_file_name):
        with open(part_file_name, "rb") as part_file:
            pickle_file = pickle.load(part_file)
            for record_dict in pickle_file:
                for code, record in record_dict.items():
                    if code not in expect_records_dict:
                        expect_records_dict[code] = 0
                        expect_prev_time_dict[code] = "0:0:0"
                    if record["date"] != CUR_DATE:
                        if expect_records_dict[code] != 1:
                            expect_records_dict[code] = 1
                    else:
                        if record["time"] != expect_prev_time_dict[code]:
                            expect_prev_time_dict[code] = record["time"]
                            expect_records_dict[code] += 1
        cur_part += 1
        part_file_name = os.path.join(
            SOURCE_DATA_FOLDER,
            get_process_file_name(CUR_DATE, cur_process, cur_part)
        )

print("Load the processed parquet files")
expect_code_to_partition_dict = None
code_to_partition_dict_path = os.path.join(
    DESTINATION_FOLDER, "code_to_partition_map.json")
with open(code_to_partition_dict_path, "r") as json_f:
    expect_code_to_partition_dict = json.load(json_f)

"""
Iterate through all the parquet partitions check for two things:
1. if the given code is in the correct partition in the code_to_partition_map.json
2. count the number of records and to see if the record count matches
3. check each record of stock is not the same as the one from the previous
4. in the end count the number of stocks recorded is the same as what the pickle recorded
"""
actual_records_dict = dict()
actual_prev_time_dict = dict()

cur_partition = 0
partition_path = os.path.join(
    DESTINATION_FOLDER, "{}.parquet".format(cur_partition))

while os.path.exists(partition_path):
    dataframe = pq.read_table(partition_path).to_pandas()
    for index, row in dataframe.iterrows():
        code = row["code"]
        if code not in actual_records_dict:
            actual_records_dict[code] = 0
            actual_prev_time_dict[code] = "0:0:0"

        actual_time = "{}:{}:{}".format(
            row["hour"], row["minute"], row["second"])
        assert actual_prev_time_dict[code] != actual_time, "Time of a stock should not overlap. code: {}, overlapping time: {}".format(
            code, actual_time)
        actual_prev_time_dict[code] = actual_time
        actual_records_dict[code] += 1
        assert expect_code_to_partition_dict[code] == cur_partition, \
            "Stocks in the code_to_partition_json should match the one in the parquet expect {} in partition {}, actual in partition {}".format(
                code, expect_code_to_partition_dict[code], cur_partition)

    cur_partition += 1
assert len(actual_records_dict) == len(
    expect_records_dict), "Number of stocks in the record should match expected: {}, actual: {}".format(len(expect_records_dict), len(actual_records_dict))

for code, count in expect_records_dict.items():
    assert expect_records_dict[code] == actual_records_dict[code], \
        "Number of record for each stock matches, exception: {} expected: {}, actual: {}".format(
            code, expect_records_dict[code], actual_records_dict[code])

"""
Check the stock list to ensure:
1. records are unique
2. number of records is the same as the original stock list
"""
dataframstock_list_frame = pq.read_table(os.path.join(DESTINATION_FOLDER, "stock_list.parquet")).to_pandas()
stock_set = set() 
with open(os.path.join(SOURCE_DATA_FOLDER, "stock_list_{}.json",format(CUR_DATE))) as json_f:
    stock_list = json.load(json_f)["stocks"]
for index, row in dataframstock_list_frame.iterrows():
    stock_set.add(row["code"])

assert len(stock_set) == len(stock_list), "Should have the same number of unique stocks, missing : {}".format(len())

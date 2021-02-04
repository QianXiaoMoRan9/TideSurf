import pickle
import json
import os

from data_source.postprocessing.pickle_to_parquet import get_process_file_name

SOURCE_DATA_FOLDER = "/home/steven/Desktop/Fast500/sina-raw/2020-12-21/data"
DESTINATION_FOLDER = "/home/steven/Desktop/Fast500/astock_parquet/2020-12-21"
CUR_DATE = "2020-12-21"

expect_records_dict = dict()

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
                        expect_records_dict[code] = set()
                    expect_records_dict[code].add((cur_process, record["name"]))
        cur_part += 1
        part_file_name = os.path.join(
            SOURCE_DATA_FOLDER,
            get_process_file_name(CUR_DATE, cur_process, cur_part)
        )

for code, s in expect_records_dict.items():
    if len(s) != 1:
        print("code {} in process {}".format(code, s))

"""
Including following duties:

- Shrink the real time data into the following columnar
0. code <str>
1. hour <int>
2. minute <int>
3. second <int>
4. handover <int>
5. price <float>

- Adjust the price according to the split adjust factor

- Store the adjusted parquet data into app_data folder

- update the split adjust metadata json
"""

import json 
import os 

from data_source.postprocessing.utils import (
    save_record_dict_to_parquet, 
    load_parquet_to_dataframe
)

def load_

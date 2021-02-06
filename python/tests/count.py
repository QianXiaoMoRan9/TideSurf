import pandas as pd 
import pyarrow.parquet as pq 

COUNT_1 = 0
COUNT_2 = 0
CODE = 'sz000001'

df0 = pq.read_table('/home/steven/Desktop/Fast500/astock_parquet/2020-12-22/0.parquet').to_pandas()
df1 = pq.read_table('/home/steven/Desktop/Fast500/astock_parquet/2020-12-22/1.parquet').to_pandas()

for index, row in df0.iterrows():
    if row["code"] == CODE:
        COUNT_1 += 1

for index, row in df1.iterrows():
    if row["code"] == CODE:
        COUNT_2 += 1

print("part 0 {} part 1 {}".format(COUNT_1, COUNT_2))

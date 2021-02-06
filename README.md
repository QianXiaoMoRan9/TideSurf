# TideSurf


# database - data warehouse - mySQL

# cache - daily processing 
# UI -
# algo - 
# backtrace - 

# Sina A Stock Data

## Raw data folder structure
```
.
+-- 2020-12-21
|   +-- data
|      +-- stock_list_2020-12-21.json
|      +-- 2020-12-21_0-0.pkl
```

## Source data folder structure
```
.
+-- 2020-12-21
|   +-- stock_list.parquet
|   +-- split_share.parquet
|   +-- code_to_partition_map.json
|   +-- 001.parquet
|   +-- 002.parquet
|   +-- ...
+-- 2020-12-22
+-- ...
```

* Each day will be a separate folder
* In each day's folder, there are couple of partitions, each with 50 stocks
* The `code_to_partition_map.json` records the map from `stock code` to `parquet partition number` 

### code_to_partition_map.json
```json
{
    "000001": "001",
    "000002": "001",
    "600809": "005",
    ...
}
```


## App data folder structure
```
.
+-- astock
|   +-- stock_list.parquet
|   +-- stock_selection
|      +-- watch_list.json
|      +-- group_1.json
|      +-- ...
|   +-- record_data
|      +-- 1_min_volume
|         +-- 2020-12-21
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|            +-- ...
|      +-- 5_min_volume
|         +-- 2020-12-21
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|      +-- 15_min_volume
|         +-- 2020-12-21
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|      +-- 30_min_volume
|         +-- 2020-12-21
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|      +-- 60_min_volume
|         +-- 2020-12-21
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|         +-- ...
|      +-- MACD
|         +-- 2020-12-21
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|         +-- ...
```

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
+-- 2020-12-21/
|   +-- data/
|      +-- stock_list_2020-12-21.json
|      +-- 2020-12-21_0-0.pkl
```

## Source data folder structure
```
.
+-- 2020-12-21/
|   +-- stock_list.parquet
|   +-- split_adjust.parquet
|   +-- code_to_partition_map.json
|   +-- 001.parquet
|   +-- 002.parquet
|   +-- ...
+-- 2020-12-22/
+-- ...
```

* Each day will be a separate folder
* In each day's folder, there are couple of partitions, each with 50 stocks
* The `code_to_partition_map.json` records the map from `stock code` to `parquet partition number` 

### code_to_partition_map.json
```json
{
    "000001": "1",
    "000002": "1",
    "600809": "5",
    ...
}
```


## App data folder structure
```
.
+-- astock/
|   +-- log/
|      +-- python/
|         +-- 2020-12-23.log
|      +-- cpp/
|   +-- temp/
|      +-- 2020-12-23/
|         +-- data/
|            +-- stock_list.json
|            +-- split_adjust_factor.json
|   +-- stock_selection/
|      +-- watch_list.json
|      +-- group_1.json
|      +-- ...
|   +-- record_data/
|      +-- realtime_data/ (after split adjust)
|         +-- 2020-12-21/
|            +-- code_to_partition_map.json
|            +-- latest_adjust_record.json
|            +-- 1.parquet
|            +-- 2.parquet
|            +-- ...
|      +-- 1_min_volume/
|         +-- 2020-12-21/
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|            +-- ...
|      +-- 5_min_volume/
|         +-- 2020-12-21/
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|      +-- 15_min_volume/
|         +-- 2020-12-21/
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|      +-- 30_min_volume/
|         +-- 2020-12-21/
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|      +-- 60_min_volume/
|         +-- 2020-12-21/
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|         +-- ...
|      +-- MACD/
|         +-- 2020-12-21/
|            +-- code_to_partition_map.json
|            +-- 001.parquet
|            +-- 002.parquet
|         +-- ...
```

### source_data_folder/2021-02-03/split_adjust.parquet
```json
[
    {
        "code": "sz000002",
        "type": AssetType.STOCK / AssetType.FUND,
        "exchange": AStockExchange.SHANGHAI / AStockExchange.SHENZHEN
        "split_date": 2020-08-14
        "price_day_before_yesterday": 28.60
        "close_price_before_split": 27.58
        "split_day_cur_price": 27.68
        "split_day_percentage_increase": 0.3626
        "split_day_handover": 94094734,
        "split_day_volume": 2592380291.0
        "pre_split_adjust_factor": 0.96433566
        "post_split_adjust_factor": 1.03698332
    }
]
```

### astock/temp/split_adjust_factor_2020-12-23.json
```json
[
    [
        "000001",
        "中国平安",
        "zgpa"
    ],
    ...
]
```

### astock/record_data/realtime_data/2020-12-21/latest_adjust_record.json
```json
{
    "sz000001": "2020-12-21",
    ...
}
```
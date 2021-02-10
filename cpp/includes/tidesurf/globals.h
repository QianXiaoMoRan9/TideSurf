#pragma once
#include <arrow/api.h>
#include "tidesurf_types.h"

namespace tidesurf {

const ParquetTableSchemaVector SINA_A_STOCK_RECORD_PARQUET_TABLE_SCHEMA = {
    arrow::field("ask1", arrow::float64()),
    arrow::field("ask1_volume", arrow::int64()),
    arrow::field("ask2", arrow::float64()),
    arrow::field("ask2_volume", arrow::int64()),
    arrow::field("ask3", arrow::float64()),
    arrow::field("ask3_volume", arrow::int64()),
    arrow::field("ask4", arrow::float64()),
    arrow::field("ask4_volume", arrow::int64()),
    arrow::field("ask5", arrow::float64()),
    arrow::field("ask5_volume", arrow::int64()),
    arrow::field("bid1", arrow::float64()),
    arrow::field("bid1_volume", arrow::int64()),
    arrow::field("bid2", arrow::float64()),
    arrow::field("bid2_volume", arrow::int64()),
    arrow::field("bid3", arrow::float64()),
    arrow::field("bid3_volume", arrow::int64()),
    arrow::field("bid4", arrow::float64()),
    arrow::field("bid4_volume", arrow::int64()),
    arrow::field("bid5", arrow::float64()),
    arrow::field("bid5_volume", arrow::int64()),
    arrow::field("buy", arrow::float64()),
    arrow::field("close", arrow::float64()),
    arrow::field("high", arrow::float64()),
    arrow::field("low", arrow::float64()),
    arrow::field("now", arrow::float64()),
    arrow::field("open", arrow::float64()),
    arrow::field("sell", arrow::float64()),
    arrow::field("hour", arrow::int64()),
    arrow::field("minute", arrow::int64()),
    arrow::field("second", arrow::int64()),
    arrow::field("turnover", arrow::int64()),
    arrow::field("volume", arrow::float64()),
};

const  ParquetTableSchemaVector SINA_A_STOCK_LIST_PARQUET_TABLE_SCHEMA = {
    arrow::field("code", arrow::utf8()),
    arrow::field("name", arrow::utf8())
};


const  ParquetTableSchemaVector SINA_A_STOCK_SPLIT_SHARE_PARQUET_TABLE_SCHEMA = {
    arrow::field("code", arrow::utf8()),
    arrow::field("type", arrow::int64()),
    arrow::field("exchange", arrow::int64()),
    arrow::field("year", arrow::int64()),
    arrow::field("month", arrow::int64()),
    arrow::field("day", arrow::int64()),
    arrow::field("price_day_before_yesterday", arrow::float64()),
    arrow::field("close_price_before_split", arrow::float64()),
    arrow::field("split_day_cur_price", arrow::float64()),
    arrow::field("split_day_percentage_increase", arrow::float64()),
    arrow::field("split_day_handover", arrow::int64()),
    arrow::field("split_day_volume", arrow::float64()),
    arrow::field("pre_split_adjust_factor", arrow::float64()),
    arrow::field("post_split_adjust_factor", arrow::float64())
};

}

#pragma once
#include <arrow/api.h>
#include "tidesurf_types.h"

namespace tidesurf {

const ParquetTableSchemaVector STOCK_RECORD_PARQUET_TABLE_SCHEMA = {
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

const  ParquetTableSchemaVector STOCK_LIST_PARQUET_TABLE_SCHEMA = {
    arrow::field("code", arrow::utf8()),
    arrow::field("name", arrow::utf8()),
    arrow::field("abbreviation", arrow::utf8())
};


}

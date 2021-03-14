#pragma once

#include <arrow/api.h>
#include <vector>

namespace tidesurf
{
    using ParquetTableSchemaVector = std::vector<std::shared_ptr<arrow::Field>>;
    enum RecordPeriod {
        YEAR,
        MONTH,
        DAY,
        HOUR,
        MINUTE,
        SECOND
    };

    enum Sign {
        POSITIVE,
        NEGATIVE
    };

    enum IntervalType {
        MIN_1,
        MIN_5,
        MIN_10,
        MIN_15,
        MIN_20,
        MIN_30,
        HOUR_1,
        HOUR_3,
        DAY_1,
        DAY_3,
        DAY_5,
        DAY_10,
        MONTH_1,
        MONTH_3,
        MONTH_6,
        YEAR_1
    };
}

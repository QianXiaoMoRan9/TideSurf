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
}

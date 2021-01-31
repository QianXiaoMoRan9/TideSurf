#pragma once

#include <arrow/api.h>
#include <vector>

namespace tidesurf
{
    using ParquetTableSchemaVector = std::vector<std::shared_ptr<arrow::Field>>;
}

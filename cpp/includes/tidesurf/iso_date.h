#pragma once
#include <arrow/api.h>
#include "tidesurf/string_utils.h"

namespace tidesurf {


static const std::string DELIMITER = "-";

class ISODate {
    public:
    ISODate(const std::string date) {
    }

    private:
    int64_t year_;
    int64_t month_;
    int64_t day_;
};
}
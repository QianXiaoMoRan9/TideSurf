#pragma once
#include <arrow/api.h>
#include "tidesurf/string_utils.h"
#include <string>
#include <vector>

namespace tidesurf
{

    static const std::string DELIMITER = "-";

    class ISODate
    {
    public:
        ISODate(const std::string date);
        ISODate(int64_t year, int64_t month, int64_t day);
        int64_t GetYear() const;
        int64_t GetMonth() const;
        int64_t GetDay() const;

        ISODate operator+(const ISODate &rhs) const;
        ISODate operator-(const ISODate &rhs) const;
        bool operator==(const ISODate &rhs) const;
        bool operator!=(const ISODate &rhs) const;
        bool operator<(const ISODate &rhs) const;
        bool operator<=(const ISODate &rhs) const;
        bool operator>(const ISODate &rhs) const;
        bool operator>=(const ISODate &rhs) const;

        std::string ToString() const;

    private:
        int64_t year_;
        int64_t month_;
        int64_t day_;
    };
} // namespace tidesurf
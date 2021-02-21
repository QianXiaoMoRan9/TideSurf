#pragma once
#include <ctime>
#include <arrow/api.h>
#include "tidesurf/string_utils.h"
#include "tidesurf/tidesurf_macros.h"
#include <string>
#include <vector>

namespace tidesurf
{

    static const std::string DATE_DELIMITER = "-";
    static const std::string TIME_DELIMITER = ":";
    static const int64_t MONTH_DAY_MAP[] = {
        31,
        28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31};
    static const int64_t RUN_BASE_YEAR = 2020;
    static const int64_t RUN_YEAR_PERIOD = 4;

    class DeltaISODatetime
    {
    public:
        DeltaISODatetime::DeltaISODatetime() = default;
        DeltaISODatetime(int year, int month, int day, int hour, int minute, int second);

        int GetYear() const;
        int GetMonth() const;
        int GetDay() const;
        int GetHour() const;
        int GetMinute() const;
        int GetSecond() const;

        DeltaISODatetime operator+(const DeltaISODatetime &rhs) const;
        DeltaISODatetime operator-(const DeltaISODatetime &rhs) const;
        time_t ToTime_T() const;
        bool operator==(const DeltaISODatetime &rhs) const;
        bool operator!=(const DeltaISODatetime &rhs) const;
        bool operator<(const DeltaISODatetime &rhs) const;
        bool operator<=(const DeltaISODatetime &rhs) const;
        bool operator>(const DeltaISODatetime &rhs) const;
        bool operator>=(const DeltaISODatetime &rhs) const;
        std::string ToString() const;

    protected:
        int year_;
        int month_;
        int day_;
        int hour_;
        int minute_;
        int second_;
    };

    class ISODatetime : public DeltaISODatetime
    {
    public:
        ISODatetime(int year, int month, int day, int hour, int minute, int second);
        ISODatetime(time_t time);
        ISODatetime(struct tm *tm_struct);

        DeltaISODatetime operator+(const DeltaISODatetime &rhs) const;
        DeltaISODatetime operator-(const DeltaISODatetime &rhs) const;
        bool operator==(const ISODatetime &rhs) const;
        bool operator!=(const ISODatetime &rhs) const;
        bool operator<(const ISODatetime &rhs) const;
        bool operator<=(const ISODatetime &rhs) const;
        bool operator>(const ISODatetime &rhs) const;
        bool operator>=(const ISODatetime &rhs) const;
    };
} // namespace tidesurf
#pragma once
#include <arrow/api.h>
#include "tidesurf/string_utils.h"
#include <string>
#include <vector>

namespace tidesurf
{

    static const std::string DATE_DELIMITER = "-";
    static const std::string TIME_DELIMITER = ":";

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

    class ISOTime
    {
    public:
        ISOTime(const std::string time_string);
        ISOTime(int64_t hour, int64_t minute, int64_t second);

        int64_t GetHour() const;
        int64_t GetMinute() const;
        int64_t GetSecond() const;

        ISOTime operator+(const ISOTime &rhs) const;
        ISOTime operator-(const ISOTime &rhs) const;
        int64_t RetrieveOverFlowDay();
        bool operator==(const ISOTime &rhs) const;
        bool operator!=(const ISOTime &rhs) const;
        bool operator<(const ISOTime &rhs) const;
        bool operator<=(const ISOTime &rhs) const;
        bool operator>(const ISOTime &rhs) const;
        bool operator>=(const ISOTime &rhs) const;

        std::string ToString() const;

    private:
        int64_t hour_;
        int64_t minute_;
        int64_t second_;
    };

    class ISODatetime
    {
    public:
        ISODatetime(ISODate date, ISOTime time);
        ISODatetime(int64_t year, int64_t month, int64_t day, int64_t hour, int64_t minute, int64_t second);

        ISODate GetDate() const;
        ISOTime GetTime() const;

        ISODatetime operator+(const ISODatetime &rhs) const;
        ISODatetime operator-(const ISODatetime &rhs) const;
        bool operator==(const ISODatetime &rhs) const;
        bool operator!=(const ISODatetime &rhs) const;
        bool operator<(const ISODatetime &rhs) const;
        bool operator<=(const ISODatetime &rhs) const;
        bool operator>(const ISODatetime &rhs) const;
        bool operator>=(const ISODatetime &rhs) const;

    private:
        ISODate date_;
        ISOTime time_;
    };
} // namespace tidesurf
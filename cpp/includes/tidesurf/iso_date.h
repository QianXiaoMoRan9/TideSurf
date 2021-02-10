#pragma once
#include <arrow/api.h>
#include "tidesurf/string_utils.h"
#include <string>
#include <vector>

namespace tidesurf {


static const std::string DELIMITER = "-";

class ISODate {
    public:
    ISODate(const std::string date);
    ISODate(int64_t year, int64_t month, int64_t day);
    int64_t GetYear() const;
    int64_t GetMonth() const;
    int64_t GetDay() const;
    
    ISODate operator+(const ISODate rhs) const {
        return ISODate(
            GetYear() + rhs.GetYear(),
            GetMonth() + rhs.GetMonth(),
            GetDay() + rhs.GetDay()
        );
    }
    ISODate operator-(const ISODate rhs) const{
        return ISODate(
            GetYear() - rhs.GetYear(),
            GetMonth() - rhs.GetMonth(),
            GetDay() - rhs.GetDay()
        );
    }

    bool operator==(const ISODate rhs) const {
        return (
            GetYear() == rhs.GetYear()
            && GetMonth() == rhs.GetMonth()
            && GetDay() == rhs.GetDay()
        );
    }
    bool operator!=(const ISODate rhs) const {
        return ! ((*this) == rhs);
    }
    bool operator<(const ISODate rhs) const {
        if (GetYear() > rhs.GetYear()) {
            return false;
        } else if (GetYear() < rhs.GetYear()) {
            return true;
        }
        // year equal
        if (GetMonth() > rhs.GetMonth()) {
            return false;
        } else if (GetMonth() < rhs.GetMonth()) {
            return true;
        }
        // Month equal
        if (GetDay() > rhs.GetDay()) {
            return false;
        } else if (GetDay() < rhs.GetDay()) {
            return true;
        }
        return false;
    }
    bool operator<=(const ISODate rhs) const {
        return (*this) == rhs || (*this) < rhs;
    }
    bool operator>(const ISODate rhs) const {
        return ! ((*this) <= rhs);
    }
    bool operator>=(const ISODate rhs) const {
        return ! ((*this) < rhs);
    }

    std::string ToString() const;

    private:
    int64_t year_;
    int64_t month_;
    int64_t day_;
};
}
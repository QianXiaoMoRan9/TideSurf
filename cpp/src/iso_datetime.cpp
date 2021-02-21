#include <arrow/api.h>
#include "tidesurf/iso_datetime.h"
using namespace tidesurf;

DeltaISODatetime::DeltaISODatetime(int year, int month, int day, int hour, int minute, int second)
    : year_(year), month_(month), day_(day), hour_(hour), minute_(minute), second_(second)
{
}

int DeltaISODatetime::GetYear() const
{
    return year_;
}
int DeltaISODatetime::GetMonth() const
{
    return month_;
}
int DeltaISODatetime::GetDay() const
{
    return day_;
}
int DeltaISODatetime::GetHour() const
{
    return hour_;
}
int DeltaISODatetime::GetMinute() const
{
    return minute_;
}
int DeltaISODatetime::GetSecond() const
{
    return second_;
}

DeltaISODatetime DeltaISODatetime::operator+(const DeltaISODatetime &rhs) const
{
    return DeltaISODatetime(
        GetYear() + rhs.GetYear(),
        GetMonth() + rhs.GetMonth(),
        GetDay() + rhs.GetDay(),
        GetHour() + rhs.GetHour(),
        GetMinute() + rhs.GetMinute(),
        GetSecond() + rhs.GetSecond()
    );
}

DeltaISODatetime DeltaISODatetime::operator-(const DeltaISODatetime &rhs) const
{
    return DeltaISODatetime(
        GetYear() - rhs.GetYear(),
        GetMonth() - rhs.GetMonth(),
        GetDay() - rhs.GetDay(),
        GetHour() - rhs.GetHour(),
        GetMinute() - rhs.GetMinute(),
        GetSecond() - rhs.GetSecond()
    );
}

bool DeltaISODatetime::operator==(const DeltaISODatetime &rhs) const {
    return (
        GetYear() == rhs.GetYear()
        && GetMonth() == rhs.GetMonth()
        && GetDay() == rhs.GetDay()
        && GetHour() == rhs.GetHour()
        && GetMinute() == rhs.GetMinute()
        && GetSecond() == rhs.GetSecond()
    );
}

bool DeltaISODatetime::operator!=(const DeltaISODatetime &rhs) const
{
    return !(*this == rhs);
}

bool DeltaISODatetime::operator<(const DeltaISODatetime &rhs) const
{
    return (
        GetYear() < rhs.GetYear()
        || GetMonth() < rhs.GetMonth()
        || GetDay() < rhs.GetDay()
        || GetHour() < rhs.GetHour()
        || GetMinute() < rhs.GetMinute()
        || GetSecond() < rhs.GetSecond()
    );
}

bool DeltaISODatetime::operator<=(const DeltaISODatetime &rhs) const {
    return (*this == rhs) || (*this < rhs);
}

bool DeltaISODatetime::operator>(const DeltaISODatetime &rhs) const
{
    return !(*this <= rhs);
}
bool DeltaISODatetime::operator>=(const DeltaISODatetime &rhs) const
{
    return !(*this < rhs);
}
std::string DeltaISODatetime::ToString() const
{
    return (
        std::to_string(GetYear()) 
        + DATE_DELIMITER 
        + std::to_string(GetMonth()) 
        + DATE_DELIMITER 
        + std::to_string(GetDay()) 
        + " " 
        + std::to_string(GetHour()) 
        + TIME_DELIMITER 
        + std::to_string(GetMinute()) 
        + TIME_DELIMITER 
        + std::to_string(GetSecond())
    );
}

ISODatetime::ISODatetime(int year, int month, int day, int hour, int minute, int second)
: DeltaISODatetime(year, month, day, hour, minute, second)
{
    ASSERT(year >= 1900, "year should be at least 1900");
    ASSERT(month > 0 && month < 13, "month should between 0 and 12");
    ASSERT(day > 0 && month < 32, "day should between 1 and 31");
    ASSERT(hour >= 0 && hour < 24, "hour should betweem 0 and 23");
    ASSERT(minute >= 0 && minute < 60, "minute should between 0 and 59");
    ASSERT(second >=0 && second < 60, "second should between 0 and 59");
}
ISODatetime::ISODatetime(time_t time)
{
    struct tm* tm_struct = gmtime(&time);
    year_ = tm_struct->tm_year + 1900;
    month_ = tm_struct->tm_mon + 1;
    day_ = tm_struct->tm_mday;
    hour_ = tm_struct->tm_hour;
    minute_ = tm_struct->tm_min;
    second_ = tm_struct->tm_sec;
}

ISODatetime::ISODatetime(struct tm *tm_struct)
{
    year_ = tm_struct->tm_year + 1900;
    month_ = tm_struct->tm_mon + 1;
    day_ = tm_struct->tm_mday;
    hour_ = tm_struct->tm_hour;
    minute_ = tm_struct->tm_min;
    second_ = tm_struct->tm_sec;
}

DeltaISODatetime ISODatetime::operator+(const DeltaISODatetime &rhs) const
{
    int new_year = year_ + rhs.GetYear();
    int new_month = month_ + rhs.GetMonth();
    if (new_month > 12) {
        new_year ++;
        new_month -= 12;
    } else if (new_month <= 0)
    {
        new_year --;
        new_month = 12 - new_month;
    }

    struct tm tm_struct;
    tm_struct.tm_sec = second_;
    tm_struct.tm_min = minute_;
    tm_struct.tm_hour = hour_;
    tm_struct.tm_mday = day_;
    tm_struct.tm_mon = new_month - 1;
    tm_struct.tm_year = new_year - 1900;

    time_t converted_time_t = std::mktime(&tm_struct);

    int added_seconds = rhs.GetSecond() + rhs.GetMinute() * 60 + rhs.GetDay() * 60 * 60 * 24;
    converted_time_t += added_seconds;

    struct tm *new_tm = std::gmtime(&converted_time_t);
    return ISODatetime(new_tm);
}

DeltaISODatetime ISODatetime::operator-(const DeltaISODatetime &rhs) const
{
    return (*this + DeltaISODatetime(-1*rhs.GetYear(), -1*rhs.GetMonth(), -1*rhs.GetDay(), -1*rhs.GetHour(), -1*rhs.GetMinute(), -1*rhs.GetSecond()));
}



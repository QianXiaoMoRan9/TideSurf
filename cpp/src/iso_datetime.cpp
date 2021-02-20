#include <arrow/api.h>
#include "tidesurf/iso_datetime.h"

using namespace tidesurf;

ISODate::ISODate(const std::string date)
{
    std::vector<std::string> split = split_string(date, DATE_DELIMITER);
    year_ = std::stoi(split[0]);
    month_ = std::stoi(split[1]);
    day_ = std::stoi(split[2]);
}

ISODate::ISODate(int64_t year, int64_t month, int64_t day) : year_(year), month_(month), day_(day)
{
}

int64_t ISODate::GetYear() const
{
    return year_;
}

int64_t ISODate::GetMonth() const
{
    return month_;
}

int64_t ISODate::GetDay() const
{
    return day_;
}

ISODate ISODate::operator+(const ISODate &rhs) const
{
    return ISODate(
        GetYear() + rhs.GetYear(),
        GetMonth() + rhs.GetMonth(),
        GetDay() + rhs.GetDay());
}
ISODate ISODate::operator-(const ISODate &rhs) const
{
    return ISODate(
        GetYear() - rhs.GetYear(),
        GetMonth() - rhs.GetMonth(),
        GetDay() - rhs.GetDay());
}

bool ISODate::operator==(const ISODate &rhs) const
{
    return (
        GetYear() == rhs.GetYear() && GetMonth() == rhs.GetMonth() && GetDay() == rhs.GetDay());
}
bool ISODate::operator!=(const ISODate &rhs) const
{
    return !((*this) == rhs);
}
bool ISODate::operator<(const ISODate &rhs) const
{
    if (GetYear() > rhs.GetYear())
    {
        return false;
    }
    else if (GetYear() < rhs.GetYear())
    {
        return true;
    }
    // year equal
    if (GetMonth() > rhs.GetMonth())
    {
        return false;
    }
    else if (GetMonth() < rhs.GetMonth())
    {
        return true;
    }
    // Month equal
    if (GetDay() > rhs.GetDay())
    {
        return false;
    }
    else if (GetDay() < rhs.GetDay())
    {
        return true;
    }
    return false;
}
bool ISODate::operator<=(const ISODate &rhs) const
{
    return (*this) == rhs || (*this) < rhs;
}
bool ISODate::operator>(const ISODate &rhs) const
{
    return !((*this) <= rhs);
}
bool ISODate::operator>=(const ISODate &rhs) const
{
    return !((*this) < rhs);
}

std::string ISODate::ToString() const
{
    return std::to_string(GetYear()) + DATE_DELIMITER + std::to_string(GetMonth()) + DATE_DELIMITER + std::to_string(GetDay());
}

ISOTime::ISOTime(const std::string time_string)
{
    std::vector<std::string> split = split_string(time_string, TIME_DELIMITER);
    hour_ = std::stoi(split[0]);
    minute_ = std::stoi(split[1]);
    second_ = std::stoi(split[2]);
}
ISOTime::ISOTime(int64_t hour, int64_t minute, int64_t second) : hour_(hour),
                                                                 minute_(minute),
                                                                 second_(second)
{
}

int64_t ISOTime::GetHour() const
{
    return hour_;
}
int64_t ISOTime::GetMinute() const
{
    return minute_;
}
int64_t ISOTime::GetSecond() const
{
    return second_;
}

ISOTime ISOTime::operator+(const ISOTime &rhs) const
{
    int64_t plus_second = GetSecond() + rhs.GetSecond();
    int64_t second_overflow = plus_second / 60;
    int64_t result_second = plus_second % 60;
    int64_t plus_minute = GetMinute() + rhs.GetMinute() + second_overflow;
    int64_t minute_overflow = plus_minute / 60;
    int64_t new_minute = minute_overflow % 60;
    int64_t new_hour = GetHour() + rhs.GetHour() + minute_overflow;
    return ISOTime(new_hour, new_minute, result_second);
}

ISOTime ISOTime::operator-(const ISOTime &rhs) const
{
    int64_t minus_hour = GetHour() - rhs.GetHour();
    int64_t minus_minute = GetMinute() - rhs.GetMinute();

    int64_t minus_second = GetSecond() - rhs.GetSecond();
    if (minus_second < 0 && minus_minute > 0)
    {
        minus_second += 60;
        minus_minute -= 1;
    }
    else if (minus_second <= -60)
    {
        minus_minute -= 1;
        minus_second += 60;
    }
    else if (minus_second >= 60)
    {
        minus_second -= 60;
        minus_minute++;
    }
    if (minus_minute < 0 && minus_hour > 0)
    {
        minus_hour -= 1;
        minus_minute += 60;
    }
    else if (minus_minute <= -60)
    {
        minus_minute += 60;
        minus_hour -= 1;
    }
    else if (minus_minute >= 60)
    {
        minus_minute -= 60;
        minus_hour++;
    }
    return ISOTime(minus_hour, minus_minute, minus_second);
}
int64_t ISOTime::RetrieveOverFlowDay()
{
    if (GetHour() >= 24)
    {
        int64_t res = GetHour() / 24;
        hour_ = hour_ % 24;
        return res;
    }
    else if (GetHour() <= -24)
    {
        int64_t res = GetHour() / -24;
        hour_ = hour_ % -24;
        return res;
    }
    return 0;
}

bool ISOTime::operator==(const ISOTime &rhs) const
{
    return GetHour() == rhs.GetHour() && GetMinute() == rhs.GetMinute() && GetSecond() == rhs.GetMinute();
}
bool ISOTime::operator!=(const ISOTime &rhs) const
{
    return !((*this) == rhs);
}
bool ISOTime::operator<(const ISOTime &rhs) const
{
    return (
        GetHour() < rhs.GetHour() || GetMinute() < rhs.GetMinute() || GetSecond() < rhs.GetSecond());
}
bool ISOTime::operator<=(const ISOTime &rhs) const
{
    return (
        (*this < rhs) || (*this == rhs));
}
bool ISOTime::operator>(const ISOTime &rhs) const
{
    return !(*this <= rhs);
}
bool ISOTime::operator>=(const ISOTime &rhs) const
{
    return !(*this < rhs);
}

std::string ISOTime::ToString() const
{
    return std::to_string(GetHour()) + TIME_DELIMITER + std::to_string(GetMinute()) + TIME_DELIMITER + std::to_string(GetSecond());
}

ISODatetime::ISODatetime(ISODate date, ISOTime time) 
: date_(date), time_(time) {

}
ISODatetime::ISODatetime(int64_t year, int64_t month, int64_t day, int64_t hour, int64_t minute, int64_t second) 
: date_(year, month, day), time_(hour, minute, second)
{

}

ISODate ISODatetime::GetDate() const {
    return date_;
}
ISOTime ISODatetime::GetTime() const {
    return time_;
}

ISODatetime ISODatetime::operator+(const ISODatetime &rhs) const {
    ISOTime new_time = GetTime() + rhs.GetTime();
    ISODate new_date = GetDate() + rhs.GetDate();
    ISODate delta = ISODate(0, 0, new_time.RetrieveOverFlowDay());
    return ISODatetime(new_date + delta, new_time);
}
ISODatetime ISODatetime::operator-(const ISODatetime &rhs) const {
    ISOTime new_time = GetTime() + rhs.GetTime();
    ISODate new_date = GetDate() + rhs.GetDate();
    ISODate delta = ISODate(0, 0, new_time.RetrieveOverFlowDay());
    return ISODatetime(new_date + delta, new_time);
}
bool ISODatetime::operator==(const ISODatetime &rhs) const {
    return GetDate() == rhs.GetDate() && GetTime() == rhs.GetTime();
}
bool ISODatetime::operator!=(const ISODatetime &rhs) const {
    return !(*this == rhs);
}
bool ISODatetime::operator<(const ISODatetime &rhs) const {
    return (this->GetDate() < rhs.GetDate() || this->GetTime() < rhs.GetTime());
}
bool ISODatetime::operator<=(const ISODatetime &rhs) const {
    return (*this < rhs || *this == rhs);
}
bool ISODatetime::operator>(const ISODatetime &rhs) const {
    return !(*this <= rhs);
}
bool ISODatetime::operator>=(const ISODatetime &rhs) const {
    return !(*this < rhs);
}

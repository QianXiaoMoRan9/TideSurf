#include "tidesurf/iso_date.h"

using namespace tidesurf;

ISODate::ISODate(const std::string date)
{
    std::vector<std::string> split = split_string(date, DELIMITER);
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
    return std::to_string(GetYear()) + "-" + std::to_string(GetMonth()) + "-" + std::to_string(GetDay());
}

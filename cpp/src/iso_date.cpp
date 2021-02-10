#include "tidesurf/iso_date.h"

using namespace tidesurf;

ISODate::ISODate(const std::string date) {
    std::vector<std::string> split = split_string(date, DELIMITER);
    year_ = std::stoi(split[0]);
    month_ = std::stoi(split[1]);
    day_ = std::stoi(split[2]);
}

ISODate::ISODate(int64_t year, int64_t month, int64_t day) : year_(year), month_(month), day_(day) {
}

int64_t ISODate::GetYear() const {
    return year_;
}

int64_t ISODate::GetMonth() const {
    return month_;
}

int64_t ISODate::GetDay() const {
    return day_;
}

std::string ISODate::ToString() const {
    return std::to_string(GetYear()) + "-" + std::to_string(GetMonth()) + "-" + std::to_string(GetDay());
}




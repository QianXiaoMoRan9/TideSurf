#include "tidesurf/string_utils.h"

using namespace tidesurf;

std::vector<std::string> tidesurf::split_string(const std::string s, const std::string delimiter)
{
    std::vector<std::string> result;
    size_t start = 0;
    size_t end = s.find(delimiter);
    while (end != std::string::npos)
    {
        result.push_back(s.substr(start, end - start));
        start = end + delimiter.length();
        end = s.find(delimiter, start);
    }
    result.push_back(s.substr(start, end));
    return result;
}
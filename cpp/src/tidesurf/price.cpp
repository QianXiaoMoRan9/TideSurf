#include "tidesurf/price.h"
#include <iostream>

using namespace tidesurf;

Price::Price(const double f_value, const uint32_t precision) {
    if (f_value >= 0) {
        sign_ = POSITIVE;
    } else {
        sign_ = NEGATIVE;
    }

    precision_ = precision;
    const auto multiplier = (double) precision_;

    const auto mult = (uint32_t) round(f_value * multiplier);
    int_part_ = mult / precision;
    float_part_ = mult % precision;
}

Price::Price(uint32_t int_part, uint32_t float_part, Sign sign, uint32_t precision)
        : int_part_(int_part), float_part_(float_part), sign_(sign), precision_(precision) {
    ASSERT(float_part >= 0, "Float Part should be non-negative");
    ASSERT(float_part < precision, "Float part should not exceed precision");
}

std::string Price::ToString() const {
    std::string res;
    if (sign_) {
        res.append("-");
    }
    res.append(std::to_string(int_part_));
    res.append(".");
    uint32_t num_zeros = GetNumFloatDigitPrecision();
    std::string float_string = std::to_string(float_part_);
    num_zeros -= float_string.length();
    for (uint32_t i = 0; i < num_zeros; i++) {
        res.append("0");
    }

    res.append(float_string);
    return res;
}


TwoDecimalPrice::TwoDecimalPrice(const double f_value) : Price(f_value, 100) {
}

TwoDecimalPrice::TwoDecimalPrice(uint32_t int_part, uint32_t float_part, Sign sign) : Price(int_part, float_part, sign,
                                                                                            100) {
}

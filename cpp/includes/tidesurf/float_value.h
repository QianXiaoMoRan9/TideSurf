#pragma once

#include <cstdint>
#include <cmath>
#include "math_util.h"

namespace tidesurf {

/**
 * @brief define the positive floating point value of the 
 * 
 */
class FloatValue {
public:
    FloatValue(float f_value, uint8_t precision = 2) {
        if (f_value >= 0) {
            sign_ = false;
        } else {
            sign_ = true;
        }
        
        precision_ = power(10, precision);
        float multiplier = (float) precision_;
        precision_ = precision;
        float int_part_float = floor(f_value);
        float float_part_float = floor((f_value - int_part_float) * multiplier);
        int_part_ = (uint32_t) int_part_float;
        float_part_ = (uint32_t) float_part_float;
    }

    FloatValue(uint32_t int_part, uint32_t float_part, bool sign, uint8_t precision = 2) {
        int_part_ = int_part;
        float_part_ = float_part;
        sign_ = sign;
        precision_ = power(10, precision);
    }

    uint32_t GetIntPart() {
        return int_part_; 
    }

    uint32_t GetFloatPart() {
        return float_part_;
    }
    
    bool Positive() {
        return ! sign_;
    }

    bool Negative() {
        return sign_;
    }

private:
    bool sign_; // false is positive, true is negative
    uint32_t precision_;
    uint32_t int_part_;
    uint32_t float_part_;

};

} // namespace TideSurf

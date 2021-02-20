#pragma once

#include <cstdint>
#include <cmath>
#include <arrow/api.h>
#include "tidesurf/math_util.h"
#include "tidesurf/tidesurf_types.h"
#include "tidesurf/tidesurf_macros.h"

namespace tidesurf {

/**
 * @brief define the positive floating point value of the 
 * 
 */
class Price {
public:
    Price(float f_value, uint32_t precision = 100) {
        if (f_value >= 0) {
            sign_ = POSITIVE;
        } else {
            sign_ = NEGATIVE;
        }
        
        precision_ = precision;
        float multiplier = (float) precision_;
        precision_ = precision;
        float int_part_float = round(f_value);
        float float_part_float = round((f_value - int_part_float) * multiplier);
        int_part_ = (int64_t) int_part_float;
        float_part_ = (int64_t) float_part_float;
    }

    Price(int64_t int_part, int64_t float_part, Sign sign, uint32_t precision = 100) {
        ASSERT(float_part >= 0, "Float Part should be non-negative");
        ASSERT(float_part < precision, "Float part should not exceed precision");

        int_part_ = int_part;
        float_part_ = float_part;
        sign_ = sign;
        precision_ = precision;
    }

    int64_t GetIntPart() {
        return int_part_; 
    }

    int64_t GetFloatPart() {
        return float_part_;
    }

    uint32_t GetNumFloatDigitPrecision() {
        return num_10th(precision_);
    }
    
    bool Positive() {
        return ! sign_;
    }

    bool Negative() {
        return sign_;
    }

private:
    Sign sign_; // false is positive, true is negative
    uint32_t precision_;
    int64_t int_part_;
    int64_t float_part_;

};

} // namespace TideSurf

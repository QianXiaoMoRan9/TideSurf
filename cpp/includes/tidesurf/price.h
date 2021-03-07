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
    Price(float f_value, uint32_t precision);

    Price(int64_t int_part, int64_t float_part, Sign sign, uint32_t precision);
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

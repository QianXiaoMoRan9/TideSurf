#pragma once
#include <iostream>
#include <cstdint>
#include <cmath>
#include <arrow/api.h>
#include "tidesurf/math_util.h"
#include "tidesurf/tidesurf_types.h"
#include "tidesurf/tidesurf_macros.h"

namespace tidesurf
{

    /**
 * @brief define the positive floating point value of the 
 * 
 */
    class Price
    {


    public:
        Price(double f_value, uint32_t precision);

        Price(uint32_t int_part, uint32_t float_part, Sign sign, uint32_t precision);
        uint32_t GetIntPart() const
        {
            return int_part_;
        }

        uint32_t GetFloatPart() const
        {
            return float_part_;
        }

        uint32_t GetNumFloatDigitPrecision() const
        {
            return num_10th(precision_);
        }

        bool Positive()
        {
            return !sign_;
        }

        bool Negative()
        {
            return sign_;
        }

        std::string ToString() const;

        double ToDouble() const;

        friend std::ostream &operator<<(std::ostream &os, const Price &price) {
            const std::string str = price.ToString();
            os << str;
            return os;
        }

    private:
        Sign sign_; // false is positive, true is negative
        uint32_t precision_;
        uint32_t int_part_;
        uint32_t float_part_;
    };

    class TwoDecimalPrice : public Price
    {

    public:
        explicit TwoDecimalPrice(double f_value);

        TwoDecimalPrice(uint32_t int_part, uint32_t float_part, Sign sign);
    };

} // namespace TideSurf

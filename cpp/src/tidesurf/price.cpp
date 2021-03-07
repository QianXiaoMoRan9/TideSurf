#include "tidesurf/price.h"

using namespace tidesurf;

Price::Price(float f_value, uint32_t precision)
{
    if (f_value >= 0)
    {
        sign_ = POSITIVE;
    }
    else
    {
        sign_ = NEGATIVE;
    }

    precision_ = precision;
    float multiplier = (float)precision_;
    precision_ = precision;
    float int_part_float = round(f_value);
    float float_part_float = round((f_value - int_part_float) * multiplier);
    int_part_ = (int64_t)int_part_float;
    float_part_ = (int64_t)float_part_float;
}

Price::Price(int64_t int_part, int64_t float_part, Sign sign, uint32_t precision)
{
    ASSERT(float_part >= 0, "Float Part should be non-negative");
    ASSERT(float_part < precision, "Float part should not exceed precision");

    int_part_ = int_part;
    float_part_ = float_part;
    sign_ = sign;
    precision_ = precision;
}
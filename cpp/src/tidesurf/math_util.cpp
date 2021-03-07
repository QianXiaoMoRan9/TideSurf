#include "tidesurf/math_util.h"

using namespace tidesurf;

uint32_t power(uint32_t base, uint32_t exp) {
    int result = 1;
    while (exp > 0) {
        if (exp & 1) {
            result *= base;
        }
        exp >>= 1;
        base *= base;
    }
    return result;
}

uint32_t num_10th(int64_t num) {
    uint32_t result = 0;
    ASSERT(num != 0xFFFFFFFFFFFFFFFF, "num_10th does not support value 0xFFFFFFFFFFFFFFFF");
    if (num < 0) {
        num = -1 * num;
    }
    while(num >= 10) {
        result ++;
        num /= 10;
    }
    return result;
}

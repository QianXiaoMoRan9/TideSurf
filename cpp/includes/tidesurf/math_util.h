#pragma once
#include <cstdint>
namespace tidesurf {

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

}



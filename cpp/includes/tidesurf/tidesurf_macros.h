#pragma once

#include <cassert>
#include <stdexcept>

#ifdef NDEBUG
#define DEBUG_ASSERT(expr, message) ((void)0)
#else
/*
 * On assert failure, most existing implementations of C++ will print out the condition.
 * By ANDing the truthy not-null message and our initial expression together, we get
 * asserts-with-messages without needing to bring in iostream or logging.
 */
#define DEBUG_ASSERT(expr, message) assert((expr) && (message))
#endif /* NDEBUG */

#define ASSERT(expr, message) assert((expr) && (message))

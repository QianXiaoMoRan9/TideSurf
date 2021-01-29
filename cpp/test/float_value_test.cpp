#include <gtest/gtest.h>
#include "float_value.h"

using namespace TideSurf;

class FloatValueTest : public ::testing::Test
{
};

TEST_F(FloatValueTest, BasicTest) {
    FloatValue *value = new FloatValue(32.56);
    EXPECT_EQ(value->GetFloatPart(), 56);
    EXPECT_EQ(value->GetIntPart(), 32);
}

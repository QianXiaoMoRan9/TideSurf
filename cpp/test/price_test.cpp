#include <gtest/gtest.h>
#include "tidesurf/price.h"

using namespace tidesurf;

class PriceTest : public ::testing::Test
{
};

TEST_F(PriceTest, BasicTest) {
    Price *value = new Price(32.56, 100);
    EXPECT_EQ(value->GetFloatPart(), 56);
    EXPECT_EQ(value->GetIntPart(), 32);
}

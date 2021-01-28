#include <gtest/gtest.h>

class FloatValueTest : public ::testing::Test
{
};

TEST_F(FloatValueTest, BasicTest) {
    EXPECT_EQ(1, 1);
}

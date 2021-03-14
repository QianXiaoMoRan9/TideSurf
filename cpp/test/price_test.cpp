#include <gtest/gtest.h>
#include "tidesurf/price.h"

using namespace tidesurf;

class PriceTest : public ::testing::Test
{
};

TEST_F(PriceTest, BasicTest) {
    auto *value = new Price(32.56, 100);
    EXPECT_EQ(value->GetFloatPart(), 56);
    EXPECT_EQ(value->GetIntPart(), 32);
}

TEST_F(PriceTest, BasicTest1) {
    auto *value = new Price(100.68, 100);
    EXPECT_EQ(value->GetIntPart(), 100);
    EXPECT_EQ(value->GetFloatPart(), 68);
}


TEST_F(PriceTest, BasicTest2) {
    auto *value = new Price(2047.86, 100);
    EXPECT_EQ(value->GetIntPart(), 2047);
    EXPECT_EQ(value->GetFloatPart(), 86);
}


TEST_F(PriceTest, BasicTest3) {
    Price *value = new Price(586.745, 1000);
    EXPECT_EQ(value->GetIntPart(), 586);
    EXPECT_EQ(value->GetFloatPart(), 745);
}


TEST_F(PriceTest, BasicTest4) {
    auto *value = new Price(312.5657, 10000);
    EXPECT_EQ(value->GetIntPart(), 312);
    EXPECT_EQ(value->GetFloatPart(), 5657);
}


TEST_F(PriceTest, BasicTest5) {
    auto *value = new Price(2.81, 100);
    EXPECT_EQ(value->GetIntPart(), 2);
    EXPECT_EQ(value->GetFloatPart(), 81);
}


TEST_F(PriceTest, BasicTest6) {
    auto *value = new Price(0.123, 1000);
    EXPECT_EQ(value->GetIntPart(), 0);
    EXPECT_EQ(value->GetFloatPart(), 123);
}


TEST_F(PriceTest, BasicTest7) {
    auto *value = new Price(137.58698, 100000);
    EXPECT_EQ(value->GetIntPart(), 137);
    EXPECT_EQ(value->GetFloatPart(), 58698);
}


TEST_F(PriceTest, BasicTest8) {
    auto *value = new Price(12.78, 100);
    EXPECT_EQ(value->GetIntPart(), 12);
    EXPECT_EQ(value->GetFloatPart(), 78);
}


TEST_F(PriceTest, BasicTest9) {
    auto *value = new Price(45876.2, 10);
    EXPECT_EQ(value->GetIntPart(), 45876);
    EXPECT_EQ(value->GetFloatPart(), 2);
}


#include <gtest/gtest.h>
#include "tidesurf/string_utils.h"
#include <string>
#include <vector>

using namespace tidesurf;

class StringUtilsTest : public ::testing::Test
{
};

TEST_F(StringUtilsTest, StringSplitNaive) {
    const std::string s = "return";
    const std::string delimiter = ".";

    std::vector<std::string> res = split_string(s, delimiter);
    EXPECT_EQ(res.size(), 1);
    EXPECT_EQ(res[0], "return");
}

TEST_F(StringUtilsTest, StringSplitNaiveTwoVal) {
    std::string s = "return.4";
    std::string delimiter = ".";

    std::vector<std::string> res = split_string(s, delimiter);
    EXPECT_EQ(res.size(), 2);
    EXPECT_EQ(res[0], "return");
    EXPECT_EQ(res[1], "4");
}

TEST_F(StringUtilsTest, StringSplitEmpty) {
    std::string s = "";
    std::string delimiter = ".";

    std::vector<std::string> res = split_string(s, delimiter);
    EXPECT_EQ(res.size(), 1);
    EXPECT_EQ(res[0], "");
}

TEST_F(StringUtilsTest, StringSplitISODate) {
    std::string s = "2020-12-23";
    std::string delimiter = "-";

    std::vector<std::string> res = split_string(s, delimiter);
    EXPECT_EQ(res.size(), 3);
    EXPECT_EQ(res[0], "2020");
    EXPECT_EQ(res[1], "12");
    EXPECT_EQ(res[2], "23");
}

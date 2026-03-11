#include <gtest/gtest.h>
#include "charge_port/utils.hpp"

TEST(UtilsTest, CommandValidation) {
    EXPECT_TRUE(charge_port::utils::is_valid_command("start"));
    EXPECT_TRUE(charge_port::utils::is_valid_command("stop"));
    EXPECT_TRUE(charge_port::utils::is_valid_command("reset"));
    EXPECT_TRUE(charge_port::utils::is_valid_command("status"));
    
    EXPECT_FALSE(charge_port::utils::is_valid_command("unknown"));
    EXPECT_FALSE(charge_port::utils::is_valid_command(""));
    EXPECT_FALSE(charge_port::utils::is_valid_command("Start")); // Case sensitive check
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

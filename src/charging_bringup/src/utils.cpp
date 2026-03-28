#include "charge_port/utils.hpp"
#include <vector>
#include <algorithm>

namespace charge_port {
namespace utils {

bool is_valid_command(const std::string& command) {
    const std::vector<std::string> valid_commands = {"start", "stop", "reset", "status"};
    return std::find(valid_commands.begin(), valid_commands.end(), command) != valid_commands.end();
}

} // namespace utils
} // namespace charge_port

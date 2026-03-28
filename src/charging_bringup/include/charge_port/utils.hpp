#ifndef CHARGE_PORT__UTILS_HPP_
#define CHARGE_PORT__UTILS_HPP_

#include <string>

namespace charge_port {
namespace utils {

/**
 * @brief Validates if a charging command is supported.
 * @param command The command string to validate.
 * @return true if valid, false otherwise.
 */
bool is_valid_command(const std::string& command);

} // namespace utils
} // namespace charge_port

#endif // CHARGE_PORT__UTILS_HPP_

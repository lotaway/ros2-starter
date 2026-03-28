# ChargingStatus.msg
std_msgs/Header header

# State
string current_state      # idle, searching, approaching, pre_align, inserting, connected, error
uint8 error_code          # 0: None, 1: Perception Lost, 2: IK Solver Failed, 3: Collision, 4: Hardware Fault

# Perception
bool is_detected
float32 confidence
string port_type          # fast, slow
int32 parking_spot_id

# Pose (relative to camera_link)
geometry_msgs/Pose target_pose

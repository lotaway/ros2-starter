# ROS2 示例项目

这是一个 ROS2 Humble 示例项目，包含 **Topic（主题）**、**Service（服务）** 和 **Action（动作）** 三种通讯方式。

## 项目结构

```
ros2-starter/
├── scripts/
│   ├── py_listener.py                  # Topic 订阅者 (Python)
│   ├── py_add_two_ints_client.py       # Service 客户端 (Python)
│   └── py_fibonacci_action_client.py   # Action 客户端 (Python)
└── src/
    ├── cpp_talker.cpp                   # Topic 发布者 (C++)
    ├── cpp_add_two_ints_server.cpp      # Service 服务器 (C++)
    ├── cpp_add_two_ints_client.cpp      # Service 客户端 (C++)
    ├── cpp_fibonacci_action_server.cpp  # Action 服务器 (C++)
    └── cpp_fibonacci_action_client.cpp  # Action 客户端 (C++)
```

---

## 1. Topic 通讯（发布/订阅）

### 运行命令（两个终端）：

```bash
# 终端 1 - C++ 发布者
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run ros2-starter cpp_talker

# 终端 2 - Python 订阅者
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run ros2-starter py_listener.py
```

**输出示例：**
- 发布者：`发布: 'C++ says hello #0'`
- 订阅者：`收到: "C++ says hello #0"`

---

## 2. Service 通讯（请求/响应）

### 运行命令（两个终端）：

```bash
# 终端 1 - Service 服务器
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run ros2-starter cpp_add_two_ints_server

# 终端 2 - Service 客户端
source /opt/ros/humble/setup.bash
source install/setup.bash

# C++ 客户端
ros2 run ros2-starter cpp_add_two_ints_client 5 3

# 或 Python 客户端
ros2 run ros2-starter py_add_two_ints_client.py 5 3
```

**输出示例：**
- 服务器：`收到请求: 5 + 3 = 8`
- 客户端：`结果: 5 + 3 = 8`

---

## 3. Action 通讯（异步、带反馈）

### 运行命令（两个终端）：

```bash
# 终端 1 - Action 服务器
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run ros2-starter cpp_fibonacci_action_server

# 终端 2 - Action 客户端
source /opt/ros/humble/setup.bash
source install/setup.bash

# C++ 客户端
ros2 run ros2-starter cpp_fibonacci_action_client

# 或 Python 客户端
ros2 run ros2-starter py_fibonacci_action_client.py
```

**输出示例：**
- 客户端发送目标：`发送目标: order=10`
- 客户端（目标被接受）：`目标已被接受`
- 服务器（反馈）：`发布反馈: 1`, `发布反馈: 2`, `发布反馈: 3`, ...
- 客户端（反馈）：`下一组数字: 0 1 1 2 3 ...`
- 客户端（最终结果）：`最终结果: 0 1 1 2 3 5 8 13 21 34 55`

---

## 编译项目

```bash
cd /root/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

---

## 三种通讯方式对比

| 通讯类型 | 特点 | 适用场景 |
|---------|------|---------|
| **Topic** | 异步、单向、持续数据流 | 传感器数据、状态更新 |
| **Service** | 同步、双向、请求-响应 | 一次性查询、触发操作 |
| **Action** | 异步、双向、带反馈 | 长时间运行任务 |


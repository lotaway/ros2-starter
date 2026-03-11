ROS 2 完全支持自动化测试，而且官方在构建系统里已经集成了一整套测试框架，可以覆盖：

单元测试（Unit Test）

集成测试（Integration Test）

系统测试（System Test）

回归测试（Regression Test）

这些通常通过 colcon + ament 体系运行。

一、ROS2 自动化测试整体架构

ROS2测试体系核心组件：

colcon test
   │
   ├─ ament_cmake
   │    ├─ gtest (C++)
   │    └─ pytest (Python)
   │
   ├─ launch_testing
   │    └─ 多节点集成测试
   │
   └─ ros2test

常见组合：

测试类型	工具
C++ 单元测试	gtest
Python 单元测试	pytest
节点集成测试	launch_testing
系统级测试	launch_testing + rosbag
二、C++ 单元测试

ROS2 默认使用 Google Test。

目录结构
my_pkg
 ├─ src
 │   └─ math.cpp
 ├─ test
 │   └─ test_math.cpp
 └─ CMakeLists.txt
示例

test_math.cpp

#include <gtest/gtest.h>

TEST(MathTest, Add)
{
    EXPECT_EQ(1 + 1, 2)
}

CMakeLists.txt

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)

  ament_add_gtest(test_math test/test_math.cpp)
endif()
三、Python 单元测试

Python包通常使用 pytest。

示例
test/test_node.py
def test_add():
    assert 1 + 1 == 2

package.xml

<test_depend>pytest</test_depend>
四、ROS2 节点集成测试

ROS2有专门的测试工具：

launch_testing

可以：

启动多个 ROS node

发布 / 订阅 topic

验证消息

测试 service / action

示例
test/test_talker_listener.py
import launch
import launch_testing
import pytest

@pytest.mark.launch_test
def generate_test_description():

    talker = launch_ros.actions.Node(
        package='demo_nodes_cpp',
        executable='talker'
    )

    listener = launch_ros.actions.Node(
        package='demo_nodes_cpp',
        executable='listener'
    )

    return (
        launch.LaunchDescription([
            talker,
            listener,
            launch_testing.actions.ReadyToTest()
        ]),
        {}
    )

可以验证：

topic 是否发送

node 是否启动

node 是否崩溃

五、完整自动化测试执行

ROS2统一使用：

colcon test

运行所有测试。

查看结果：

colcon test-result --verbose

CI环境常用：

colcon build
colcon test
colcon test-result
六、机器人项目常见测试层级

实际机器人项目一般是：

1 单元测试
   算法 / math / planner

2 节点测试
   单个 node

3 集成测试
   多 node + topic

4 仿真测试
   Gazebo 环境

例如：

控制算法

感知模块

SLAM模块

navigation

都可以单独测试。

七、仿真环境测试

ROS2通常结合：

Gazebo

rosbag

launch_testing

测试流程：

launch gazebo
launch robot
执行任务
验证topic输出

例如验证：

robot是否到达目标

是否避障

控制是否稳定

八、CI自动测试（非常常见）

ROS2项目通常在 CI 里跑：

GitHub Actions

GitLab CI

CI脚本通常：

colcon build
colcon test
colcon test-result

如果失败：

CI直接阻止 merge。

九、真实机器人公司测试架构（典型）

大型机器人项目通常是：

tests/
   unit/
   integration/
   simulation/
   hardware/

例如：

unit
   planner_test.cpp

integration
   navigation_stack_test.py

simulation
   gazebo_navigation_test.py

hardware
   real_robot_smoke_test.py
十、结论

ROS2 的自动化测试能力是官方支持并且非常完善的：

支持：

单元测试（gtest / pytest）

多节点集成测试（launch_testing）

仿真测试（Gazebo）

CI 自动测试（colcon test）
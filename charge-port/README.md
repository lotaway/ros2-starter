# Charge Port Detection & Control System

## 🎯 项目目标 (Project Goals)

本系统针对大型停车场内部的充电站上千个车位设计，旨在通过智能化手段解决非充电车辆占用充电位的问题：

- **精准识别**: 自动寻找并识别电动车充电口。
- **违停判定**: 利用视觉识别技术，自动判断非充电车辆（油车或不充电电车）长时间占位行为。
- **软性执法**: 
    - 自动计算占位费。
    - 将数据推送至物业道闸系统，实现出场时代收。
- **全流程自动化**: **识别车牌 -> 比对充电状态 -> 判定违停 -> 计算费用 -> 推送道闸 -> 留存证据**。

---

## 🌟 核心功能

- **双模型协同检测**: 
    - 车辆检测/跟踪 (YOLOv8n) 判定车位占用。
    - 专用充电口检测模型 (Custom YOLOv8) 识别电动车类型。
- **C++ 硬件控制层**:
    - 实时摄像头流采集与发布 (`sensor_msgs/Image`)。
    - 充电桩硬件指令下发接口 (支持扩展串口/CAN 控制)。
- **Python AI 推理层**:
    - 订阅图像流进行实时目标检测。
    - 自动判断“占位”行为并生成状态汇总。
- **自定义消息接口**: 使用 `charge_port/msg/ChargingStatus` 传递结构化检测数据。

## 📁 目录结构

```text
charge-port/
├── CMakeLists.txt              # 跨语言混合编译配置
├── package.xml                 # ROS2 包定义
├── msg/                        # 自定义 ROS2 消息 (ChargingStatus.msg)
├── include/                    # C++ 头文件 (硬件控制骨架)
├── src/                        # C++ 源代码 (硬件驱动 & 图像采集)
├── scripts/                    # Python 源代码 (AI 推理 & 训练)
│   ├── detection_node.py       # 推理节点
│   └── train_charging.py       # 训练脚本
├── test/                       # 自动化测试 (GTest, Pytest, Integration)
├── config/                     # 停车位 ROI 区域配置文件
└── dataset/                    # YOLO 训练数据集结构 (含配置文件)
```

## 🚀 部署与运行

### 1. 环境准备
确保已安装 ROS2 (Humble 或更高版本) 及相关依赖。

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 ROS2 依赖 (在工作空间根目录)
rosdep install --from-paths src --ignore-src -r -y
```

### 2. 编译
在 ROS2 工作空间根目录下执行：

```powershell
colcon build --packages-select charge_port
# 激活环境
.\install\setup.ps1
```

### 3. 运行系统

**启动硬件/图像采集节点 (C++):**
```powershell
ros2 run charge_port hardware_node --ros-args -p camera_id:=0
```

**启动 AI 检测推理节点 (Python):**
```powershell
ros2 run charge_port detection_node.py
```

### 4. 训练模型 (可选)
如果您需要重新训练针对特定场景的探测器：
1. 将标注好的图片放入 `dataset/train/images` 和 `labels`。
2. 运行训练脚本：
```powershell
python ./scripts/train_charging.py
```

## 🧪 自动化测试 (Automated Testing)

项目遵循 ROS 2 标准化测试流程，包含单元测试、逻辑测试与集成测试。

### 1. 运行测试
在工作空间根目录下执行：

```bash
# 编译并运行所有测试
colcon test --packages-select charge_port

# 查看测试结果汇总
colcon test-result --verbose
```

### 2. 测试覆盖范围
- **C++ 单元测试 (GTest)**: 验证核心控制逻辑与命令校验 (`test/test_utils.cpp`)。
- **Python 逻辑测试 (Pytest)**: 验证检测算法数据处理与配置解析 (`test/test_detection.py`)。
- **集成测试 (Launch Testing)**: 模拟多节点启动环境，验证节点生命周期与通信链路 (`test/test_integration.py`)。

---

## 🛠️ 硬件扩展说明

- **摄像头**: 在 `hardware_node` 中通过 `camera_id` 参数切换。
- **充电桩控制**: 
    - 修改 `src/hardware_node.cpp` 中的 `control_charging_pile` 函数。
    - 建议使用 `libserial` 或 `SocketCAN` 进行实际硬件通信。

## 📝 需求背景
本项目针对大型停车场内部的充电站，通过视觉技术自动计算非充电车辆的占位费，并与物业系统对接实现无人值守管理。

# 微分 Skill 组 - 基础架构和约定

**版本**: 1.0
**更新日期**: 2026-02-28

---

## 核心理念

### 什么是微分 Skill？
微分 Skill 是对**任意复杂问题进行微分拆解**（Differential Decomposition）的元级工具，将复杂目标拆分为：
- **变量**（Variables）：影响结果的参数
- **变化量**（Deltas）：变量的微小变化
- **关系**（Relationships）：变量之间的依赖关系
- **边界条件**（Boundaries）：变量的取值范围
- **约束条件**（Constraints）：必须满足的限制
- **优化目标**（Optimization Goals）：最大化或最小化的目标函数
- **求解策略**（Solution Strategies）：寻找最优解的方法

**应用领域**：
- 代码领域（Flutter 蓝牙实现、RSSI 图表、状态管理）
- 逻辑/数学问题（算法、数据结构、概率问题）
- 物理/工程问题（电路、力学、热力学）
- 商业问题（定价、库存、调度）
- 游戏问题（数值平衡、经济系统）

---

## 核心组件

### 1. 参考文件夹系统
```
references/
├── micro-diff-cases/           # 微分拆解案例
│   ├── bluetooth/            # 蓝牙相关
│   ├── rssi-chart/           # RSSI 图表
│   ├── state-management/      # 状态管理
│   ├── algorithm/             # 算法问题
│   ├── probability/          # 概率问题
│   └── optimization/          # 优化问题
├── formulas/               # 微分公式库
├── constraints/             # 边界条件
├── strategies/             # 求解策略
└── meta.json              # 元数据和索引
```

### 2. 微分拆解引擎
```
micro-diff-engine/
├── analyzer/              # 分析器
│   ├── variable_extractor.py  # 变量提取
│   ├── relationship_finder.py   # 关系发现
│   ├── constraint_detector.py # 约束检测
│   └── strategy_selector.py   # 策略选择
├── solver/               # 求解器
│   ├── incremental_solver.py # 增量求解器
│   ├── optimization_solver.py # 优化求解器
│   └── formula_validator.py   # 公式验证
└── visualizer/          # 可视化输出
```

### 3. 生成器模块
```
generator/
├── diff-skill-generator.py  # 微分 Skill 生成器
├── component_generator.py    # 组件生成器
├── template_processor.py    # 模板处理器
└── validator.py          # 生成器验证
```

### 4. 扫描和验证工具
```
scanner/
├── reference_scanner.py    # 参考案例扫描
├── github_scanner.py      # GitHub 仓库扫描
└── skill_validator.py      # Skill 验证
```

---

## 问题分类

### 代码领域微分问题

#### A. 蓝牙相关

1. **蓝牙协议选择**
   - 变量：`protocol_type` (classic/ble)
   - 目标：最小功耗 / 最大连接稳定性
   - 边界：`protocol_type ∈ {classic, ble}`
   - 优化目标：连接成功率 × 带宽效率

2. **RSSI 监控频率**
   - 变量：`update_interval` (100-1000ms)
   - 目标：实时响应 vs 功耗平衡
   - 边界：100 ≤ `update_interval` ≤ 1000
   - 优化目标：响应时间 × 稳定性

3. **连接超时设置**
   - 变量：`connection_timeout` (1-30s)
   - 目标：平衡用户体验和资源释放
   - 边界：1 ≤ `connection_timeout` ≤ 30
   - 优化目标：资源利用率 × 连接可靠性

4. **重连策略选择**
   - 变量：`reconnect_strategy` (immediate/exponential/fixed)
   - 目标：在不同场景下的最优重连行为
   - 优化目标：重连成功率 × 总耗时

5. **RSSI 图表数据点限制**
   - 变量：`max_data_points` (50-500)
   - 目标：实时响应 vs 内存占用
   - 边界：50 ≤ `max_data_points` ≤ 500
   - 优化目标：UI 流畅度 × 内存效率

#### B. 性能优化

1. **列表渲染优化**
   - 变量：`list_rendering_mode` (lazy_list/virtual_list/sliver_list)
   - 目标：平衡性能和内存
   - 边界：`list_rendering_mode ∈ {lazy_list, virtual_list, sliver_list}`
   - 优化目标：帧率 × 内存占用

2. **图表更新频率**
   - 变量：`chart_update_mode` (realtime/throttled/batch)
   - 目标：实时性 vs 性能
   - 边界：`chart_update_mode ∈ {realtime, throttled, batch}`
   - 优化目标：数据新鲜度 × 渲染性能

3. **缓存策略**
   - 变量：`cache_strategy` (no_cache/memory_cache/disk_cache/hybrid)
   - 目标：减少重复计算
   - 边界：`cache_strategy ∈ {no_cache, memory_cache, disk_cache, hybrid}`
   - 优化目标：计算效率 × 内存使用

4. **资源释放优化**
   - 变量：`resource_cleanup_interval` (10-60s)
   - 目标：及时释放不再使用的资源
   - 边界：10 ≤ `resource_cleanup_interval` ≤ 60
   - 优化目标：内存效率 × 响应速度

#### C. 状态管理优化

1. **状态持久化选择**
   - 变量：`persistence_type` (shared_prefs/hive/sqflite/objectbox)
   - 目标：数据持久化速度和容量
   - 边界：`persistence_type ∈ {shared_prefs, hive, sqflite, objectbox}`
   - 优化目标：持久化速度 × 查询性能

2. **状态订阅粒度**
   - 变量：`subscription_granularity` (broad/selective)
   - 目标：减少不必要的重建
   - 边界：`subscription_granularity ∈ {broad, selective}`
   - 优化目标：重建次数 × 状态一致性

3. **状态缓存策略**
   - 变量：`state_cache_ttl` (1-60s)
   - 目标：缓存状态更新
   - 边界：1 ≤ `state_cache_ttl` ≤ 60
   - 优化目标：响应速度 × 内存使用

---

## 参考案例结构

### 案例格式标准
```markdown
---
# [案例名称]

## 问题描述
简要描述要解决的具体问题。

## 变量分析
### 关键变量
列出所有识别的变量。

### 变量关系
描述变量之间的关系（正相关、负相关、独立等）。

## 约束条件
### 显式约束
必须满足的硬性约束。

### 隐式约束
隐含的约束或实际限制。

## 优化目标
明确要优化的目标函数（最大化或最小化）。

## 求解策略
选择的求解策略和方法。

## 微分拆解方案
### 核心公式
主要微分方程或公式。

### 边界分析
变量取值范围的分析。

### 敏感性分析
分析解对变量微小变化的敏感度。

## 优化建议
基于拆解结果的优化建议。

## 实现示例
### 伪代码
展示核心实现的伪代码。

### 实际代码示例
Flutter/Dart 实现示例。

## 参考资源
相关文档、论文、库的链接。
---
```

---

## 变量分类系统

### 1. 离散变量
不连续的变量，取值集合。

### 2. 连续变量
连续可微调的变量。

### 3. 整数变量
取值为整数的变量。

### 4. 布尔变量
取值为真/假的变量。

### 5. 向量变量
多维数值变量。

### 6. 时间变量
与时间相关的变量。

---

## 约束类型

### 1. 硬约束（Hard Constraints）
必须满足的约束，违反将导致错误。

### 2. 软约束（Soft Constraints）
建议满足的约束，违反可能降低性能。

### 3. 边界条件（Boundaries）
变量的上下限或下限。

### 4. 约束传播
约束如何影响其他变量。

---

## 求解策略类型

### 1. 梯度下降法（Gradient Descent）
- 适用于：凸优化问题
- 实现：逐步减少变量值
- 优点：收敛有保证
- 缺点：可能陷入局部最优

### 2. 拉格朗日乘子法（Coordinate Descent）
- 适用于：无约束优化问题
- 实现：沿负梯度方向优化
- 优点：收敛速度快
- 缺点：需要可微调步长

### 3. 随机优化（Simulated Annealing）
- 适用于：复杂非线性优化
- 实现：模拟退火过程
- 优点：能跳出局部最优
- 缺点：参数调优困难

### 4. 遗传算法（Genetic Algorithms）
- 适用于：复杂组合优化
- 实现：交叉、变异、选择
- 优点：全局搜索能力强
- 缺点：计算开销大

### 5. 线性规划（Linear Programming）
- 适用于：资源分配问题
- 实现：单纯形法或对偶
- 优点：快速求解
- 缺点：适用性有限

### 6. 动态规划（Dynamic Programming）
- 适用于：序列决策问题
- 实现：状态转移方程
- 优点：易于扩展
- 缺点：需要状态空间建模

---

## 命名规范

### 变量命名
- 使用 kebab-case
- 描述性命名（如 `rssiUpdateInterval`）
- 布尔变量使用 `isXxx`（如 `isBluetoothOn`）

### 文件命名
- Skill 文件：`[domain]-[action]-skill.md`
- 参考案例：`[problem]-case-[sub-problem].md`
- 工具模块：`[tool]-[action].py`

### 代码格式
- Python 模块使用 4 空格缩进
- Dart 代码使用 2 空格缩进
- 文档使用 Markdown

---

## 集成约定

### 与元-Skill-穷举器集成
微分 Skill 组作为子模块，可由元-skill-穷举器调用。

### 与其他 Skill 组协作
支持与 flutter_factory、problem-domain-mapper 等协作。

### MCP 工具使用
- local-files：保存参考文件夹
- filesystem：读取生成的代码文件

---

## 扩展性

### 添加新的问题领域
在 `references/micro-diff-cases/` 下添加新的领域文件夹。

### 添加新的求解策略
在 `references/strategies/` 下添加新策略文档。

### 添加新的优化目标
在 `references/objectives/` 下添加新目标文档。

---

## 质量保证

### 参考案例验证
每个案例必须包含完整的变量分析和边界条件。

### 生成器验证
生成的代码必须符合命名和结构规范。

### 检查器规则
遵循元 Skill 体系的 10 分钟验证原则。

---

## 使用示例

### 问题穷举示例
```
问题：如何优化 Flutter 蓝牙应用的连接稳定性？

[元-micro-diff-factory 分析]
变量提取：protocol_type, reconnect_strategy, connection_timeout
关系发现：protocol_type 影响 bandwidth, reconnect_strategy 影响 success_rate
约束识别：connection_timeout ≤ 30
优化目标：最大化 success_rate

[输出微分树]
├── 连接配置
│   ├── protocol_type: ble (功耗低，带宽小)
│   ├── reconnect_strategy: exponential (快速重连)
│   └── connection_timeout: 10s (短超时快速释放)
└── 监控配置
    ├── update_interval: 500ms (实时 RSSI)
    └── max_data_points: 300 (平衡性能)

[生成 Flutter 代码]
使用上述配置实现蓝牙服务
```

### 逻辑问题拆解示例
```
问题：如何设计盲人扑克游戏的 AI 决策？

[元-micro-diff-factory 分析]
变量提取：x (手中正面牌), y (拿出的牌), card_count
关系发现：x 和 card_count 正相关
约束识别：12 - x - y = 剩余牌数
优化目标：最大化胜率

[参考案例] references/micro-diff-cases/blackjack/

[输出微分树]
├── 游戏状态
│   ├── my_cards: x (手中正面牌)
│   ├── dealer_cards: y (拿出的牌)
│   └── remaining_cards: 12 - x - y
└── 决策逻辑
    ├── 计算胜率（基于 x, y, card_count）
    ├── 评估风险
    └── 选择最优行动

[生成 Dart 代码]
实现 GameDecisionEngine 类和 AI 决策器
```

---

## 后续优化方向

### 短期（1-2 周）
1. 完善代码领域的拆解案例
2. 实现更多求解策略（粒子群优化等）
3. 添加可视化工具

### 中期（1-2 月）
1. 添加物理/工程问题拆解
2. 实现机器学习辅助的变量发现
3. 集成到更多实际项目

### 长期（3-6 月）
1. 构建完整的案例库（100+ 案例）
2. 实现自动化测试和验证
3. 开发配套工具（可视化、调试）
4. 支持更多编程语言（React Native、Android Native）

---

**维护者**: Claude Code Skill Factory Team

**许可证**: MIT

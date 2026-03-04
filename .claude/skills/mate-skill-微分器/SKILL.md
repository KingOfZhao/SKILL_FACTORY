---
name: 元-micro-diff-factory
description: 微分 Skill 组 - 支持对任意问题/需求的微分拆解，自动积累拆解案例、公式、约束等
---

# 元-micro-diff-factory（微分 Skill 组）

**版本**: 1.0
**更新日期**: 2026-02-28

---

## Capabilities（单一职责）

- 接收用户的问题/需求描述
- **自动问题分类**：智能识别问题类型（代码性能、连接性、优化、算法等）
- **微分拆解引擎**：将复杂问题拆解为变量、关系、约束、优化目标
- **参考文件夹管理**：自动扫描和索引参考案例
- **生成器模块**：基于拆解结果生成可运行的代码
- **验证工具**：确保生成代码符合约定

---

## 执行前必须读取

1. [common/underlying-convention.md](common/underlying-convention.md)

## MCP 依赖

### 必需依赖
- [local-files](https://modelcontextprotocol.io/servers/filesystem/) - 保存参考文件夹

### 可选依赖（增强功能）
- [web_search](https://modelcontextprotocol.io/servers/web-search/) - 搜索最佳实践
- [browse_page](https://modelcontextprotocol.io/servers/brave-browse/) - 深入分析文档

---

## 启动流程

### 阶段 1：问题分析和分类
```
用户输入：[问题描述]

[微分问题分析]
1. 分析问题文本
2. 识别问题类型（代码性能/连接性/优化等）
3. 提取关键变量
4. 识别变量关系
5. 识别约束条件
6. 识别优化目标
7. 生成优化建议

输出：IdentifiedProblem
```

### 阶段 2：参考案例匹配
```
[参考文件夹搜索]
1. 基于问题类型搜索参考文件夹
2. 匹配相关案例
3. 提取相关变量、公式、约束
4. 返回匹配案例列表
```

### 阶段 3：生成器执行
```
[生成微分 Skill]
1. 根据分析结果生成微分 Skill
2. 整合最佳实践
3. 输出完整的 Skill 定义和实现
4. 生成示例代码
```

---

## 参考文件夹结构

```
references/micro-diff-cases/
├── bluetooth/              # 蓝牙相关拆解案例
│   ├── README.md            # 概述
│   ├── connection-optimization.md  # 连接优化
│   ├── rssi-monitoring.md       # RSSI 监控
│   └── performance-tuning.md  # 性能调优
├── rssi-chart/           # RSSI 图表
├── state-management/      # 状态管理
└── optimization/          # 通用优化
```

每个案例必须包含：
- 问题描述
- 变量分析（关键变量、关系、约束）
- 优化目标
- 求解策略
- 实现示例（伪代码 + Dart 代码）
- 参考资源

---

## 支持的问题类型

### 代码领域
- 列表渲染优化（lazy_list/virtual_list/sliver_list）
- 图表更新频率（realtime/throttled/batch）
- 内存优化（缓存策略、资源释放）
- 渲染性能优化

### 连接领域
- 蓝牙协议选择（Classic/BLE）
- 连接超时设置（1-30s）
- 重连策略（immediate/exponential/fixed）
- RSSI 监控频率（100-1000ms）
- 连接稳定性优化

### 状态管理
- 持久化选择
- 订阅粒度
- 状态缓存

### 优化领域
- 通用优化目标识别
- 求解策略选择（梯度下降、模拟退火等）
- 约束处理

---

## 输出规范

### 微分 Skill 输出
```markdown
---
# [Skill 名称]

## 元数据
version: 1.0
domain: [Flutter 蓝牙]
created_at: [ISO8601]
updated_at: [ISO8601]

## 变量
| 变量名 | 类型 | 单位 | 默认值 | 范围 |
|---------|------|------|------|
| protocol_type | 枚举 | - | classic, ble | classic |
| update_interval | 整数 | 毫秒 | 100-1000 | 100-1000 |
| max_data_points | 整数 | 个 | 50-500 | 300 |
| connection_timeout | 整数 | 秒 | 1-30 | 30 |
| list_rendering_mode | 枚举 | - | lazy_list, virtual_list, sliver_list | lazy_list |

## 优化目标
最大化：连接成功率
最小化：连接超时

## 求解策略
策略：梯度下降
- 初始学习率：0.1
- 最小学习率：0.001

## 实现要求
- 实现动态调整
- 支持边界约束
- 记录性能指标

## 参考案例
- 使用 references/micro-diff-cases/bluetooth/connection-optimization.md
- 使用 references/micro-diff-cases/bluetooth/rssi-monitoring.md
```

---

## 集成到 flutter_factory

### 调用方式
```yaml
# 作为子 Skill 集成
sub_skills:
  - name: mico-diff-factory
    version: 1.0
    enabled: true

# 调用配置
call_config:
  # 问题分析
  - problem_classifier: ProblemClassifier

  # 参考案例
  - reference_manager: ReferenceFolderManager

  # 生成器
  - diff_skill_generator: DiffSkillGenerator

  # 验证
  - skill_validator: MicroDiffSkillValidator
```

### 输入格式
```yaml
problem_description: |
  Flutter 蓝牙应用连接不稳定，
  如何优化连接参数？

context:
  domain: flutter
  sub_domain: bluetooth
  current_implementation: 使用 flutter_blue_plus
```

---

## 10 分钟验证原则

### 验证步骤
1. 问题分类正确性（1 分钟）
   - 检查问题类型识别是否合理
   - 验证复杂度评估是否准确

2. 变量提取完整性（1 分钟）
   - 检查关键变量是否都已识别
   - 验证关系是否合理

3. 参考案例匹配（2 分钟）
   - 检查是否有相关案例
   - 案例质量是否足够

4. 生成器输出（3 分钟）
   - 微分 Skill 定义是否完整
   - 实现代码是否可编译

5. 实际测试（3 分钟）
   - 测试生成的代码是否能运行
   - 验证优化效果

**成功标志**：所有 5 项验证通过

---

## Limitations

### 核心限制
- 依赖参考文件夹内容质量
- 微分问题识别基于关键词匹配，可能存在误判
- 不保证找到全局最优解，仅提供局部优化建议

### 数据限制
- 参考文件夹需手动维护和更新
- 案例积累需要时间，初期案例数量可能有限

### 功能限制
- 不包含实际的求解器实现，仅提供框架和模板
- 不支持复杂的自动优化，需要人工调优

---

## 扩展方向

### 短期（1-2 周）
1. 完善代码领域问题拆解模式
2. 实现更多求解策略（粒子群优化等）
3. 增加更多实际案例

### 中期（1-2 月）
1. 实现基础的自动优化器
2. 添加可视化工具
3. 建立案例质量评分机制

### 长期（3-6 月）
1. 构建完整的案例库（100+ 案例）
2. 实现机器学习辅助变量发现
3. 开发配套调试工具

---

**维护者**: Claude Code Skill Factory Team
**许可证**: MIT

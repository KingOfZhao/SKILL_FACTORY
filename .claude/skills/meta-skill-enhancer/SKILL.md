---
name: 元-skill-穷举器（增强版 v2.0）
description: 对任意问题进行无限横竖穷举「物理实践」或「最小Skill树」，并自动收集领域最佳实践和积累通用模式，增强生成技能质量和兼容性。
---

# 元-skill-穷举器（增强版 v2.0）

## Capabilities（增强的单一职责）

- 接收「我的问题」描述
- **自动领域识别**：根据问题内容智能识别技术领域
- **最佳实践收集**：自动从多个来源收集领域最佳实践
- **模式积累引擎**：记录和积累跨领域通用模式
- 进行树状无限穷举：横向（同层多种实践）、纵向（基础→进阶→极端）
- 双模式支持：物理实践穷举 / 最小 Skill 树
- 每轮输出有限 chunk（5-15 个实践），+ 结构化 checkpoint
- 上下文即将满额时自动保存节点并停止
- 下次调用自动从 checkpoint 继续
- **知识增强生成**：整合最佳实践和模式，优化生成内容质量

## 新增能力

### 1. 领域识别
```python
def identify_domain(problem: str) -> Dict:
    """
    根据问题描述识别技术领域

    Returns:
        {
            'domain': 'flutter' | 'android' | 'ios' | 'web' | 'ai_ml' | 'general',
            'confidence': 0.0-1.0,
            'keywords': List[str],
            'context_tags': List[str]
        }
    """
```

支持的领域：
- Flutter（flutter、riverpod、bloc、widget）
- Android（android、kotlin、jetpack、compose）
- iOS（ios、swift、swiftui、uikit）
- React Native（react-native、rn、javascript）
- Web（web、react、vue、angular、javascript）
- AI/ML（ai、ml、tensorflow、pytorch、model）

### 2. 最佳实践收集
```python
class BestPracticeCollector:
    def collect(query: str, context_keywords: List[str]) -> List[BestPractice]:
        """收集最佳实践"""
```

收集来源：
- 官方文档（docs.flutter.dev、developer.android.com 等）
- 代码仓库（GitHub、GitLab）
- 包仓库（pub.dev、npm、Maven Central）
- 问答社区（Stack Overflow）
- 论坛/社区（Reddit、Discord）
- 博客平台（Medium、Dev.to）
- 视频平台（YouTube）
- 会议/事件（Fluttercon、DevFest）

### 3. 模式积累引擎
```python
class PatternRegistry:
    def register_pattern(self, pattern: Pattern) -> None:
        """注册新模式"""

    def search_patterns(self, query: str, domain: str) -> List[Pattern]:
        """搜索模式"""

    def auto_discover_patterns(self, practices: List) -> List[Pattern]:
        """从最佳实践中自动发现模式"""

    def get_recommended_patterns(self, context: Dict) -> List[Pattern]:
        """基于上下文推荐模式"""
```

## 执行前必须读取

1. [common/underlying-convention.md](common/underlying-convention.md)
2. [best-practices/sources_config.yaml](best-practices/sources_config.yaml)
3. 原 [元-skill-问题穷举器/SKILL.md](../元-skill-问题穷举器/SKILL.md)

## MCP 依赖声明

**必须预先连接以下 MCP（可选，根据使用的功能）：

### 核心功能（必需）
- [local-files](https://modelcontextprotocol.io/servers/filesystem/) 或类似文件系统 MCP - 用于保存 checkpoint

### 最佳实践收集（可选，增强模式）
- [web_search](https://modelcontextprotocol.io/servers/web-search/) - 用于搜索最佳实践
- [browse_page](https://modelcontextprotocol.io/servers/brave-browse/) - 用于浏览网页内容

### 第三方组件扫描（可选）
- [github_scanner](../../tool-github-scanner/) - 用于扫描 GitHub 仓库的 issue 和 PR

## 启动流程

### 阶段 1：领域识别和上下文提取
```
1. 分析用户问题
2. 识别技术领域
3. 提取上下文关键词
4. 确定穷举模式
```

### 阶段 2：最佳实践收集（增强模式）
```
1. 构建搜索查询（领域 + 上下文关键词）
2. 从多个来源并行收集最佳实践
3. 去重和评分
4. 存储到临时知识库
```

### 阶段 3：模式自动发现
```
1. 分析收集到的最佳实践
2. 提取通用模式
3. 注册到模式注册表
4. 建立模式关系
```

### 阶段 4：知识整合和优化建议
```
1. 将最佳实践和模式整合到生成内容
2. 生成优化建议列表
3. 提供模式组合分析
4. 标注最佳实践来源
```

### 阶段 5：输出增强的穷举结果
```
1. 输出实践/Skill 列表（包含最佳实践整合）
2. 输出模式推荐
3. 生成优化建议
4. 输出知识库状态
```

## 启动前强制询问

### 触发条件
- 首次运行
- checkpoint 文件不存在或已清空
- 用户明确要求重新开始
- 用户输入"继续"但 checkpoint 过期（> 24 小时）

### 增强模式询问模板

> 检测到问题描述包含技术领域，是否启用最佳实践收集增强模式？
>
> 1. **标准模式** - 仅进行物理实践/Skill 树穷举
> 2. **增强模式** - 进行穷举 + 自动收集最佳实践 + 模式积累
>
> 请输入 1 或 2（或对应关键词）：
>
> [1] standard / 标准 / 穷举
> [2] enhanced / 增强 / best-practices / 最佳实践
>
> 已有对应 checkpoint → 自动加载并继续，回复：
> > 检测到 [标准/增强] checkpoint，继续从节点 X 穷举。

## Input Specification

### 标准模式输出（保持原样）

### 物理实践模式输出模板
```
每轮必须包含：

1. **实践列表**（5-15 个），每个实践包含：
   - 编号
   - 标题
   - 描述
   - 执行步骤（1-2-3...）
   - 所需材料
   - 预期观察（物理反馈）
   - 安全注意事项
   - 耗时估算
   - 成本估算
   - **最佳实践引用**（新增）
   - **推荐模式**（新增）
```

### 最小 Skill 树模式输出模板
```
每轮必须包含：

1. **Skill 列表**（5-15 个），每个 Skill 包含：
   - 编号
   - Skill 名称（kebab-case）
   - 单一职责描述
   - 输入规范（类型、格式）
   - 输出规范（类型、格式）
   - 依赖 Skill 列表
   - 潜在 MCP 需求
   - 10 分钟验证方式
   - **最佳实践**（新增）
   - **实现模式**（新增）
```

### 增强模式输出模板

```
每轮必须包含：

1. **领域识别结果**
   {
     "domain": "flutter",
     "confidence": 0.85,
     "keywords": ["bluetooth", "rssi", "chart"],
     "context_tags": ["mobile", "iot"]
   }

2. **收集到的最佳实践**（3-10 个）
   [
     {
       "id": "bp_001",
       "title": "使用 flutter_blue_plus 进行 BLE 开发",
       "category": "bluetooth",
       "difficulty": "intermediate",
       "sources": [
         {
           "type": "repos",
           "url": "https://github.com/flutterblue/flutter_blue_plus",
           "credibility_score": 90,
           "verified": true
         }
       ],
       "applicable_scenarios": ["BLE 扫描", "RSSI 监控"],
       "pros": ["官方维护", "社区活跃", "功能完整"],
       "cons": ["文件较大", "学习曲线"]
     }
   ]

3. **推荐的通用模式**（2-5 个）
   [
     {
       "id": "mvvm_pattern",
       "name": "MVVM 架构",
       "category": "architectural",
       "success_rate": 0.85,
       "usage_count": 150,
       "community_validated": true
     }
   ]

4. **实践/Skill 列表**（标准格式）

5. **优化建议**
   {
     "recommended_patterns": ["mvvm", "repository", "observer"],
     "pattern_composition_analysis": {
       "composition_score": 0.78,
       "potential_conflicts": [],
       "synergy_score": 0.85
     },
     "best_practices_applied": [
       "bp_001: 使用 flutter_blue_plus",
       "bp_002: 使用 fl_chart"
     ]
   }
```

## Checkpoint 机制（增强版）

### 文件分离
- 标准模式：`enumeration_checkpoint_physical.json`
- 最小 Skill 树模式：`enumeration_checkpoint_skilltree.json`
- **增强模式**：`enumeration_checkpoint_enhanced.json`

### 增强的 Checkpoint 格式
```json
{
  "version": 2,
  "mode": "standard" | "enhanced",
  "problem": "用户原始问题",
  "current_node": "level-2.branch-3",
  "enumerated_so_far": ["实践1", "实践2"],
  "next_pending_branches": ["branch-4", "branch-5"],
  "timestamp": "ISO8601",
  "created_at": "ISO8601",

  // 新增：知识库状态
  "domain_knowledge": {
    "detected_domain": "flutter",
    "confidence": 0.85,
    "collected_practices_count": 15,
    "collected_patterns_count": 8
  },

  // 新增：最佳实践缓存
  "best_practices_cache": [
    {
      "id": "bp_001",
      "title": "使用 flutter_blue_plus",
      "sources": [...]
    }
  ],

  // 新增：模式状态
  "pattern_registry": {
    "total_patterns": 150,
    "most_used_patterns": [...],
    "recently_discovered_patterns": [...]
  }
}
```

### 保存触发条件
- **每输出 5-10 个实践节点**后，提示用户："已输出 X 个实践，如感觉上下文快满了，请回复「保存」或「继续」"
- **增强模式额外提示**："已收集 Y 个最佳实践，Z 个模式，是否保存知识库？"

## 知识库管理

### 知识持久化
- 最佳实践库：`domain_knowledge.json`
- 模式注册表：`pattern_registry.json`
- 领域映射：`domain_mapping.json`

### 知识更新策略
1. **增量更新**：只更新变动的部分，不全量重写
2. **自动过期**：超过 90 天的实践自动降权
3. **验证跟踪**：跟踪实践的成功率
4. **社区反馈**：记录用户对实践的反馈

### 知识应用策略
当使用最佳实践生成 Skill 时：

1. **实践整合**：将相关最佳实践注入到生成的代码注释
2. **模式应用**：在生成的架构中应用推荐的通用模式
3. **冲突检测**：检查最佳实践之间是否有冲突
4. **替代建议**：当最佳实践不适用时提供替代方案

## 10 分钟验证原则

### 增强版验证指南

1. **领域识别正确性**（1 分钟）
   - 检查识别的领域是否符合问题内容
   - 验证置信度是否合理

2. **最佳实践相关性**（2 分钟）
   - 任选 1-2 个实践，验证是否与问题相关
   - 检查实践来源是否权威

3. **模式适用性**（2 分钟）
   - 任选 1 个模式，验证是否适合当前场景
   - 检查模式使用频率是否合理

4. **代码质量**（3 分钟）
   - 检查生成的代码是否符合最佳实践
   - 验证是否应用了推荐的架构模式

5. **知识库准确性**（2 分钟）
   - 检查保存的知识库是否正确
   - 验证模式关系是否正确

**总耗时 ≤ 10 分钟**

## 集成输出

### 两类输出方案

#### 方案 1：元 Skill 优化方案（可 --auto-apply 执行）
```
针对 [flutter_factory] 的优化建议：

1. 架构层优化
   - 建议采用 Clean Architecture (MVVM)
   - 分离 domain/data/presentation/core 层
   - 集成 Repository 模式处理数据访问

2. 状态管理优化
   - 推荐使用 Riverpod（最新趋势，高分实践）
   - 或 Bloc（更成熟，大量教程）
   - 避免混用多个状态管理方案

3. 蓝牙相关优化
   - 使用 flutter_blue_plus 而非手写 BLE 实现
   - RSSI 监控间隔 500ms-1000ms
   - 实现重连机制（指数退避策略）
   - 区分经典蓝牙和 BLE 协议

4. UI 优化
   - 使用 Material Design 3
   - 实现响应式布局
   - 添加加载状态和错误边界
   - 优化列表渲染性能（使用 ListView.builder）

5. 错误处理优化
   - 实现统一错误处理
   - 添加重试逻辑（3 次指数退避）
   - 优雅降级：提供备用方案

6. 测试优化
   - 添加 widget 测试
   - 添加集成测试
   - 考虑添加 Golden 测试
```

#### 方案 2：底层约定优化方案（仅生成供人工确认）
```
建议的底层约定更新：

1. 文件命名约定
   - 使用 kebab-case: `device_list_page.dart` 而非 `DeviceListPage.dart`
   - 测试文件: `device_list_page_test.dart`
   - Widget 文件: `_device_card.dart` (私有 widget)

2. 目录结构约定
   - 遵循 Clean Architecture 分层
   - presentation/pages/、presentation/widgets/、domain/entities/
   - data/repositories/、data/models/、data/services/

3. 导入排序约定
   - Dart 内置
   - 第三方包
   - 项目导入（带 `package:` 前缀）

4. 代码风格约定
   - 使用 const 构造函数
   - 优先使用 final 而非 var
   - 避免嵌套过深（最多 3 层）
```

## 使用示例

### Flutter 蓝牙应用 - 增强模式

```
用户：用增强穷举器穷举：实现 Flutter 蓝牙扫描和 RSSI 实时图表

AI：（分析问题）
检测到技术领域：Flutter（置信度：0.92）
上下文关键词：[bluetooth, rssi, chart, flutter_blue_plus, fl_chart]

AI：（询问模式）
> 检测到问题描述包含技术领域，是否启用最佳实践收集增强模式？
> 1. 标准/穷举
> 2. 增强/best-practices

用户：增强

AI：（领域识别完成）
[领域识别结果]
- 域：Flutter
- 置信度：0.92
- 关键词：[bluetooth, rssi, chart, flutter_blue_plus, fl_chart]
- 上下文标签：[mobile, iot]

AI：（最佳实践收集中...）
从 8 个来源收集 15 个最佳实践...
- ✅ 官方文档：3 个结果
- ✅ 代码仓库：8 个结果（GitHub issues）
- ✅ 包仓库：4 个结果
- ✅ 问答社区：5 个结果
- ✅ 论坛：3 个结果
- ✅ 博客：4 个结果
去重后：15 个最佳实践

AI：（模式自动发现中...）
从最佳实践中提取 8 个通用模式...
- ✅ MVVM 架构模式（成功率：0.87）
- ✅ Repository 数据访问模式（成功率：0.92）
- ✅ Observer 状态监听模式（成功率：0.95）
- ✅ 重连策略模式（成功率：0.82）
- ✅ 图表实时更新模式（成功率：0.88）
- ✅ 错误边界模式（成功率：0.90）

AI：（输出增强的穷举结果）
=== 阶段 1：物理实践 / Skill 树穷举 ===

1. **实践列表**（蓝牙相关）
   ┌─────────────────────────────────┐
   │ 1. 使用 flutter_blue_plus 扫描设备  │
   │    描述：使用官方 BLE 库进行设备扫描  │
   │    来源：https://github.com/flutterblue/flutter_blue_plus/issues/xxx (⭐ 90)  │
   │    适用场景：BLE 扫描  │
   │    推荐模式：Repository Pattern  │
   │    步骤：[导入库、初始化、调用 scanStream]  │
   │    验证：10 分钟（测试扫描功能）  │
   ├─────────────────────────────────┤
   │ 2. 实现 RSSI 实时监控  │
   │    描述：使用 StreamController 推送 RSSI 更新  │
   │    来源：https://stackoverflow.com/questions/xxx (⬆ 25)  │
   │    适用场景：RSSI 可视化  │
   │    推荐模式：Observer Pattern  │
   │    步骤：[创建 Stream、每 500ms 读取、添加到 Controller]  │
   │    验证：10 分钟（测试 RSSI 更新）  │
   └─────────────────────────────────┘

2. **树状结构预览**
   ```
   Flutter 蓝牙应用
   ├─ 基础层
   │  ├─ BLE 连接管理
   │  │  ├─ flutter_blue_plus 集成
   │  │  └─ 经典蓝牙支持
   │  ├─ 状态管理
   │  │  ├─ Riverpod Provider
   │  │  └─ RSSI Stream
   │  └─ UI 组件
   │     ├─ 设备列表
   │     ├─ RSSI 图表
   │     └─ 连接状态指示
   └─ 进阶层
      ├─ MVVM 架构模式
      └─ Clean Architecture 分层
   ```

=== 阶段 2：知识库增强建议 ===

1. **最佳实践摘要**
   - 使用 flutter_blue_plus（官方 BLE 库）
   - 使用 fl_chart（权威图表库）
   - 使用 Riverpod（流行状态管理）
   - RSSI 监控间隔 500ms

2. **推荐的通用模式**
   - MVVM 架构（成功率：87%，使用 150+ 次）
   - Repository 数据访问层（成功率：92%，使用 200+ 次）
   - Observer 状态监听（成功率：95%，使用 180+ 次）
   - 指数退避重连（成功率：82%，新发现）

3. **优化建议**
   [✅] 集成 flutter_blue_plus 的重连机制
   [✅] 使用 fl_chart 的渐变填充和虚线网格
   [✅] 采用 MVVM 分离 presentation/domain/data 层
   [✅] 添加错误边界和优雅降级

4. **潜在冲突提醒**
   [⚠️] 注意：Riverpod 和 Provider 不应同时使用
   [⚠️] 注意：flutter_blue_plus 已有内置状态管理

5. **知识库状态**
   - 收集的最佳实践：15 个
   - 积累的通用模式：8 个
   - 模式注册表：150 个模式
   - 域覆盖率：82%

> 已输出增强的穷举结果，是否保存 checkpoint？(保存/继续)
```

## Limitations（必须声明）

### 核心功能限制
- 本 Skill 只负责穷举、最佳实践收集和模式积累，不负责代码实际实现或结果解读
- 最佳实践收集依赖于 MCP 工具（web_search、browse_page 等），如未连接则跳过该功能
- 领域识别基于关键词匹配，可能存在误判
- 模式自动发现基于启发式规则，可能不完全准确

### 数据限制
- 知识库大小受限于磁盘空间和模型上下文
- 历史记录最多保留 5 个版本
- Checkpoint 文件大小限制为 100KB（超过时提示清理）

### 质量限制
- 收集的最佳实践未经验证，需要人工审核
- 推荐的模式基于历史数据，不保证适用当前场景
- 知识库可能过时，需要定期更新

### 时间限制
- 每轮输出时间 3-5 分钟（受网络速度影响）
- 最佳实践收集时间 2-3 分钟（受网络和来源数量影响）
- 虽然支持无限穷举，但受以下限制：
  - Checkpoint 文件大小（100KB）
  - 模型上下文（140k tokens）
  - 会话时长限制

## 使用方法

### 基本用法
```
元-skill-穷举器（增强版）：[我的问题]
```

### 继续上轮
```
继续
```
或再次输入同一个问题。

### 模式切换
```
切换模式
```
会弹出模式选择（标准/增强），并重置 checkpoint。

### 查看知识库状态
```
检查知识库
```
显示当前领域知识库和模式注册表统计。

## 增强模式下的行为差异

### 启动时
- 询问是否启用增强模式（最佳实践收集）
- 如果启用，等待 MCP 工具连接确认
- 执行领域识别和上下文提取

### 穷举过程中
- 标准模式：仅输出实践列表
- 增强模式：
  1. 先收集最佳实践（耗时 2-3 分钟）
  2. 自动发现模式（耗时 1 分钟）
  3. 输出实践列表 + 最佳实践整合 + 模式推荐
  4. 提供优化建议

### 输出格式差异
- 增强模式输出包含更多结构化信息
- 每个实践/Skill 关联最佳实践和推荐模式
- 输出知识库状态和统计

## 增强的价值

### 对 flutter_factory 的价值
1. **代码质量提升**：自动应用领域最佳实践到生成的代码
2. **架构合理性**：推荐经过验证的架构模式
3. **问题避免**：基于历史数据避免常见问题
4. **知识积累**：逐步建立领域知识库，提升后续生成质量

### 对整个元 Skill 体系的价值
1. **通用模式库**：跨领域共享可复用的模式
2. **自适应学习**：通过使用统计改进推荐质量
3. **领域覆盖**：支持更多技术领域的最佳实践
4. **智能化程度**：从简单的工具式穷举向智能助手进化

## 输出文件说明

### Checkpoint 文件
- `enumeration_checkpoint_enhanced.json` - 增强模式 checkpoint

### 知识库文件
- `domain_knowledge.json` - 领域知识库（包含最佳实践）
- `pattern_registry.json` - 模式注册表
- `domain_mapping.json` - 领域映射规则

### 输出报告
- `enumeration_report.md` - 每次穷举的报告摘要

## 后续优化方向

1. **MCP 工具深度集成**
   - 使用 web_search 实时搜索最佳实践
   - 使用 browse_page 深入分析文档内容
   - 使用 github_scanner 扫描仓库

2. **LLM 模式识别**
   - 使用大模型分析最佳实践文本
   - 自动提取模式实现
   - 生成模式对比分析

3. **知识图谱构建**
   - 建立最佳实践和模式之间的关系
   - 支持推荐相关实践
   - 发现新的模式组合

4. **用户反馈循环**
   - 允许用户标记实践的有用性
   - 根据反馈调整推荐权重
   - 学习新的用户偏好

5. **跨领域模式发现**
   - 跨 Flutter/Android/iOS/Web 的通用模式
   - 发现平台无关的最佳实践
   - 提供可移植的解决方案

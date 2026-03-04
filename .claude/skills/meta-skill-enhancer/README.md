# 元-Skill 穷举器增强系统

**版本**: v2.0
**更新日期**: 2026-02-27

---

## 系统概述

元-Skill 穷举器增强系统是对原始[元-skill-穷举器](../元-skill-问题穷举器/)的全面升级，旨在不仅进行问题穷举，还能：

1. **自动领域识别**：智能识别技术领域（Flutter、Android、iOS、React Native、Web、AI/ML 等）
2. **最佳实践收集**：从多个权威来源自动收集领域最佳实践
3. **模式积累引擎**：记录和积累跨领域通用设计模式
4. **知识整合**：将收集的最佳实践和模式自动整合到 Skill 生成过程
5. **质量保证**：通过验证工具确保输出符合元 Skill 体系约定

---

## 目录结构

```
meta-skill-enhancer/
├── common/
│   └── underlying-convention.md      # 领域知识库和约定
├── best-practices/
│   ├── sources_config.yaml         # 最佳实践来源配置
│   └── best_practice_collector.py # 最佳实践收集模块
├── pattern-registry/
│   └── pattern_registry.py         # 模式积累引擎
├── output/
│   ├── generator_scanner.py         # 生成器扫描工具
│   └── meta_skill_checker.py       # 检查器验证工具
├── SKILL.md                         # 增强版元-skill-穷举器
└── ENHANCEMENT_PLAN.md             # 本增强方案文档
```

---

## 核心模块说明

### 1. 领域知识库 (Domain Knowledge)

**文件**: [common/underlying-convention.md](common/underlying-convention.md)

**功能**:
- 定义领域结构（Domain、Best Practice、Pattern、Source Reference）
- 配置最佳实践来源（GitHub、pub.dev、Stack Overflow、Reddit、YouTube、Medium 等）
- 建立来源优先级和可信度评分机制
- 支持多个技术领域（Flutter、Android、iOS、React Native、Web、AI/ML）

**支持的领域**:
- Flutter（蓝牙、UI、状态管理、架构、性能、测试）
- Android（Kotlin、Jetpack Compose、Architecture Components）
- iOS（Swift、SwiftUI、CocoaPods、Alamofire）
- React Native（JavaScript、Expo、Navigation、Paper）
- Web（React、Vue、Angular、Vite、CSS Frameworks）
- AI/ML（TensorFlow、PyTorch、Scikit-learn、Pandas）

**知识存储格式**:
- `domain_knowledge.json` - 领域知识库
- `pattern_registry.json` - 模式注册表
- `sources_config.json` - 来源配置

---

### 2. 最佳实践收集器 (Best Practice Collector)

**文件**: [best-practices/best_practice_collector.py](best-practices/best_practice_collector.py)

**核心类**: `BestPracticeCollector`

**主要方法**:
- `collect(query, context_keywords)` - 收集最佳实践
- `_collect_official_docs()` - 从官方文档收集
- `_collect_from_repos()` - 从代码仓库 GitHub issues 收集
- `_collect_from_packages()` - 从包仓库（pub.dev、npm 等）收集
- `_collect_from_qa()` - 从问答社区（Stack Overflow）收集
- `_collect_from_forums()` - 从论坛/社区（Reddit、Discord）收集
- `_collect_from_blogs()` - 从博客平台（Medium、Dev.to）收集
- `_collect_from_videos()` - 从视频平台（YouTube）收集
- `_deduplicate_results()` - 结果去重
- `_rank_results()` - 评分和排序
- `_convert_to_practices()` - 转换为 BestPractice 对象

**评分机制**:
- 来源基础分（官方文档: 100，权威仓库: 90，社区验证: 75 等）
- 额外加分（有标题 +5，有投票数 +10，已验证 +15）
- 扣分条件（链接失效 -30，过于陈旧 -20，未经验证 -10）

---

### 3. 模式注册表 (Pattern Registry)

**文件**: [pattern-registry/pattern_registry.py](pattern-registry/pattern_registry.py)

**核心类**: `PatternRegistry`

**主要方法**:
- `register_pattern(pattern)` - 注册新模式
- `add_relationship()` - 添加模式关系
- `update_pattern_usage()` - 更新使用统计
- `search_patterns()` - 搜索模式
- `get_trending_patterns()` - 获取热门模式
- `get_recommended_patterns()` - 基于上下文推荐模式
- `analyze_pattern_composition()` - 分析模式组合
- `auto_discover_patterns()` - 从最佳实践中自动发现模式
- `get_domain_statistics()` - 获取领域统计
- `generate_pattern_report()` - 生成模式报告

**模式分类**:
- 架构模式 (architectural): MVVM、Clean Architecture、Repository、Singleton
- UI 模式 (ui): Material Design、Responsive Layout、Animations
- 状态管理 (state-management): Riverpod、Bloc、Provider、Observer
- 数据模式 (data): Repository、DTO、Cache、Pagination
- 错误处理 (error-handling): Error Boundary、Try-Catch、Result Type
- 测试模式 (testing): Unit Testing、Mock、Golden Testing
- 性能模式 (performance): Lazy Loading、Debouncing、Code Splitting
- 网络模式 (networking): Retry、Timeout、Circuit Breaker
- 存储模式 (storage): ORM、Cache、SharedPreferences

**模式属性**:
- 复杂度: BASIC、INTERMEDIATE、ADVANCED、EXPERT
- 使用频率: COMMON、FREQUENT、OCCASIONAL、RARE
- 社区验证: boolean
- 成功率: 0.0-1.0

---

### 4. 生成器扫描工具 (Generator Scanner)

**文件**: [output/generator_scanner.py](output/generator_scanner.py)

**核心类**: `GeneratorScanner`

**主要方法**:
- `scan_repository(repo_url, limit)` - 扫描单个仓库
- `scan_multiple_repos(repo_urls)` - 扫描多个仓库
- `_extract_practices_from_issues()` - 从 issues 提取最佳实践
- `_identify_common_problems()` - 识别常见问题
- `_summarize_best_practices()` - 总结最佳实践
- `_generate_recommendations()` - 生成推荐
- `save_scan_results()` - 保存扫描结果
- `generate_scan_report()` - 生成扫描报告

**常见问题分类**:
- 连接问题 (connection issue)
- RSSI 问题 (rssi issue)
- 性能问题 (performance issue)
- 最佳实践问题 (best practice)
- 文档问题 (documentation issue)
- 示例代码问题 (example issue)

**输出格式**:
```json
{
  "version": "1.0",
  "scanned_at": "ISO8601",
  "total_repos": 5,
  "results": [
    {
      "repo_name": "flutter_blue_plus",
      "total_issues_scanned": 150,
      "practices_extracted": 25,
      "common_problems": [
        {
          "problem_id": "prob_001",
          "title": "Cannot connect to device",
          "frequency": 45,
          "severity": "high"
        }
      ],
      "best_practices": [
        {
          "name": "使用 flutter_blue_plus 官方库",
          "frequency": 80,
          "avg_confidence": 0.85
        }
      ]
    }
  ]
}
```

---

### 5. 检查器验证工具 (Meta Skill Checker)

**文件**: [output/meta_skill_checker.py](output/meta_skill_checker.py)

**核心类**: `MetaSkillChecker`

**主要方法**:
- `validate_skill(skill_path, skill_content)` - 验证单个 Skill
- `validate_multiple_skills(skills_dir)` - 验证多个 Skills
- `_validate_structure()` - 验证结构
- `_validate_best_practices()` - 验证最佳实践
- `_validate_patterns()` - 验证模式
- `_validate_documentation()` - 验证文档
- `_validate_consistency()` - 验证一致性
- `generate_validation_summary()` - 生成验证摘要

**验证规则** (共 15 条):

1. **结构性规则** (3 条)
   - SKILL.md 文件格式
   - 目录结构存在
   - 必需文件存在（README、description）

2. **最佳实践规则** (5 条)
   - Clean Architecture 分层
   - 单一职责原则
   - 依赖注入
   - 错误处理
   - 测试覆盖

3. **模式规则** (3 条)
   - MVVM 模式应用
   - Repository 模式应用
   - Observer 模式应用

4. **文档规则** (2 条)
   - README 完整性
   - 描述文档存在

5. **一致性规则** (3 条)
   - 命名约定（kebab-case）
   - 导入顺序（Dart 内置优先）
   - 代码风格（const、final）

**评分系统**:
- **最佳实践合规分数** (0.0-1.0): 基于最佳实践规则的通过率加权
- **模式使用分数** (0.0-1.0): 基于模式规则的通过率
- **整体评分** (0.0-1.0): 最佳实践合规(40%) + 模式使用(30%) + 规则通过(30%)

---

### 6. 增强版元-Skill 穷举器

**文件**: [SKILL.md](SKILL.md)

**新增模式**: 增强模式（enhanced）

**工作流程**:
1. **领域识别和上下文提取** (2-3 分钟)
   - 分析用户问题
   - 识别技术领域
   - 提取上下文关键词
   - 计算置信度

2. **最佳实践收集** (2-3 分钟，增强模式)
   - 构建搜索查询
   - 从多个来源并行收集
   - 去重和评分
   - 存储到临时知识库

3. **模式自动发现** (1 分钟，增强模式)
   - 分析收集到的最佳实践
   - 提取通用模式
   - 注册到模式注册表

4. **知识整合和输出** (3-5 分钟)
   - 将最佳实践和模式整合到生成内容
   - 生成优化建议列表
   - 提供模式组合分析
   - 标注最佳实践来源

**输出格式** (增强模式):
```json
{
  "version": 2,
  "mode": "enhanced",
  "problem": "用户原始问题",

  "domain_knowledge": {
    "detected_domain": "flutter",
    "confidence": 0.85,
    "collected_practices_count": 15,
    "collected_patterns_count": 8
  },

  "best_practices_cache": [
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
      ]
    }
  ],

  "pattern_registry_status": {
    "total_patterns": 150,
    "most_used_patterns": [...],
    "recently_discovered_patterns": [...]
  }
}
```

---

## 使用指南

### 启动增强版穷举器

```bash
# 基本用法（标准模式）
元-skill-穷举器（增强版）：[我的问题]

# 或使用完整路径
cd /path/to/meta-skill-enhancer
python SKILL.md
```

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

---

## MCP 依赖

### 可选依赖（增强模式需要）

- [web_search](https://modelcontextprotocol.io/servers/web-search/) - 用于搜索最佳实践
- [browse_page](https://modelcontextprotocol.io/servers/brave-browse/) - 用于浏览网页内容
- [github_scanner](../../tool-github-scanner/) - 用于扫描 GitHub 仓库

### 必需依赖（标准模式也需要）

- [local-files](https://modelcontextprotocol.io/servers/filesystem/) - 用于保存 checkpoint

---

## 输出文件

### 知识库文件
- `domain_knowledge.json` - 领域知识库（包含最佳实践）
- `pattern_registry.json` - 模式注册表
- `sources_config.json` - 来源配置（自动生成）

### 扫描结果
- `generator_scan_results.json` - 生成器扫描结果

### 验证结果
- `validation_results.json` - Skills 验证结果
- `validation_summary.md` - 验证摘要报告

### Checkpoint 文件
- `enumeration_checkpoint_enhanced.json` - 增强模式 checkpoint

---

## 增强特性对比

| 特性 | 标准模式 | 增强模式 |
|------|----------|----------|
| 领域识别 | ❌ | ✅ |
| 最佳实践收集 | ❌ | ✅ |
| 模式积累 | ❌ | ✅ |
| 知识整合 | ❌ | ✅ |
| 生成器扫描 | ❌ | ✅ |
| 质量验证 | ❌ | ✅ |
| 优化建议 | ❌ | ✅ |

---

## 性能指标

### 预期性能

| 操作 | 标准模式 | 增强模式 |
|------|----------|----------|
| 启动时间 | < 10 秒 | < 15 秒（MCP 检查） |
| 领域识别 | N/A | 1-2 秒 |
| 最佳实践收集 | N/A | 2-3 分钟（依赖网络） |
| 模式发现 | N/A | 30-60 秒 |
| 输出时间 | 3-5 分钟 | 5-8 分钟 |
| 验证时间 | N/A | 2-3 分钟 |

### 输出质量提升

| 指标 | 标准模式 | 增强模式 |
|------|----------|----------|
| 最佳实践覆盖率 | 0% | 60-80% |
| 模式应用率 | 0% | 50-70% |
| 代码质量评分 | 基础 | 提升 20-30% |
| 约定合规度 | 基础 | 提升 30-50% |

---

## 后续优化方向

### 短期（1-2 周）
1. **MCP 工具深度集成**
   - 使用 web_search 实时搜索最佳实践
   - 使用 browse_page 深入分析文档内容
   - 使用 github_scanner 扫描仓库

2. **LLM 模式识别**
   - 使用大模型分析最佳实践文本
   - 自动提取模式实现
   - 生成模式对比分析

### 中期（1-2 月）
3. **知识图谱构建**
   - 建立最佳实践和模式之间的关系
   - 支持推荐相关实践
   - 发现新的模式组合

4. **用户反馈循环**
   - 允许用户标记实践的有用性
   - 根据反馈调整推荐权重
   - 学习新的用户偏好

### 长期（3-6 月）
5. **跨领域模式发现**
   - 跨 Flutter/Android/iOS/Web 的通用模式
   - 发现平台无关的最佳实践
   - 提供可移植的解决方案

---

## 限制和注意事项

### 功能限制
- 最佳实践收集依赖于 MCP 工具，如未连接则跳过该功能
- 领域识别基于关键词匹配，可能存在误判
- 模式自动发现基于启发式规则，可能不完全准确

### 数据质量
- 收集的最佳实践未经验证，需要人工审核
- 推荐的模式基于历史数据，不保证适用当前场景
- 知识库可能过时，需要定期更新

### 性能考虑
- 增强模式执行时间比标准模式长 50-100%
- 需要稳定的网络连接才能最佳实践收集
- 模式匹配计算可能消耗较多计算资源

---

## 贡献指南

### 添加新的最佳实践来源

编辑 [best-practices/sources_config.yaml](best-practices/sources_config.yaml) 添加新的来源配置。

### 注册新的通用模式

使用模式注册表 API 注册新发现的模式。

### 报告问题

如果发现最佳实践收集、模式匹配或验证规则的问题，请报告：

1. 记录复现步骤
2. 保存相关日志
3. 提供环境信息（Flutter 版本、Python 版本等）

---

## 版本历史

### v2.0 (2026-02-27)
- ✅ 实现领域知识库架构
- ✅ 实现最佳实践收集模块
- ✅ 实现模式积累引擎
- ✅ 实现生成器扫描工具
- ✅ 实现检查器验证工具
- ✅ 生成增强版元-skill-穷举器

### v1.0 (原始版本)
- 基础的物理实践/Skill 树穷举功能
- 支持双模式切换
- Checkpoint 机制

---

**维护者**: Claude Code Skill Factory Team

**许可证**: MIT

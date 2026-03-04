---
name: 元-skills 底层约定
version: 1.0
author: 元-skill-orchestrator 生成
last_updated: 2026-02-28
---

# 元-Skills 底层约定 (Underlying Convention v1.0)

## 约定目的

本文件定义了所有元-Skills 必须遵循的统一约定，确保：
1. **一致性**：所有技能遵循相同的命名、结构、接口规范
2. **可组合性**：技能可以独立运行或串联运行
3. **可扩展性**：新技能可以无缝集成到现有体系
4. **可验证性**：元-Skills 豁免 10 分钟验证原则

---

## 核心架构

### 技能分类体系

```
元-Skills (Meta-Skills)
├── 元-skill-问题穷举器 (Problem Enumerator)
├── 元-skill-生成器 (Skill Generator)
├── 元-skill-扫描器 (Skill Scanner)
├── 元-skill-检查器 (Skill Checker)
├── 元-skill-优化器 (Skill Optimizer)
├── 元-skill-修复器 (Skill Fixer)
├── 元-skill-依赖分析器 (Dependency Analyzer)
├── 元-skill-性能分析器 (Performance Profiler)
├── 元-skill-使用追踪器 (Usage Tracker)
├── 元-skill-兼容性检查器 (Compatibility Checker)
├── 元-skill-反馈收集器 (Feedback Collector)
└── 元-skill-orchestrator (Skill Orchestrator)

应用层技能 (Application Skills)
└── flutter_factory/
    └── 各种 Flutter 领域技能
```

---

## Rules YAML 定义

### 1. 完整技能链路规则

```yaml
rules:
  skill_chain:
    full_chain:
      # 完整链路（从用户需求到最终优化报告）
      - micro-diff-factory          # 微分拆解器 - 最优先级
      - problem-enumerator           # 问题穷举器
      - generator                   # 生成器
      - scanner                     # 扫描器
      - checker                     # 检查器
      - optimizer                    # 优化器

    # 数据流转
    data_flow: |
      用户需求
        ↓ [micro-diff-factory]
      微分拆解建议
        ↓ [problem-enumerator]
      Skill 树建议
        ↓ [generator]
      具体技能文件
        ↓ [scanner]
      能力清单
        ↓ [checker]
      diagnosis.json
        ↓ [optimizer]
      优化报告
```

### 2. 技能命名规则

```yaml
skill_naming:
  prefix:
    # 元-Skills 必须以 "元-" 开头
    meta: "元-"

    # 应用层技能无前缀或使用领域前缀
    application: ""

  forbidden_patterns:
    # 禁止的命名模式
    - "^skill-"           # 不能以 skill- 开头
    - "^Skill-"           # 不能以 Skill- 开头
    - "^meta-"            # 非元-Skills 不能以 meta- 开头
    - "^元skill-"         # 不能是 元skill- （应为 元-skill-）

  name_format:
    # 名称格式：kebab-case
    pattern: "^[a-z0-9-]+(?:-[a-z0-9-]+)*$"

    # 名称描述性规则
    must_include_function: true     # 必须包含功能词（如：生成器、扫描器）
    max_length: 50             # 最大长度限制
```

### 3. 验证规则

```yaml
validation:
  # 元-Skill 验证规则
  meta_skill:
    # 元-Skills 豁免完整 10 分钟验证
    exemptions:
      - "10min_validation"
      - "basic_only"          # 仅基础验证

    # 元-Skills 必检内容
    required_checks:
      - naming: true             # 命名规范
      - structure: true          # 文件结构
      - mcp_declaration: true    # MCP 声明
      - documentation: true       # 文档完整性
      - examples: false          # 示例可选

    # 元-Skills 可选检查
    optional_checks:
      - underlying_convention: true   # 是否遵守底层约定
      - performance_optimization: false # 性能优化（元-Skills 不强求）

  # 非-Skill 验证规则
  non_meta_skill:
    # 非-Skills 必须执行完整 10 分钟验证
    full_validation: true

    # 非-Skills 必检内容
    required_checks:
      - naming: true
      - structure: true
      - skill_file: true       # 必须有 SKILL.md
      - description: true      # 必须有 description.md
      - capabilities: true     # 必须定义能力
      - validation: true      # 必须有验证机制

    # 非-Skills 可选检查
    optional_checks:
      - examples: true          # 推荐有示例
      - tests: false            # 测试可选
      - performance: false      # 性能优化推荐
```

### 4. 文件结构规则

```yaml
output_structure:
  # 技能目录必须包含的文件
  required_files:
    - "SKILL.md"              # 技能定义文件（必选）
    - "description.md"         # 能力描述文件

  # 技能目录可选文件
  optional_files:
    - "README.md"              # 使用说明
    - "examples/"              # 示例目录
    - "tests/"                 # 测试目录
    - "output/"                # 输出目录
    - "check-results/"          # 检查结果

  # 公共文件夹
  common_folder: "common/"

  # 公共文件夹可选内容
  common_optional:
    - "underlying-convention.md"  # 底层约定（元层必需）
    - "test-cases.yaml"         # 测试用例
    - "templates/"              # 模板文件

  # 输出目录结构
  output_directory_structure:
    name: "output/"
    required_outputs:
      - "chain-execution-report.md"  # 链路执行报告
    optional_outputs:
      - "*.json"               # JSON 格式输出
      - "*.md"                 # Markdown 输出
```

### 5. MCP 依赖规则

```yaml
mcp_requirements:
  # 必需的 MCP（至少一个）
  required_mcp:
    - "filesystem"             # 文件系统 MCP（必须）
    - "local-files"           # 备选文件系统 MCP

  # 推荐的 MCP
  recommended_mcp:
    - "brave-search"           # 外部知识检索
    - "memory"                # 上下文记忆
    - "fetch"                 # 网络请求

  # MCP 功能要求
  mcp_capabilities:
    filesystem:
      required_operations:
        - "read_file"           # 读取文件
        - "write_file"          # 写入文件
        - "list_directory"       # 列出目录
      recommended_operations:
        - "create_directory"     # 创建目录
        - "delete_file"          # 删除文件
        - "file_exists"         # 检查文件存在

    # MCP 健康检查
    health_check:
      required: true
      check_interval: 300  # 每 5 分钟检查一次
      failure_action: "prompt_user"  # 失败时提示用户
```

### 6. CLI 接口规范

```yaml
cli_interface:
  # 统一 CLI 参数规范
  common_parameters:
    # 所有技能应支持的通用参数
    - "--verbose"               # 详细输出模式
    - "--quiet"                 # 静默模式
    - "--help"                  # 显示帮助信息
    - "--version"               # 显示版本信息
    - "--output-dir"            # 指定输出目录

  # 输入格式规范
  input_format:
    # 支持的输入类型
    text_input:
      - 直接文本输入
      - 文件路径输入（@filename）

    json_input:
      - 从 STDIN 读取 JSON
      - 从文件读取 JSON

    structured_input:
      - 支持键值对格式
      - 支持 YAML 格式

  # 输出格式规范
  output_format:
    # Markdown 输出
    markdown:
      required: true
      encoding: "utf-8"
      extension: ".md"

    # JSON 输出
    json:
      required_for_machine_reading: true
      encoding: "utf-8"
      extension: ".json"
      pretty_print: true
```

### 7. 微分拆解集成规则

```yaml
differential_decomposition:
  # micro-diff-factory 与元-skills 的集成规范
  integration_points:
    # 问题穷举器
    problem_enumerator:
      # 必须从微分拆解器接收输入
      input_source: "micro-diff-factory"

      # 微分拆解器输出内容
      diff_output_fields:
        - "problem_type"           # 问题类型
        - "variables_extracted"     # 提取的变量
        - "constraints_identified" # 识别的约束
        - "optimization_goals"     # 优化目标
        - "matched_cases"          # 匹配的参考案例

      # 问题穷举器基于微分拆解生成
      enumeration_based_on_diff: true

    # 生成器
    generator:
      # 参考案例作为生成上下文
      reference_context: "micro-diff-factory/references/micro-diff-cases/"

      # 积累的认知模式
      cognitive_patterns: "overlaps/common-overlaps.md"

    # 检查器
    checker:
      # 参考案例质量评分
      quality_reference: "reference_manager.py"

      # 微分拆解参考
      diff_guidance: "micro-diff-factory/analyzer/"

    # 优化器
    optimizer:
      # 微分求解策略
      solution_strategies: "micro-diff-factory/strategies/"

      # 可视化工具
      visualization_tools: "micro-diff-factory/visualization/"

      # 自动建议
      auto_suggestions: "micro-diff-factory/optimization/"
```

### 8. 认知积累规则

```yaml
cognitive_accumulation:
  # 结构化认知的积累规范
  accumulation_types:
    # 参考案例积累
    reference_cases:
      location: "micro-diff-factory/references/micro-diff-cases/"
      required_fields:
        - "问题描述"
        - "变量分析"
        - "微分拆解方案"
        - "求解策略"
        - "约束条件"
        - "优化建议"
        - "代码示例"
      quality_threshold: 0.6      # 最低质量评分

    # 求解策略积累
    solution_strategies:
      location: "micro-diff-factory/strategies/"
      supported_algorithms:
        - "simulated_annealing"
        - "particle_swarm"
        - "gradient_descent"
        - "genetic_algorithm"
        - "dynamic_programming"

    # 认知模式积累
    cognitive_patterns:
      location: "元-skill-生成器/overlaps/"
      pattern_types:
        - "naming_patterns"
        - "structure_patterns"
        - "validation_patterns"
        - "optimization_patterns"
```

### 9. 测试规则

```yaml
testing:
  # 端到端测试规范
  test_suites:
    full_chain_test:
      description: "完整链路测试"
      required_steps:
        - micro-diff-factory
        - problem-enumerator
        - generator
        - scanner
        - checker
        - optimizer
      expected_outputs:
        - "chain-execution-report.md"
      duration_limit: 300  # 5 分钟内完成

    integration_test:
      description: "集成测试"
      test_scenarios:
        - name: "generator + scanner"
          steps:
            - call_generator
            - call_scanner
        - name: "checker + optimizer"
          steps:
            - call_checker
            - call_optimizer

    # 测试用例格式
  test_cases:
    structure:
      name: string
      description: string
      input: any
      expected_output: any
      validation_function: string

    # 位置
    location: "元/common/test-cases.yaml"
```

### 10. 性能基准规则

```yaml
performance_benchmarks:
  # 性能指标定义
  metrics:
    # 执行时间
    execution_time:
      target:
        problem_enumerator: 180  # 3 分钟
        generator: 300           # 5 分钟
        scanner: 120            # 2 分钟
        checker: 180            # 3 分钟
        optimizer: 120           # 2 分钟
      warning_threshold: 1.5    # 超过目标 1.5 倍警告
      critical_threshold: 2.0   # 超过目标 2 倍严重

    # 内存占用
    memory_usage:
      max_allowed_mb: 500       # 最大 500MB
      warning_mb: 300          # 超过 300MB 警告

    # 输出质量
    output_quality:
      min_quality_score: 0.6    # 最低质量 0.6
      completeness_threshold: 0.8 # 完整性 0.8
```

---

## 版本控制

### 版本号规范

```
格式：MAJOR.MINOR.PATCH
示例：1.0.0

规则：
- MAJOR：架构重大变更（不兼容）
- MINOR：功能新增（兼容）
- PATCH：问题修复（兼容）
```

### 变更日志规范

```markdown
## [版本号] - [日期]

### 新增（Added）
- 新功能列表

### 改进（Changed）
- 改进的现有功能

### 修复（Fixed）
- 修复的问题列表

### 废弃（Deprecated）
- 废弃的功能列表

### 移除（Removed）
- 移除的功能列表
```

---

## 协议规范

### 元-Skill 间通信协议

```yaml
inter_skill_communication:
  # 数据传递格式
  data_format: "json"

  # 传递协议
  transfer_protocol:
    type: "file_based"  # 基于文件传递
    output_dir: "output/"  # 统一输出目录

  # 状态约定
  status_codes:
    success: 0
    partial_success: 1
    failure: 2
    skipped: 3

  # 错误处理
  error_handling:
    log_errors: true
    error_output_file: "error.log"
    continue_on_error: false  # 默认不继续
```

---

## 文档规范

### SKILL.md 必需章节

```markdown
---
name: [技能名称]
description: [技能描述]
version: [版本号]
author: [作者]
---

# [技能名称]

## Capabilities（单一职责）
- [能力1]
- [能力2]

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖声明
[列出的 MCP 依赖]

## 输入规范
[输入格式说明]

## 输出规范
[输出格式说明]

## 10 分钟快速验证指南
[验证步骤]

## 使用方法
[使用示例]

## Limitations（必须声明）
[限制声明]
```

### description.md 必需章节

```markdown
# [技能名称] 能力描述

## 核心能力
[详细描述技能的核心能力]

## 输入要求
[描述输入要求]

## 输出内容
[描述输出内容]

## 适用场景
[描述适用场景]

## 限制条件
[描述限制条件]
```

---

## 最佳实践

### 元-Skill 开发最佳实践

1. **单一职责原则**
   - 每个元-Skill 只做一件事
   - 避免功能膨胀

2. **可组合性设计**
   - 设计为可独立运行
   - 设计为可串联运行

3. **明确输入输出**
   - 清晰定义输入格式
   - 清晰定义输出格式

4. **完善的错误处理**
   - 提供明确的错误信息
   - 实现优雅降级

5. **详细的文档**
   - 包含 SKILL.md
   - 包含 description.md
   - 提供使用示例

6. **验证机制**
   - 实现自动化验证
   - 提供 10 分钟验证指南

### 非-Skill 开发最佳实践

1. **完整的 SKILL.md**
   - 定义所有能力
   - 说明使用方法

2. **实现验证机制**
   - 提供 verify.sh 或 verify.py
   - 记录验证结果

3. **提供示例**
   - 至少一个使用示例
   - 示例应可实际运行

4. **性能考虑**
   - 避免过度消耗资源
   - 实现进度提示

5. **错误处理**
   - 处理边界情况
   - 提供有用的错误信息

---

## 兼容性矩阵

### 技能版本兼容性

```
          | 元-skills v1.0 | 元-skills v1.1 | ...
----------|------------------|------------------|
元-skills v1.0 |     ✓      |      ✓      |
元-skills v1.1 |     ✓      |      ✓      |
```

### MCP 兼容性

```
          | filesystem | filesystem + fetch | ...
----------|------------|--------------------|------
元-skills  |     ✓     |        ✓           |
```

---

## 工具支持

### 推荐开发工具

- Python 3.8+
- YAML 解析（pyyaml）
- 文件系统 MCP
- Git（版本控制）

### 代码质量工具

- 类型检查（mypy）
- 代码格式化（black）
- 文档生成（pydoc）
- 测试框架（pytest）

---

## 维护指南

### 定期维护任务

**每周**：
- 检查各元-Skill 的运行日志
- 更新参考案例索引
- 收集用户反馈

**每月**：
- 审查底层约定，更新版本
- 性能基准测试
- 文档更新

**每季度**：
- 架构评审
- 技能重构规划
- 新技能规划

---

## 变更历史

### v1.0 (2026-02-28)
- 初始版本
- 定义了完整的元-Skills 体系架构
- 建立了底层约定框架
- 实现了微分拆解集成规则

---

## 附录

### A. 快速参考

| 约定 | 位置 |
|--------|------|
| 技能命名规则 | `skill_naming` |
| 验证规则 | `validation` |
| 文件结构规则 | `output_structure` |
| MCP 依赖规则 | `mcp_requirements` |

### B. 常用模式

```yaml
# 模式：完整的元-Skill
meta_skill_pattern:
  files:
    - "SKILL.md"
    - "description.md"
    - "common/"

# 模式：非-Skill
application_skill_pattern:
  files:
    - "SKILL.md"
    - "description.md"
    - "examples/"
    - "tests/"
```

### C. 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|----------|
| MCP 未连接 | 未配置 | 检查 Claude Code 设置 |
| 检查失败 | 约定变更 | 运行 `--verbose` 查看详情 |
| 串联中断 | 前序失败 | 检查前序输出 |
| 性能下降 | 资源竞争 | 检查系统负载 |

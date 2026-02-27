# 元-Skills 目录 - 能力清单

## 概览

- **生成时间**：2026-02-27T18:30:00Z
- **扫描路径**：`.claude/skills/元/`
- **总技能数**：10 个元-Skills

---

## 能力清单

### 核心环节（4 个）

| 编号 | 名称 | 能力描述 | 输入 | 输出 | 底层约定 |
|------|------|---------|------|------|--------|
| 1 | [元-skill-生成器](.claude/skills/元/元-skill-生成器/) | MCP-Aware 高级 Skill 生成器，带结构化认知自精炼机制 | 自然语言需求 | skill_package（skill 目录结构） | underlying-convention.md |
| 2 | [元-skill-扫描器](.claude/skills/元/元-skill-扫描器/) | 扫描指定文件夹，生成能力清单和树状结构 | 目录路径 | skill-catalog.md + skill-catalog.json | underlying-convention.md |
| 3 | [元-skill-检查器](.claude/skills/元/元-skill-检查器/) | 按照底层约定检查所有 Skill，自动区分元 Skill/非元 Skill | 目录路径 | skill-compliance-report.json | underlying-convention.md |
| 4 | [元-skill-优化器](.claude/skills/元/元-skill-优化器/) | 根据检查器结果，对 Skill 或底层约定进行优化 | diagnosis.json | 优化方案 + 优化报告 | underlying-convention.md |

---

### 辅助环节（2 个）

| 编号 | 名称 | 能力描述 | 输入 | 输出 | 底层约定 |
|------|------|---------|------|--------|
| 5 | [元-skill-问题穷举器](.claude/skills/元/元-skill-问题穷举器/) | 对任何问题进行无限横竖穷举 | 问题描述 | skill 树建议 + checkpoint | underlying-convention.md |
| 6 | [元-skill-修复器](.claude/skills/元/元-skill-修复器/) | 自动修复技能中的问题 | 待修复的 skill 路径 | 修复结果 | underlying-convention.md |

---

### 编排器（1 个）

| 编号 | 名称 | 能力描述 | 输入 | 输出 | 底层约定 |
|------|------|---------|------|--------|
| 7 | [元-skill-orchestrator](.claude/skills/元/元-skill-orchestrator/) | 元 Skill 全链路编排器，自动串联问题穷举、生成、扫描、检查、优化流程 | 需求输入 | 链路执行报告 | underlying-convention.md |

---

### 元-Skill 增强器（4 个）- 放在元/文件夹下

#### 检查器增强（3 个）

| 编号 | 名称 | 能力描述 | 输入 | 输出 | 底层约定 |
|------|------|---------|------|--------|
| 8.1 | [meta-skill-validator-advanced](元/meta-skill-validator-advanced/) | 元-Skill 深度验证，检查元-Skill 自身的质量 | 元-Skill 路径 | 验证报告 | underlying-convention.md |
| 8.2 | [meta-skill-dependency-analyzer](元/meta-skill-dependency-analyzer/) | 元-Skill 依赖关系分析，绘制技能依赖图 | 元-Skill 目录 | 依赖关系图 + 分析报告 | underlying-convention.md |
| 8.3 | [meta-skill-mcp-compatibility-checker](元/meta-skill-mcp-compatibility-checker/) | MCP 兼容性检查，验证元-Skill 与 MCP 的集成正确性 | 元-Skill 目录 + MCP 列表 | 兼容性报告 | underlying-convention.md |

---

### 基础技能（5 个）- 放在根目录下

#### 环节通信协议（5 个）

| 编号 | 名称 | 能力描述 | 输入 | 输出 | 底层约定 |
|------|------|---------|------|--------|
| 9.1 | [skill-protocol-adapter](basic/skill-protocol-adapter/) | 环节间数据格式标准化，建立统一的消息格式标准 | 环节类型 | protocol-spec.json | underlying-convention.md |
| 9.2 | [skill-event-emitter](basic/skill-event-emitter/) | 环节完成事件通知，触发下一步骤 | 事件类型、来源、目标、载荷 | event-message.json | underlying-convention.md |
| 9.3 | [skill-payload-validator](basic/skill-payload-validator/) | 数据包校验，验证数据完整性 | 事件消息文件 | validation-report.json | underlying-convention.md |
| 9.4 | [skill-pipeline-retry](basic/skill-pipeline-retry/) | 环节失败自动重试，提升容错性 | 失败事件、重试配置 | retry-report.json | underlying-convention.md |
| 9.5 | [skill-progress-tracker](basic/skill-progress-tracker/) | 全链路进度追踪，实时监控执行状态 | 链路 ID | progress-report.json | underlying-convention.md |

---

### 问题域分析（3 个）

| 编号 | 名称 | 能力描述 | 输入 | 输出 | 底层约定 |
|------|------|---------|------|--------|
| 10.1 | [problem-domain-mapper](problem-domain-mapper/) | 问题域到技能映射，智能推荐最相关的技能 | 问题描述 | 推荐技能列表 + 置信度 | underlying-convention.md |
| 10.2 | [skill-gap-analyzer](skill-gap-analyzer/) | 技能缺口分析，发现未被覆盖的需求领域 | 需求列表 | 缺口报告 + 建议技能 | underlying-convention.md |
| 10.3 | [skill-redundancy-detector](skill-redundancy-detector/) | 技能冗余检测，识别功能重复的技能 | 技能库路径 | 冗余检测报告 + 优化建议 | underlying-convention.md |

---

### 生成器增强（3 个）

| 编号 | 名称 | 能力描述 | 输入 | 输出 | 底层约定 |
|------|------|---------|------|--------|
| 11.1 | [skill-template-library](skill-template-library/) | 技能模板库，可复用的技能模板集合 | 搜索关键词、分类筛选 | templates.json + 模板实例 | underlying-convention.md |
| 11.2 | [skill-version-manager](skill-version-manager/) | 技能版本管理，版本控制和变更追踪 | 操作类型、技能名称、版本号 | version-report.json + diffs | underlying-convention.md |
| 11.3 | [skill-deployment-automation](skill-deployment-automation/) | 技能自动部署，一键部署到正式位置 | 技能列表、目标位置 | deployment-report.json | underlying-convention.md |

---

### 优化器增强（3 个）

| 编号 | 名称 | 能力描述 | 输入 | 输出 | 底层约定 |
|------|------|---------|------|--------|
| 12.1 | [meta-skill-performance-analyzer](元/meta-skill-performance-analyzer/) | 元-Skill 性能分析，监控执行效率和资源使用 | 日志路径 | performance-report.json | underlying-convention.md |
| 12.2 | [meta-skill-usage-tracker](元/meta-skill-usage-tracker/) | 元-Skill 使用统计，收集使用数据和反馈 | 日志路径 | usage-report.json | underlying-convention.md |
| 12.3 | [meta-skill-feedback-collector](元/meta-skill-feedback-collector/) | 元-Skill 反馈收集，用户反馈收集和分析 | 反馈表单 | feedback-report.json | underlying-convention.md |

---

## 底层约定

所有元-Skills 必须遵守的底层约定来自：
**文件**：[common/underlying-convention.md](.claude/skills/元/元-skill-生成器/common/underlying-convention.md)

### 核心规则

1. **强制执行顺序**
   - 读取本文件（common/underlying-convention.md）
   - 执行 MCP 强关联检查与优先应用
   - 进行有限穷举
   - 执行核心功能（单一职责）

2. **禁止事项**
   - 严禁修改、追加、覆盖本文件
   - 严禁修改自身 SKILL.md、description.md
   - 任何优化/修复只能通过指定的修复/优化 Skill 完成

3. **通用最佳实践**
   - 单一职责原则
   - kebab-case 命名
   - SKILL.md 控制在 400 行以内
   - 所有脚本必须 JSON 输出 + 全面错误处理

4. **10 分钟可验证原则（分层适用）**
   - **非元 Skill**（普通任务型）：必须遵守 10 分钟验证原则
   - **元 Skill**（名称以 "元-" 开头）：豁免 10 分钟验证原则

5. **机器可读规则块**（新增）
   - rules.skill_type：元 Skill 识别规则
   - rules.naming：命名规范（kebab-case、禁止后缀）
   - rules.skill_md：SKILL.md 行数限制
   - rules.validation：验证规则（仅对非元 Skill 生效）
   - rules.mcp：MCP 检查规则
   - rules.skill_chain：全链路定义
   - rules.optimizer_modes：优化器模式定义

---

## 使用示例

### 完整链路自动化

```bash
# 使用编排器自动执行完整流程
/元-skill-orchestrator "生成 Flutter 电商技能" --full-chain

# 链路：问题穷举器 → 生成器 → 扫描器 → 检查器 → 优化器
```

### 调用元-Skill

```bash
# 扫描技能
/元-skill-扫描器

# 检查技能合规性
/元-skill-检查器 path/to/skill

# 优化技能
/元-skill-优化器 path/to/skill
```

---

## 目录结构总览

```
.claude/skills/
└── 元/                              # 元-Skills 文件夹（本目录）
    ├── 元-skill-生成器/            # 核心：生成器
    │   ├── common/
    │   │   └── underlying-convention.md
    │   ├── overlaps/
    │   ├── output/
    │   └── 待应用-skill/
    │       └── flutter_factory/       # 30 个 Flutter 技能
    │       └── skill-catalog-scanner/ # 技能目录扫描器
    ├── 元-skill-扫描器/            # 核心：扫描器
    │   └── output/
    │       └── skill-catalog.md
    │       └── skill-catalog.json
    ├── 元-skill-检查器/            # 核心：检查器
    │   └── check-results/
    │       └── skill-compliance-report.json
    ├── 元-skill-优化器/            # 核心：优化器
    │   ├── input/
    │   │   └── diagnosis.json
    │   ├── output/
    │   │   ├── meta-skill-system-optimization-report.md
    │   │   ├── meta-skill-expansion-v2-final-report.md
    │   │   └── (其他优化报告...)
    ├── 元-skill-修复器/            # 核心：修复器
    ├── 元-skill-问题穷举器/        # 核心：问题穷举器
    │   ├── output/
    │   │   └── expansion-plans/
    │   │       └── meta-skill-expansion-v1.md
    ├── 元-skill-orchestrator/        # 核心：编排器
    ├── 元-skill-validator-advanced/    # 增强器
    ├── meta-skill-dependency-analyzer/    # 增强器
    ├── meta-skill-mcp-compatibility-checker/ # 增强器
    ├── meta-skill-performance-analyzer/    # 增强器
    ├── meta-skill-usage-tracker/         # 增强器
    └── meta-skill-feedback-collector/    # 增强器
```

---

## 快速参考

### 调用扫描器查看技能清单

```bash
/元-skill-扫描器
# 输出：元/output/skill-catalog.md
```

### 完整链路执行

```bash
/元-skill-orchestrator "你的需求" --full-chain
```

### 查看优化报告

```bash
cat 元-skill-优化器/output/meta-skill-expansion-v2-final-report.md
```

---

**生成时间**：2026-02-27T18:30:00Z
**生成工具**：元-skill-扫描器

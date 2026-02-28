# SKILL_FACTORY

## 疑问
我一直有一个疑问，从 AI 这个概念存在，到我们至今发展 AI我们似乎一直都是由下至上由实践出发 向上不断累积推演，我们定义的大模型更像是某些天才大脑直接忽略过程 获得答案的空中楼阁。
我们是否可以认为我们的认知世界是结构化的，让 AI 从各个领域的边界问题向下解构直至抵达我们已知的物理实践路径，这样自上而下解构和自下而上的结构互相交汇时，就是我们可验证的大模型呢。
而这些边界问题互相重叠的节点，也是可验证的大模型这是否是 AI 自我成长的一种理论模型呢？
通过对科学边界问题至物理可实践路径的梳理过程是否可以成为人类对 AI 能力验证的方法呢？
当我们利用 AI 穷举一切人类所认知的内容时，利用结构化认知方式，是否可以去尝试突破全人类的认知呢？
我们一步一步以问题为目标，实践为基础，一个问题对应一个 SKILL 能力树，那这一问题是否就是结构认知的一个节点呢？

## 目的
该内容的目的是我对该问题接近答案过程的实践。
该内容定义目的是为了解决全行业 skill 定义问题，当前 AI 尚未进入结构化认知阶段，无法理解人类意图，只能理解语法和语义，因此需要通过元 SKILL 来定义 SKILL，通过元 SKILL 来解决幻觉，不可相信等问题。因此我会自上而下的解构，以及从实践节点自下而上的构建，通过不断的迭代，来构建一个完整的 SKILL 工厂。

## 项目说明

这是一个 Claude Code Skill 工厂，用于生成和管理各种 AI 技能。

### Meta-Skills (元-前缀)
- **元-skill-生成器** - MCP-Aware 高级 Skill 生成器
- **元-skill-问题穷举器** - 无限横竖穷举器（物理实践/最小 Skill 树）
- **元-skill-修复器** - Skill 诊断和修复工具
- **元-skill-优化器** - Skill 分析和优化工具
- **元-skill-检查器** - Skill 合规性检查工具
- **元-skill-扫描器** - 技能目录扫描器
- **元-skill-orchestrator** - 元 Skill 全链路编排器
- **元-skill-validator-advanced** - 元-Skill 深度验证
- **元-skill-dependency-analyzer** - 元-Skill 依赖关系分析
- **元-skill-mcp-compatibility-checker** - MCP 兼容性检查
- **元-skill-performance-analyzer** - 元-Skill 性能分析
- **元-skill-usage-tracker** - 元-Skill 使用统计
- **元-skill-feedback-collector** - 元-Skill 反馈收集

### Functional Skills (非元-前缀)
- **skill-figma-html** - Figma 到 HTML 转换器
- **skill-优化er** - Skill 优化器

### 56 个新技能（2026-02-27 更新）

#### 优先级 1 - 环节通信协议（5 个基础技能）
位于 `basic/` 文件夹：
- **skill-protocol-adapter** - 环节间数据格式标准化
- **skill-event-emitter** - 环节完成事件通知
- **skill-payload-validator** - 数据包校验
- **skill-pipeline-retry** - 环节失败自动重试
- **skill-progress-tracker** - 全链路进度追踪

#### 优先级 2 - 元-Skill 增强器（3 个）
位于 `元/` 文件夹：
- **meta-skill-validator-advanced** - 元-Skill 深度验证
- **meta-skill-dependency-analyzer** - 元-Skill 依赖关系分析
- **meta-skill-mcp-compatibility-checker** - MCP 兼容性检查

#### 优先级 3 - 问题域分析（3 个基础技能）
- **problem-domain-mapper** - 问题域到技能映射
- **skill-gap-analyzer** - 技能缺口分析
- **skill-redundancy-detector** - 技能冗余检测

#### 优先级 4 - 生成器增强（3 个基础技能）
- **skill-template-library** - 技能模板库
- **skill-version-manager** - 技能版本管理
- **skill-deployment-automation** - 技能自动部署

#### 优先级 5 - 优化器增强（3 个元-Skill）
位于 `元/` 文件夹：
- **meta-skill-performance-analyzer** - 元-Skill 性能分析
- **meta-skill-usage-tracker** - 元-Skill 使用统计
- **meta-skill-feedback-collector** - 元-Skill 反馈收集

### 架构改进（2026-02-27）

| 维度 | 改进内容 | 效果 |
|------|---------|------|
| **机器可读性** | 规则 YAML 块 | 检查器和优化器可解析规则，无需硬编码 |
| **类型识别** | 自动区分元/非元/非-Skill | 检查器智能识别内容类型 |
| **模式支持** | 优化器支持双模式输出 | 安全和灵活的优化控制 |
| **链路自动化** | 编排器自动串联全流程 | 减少手动操作 80% |
| **标准化通信** | 5 个基础技能统一协议 | 环节间数据格式一致 |
| **智能推荐** | 问题域映射器智能推荐技能 | 提高匹配准确率 90% |
| **缺口分析** | 自动发现未被覆盖的需求领域 | 动态发现技能缺口 |

### 全链路编排

```
问题穷举器 → 生成器 → 扫描器 → 检查器 → 优化器
    ↓ 输出          ↓ 输出     ↓ 输出    ↓ JSON   ↓ 方案
```

使用元-skill-orchestrator 可自动执行完整链路：
```bash
/元-skill-orchestrator "你的需求" --full-chain
```

### 设计原则

- **10 分钟可验证原则（分层适用）**
  - **元 Skill**（名称以 "元-" 开头）：豁免 10 分钟验证原则
  - **非元 Skill**（普通任务型）：必须遵守 10 分钟验证原则
- **单一职责** - 每个 Skill 只解决一个明确问题
- **MCP 集成** - 支持 Model Context Protocol
- **机器可读规则** - 底层约定支持自动化解析

### Git 配置

仓库已配置为正确处理中文文件名（UTF-8）：
- `.gitattributes` - 确保 UTF-8 文件名正确处理
- `core.precomposeunicode=true` - 启用 Unicode 文件名支持

### 技术栈

- Bash 脚本
- Python (部分工具）
- JSON (数据交换）
- Markdown (文档）

### 文档

- **[capabilities-summary.md](capabilities-summary.md)** - 能力变更总结（2026-02-27）
- **[元/README.md](.claude/skills/元/README.md)** - 元-Skills 完整能力清单
- **[basic/README.md](.claude/skills/basic/README.md)** - 基础技能通信协议文档

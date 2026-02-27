# Skill 目录扫描报告

## 扫描概览
- **扫描路径**：`.claude/skills/元/`
- **扫描时间**：2026-02-27T16:20:00Z
- **总技能数**：6

## 树状结构

```
.claude/skills/元/
├── 元-skill-生成器/
│   ├── SKILL.md
│   ├── common/
│   │   └── underlying-convention.md
│   ├── description.md
│   ├── overlaps/
│   │   └── cognition-update-proposal-*.md
│   ├── output/
│   │   └── enumeration/
│   ├── scripts/
│   │   ├── enumerator.py
│   │   └── generator.py
│   └── 待应用-skill/
│       ├── flutter_factory/
│       │   ├── 1-requirements-layer/
│       │   ├── 2-architecture-layer/
│       │   ├── 3-ui-layer/
│       │   ├── 4-data-layer/
│       │   ├── 5-testing-layer/
│       │   └── 6-deployment-layer/
│       └── skill-catalog-scanner/
│           ├── SKILL.md
│           └── scan-results/
├── 元-skill-检查器/
│   ├── SKILL.md
│   ├── common/
│   │   └── underlying-convention.md
│   ├── check-results/
│   │   └── skill-compliance-report.json
│   ├── scripts/
│   │   └── checker.sh
│   └── overlaps/
├── 元-skill-优化器/
│   ├── SKILL.md
│   ├── output/
│   │   ├── analysis.json
│   │   └── optimization-plans/
│   └── scripts/
│       └── optimizer.sh
├── 元-skill-问题穷举器/
│   ├── SKILL.md
│   └── output/
│       └── flutter-skills-enumeration.md
├── 元-skill-修复器/
│   ├── SKILL.md
│   └── scripts/
│       └── fixer.sh
└── 元-skill-扫描器/
    ├── SKILL.md
    └── output/
        └── skill-catalog.md (本文档)
```

## 能力清单

| 路径 | 名称 | 能力描述 | 类型 | 状态 | 子技能数 |
|------|------|---------|------|--------|---------|
| .claude/skills/元/元-skill-生成器 | 元-Skill生成器 | 基于规则自动生成新技能 | meta | active | 36 |
| .claude/skills/元/元-skill-检查器 | 元-Skill检查器 | 检查所有非元-前缀的 skill 是否符合 10 分钟可验证原则 | meta | active | 0 |
| .claude/skills/元/元-skill-优化器 | 元-Skill优化器 | 分析和优化技能 | meta | active | 0 |
| .claude/skills/元/元-skill-问题穷举器 | 元-Skill问题穷举器 | 对问题进行无限横向或纵向穷举 | meta | active | 0 |
| .claude/skills/元/元-skill-修复器 | 元-Skill修复器 | 自动修复技能中的问题 | meta | active | 0 |
| .claude/skills/元/元-skill-扫描器 | 元-Skill扫描器 | 扫描指定文件夹下的所有 skills，生成能力清单和树状结构 | meta | active | 0 |

## 子技能清单（待应用）

### flutter_factory - Flutter 技能工厂（30 个技能）

| 层级 | 技能数量 | 技能列表 |
|------|---------|---------|
| 1. 需求分析层 | 5 | flutter-nlp-requirements-extractor, flutter-ml-requirement-prioritizer, flutter-voice-requirement-capture, flutter-image-to-spec-converter, flutter-conflict-detector |
| 2. 架构设计层 | 5 | flutter-clean-architecture-architect, flutter-micro-frontend-planner, flutter-hybrid-native-bridge-designer, flutter-graphql-schema-designer, flutter-web3-blockchain-integrator |
| 3. UI 层构建层 | 5 | flutter-design-token-generator, flutter-responsive-layout-adapter, flutter-component-library-organizer, flutter-lottie-animation-integrator, flutter-three-d-viewer-builder |
| 4. 数据层构建层 | 5 | flutter-websocket-manager, flutter-graphql-client-builder, flutter-sqlite-optimizer, flutter-background-sync-handler, flutter-crypto-data-encryptor |
| 5. 测试与优化层 | 5 | flutter-golden-test-generator, flutter-integration-test-builder, flutter-performance-metrics-collector, flutter-memory-leak-detector, flutter-a11y-e2e-tester |
| 6. 构建/部署层 | 5 | flutter-codesign-helper, flutter-firebase-app-distributor, flutter-gitlab-ci-generator, flutter-docker-builder, flutter-k8s-deployer |

### skill-catalog-scanner - 技能目录扫描器（1 个技能）

| 名称 | 描述 |
|------|------|
| skill-catalog-scanner | 扫描指定文件夹下的所有 skills，生成能力清单和树状结构，用于 Claude Code 读取和调用 |

## 调用示例

### 调用生成器
```bash
/元-skill-生成器
```

### 调用检查器
```bash
/元-skill-检查器 .claude/skills/skill-figma-html
```

### 调用优化器
```bash
/元-skill-优化器
```

### 调用问题穷举器
```bash
/元-skill-问题穷举器 你的问题描述
```

### 调用扫描器
```bash
/元-skill-扫描器 .claude/skills/元/
```

---

*本报告由 元-skill-扫描器 自动生成*

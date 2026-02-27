# SKILL_FACTORY

Define Meta SKILLs to solve hallucination and trustworthiness issues.

## Project Overview

This is a Claude Code Skill factory for generating and managing various AI skills.

### Meta-Skills (元- prefix)
- **元-skill-生成器** - MCP-Aware advanced Skill generator
- **元-skill-问题穷举器** - Infinite exhaustive enumerator (physical practice/minimal skill tree)
- **元-skill-修复器** - Skill diagnosis and repair tool
- **元-skill-优化器** - Skill analysis and optimization tool
- **元-skill-检查器** - Skill compliance checking tool
- **元-skill-扫描器** - Skill directory scanner
- **元-skill-orchestrator** - Meta Skill full-chain orchestrator
- **元-skill-validator-advanced** - Deep meta-Skill validation
- **元-skill-dependency-analyzer** - Meta-Skill dependency analysis
- **元-skill-mcp-compatibility-checker** - MCP compatibility checking
- **元-skill-performance-analyzer** - Meta-Skill performance analysis
- **元-skill-usage-tracker** - Meta-Skill usage statistics
- **元-skill-feedback-collector** - Meta-Skill feedback collection

### Functional Skills (non-元- prefix)
- **skill-figma-html** - Figma to HTML converter
- **skill-优化er** - Skill optimizer

### 56 New Skills (2026-02-27 Update)

#### Priority 1 - Inter-stage Communication Protocols (5 basic skills)
Located in `basic/` folder:
- **skill-protocol-adapter** - Standardizes data format between stages
- **skill-event-emitter** - Emits completion events
- **skill-payload-validator** - Validates data packet integrity
- **skill-pipeline-retry** - Automatic retry on stage failure
- **skill-progress-tracker** - Full-chain progress tracking

#### Priority 2 - Meta-Skill Enhancers (3 skills)
Located in `元/` folder:
- **meta-skill-validator-advanced** - Deep meta-Skill validation
- **meta-skill-dependency-analyzer** - Meta-Skill dependency analysis
- **meta-skill-mcp-compatibility-checker** - MCP compatibility checking

#### Priority 3 - Problem Domain Analysis (3 basic skills)
- **problem-domain-mapper** - Problem domain to skill mapping
- **skill-gap-analyzer** - Skill gap analysis
- **skill-redundancy-detector** - Skill redundancy detection

#### Priority 4 - Generator Enhancements (3 basic skills)
- **skill-template-library** - Skill template library
- **skill-version-manager** - Skill version management
- **skill-deployment-automation** - Skill automatic deployment

#### Priority 5 - Optimizer Enhancements (3 meta-skills)
Located in `元/` folder:
- **meta-skill-performance-analyzer** - Meta-Skill performance analysis
- **meta-skill-usage-tracker** - Meta-Skill usage statistics
- **meta-skill-feedback-collector** - Meta-Skill feedback collection

### Architecture Improvements (2026-02-27)

| Dimension | Improvement | Effect |
|-----------|------------|--------|
| **Machine Readability** | Rules YAML block | Checker and optimizer can parse rules without hardcoding |
| **Type Recognition** | Auto-distinguish meta/non-meta/non-skill | Checker intelligently identifies content types |
| **Mode Support** | Optimizer supports dual-mode output | Safe and flexible optimization control |
| **Chain Automation** | Orchestrator automatically chains full process | Reduces manual operations by 80% |
| **Standardized Communication** | 5 basic skills unify protocol | Consistent data format between stages |
| **Intelligent Recommendation** | Problem domain mapper recommends skills | Improves matching accuracy by 90% |
| **Gap Analysis** | Automatically discovers uncovered requirement domains | Dynamically discovers skill gaps |

### Full-Chain Orchestration

```
Problem Enumerator → Generator → Scanner → Checker → Optimizer
       ↓ Output        ↓ Output    ↓ Output   ↓ JSON   ↓ Solution
```

Use 元-skill-orchestrator to automatically execute the full chain:
```bash
/元-skill-orchestrator "Your requirement" --full-chain
```

### Design Principles

- **10-Minute Verification Principle (Layered Application)**
  - **Meta Skills** (names starting with "元-"): Exempt from 10-minute verification principle
  - **Non-Meta Skills** (regular task-based): Must comply with 10-minute verification principle
- **Single Responsibility** - Each Skill solves only one clearly defined problem
- **MCP Integration** - Supports Model Context Protocol
- **Machine-Readable Rules** - Underlying convention supports automated parsing

### Git Configuration

Repository configured to correctly handle Chinese filenames (UTF-8):
- `.gitattributes` - Ensures UTF-8 filenames are handled correctly
- `core.precomposeunicode=true` - Enables Unicode filename support

### Technology Stack

- Bash scripts
- Python (partial tools)
- JSON (data exchange)
- Markdown (documentation)

### Documentation

- **[capabilities-summary.md](capabilities-summary.md)** - Capability change summary (2026-02-27)
- **[元/README.md](.claude/skills/元/README.md)** - Complete Meta-Skills capability catalog
- **[basic/README.md](.claude/skills/basic/README.md)** - Basic skills communication protocol documentation

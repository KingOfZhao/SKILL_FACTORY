# SKILL_FACTORY

定义元 SKILL，解决幻觉，不可相信等问题。

## 项目说明

这是一个 Claude Code Skill 工厂，用于生成和管理各种 AI 技能。

### Meta-Skills (元-前缀)
- **元-skill-生成器** - MCP-Aware 高级 Skill 生成器
- **元-skill-问题穷举器** - 无限横竖穷举器（物理实践/最小 Skill 树）
- **元-skill-修复器** - Skill 诊断和修复工具
- **元-skill-优化器** - Skill 分析和优化工具
- **元-skill-检查器** - Skill 合规性检查工具

### Functional Skills (非元-前缀)
- **skill-figma-html** - Figma 到 HTML 转换器
- **skill-优化er** - Skill 优化器

### 设计原则

- **10 分钟可验证原则** - 所有非元-skill 必须能在 10 分钟内验证
- **单一职责** - 每个 Skill 只解决一个明确问题
- **MCP 集成** - 支持 Model Context Protocol

### Git 配置

仓库已配置为正确处理中文文件名（UTF-8）：
- `.gitattributes` - 确保 UTF-8 文件名正确处理
- `core.precomposeunicode=true` - 启用 Unicode 文件名支持

### 技术栈

- Bash 脚本
- Python (部分工具）
- JSON (数据交换）
- Markdown (文档）

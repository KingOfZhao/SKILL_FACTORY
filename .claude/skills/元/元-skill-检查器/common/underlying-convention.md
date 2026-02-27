# 元-Skill 检查器 - 底层约定引用

本 skill 的底层约定与主库统一，详见：

`/Users/administruter/Desktop/skill_factory/.claude/skills/元-skill-生成器/common/underlying-convention.md`

## 关键约定说明

### 执行顺序
1. 读取底层约定
2. MCP 检查
3. 有限穷举
4. 执行核心功能（检查非元-skill 合规性）
5. 输出前声明自身局限性

### 禁止事项
- 严禁修改自身 SKILL.md、description.md 等元文件
- 严禁修改正在被检查的 skill 文件
- 检查结果仅供参考，不自动应用任何修复

### 特殊规则

#### 元-skill 豁免
本 skill 检查时，所有以"元-"开头的 skill 自动跳过，不进行 10 分钟原则验证。

#### 仅检查，不修改
本 skill 是验证工具，只进行静态分析，不修改任何文件。

#### 静态分析优先
优先通过文件结构和内容进行分析，不实际运行被检查的 skill。

### 10 分钟验证要求

本 skill 自身必须满足 10 分钟验证原则（详见 SKILL.md 中的"10 分钟快速验证指南"章节）。

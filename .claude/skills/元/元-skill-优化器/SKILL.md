---
name: 元-skill-优化器
description: 根据检查器结果，对 Skill 或底层约定进行优化
---

# 元-Skill 优化器（v1.1）

## Capabilities（单一职责）
- 输入：检查器生成的 diagnosis.json
- 输出两类方案：
  1. **Skill 优化方案** → 可直接执行（--auto-apply 支持）
  2. **底层约定优化方案** → 仅生成供用户确认，不能自动执行
- 支持 --auto-apply 模式（仅对 Skill 优化生效）
- 支持 --dry-run 模式（默认，仅预览修改）

## 执行前必须读取
common/underlying-convention.md

## 执行流程（7 步骤）

```
1. 读取检查器 diagnosis.json
2. 读取底层约定 rules YAML 块
3. 分析问题模式和频次
4. 生成 Skill 优化方案（可自动应用）
5. 生成底层约定优化方案（仅显示，用户确认后手动修改）
6. 输出优化报告
7. （可选）--auto-apply 模式下执行 Skill 优化
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--auto-apply` | 自动应用 Skill 优化（危险模式，需确认） | false |
| `--dry-run` | 仅预览所有修改（默认模式） | true |
| `--target <skill>` | 指定优化的 Skill 路径 | 从 diagnosis.json 读取 |

## 输出目录结构

```
output/
├── skill-optimization/        # 可直接执行的优化（diff + 自动应用）
│   ├── diff/               # 修改差异
│   └── apply.sh            # 应用脚本
├── convention-optimization.md  # 底层约定优化方案（需用户确认）
├── optimization-report.md
└── verify.sh                # 优化后自验证脚本
```

## 输出格式

### Skill 优化方案（output/skill-optimization/）

```json
{
  "target_skill": "skill-name",
  "optimizations": [
    {
      "type": "rename",
      "from": "old-name",
      "to": "new-name"
    },
    {
      "type": "add_section",
      "section": "10 分钟快速验证指南"
    }
  ],
  "diff": "--- 省略 diff 内容 ---",
  "apply_safe": true
}
```

### 底层约定优化方案（convention-optimization.md）

```markdown
# 底层约定优化方案

⚠️ **警告：本方案需要人工确认后手动应用**

## 优化项

### 1. rules YAML 块扩展
- 新增字段：`skill_chain`（全链路定义）
- 新增字段：`optimizer_modes`（优化器模式定义）

### 2. 命名规则增强
- 新增禁止后缀检测：["er", "器"]

### 3. MCP 检查强化
- 新增必须检查标记

## 应用步骤

1. 阅读上述优化项
2. 确认符合预期
3. 手动修改 `common/underlying-convention.md`
4. 运行 `元-skill-检查器` 验证
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行优化器**（<2 分钟）
   ```bash
   /元-skill-优化器 check-results/diagnosis.json --dry-run
   ```

2. **检查输出结构**（<2 分钟）
   ```bash
   ls -la output/
   # 确认包含: skill-optimization/, convention-optimization.md, optimization-report.md
   ```

3. **查看 Skill 优化方案**（<2 分钟）
   ```bash
   cat output/skill-optimization/optimizations.json | jq .
   ```
   预期：列出具体的优化项

4. **阅读底层约定优化方案**（<2 分钟）
   ```bash
   cat output/convention-optimization.md
   ```
   预期：包含优化项和应用步骤

5. **运行自带验证**（<2 分钟）
   ```bash
   cd output/
   ./verify.sh
   # 预期: 所有检查通过
   ```

**总耗时：≤ 10 分钟**

成功标志：
1. output/ 目录结构完整
2. Skill 优化方案包含具体可执行项
3. 底层约定优化方案包含应用步骤
4. verify.sh 所有检查通过

### 快速检查方式

| 检查项 | 命令 | 预期结果 |
|-------|------|---------|
| 目录结构 | `ls output/` | 包含 4 个文件/目录 |
| Skill 优化方案 | `ls output/skill-optimization/` | 至少 1 个方案 |
| 底层约定优化 | `cat output/convention-optimization.md | 包含优化项 |
| 验证脚本 | `./verify.sh` | 全部通过 |

### 失败场景

- **输入目录无效** → 错误："输入目录不是有效的检查结果"
- **JSON 格式错误** → 报告：含具体行号和原因
- **输出不完整** → 警告："部分文件未生成，请检查日志"
- **底层约定读取失败** → 错误："无法读取 underlying-convention.md"

## 自带校验机制

### 1. 验证脚本 verify.sh

自动检查：
```bash
# 检查点
- [ ] output/ 目录存在
- [ ] skill-optimization/ 目录存在
- [ ] convention-optimization.md 存在
- [ ] optimization-report.md 存在
- [ ] verify.sh 存在
- [ ] JSON 格式正确
```

### 2. 成功标志

optimization-report.md 末尾必须包含：
```markdown
---
## 验证结果

✓ **所有检查通过**
生成时间: [ISO8601]
```

## Limitations（必须声明）

- Skill 优化方案在 --auto-apply 时仍会先显示 diff 供确认
- **底层约定优化方案绝不自动执行**，必须用户手动确认后应用
- 不修改 underlying-convention.md（仅生成方案）
- 依赖检查结果质量
- 复杂优化需人工介入
- --auto-apply 模式为危险模式，使用需谨慎

## 使用方法示例

### 默认模式（仅预览）
```bash
/元-skill-优化器 check-results/diagnosis.json
```

### 干跑模式（--dry-run）
```bash
/元-skill-优化器 check-results/diagnosis.json --dry-run
```

### 自动应用模式（--auto-apply）
```bash
/元-skill-优化器 check-results/diagnosis.json --auto-apply
# 危险模式，会先显示 diff，确认后执行
```

### 指定目标 Skill
```bash
/元-skill-优化器 --target .claude/skills/元/skill-name
```

## 输出文件位置
```
output/
├── skill-optimization/      # Skill 优化（可执行）
├── convention-optimization.md   # 底层约定优化（需手动应用）
├── optimization-report.md
└── verify.sh                # 验证脚本
```

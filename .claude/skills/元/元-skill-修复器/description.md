# Skill 修复器

## 描述
自动化诊断和修复 Skill 配置问题的工具。检查目标 skill 目录的结构、语法、约定遵守情况，生成修复方案并验证结果。

## 能力范围
- 诊断 Skill 目录结构完整性
- 检测 YAML/JSON 格式问题
- 验证是否遵守底层约定
- 检查工具调用合法性
- 生成可执行的修复方案
- 验证修复后的输出条件

## 使用方法

### 基本用法
```
/skill-修复器 <target-skill-path>
```

### 选项
- `--apply` - 自动应用修复（默认仅生成方案）
- `--output-dir` - 指定输出目录（默认: 自身 output/）
- `--verbose` - 显示详细诊断过程

## 输出

修复方案将存储在 `output/` 文件夹中，包含：
1. `diagnosis.json` - 问题诊断详情
2. `fix-plan.md` - 修复方案说明
3. `verification.json` - 验证结果

## Limitations

- 不修改 `underlying-convention.md`
- 不修复正在运行的本 skill 自身
- 自动修复可能导致意外行为，建议先审查方案
- 复杂逻辑问题需要人工介入
- 无法验证动态生成的错误

## 使用示例

```bash
# 仅诊断
/skill-修复器 ~/.claude/skills/my-skill

# 自动修复
/skill-修复器 ~/.claude/skills/my-skill --apply

# 详细输出
/skill-修复器 ~/.claude/skills/my-skill --verbose
```

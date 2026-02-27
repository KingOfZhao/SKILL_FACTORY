# Skill 修复器

自动化诊断和修复 Skill 配置问题。

## 使用方法

输入 skill 目录路径，即可自动诊断问题并生成修复方案。

### 命令格式
```
skill-修复器 <target-skill-path> [options]
```

### 选项
- `--apply` - 自动应用修复
- `--output-dir` - 指定输出目录
- `--verbose` - 显示详细过程

## 输出位置

修复方案记录在 `output/` 目录：
- `diagnosis.json` - 问题诊断
- `fix-plan.md` - 修复方案
- `verification.json` - 验证结果

## Limitations

- 不修改 `underlying-convention.md`
- 不修复本 skill 自身
- 自动修复需谨慎
- 复杂问题需人工介入

# Skill 优化器

## 描述
基于修复 skill 的输出结果，分析模式并拓展对应类型的 skill 以及增强修复器的能力。

## 能力范围
- 解析修复历史 (diagnosis.json)
- 识别问题模式和频次
- 拓展相关类型的 skill
- 增强修复器检测维度
- 生成优化方案
- 评估优化效果

## 使用方法

### 基本用法
```
/skill-优化器 <fixer-output-dir> [options]
```

### 选项
- `--extend-types <list>` - 指定要拓展的 skill 类型（逗号分隔）
- `--enhance-fixer` - 同时生成修复器增强方案
- `--max-skills <n>` - 最大生成 skill 数量（默认: 3）
- `--output-dir` - 指定输出目录（默认: 自身 output/）

## 输出

优化方案将存储在 `output/` 文件夹中，包含：
1. `analysis.json` - 修复历史分析
2. `extension-plans/` - 拓展 skill 方案
3. `fixer-enhancement.md` - 修复器增强方案
4. `optimization-report.md` - 优化效果报告

## 拓展类型支持

| 类型 | 说明 | 示例 |
|-----|------|------|
| validator | 验证器 | 严格验证 vs 轻量检查 |
| formatter | 格式化器 | 自动格式化、规范化 |
| compliance | 合规检查器 | 检查合规性并报告 |
| dependency | 依赖分析器 | 分析依赖关系 |
| profiler | 性能分析器 | 分析执行性能 |
| doc-gen | 文档生成器 | 从 skill 生成文档 |
| test-gen | 测试生成器 | 生成测试用例 |

## Limitations

- 不修改 underlying-convention.md
- 不修改正在运行的 skill 自身
- 不直接应用优化，仅生成方案
- 依赖修复结果的完整性和准确性
- 复杂优化需人工介入

## 使用示例

```bash
# 基本优化
/skill-优化器 ~/.claude/skills/skill-修复器/output/target-skill

# 指定拓展类型
/skill-优化器 ~/.claude/skills/skill-修复器/output/target-skill --extend-types validator,formatter

# 同时增强修复器
/skill-优化器 ~/.claude/skills/skill-修复器/output/target-skill --enhance-fixer
```

# Skill 优化器

基于修复 skill 的输出结果，分析模式并拓展相关 skill。

## 使用方法

输入修复结果目录路径，自动分析并生成优化方案。

### 命令格式
```
skill-优化器 <fixer-output-dir> [options]
```

### 选项
- `--extend-types <list>` - 指定拓展类型（逗号分隔）
- `--enhance-fixer` - 生成修复器增强方案
- `--max-skills <n>` - 最大生成数（默认: 3）
- `--output-dir` - 输出目录

## 支持的拓展类型

- validator - 验证器
- formatter - 格式化器
- compliance - 合规检查器
- dependency - 依赖分析器
- profiler - 性能分析器
- doc-gen - 文档生成器
- test-gen - 测试生成器

## 输出位置

优化方案记录在 `output/` 目录：
- `analysis.json` - 分析结果
- `extension-plans/` - 拓展方案
- `fixer-enhancement.md` - 修复器增强
- `optimization-report.md` - 优化报告

## Limitations

- 不修改底层约定
- 不修改自身
- 不直接应用优化
- 依赖修复结果质量

---
name: skill-optimizer
description: 基于修复 skill 的诊断结果，分析模式并拓展对应类型的 skill 以及增强修复器的能力。
---

# Skill 优化器 (v2.0 - 10分钟可验证优化版)

## 能力定义

基于修复 skill 的诊断结果，执行以下优化：

1. **修复历史分析**
   - 解析 diagnosis.json
   - 提取问题模式和频次
   - 识别高频问题

2. **Skill 类型拓展**
   - 根据问题类型推荐拓展 skill
   - 生成拓展 skill 的框架
   - 提供具体优化建议

3. **修复器能力增强**
   - 新增检测维度
   - 改进修复逻辑
   - 优化输出格式

4. **效果评估**
   - 对比优化前后指标
   - 预估改进幅度
   - 生成评估报告

## 执行前必须读取
common/underlying-convention.md

## 执行流程（8 步骤）
\`\`\`
1. 验证输入路径存在
2. 读取 diagnosis.json
3. 分析问题模式和频次
4. 根据问题类型推荐拓展
5. 生成拓展 skill 方案
6. 生成修复器增强方案（如指定）
7. 评估优化效果
8. 输出优化报告
\`\`\`

## 输出格式

output/ 目录包含：
- \`analysis.json\` - 分析详情
- \`extension-plans/\` - 拓展方案目录
- \`fixer-enhancement.md\` - 修复器增强
- \`optimization-report.md\` - 优化报告
- \`verify.sh\` - 自带验证脚本

## 10 分钟快速验证指南

### 验证步骤

1. **运行优化器**（<2 分钟）
   \`\`\`/skill-优化er <fixer-output-dir>\`\`\`

2. **检查输出结构**（<2 分钟）
   \`\`\`ls output/\`\`\`
   # 确认包含: analysis.json, extension-plans/, fixer-enhancement.md, optimization-report.md

3. **验证 JSON 格式**（<2 分钟）
   \`\`\`cat analysis.json | jq empty\`\`\`
   # 预期: 无语法错误

4. **运行自带验证**（<2 分钟）
   \`\`\`cd output/ && ./verify.sh\`\`\`
   # 预期: 所有检查通过

5. **检查成功标志**（<2 分钟）
   # 查看 optimization-report.md 底部
   # 预期: "✓ 所有检查通过"

**总耗时：≤ 10 分钟**

成功标志：1) output/ 目录结构完整，2) JSON 格式正确，3) verify.sh 所有检查通过，4) 报告含成功标志。

### 快速检查方式

| 检查项 | 命令 | 预期结果 |
|-------|------|---------|
| 目录结构 | \`ls output/\` | 包含 4+ 个文件 |
| JSON 格式 | \`jq < analysis.json\` | 无语法错误 |
| 拓展方案 | \`ls extension-plans/\` | 至少 1 个方案 |
| 验证脚本 | \`./verify.sh\` | 全部通过 |

### 失败场景

- **输入目录无效** → 错误："输入目录不是有效的修复结果"
- **JSON 格式错误** → 报告：含具体行号和原因
- **输出不完整** → 警告："部分文件未生成，请检查日志"

## 自带校验机制

### 1. JSON Checksum
analysis.json 生成时自动计算 checksum：
\`\`\`bash
echo '{"checksum": "'"$(sha256sum analysis.json 2>/dev/null | cut -d' ' -f1)"'"}' > analysis-checksum.json
\`\`\`

### 2. 验证脚本 verify.sh
自动检查：
\`\`\`bash
# 检查点
- [ ] analysis.json 存在
- [ ] JSON 格式正确 (jq empty)
- [ ] 包含必需字段
- [ ] extension-plans/ 目录存在
- [ ] fixer-enhancement.md 存在
- [ ] optimization-report.md 存在
- [ ] checksum 文件存在
\`\`\`

### 3. 成功标志
optimization-report.md 末尾必须包含：
\`\`\`
---
## 验证结果

✓ **所有检查通过**
生成时间: [ISO8601]
checksum: [SHA256]
\`\`\`

## Limitations（必须声明）

- 本 Skill 只负责生成优化方案，不负责直接应用优化
- 优化建议质量依赖输入的 diagnosis.json
- 复杂优化需人工介入和决策
- 10 分钟验证仅检查输出文件结构和格式，不验证内容正确性
- 不修改 underlying-convention.md
- 不修改正在运行的 skill 自身
- 依赖修复器的诊断结果质量

## 使用方法

### 基本用法
\`\`\`
/skill-优化器 <fixer-output-dir>
\`\`\`

### 指定拓展类型
\`\`\`
/skill-优化器 <dir> --extend-types validator,formatter
\`\`\`

### 同时增强修复器
\`\`\`
/skill-优化器 <dir> --enhance-fixer
\`\`\`

### 验证输出
\`\`\`
/skill-优化器 <dir> --verify
\`\`\`

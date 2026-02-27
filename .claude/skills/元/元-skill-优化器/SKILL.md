# 元-Skill 优化器 (Skill-Optimizer)

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

## 支持的拓展类型

### validator（验证器）
- 严格验证：完整检查所有规则
- 轻量检查：快速检查核心规则
- 增量验证：仅检查变更部分

### formatter（格式化器）
- 自动格式化 YAML/JSON
- 规范化 markdown 格式
- 统一代码风格

### compliance（合规检查器）
- 检查 SKILL.md 行数
- 验证命名约定
- 检查错误处理

### dependency（依赖分析器）
- 分析工具使用统计
- 检测未使用的依赖
- 识别循环依赖

### profiler（性能分析器）
- 分析脚本执行时间
- 检测性能瓶颈
- 提供优化建议

### doc-gen（文档生成器）
- 从 SKILL.md 生成 README
- 生成 API 文档
- 生成使用示例

### test-gen（测试生成器）
- 生成单元测试
- 生成集成测试
- 生成边界用例

## 执行流程

```
1. 验证输入路径存在
2. 读取 diagnosis.json
3. 分析问题模式和频次
4. 根据问题类型推荐拓展
5. 生成拓展 skill 方案
6. 生成修复器增强方案（如指定）
7. 评估优化效果
8. 输出优化报告
```

## 输出格式

output/ 目录包含：
- `analysis.json` - 分析详情
- `extension-plans/` - 拓展方案目录
- `fixer-enhancement.md` - 修复器增强
- `optimization-report.md` - 优化报告
- `verify.sh` - 自带验证脚本

## 10 分钟快速验证指南

### 验证步骤

1. **运行优化器**（<2 分钟）
   ```bash
   /skill-优化器 <fixer-output-dir>
   ```

2. **检查输出结构**（<2 分钟）
   ```bash
   ls -la output/
   # 确认包含: analysis.json, extension-plans/, fixer-enhancement.md, optimization-report.md
   ```

3. **验证 JSON 格式**（<2 分钟）
   ```bash
   cat analysis.json | jq empty
   # 预期: 无语法错误
   ```

4. **运行自带验证**（<2 分钟）
   ```bash
   cd output/
   ./verify.sh
   # 预期: 所有检查通过
   ```

5. **检查成功标志**（<2 分钟）
   ```bash
   # 查看 optimization-report.md 底部
   # 预期: "✓ 所有检查通过"
   ```

**总耗时：≤ 10 分钟**

成功标志：1) output/ 目录结构完整，2) JSON 格式正确，3) verify.sh 所有检查通过，4) 报告含成功标志。

### 快速检查方式

| 检查项 | 命令 | 预期结果 |
|-------|------|---------|
| 目录结构 | `ls output/` | 包含 4+ 个文件 |
| JSON 格式 | `jq < analysis.json` | 无语法错误 |
| 拓展方案 | `ls extension-plans/` | 至少 1 个方案 |
| 验证脚本 | `./verify.sh` | 全部通过 |

### 失败场景

- **输入目录无效** → 错误："输入目录不是有效的修复结果"
- **JSON 格式错误** → 报告：含具体行号和原因
- **输出不完整** → 警告："部分文件未生成，请检查日志"

## 自带校验机制

### 1. JSON Checksum
analysis.json 生成时自动计算 checksum：
```bash
echo '{"checksum": "'"$(sha256sum analysis.json 2>/dev/null | cut -d' ' -f1)"'"}' > analysis-checksum.json
```

### 2. 验证脚本 verify.sh
自动检查：
```bash
# 检查点
- [ ] analysis.json 存在
- [ ] JSON 格式正确 (jq empty)
- [ ] 包含必需字段
- [ ] extension-plans/ 目录存在
- [ ] fixer-enhancement.md 存在
- [ ] optimization-report.md 存在
- [ ] checksum 文件存在
```

### 3. 成功标志
optimization-report.md 末尾必须包含：
```
---
## 验证结果

✓ **所有检查通过**
生成时间: [ISO8601]
checksum: [SHA256]
```

## Limitations
- `extension-plans/` - 拓展方案目录
- `fixer-enhancement.md` - 修复器增强
- `optimization-report.md` - 优化报告

## Limitations

- 不修改 underlying-convention.md
- 不修改正在运行的 skill 自身
- 不直接应用优化
- 依赖修复结果质量
- 复杂优化需人工介入

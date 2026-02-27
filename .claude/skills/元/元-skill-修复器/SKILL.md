# 元-Skill 修复器 (Skill-Fixer)

## 能力定义

检查目标 skill 目录是否存在以下问题，并生成修复方案：

1. **结构完整性检查**
   - SKILL.md 是否存在
   - description.md 是否存在
   - 必需的 scripts/ 目录
   - 符合命名约定（kebab-case）

2. **语法格式检查**
   - YAML 语法错误
   - JSON 格式错误
   - Markdown 格式问题

3. **约定遵守检查**
   - 是否违反 underlying-convention.md
   - SKILL.md 是否超过 400 行
   - 脚本是否有完整错误处理

4. **工具调用检查**
   - 使用了不存在的工具
   - 工具参数不正确
   - 工具使用不合法

5. **输出验证**
   - 检查修复后是否满足 skill 的输出条件
   - 验证文件结构完整性

## 执行流程

```
1. 验证目标路径存在
2. 读取底层约定
3. 扫描目标目录结构
4. 执行各项检查
5. 生成修复方案
6. 应用修复（如指定 --apply）
7. 验证结果
8. 记录到 output/
```

## 输出格式

output/ 目录包含：
- `diagnosis.json` - 诊断详情
- `fix-plan.md` - 修复方案
- `verification.json` - 验证结果

## Limitations

- 不修改 underlying-convention.md
- 不修复本 skill 自身
- 自动修复需谨慎使用
- 复杂问题需人工介入

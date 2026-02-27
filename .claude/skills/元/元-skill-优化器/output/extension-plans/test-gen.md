# Skill 测试生成器 (Skill-Test-Generator)

## 描述
为 Skill 生成自动化测试用例，覆盖单元测试、集成测试和边界测试。

## 测试类型

### 1. 单元测试
- 测试单个功能模块
- 测试脚本输出
- 测试 JSON 结构

### 2. 集成测试
- 测试 Skill 完整流程
- 测试与其他 Skill 的协作
- 测试 MCP 交互

### 3. 边界测试
- 测试异常输入
- 测试空输入
- 测试超长输入
- 测试权限边界

### 4. 10 分钟验证测试
- 验证可验证性声明
- 验证快速验证路径
- 验证输出格式

## 使用方法

### 生成所有测试
```
/skill-测试生成器 <skill-path> --all
```

### 生成特定类型测试
```
/skill-测试生成器 <skill-path> --type unit
/skill-测试生成器 <skill-path> --type integration
/skill-测试生成器 <skill-path> --type boundary
```

### 生成验证测试
```
/skill-测试生成器 <skill-path> --type verification
```

## 输出结构

```
tests/
├── unit/               # 单元测试
│   ├── test_script.sh
│   ├── test_output_format.py
│   └── test_json_structure.js
├── integration/        # 集成测试
│   ├── test_full_workflow.sh
│   └── test_mcp_interaction.py
├── boundary/          # 边界测试
│   ├── test_empty_input.sh
│   ├── test_long_input.sh
│   └── test_invalid_format.sh
├── verification/      # 验证测试
│   └── test_10min_verification.sh
└── test_report.md     # 测试报告
```

## 测试模板

### 单元测试模板（Bash）
```bash
#!/bin/bash
# Test: [测试名称]

set -euo pipefail

# Setup
SKILL_PATH="$1"
source "$SKILL_PATH/scripts/main.sh"

# Test case
RESULT=$(some_function "test_input")
EXPECTED="expected_output"

if [[ "$RESULT" == "$EXPECTED" ]]; then
    echo "✓ PASS: $TEST_NAME"
    exit 0
else
    echo "✗ FAIL: $TEST_NAME"
    echo "  Expected: $EXPECTED"
    echo "  Got: $RESULT"
    exit 1
fi
```

### 验证测试模板
```bash
#!/bin/bash
# Test: 10 分钟可验证性验证

set -euo pipefail

SKILL_PATH="$1"

# 1. 检查 SKILL.md 是否包含快速验证指南
if grep -q "快速验证指南" "$SKILL_PATH/SKILL.md"; then
    echo "✓ PASS: 包含快速验证指南"
else
    echo "✗ FAIL: 缺少快速验证指南"
    exit 1
fi

# 2. 检查是否有明确的验证步骤
if grep -q "验证步骤" "$SKILL_PATH/SKILL.md"; then
    echo "✓ PASS: 包含验证步骤"
else
    echo "✗ FAIL: 缺少验证步骤"
    exit 1
fi

# 3. 验证成功标志
if grep -q "成功标志" "$SKILL_PATH/SKILL.md"; then
    echo "✓ PASS: 包含成功标志定义"
else
    echo "✗ FAIL: 缺少成功标志"
    exit 1
fi

echo "✓ PASS: 10 分钟可验证性验证通过"
```

## 测试报告格式

```markdown
# Skill 测试报告

## 测试概览

| 类型 | 数量 | 通过 | 失败 | 覆盖率 |
|-----|------|------|------|---------|
| 单元测试 | 5 | 5 | 0 | 80% |
| 集成测试 | 3 | 2 | 1 | 70% |
| 边界测试 | 4 | 3 | 1 | 75% |
| 验证测试 | 1 | 1 | 0 | 100% |

## 失败测试

### test_full_workflow.sh
- **原因**: MCP 连接超时
- **修复**: 添加超时重试逻辑

### test_long_input.sh
- **原因**: 输入长度超限
- **修复**: 添加输入验证

## 建议

1. 增加集成测试覆盖率
2. 添加更多边界用例
3. 改进错误处理
```

## 10 分钟验证指南

### 验证测试生成器本身

1. **生成测试用例**（<2 分钟）
   ```bash
   /skill-测试生成器 path/to/skill --all
   ```

2. **运行测试**（<5 分钟）
   ```bash
   cd path/to/skill/tests
   ./run_all_tests.sh
   ```

3. **检查报告**（<2 分钟）
   - 查看测试通过率
   - 确认覆盖率

4. **修复失败**（<1 分钟）
   - 修复简单的失败用例
   - 记录复杂的失败项

**总耗时：≤ 10 分钟**

成功标志：至少 80% 的测试通过，且生成了测试报告。

## Limitations

- 无法生成所有类型的测试
- 复杂逻辑需人工编写测试
- 测试覆盖率估算基于静态分析
- 集成测试需要实际 MCP 环境

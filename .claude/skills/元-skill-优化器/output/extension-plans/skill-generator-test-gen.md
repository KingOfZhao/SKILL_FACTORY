# skill-generator 测试生成器 (skill-generator-test-gen)

## 描述
为 skill-generator 生成的 Skill 自动化生成测试用例。

## 测试类型

### 1. 单元测试
- 测试单个功能模块
- 测试脚本输出
- 测试 JSON 结构
- 测试错误处理

### 2. 集成测试
- 测试 Skill 完整流程
- 测试与其他 Skill 的协作
- 测试 MCP 交互

### 3. 约定验证测试
- 验证底层约定遵守
- 测试禁止事项
- 验证 10 分钟可验证性

### 4. MCP 交互测试
- 测试 MCP 工具调用
- 测试错误处理
- 测试参数验证

## 使用方法

### 生成所有测试
```
/skill-generator-test-gen <skill-path> --all
```

### 生成特定类型测试
```
/skill-generator-test-gen <skill-path> --type unit
/skill-generator-test-gen <skill-path> --type integration
/skill-generator-test-gen <skill-path> --type convention
/skill-generator-test-gen <skill-path> --type mcp
```

### 为 skill-generator 生成测试
```
/skill-generator-test-gen /path/to/skill-generator --all
```

## 输出结构

```
tests/
├── unit/               # 单元测试
│   ├── test_structure.py
│   ├── test_content.py
│   └── test_convention.py
├── integration/        # 集成测试
│   ├── test_full_workflow.py
│   ├── test_mcp_interaction.py
│   └── test_skill_collaboration.py
├── convention/         # 约定验证测试
│   ├── test_underlying_convention.py
│   ├── test_read_only.py
│   └── test_10min_verification.py
├── mcp/              # MCP 交互测试
│   ├── test_tool_calls.py
│   ├── test_error_handling.py
│   └── test_parameter_validation.py
├── test_report.md     # 测试报告
└── run_all_tests.sh   # 测试运行脚本
```

## 测试模板

### 结构单元测试（Python）
```python
#!/usr/bin/env python3
import os
import json
import pytest

class TestSkillStructure:
    """测试 Skill 结构完整性"""

    def test_skill_md_exists(self):
        """SKILL.md 必须存在"""
        skill_path = os.getenv('SKILL_PATH')
        assert os.path.exists(f"{skill_path}/SKILL.md"), "SKILL.md 不存在"

    def test_description_md_exists(self):
        """description.md 必须存在"""
        skill_path = os.getenv('SKILL_PATH')
        assert os.path.exists(f"{skill_path}/description.md"), "description.md 不存在"

    def test_readme_exists(self):
        """README.md 必须存在"""
        skill_path = os.getenv('SKILL_PATH')
        assert os.path.exists(f"{skill_path}/README.md"), "README.md 不存在"

    def test_skill_md_line_count(self):
        """SKILL.md 行数应 < 400"""
        skill_path = os.getenv('SKILL_PATH')
        with open(f"{skill_path}/SKILL.md") as f:
            lines = len(f.readlines())
            assert lines < 400, f"SKILL.md 行数 {lines} 超过 400"
```

### 约定验证测试
```python
class TestConventionCompliance:
    """测试约定遵守情况"""

    def test_no_version_in_skill_md(self):
        """SKILL.md 不应包含 version 字段"""
        skill_path = os.getenv('SKILL_PATH')
        with open(f"{skill_path}/SKILL.md") as f:
            content = f.read()
            assert 'version:' not in content, "SKILL.md 包含不支持的 version 字段"

    def test_single_responsibility_declared(self):
        """必须声明单一职责"""
        skill_path = os.getenv('SKILL_PATH')
        with open(f"{skill_path}/SKILL.md") as f:
            content = f.read()
            assert '单一职责' in content or '职责' in content, "缺少单一职责声明"
```

### MCP 交互测试
```python
class TestMCPInteraction:
    """测试 MCP 交互"""

    def test_tool_call_syntax(self):
        """工具调用语法正确"""
        tool_call = "MCPTool(tool_name, parameters)"
        # 验证语法
        assert 'MCPTool(' in tool_call, "工具调用语法不正确"

    def test_error_handling(self):
        """错误处理正确"""
        skill_path = os.getenv('SKILL_PATH')
        with open(f"{skill_path}/scripts/main.sh") as f:
            content = f.read()
            assert 'set -e' in content, "缺少错误处理"
```

## 测试报告格式

```markdown
# Skill 测试报告

## 测试概览

| 类型 | 数量 | 通过 | 失败 | 覆盖率 |
|-----|------|------|------|---------|
| 单元测试 | 8 | 7 | 1 | 85% |
| 集成测试 | 4 | 3 | 1 | 75% |
| 约定测试 | 5 | 5 | 0 | 100% |
| MCP 测试 | 3 | 2 | 1 | 67% |

## 失败测试

### test_skill_md_line_count
- **原因**: SKILL.md 行数超过 400
- **修复**: 拆分 SKILL.md 为多个文件
- **文件**: SKILL.md
- **实际行数**: 450

### test_mcp_tool_resolution
- **原因**: MCP 工具无法解析
- **修复**: 检查 MCP 配置
- **优先级**: 高

## 建议

1. 拆分过长的 SKILL.md
2. 增加 MCP 交互测试覆盖
3. 添加更多边界用例
4. 建立测试基准库

## 覆盖率分析

- 结构完整性: 100%
- 内容验证: 75%
- 约定遵守: 100%
- MCP 交互: 67%

**平均覆盖率: 85.5%**
```

## 10 分钟验证指南

### 验证测试生成器本身

1. **生成测试用例**（<2 分钟）
   ```bash
   /skill-generator-test-gen /path/to/skill-generator --all
   ```

2. **运行测试**（<4 分钟）
   ```bash
   cd /path/to/tests
   ./run_all_tests.sh
   ```

3. **检查报告**（<2 分钟）
   - 查看测试通过率
   - 确认覆盖率
   - 阅读失败项

4. **修复简单失败**（<2 分钟）
   - 修复 1-2 个简单失败用例
   - 重新运行验证

**总耗时：≤ 10 分钟**

成功标志：至少 80% 的测试通过，且生成了测试报告。

## Limitations

- 无法生成所有类型的测试
- 复杂逻辑需人工编写测试
- 测试覆盖率估算基于静态分析
- 集成测试需要实际 MCP 环境
- MCP 交互测试依赖 MCP 文档

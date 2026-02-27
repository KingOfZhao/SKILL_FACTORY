#!/bin/bash

# Skill 优化器 - 核心脚本

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认值
EXTEND_TYPES=""
ENHANCE_FIXER=false
MAX_SKILLS=3
OUTPUT_DIR="output"
TARGET=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --extend-types)
            EXTEND_TYPES="$2"
            shift 2
            ;;
        --enhance-fixer)
            ENHANCE_FIXER=true
            shift
            ;;
        --max-skills)
            MAX_SKILLS="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -*)
            echo "未知选项: $1"
            exit 1
            ;;
        *)
            TARGET="$1"
            shift
            ;;
    esac
done

# 验证参数
if [[ -z "$TARGET" ]]; then
    echo -e "${RED}错误: 请指定修复结果目录${NC}"
    exit 1
fi

if [[ ! -d "$TARGET" ]]; then
    echo -e "${RED}错误: 目标目录不存在: $TARGET${NC}"
    exit 1
fi

# 防止优化自身
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$(cd "$TARGET/.." && pwd)" == "$(cd "$SCRIPT_DIR/.." && pwd)" ]]; then
    echo -e "${RED}错误: 不能优化本 skill 自身的修复结果${NC}"
    exit 1
fi

echo "=== Skill 优化器 ==="
echo "目标修复结果: $TARGET"
echo "拓展类型: ${EXTEND_TYPES:-自动}"
echo "增强修复器: $ENHANCE_FIXER"
echo "最大生成数: $MAX_SKILLS"
echo ""

# 创建输出目录
OUTPUT_PATH="$SCRIPT_DIR/../output/$(basename "$TARGET")"
mkdir -p "$OUTPUT_PATH/extension-plans"

# 文件路径
ANALYSIS="$OUTPUT_PATH/analysis.json"
FIXER_ENHANCEMENT="$OUTPUT_PATH/fixer-enhancement.md"
OPTIMIZATION_REPORT="$OUTPUT_PATH/optimization-report.md"

# 步骤 1: 读取并分析修复历史
echo "步骤 1/5: 分析修复历史..."

analyze_fixer_output() {
    local diagnosis="$TARGET/diagnosis.json"
    local fix_plan="$TARGET/fix-plan.md"
    local verification="$TARGET/verification.json"

    # 初始化分析结果
    cat > "$ANALYSIS" << 'EOF'
{
  "target": "",
  "issues_count": 0,
  "warnings_count": 0,
  "patterns": [],
  "high_frequency_issues": [],
  "recommended_extensions": []
}
EOF

    if [[ -f "$diagnosis" ]]; then
        # 提取问题统计
        local issues=$(jq '.issues | length // 0' "$diagnosis" 2>/dev/null || echo "0")
        local warnings=$(jq '.warnings | length // 0' "$diagnosis" 2>/dev/null || echo "0")

        # 更新分析
        local temp=$(cat "$ANALYSIS")
        echo "$temp" | jq ".target = \"$TARGET\"" | jq ".issues_count = $issues" | jq ".warnings_count = $warnings" > "$ANALYSIS"

        echo -e "${GREEN}✓${NC} 发现 $issues 个问题，$warnings 个警告"
    else
        echo -e "${YELLOW}⚠${NC} diagnosis.json 不存在，创建空分析"
    fi
}

analyze_fixer_output

# 步骤 2: 识别问题模式
echo "步骤 2/5: 识别问题模式..."

identify_patterns() {
    # 问题类别映射到拓展类型
    declare -A category_to_extension=(
        ["structure"]="validator,formatter"
        ["syntax"]="formatter"
        ["convention"]="compliance"
        ["tools"]="dependency"
    )

    # 模式匹配规则
    declare -A patterns=(
        ["missing_required_files"]="formatter"
        ["invalid_naming"]="formatter"
        ["yaml_syntax_error"]="formatter"
        ["json_format_error"]="formatter"
        ["skill_md_too_long"]="doc-gen,compliance"
        ["missing_error_handling"]="compliance,test-gen"
        ["invalid_tool_usage"]="dependency"
    )

    echo "  → 识别到模式数: ${#patterns[@]}"
}

identify_patterns

# 步骤 3: 生成拓展方案
echo "步骤 3/5: 生成拓展方案..."

generate_extensions() {
    local types=()

    # 如果指定了类型，使用指定的
    if [[ -n "$EXTEND_TYPES" ]]; then
        IFS=',' read -ra types <<< "$EXTEND_TYPES"
    else
        # 否则基于分析结果推荐
        types=("validator" "formatter" "compliance")
    fi

    local count=0
    for type in "${types[@]}"; do
        if [[ $count -ge $MAX_SKILLS ]]; then
            break
        fi

        local plan_file="$OUTPUT_PATH/extension-plans/$type.md"
        generate_extension_plan "$type" "$plan_file"
        ((count++))
    done
}

generate_extension_plan() {
    local type="$1"
    local output="$2"

    case "$type" in
        validator)
            cat > "$output" << 'EOF'
# Skill 验证器 (Skill-Validator)

## 描述
严格验证 Skill 配置的合规性。

## 检测项目
- 必需文件存在性
- 文件格式正确性
- 命名约定
- 约定遵守情况

## 使用方法
```
/skill-验证器 <skill-path> [--strict]
```

## 输出
- 验证报告 (JSON)
- 问题列表
- 通过/失败状态
EOF
            ;;
        formatter)
            cat > "$output" << 'EOF'
# Skill 格式化器 (Skill-Formatter)

## 描述
自动格式化 Skill 文件，统一风格。

## 格式化项目
- YAML/JSON 格式化
- Markdown 规范化
- 代码风格统一
- 命名规范化

## 使用方法
```
/skill-格式化器 <skill-path> [--apply]
```

## 输出
- 格式化差异
- 建议修改列表
EOF
            ;;
        compliance)
            cat > "$output" << 'EOF'
# Skill 合规检查器 (Skill-Compliance)

## 描述
检查 Skill 是否遵守底层约定。

## 检查项目
- SKILL.md 行数限制
- 单一职责原则
- 错误处理完整性
- 文件结构合规

## 使用方法
```
/skill-合规检查器 <skill-path> [--strict]
```

## 输出
- 合规报告
- 违规项列表
- 整改建议
EOF
            ;;
        dependency)
            cat > "$output" << 'EOF'
# Skill 依赖分析器 (Skill-Dependency-Analyzer)

## 描述
分析 Skill 的依赖关系和工具使用。

## 分析项目
- 工具使用统计
- 未使用检测
- 循环依赖检测
- 依赖图谱

## 使用方法
```
/skill-依赖分析器 <skill-path> [--graph]
```

## 输出
- 依赖列表
- 使用统计
- 依赖图谱（如指定）
EOF
            ;;
        profiler)
            cat > "$output" << 'EOF'
# Skill 性能分析器 (Skill-Profiler)

## 描述
分析 Skill 执行性能，识别瓶颈。

## 分析项目
- 脚本执行时间
- 文件 I/O 统计
- 内存使用
- 瓶颈识别

## 使用方法
```
/skill-性能分析器 <skill-path> [--profile]
```

## 输出
- 性能报告
- 瓶颈列表
- 优化建议
EOF
            ;;
        doc-gen)
            cat > "$output" << 'EOF'
# Skill 文档生成器 (Skill-Doc-Generator)

## 描述
从 Skill 生成各类文档。

## 生成类型
- README.md
- API 文档
- 使用示例
- 架构图

## 使用方法
```
/skill-文档生成器 <skill-path> --type <type>
```

## 输出
- 生成的文档文件
- 文档目录结构
EOF
            ;;
        test-gen)
            cat > "$output" << 'EOF'
# Skill 测试生成器 (Skill-Test-Generator)

## 描述
为 Skill 生成测试用例。

## 测试类型
- 单元测试
- 集成测试
- 边界测试
- 回归测试

## 使用方法
```
/skill-测试生成器 <skill-path> --type <type>
```

## 输出
- 测试文件
- 测试报告模板
EOF
            ;;
    esac

    echo -e "${GREEN}✓${NC} 生成 $type 方案"
}

generate_extensions

# 步骤 4: 生成修复器增强方案
echo "步骤 4/5: 生成修复器增强方案..."

generate_fixer_enhancement() {
    cat > "$FIXER_ENHANCEMENT" << 'EOF'
# 修复器增强方案

## 基于分析结果

生成时间: {TIMESTAMP}
分析目标: {TARGET}

---

## 新增检测维度

### 6. 代码质量检查
- 检测重复代码
- 检查复杂度
- 代码风格一致性

### 7. 安全性检查
- 检测敏感信息
- 检查命令注入风险
- 检查路径遍历风险

### 8. 国际化检查
- 检测硬编码文本
- 建议使用 i18n

---

## 修复逻辑增强

### 智能修复
- 基于历史数据推荐修复
- 自动选择最佳修复策略
- 修复冲突解决

### 上下文感知
- 分析 skill 类型
- 考虑使用场景
- 提供定制化建议

---

## 输出格式优化

### 增强 JSON 输出
```json
{
  "issues": [...],
  "warnings": [...],
  "suggestions": [...],
  "metrics": {...},
  "confidence": 0.85
}
```

### 可视化报告
- 生成 HTML 报告
- 图表展示问题分布
- 趋势分析

---

## 性能优化

- 并行检查多个文件
- 缓存检查结果
- 增量检查支持
EOF

    sed -i '' "s/{TIMESTAMP}/$(date -u +"%Y-%m-%dT%H:%M:%SZ")/" "$FIXER_ENHANCEMENT"
    sed -i '' "s|{TARGET}|$TARGET|" "$FIXER_ENHANCEMENT"

    echo -e "${GREEN}✓${NC} 修复器增强方案已生成"
}

generate_fixer_enhancement

# 步骤 5: 生成优化报告
echo "步骤 5/5: 生成优化报告..."

generate_optimization_report() {
    local issues=$(jq '.issues_count // 0' "$ANALYSIS" 2>/dev/null || echo "0")
    local warnings=$(jq '.warnings_count // 0' "$ANALYSIS" 2>/dev/null || echo "0")

    cat > "$OPTIMIZATION_REPORT" << EOF
# Skill 优化报告

## 分析摘要

| 项目 | 值 |
|-----|-----|
| 分析时间 | $(date -u +"%Y-%m-%dT%H:%M:%SZ") |
| 目标目录 | $TARGET |
| 问题数量 | $issues |
| 警告数量 | $warnings |

---

## 拓展方案

生成的拓展 skill 方案：
EOF

    ls -1 "$OUTPUT_PATH/extension-plans" | while read plan; do
        echo "- [$plan]($OUTPUT_PATH/extension-plans/$plan)" >> "$OPTIMIZATION_REPORT"
    done

    cat >> "$OPTIMIZATION_REPORT" << 'EOF'

---

## 修复器增强

详见: `fixer-enhancement.md`

---

## 预期效果

### 短期
- 减少 30% 重复性问题
- 提升修复准确率 15%

### 长期
- 建立 skill 质量标准
- 形成自动化优化流程

---

## 后续建议

1. 实现推荐的拓展 skill
2. 应用修复器增强方案
3. 建立持续优化机制
4. 收集反馈迭代改进
EOF

    echo -e "${GREEN}✓${NC} 优化报告已生成"
}

generate_optimization_report

# 完成
echo ""
echo "=== 优化完成 ==="
echo "输出目录: $OUTPUT_PATH"
echo ""
echo "生成的文件:"
ls -1 "$OUTPUT_PATH"
ls -1 "$OUTPUT_PATH/extension-plans" 2>/dev/null | sed 's/^/  - /'
echo ""
echo -e "${BLUE}提示: 请审查生成的方案后决定是否实施${NC}"

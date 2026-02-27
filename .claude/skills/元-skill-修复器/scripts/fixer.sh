#!/bin/bash

# Skill 修复器 - 核心脚本

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认值
APPLY_FIX=false
VERBOSE=false
OUTPUT_DIR="output"
TARGET=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --apply)
            APPLY_FIX=true
            shift
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
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
    echo "错误: 请指定目标 skill 目录"
    exit 1
fi

if [[ ! -d "$TARGET" ]]; then
    echo "错误: 目标目录不存在: $TARGET"
    exit 1
fi

# 防止修复自身
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$(cd "$TARGET" && pwd)" == "$(cd "$SCRIPT_DIR/.." && pwd)" ]]; then
    echo "错误: 不能修复本 skill 自身"
    exit 1
fi

verbose() {
    if [[ "$VERBOSE" == true ]]; then
        echo -e "${YELLOW}[DEBUG]${NC} $*"
    fi
}

echo "=== Skill 修复器 ==="
echo "目标: $TARGET"
echo "自动应用修复: $APPLY_FIX"
echo ""

# 创建输出目录
OUTPUT_PATH="$SCRIPT_DIR/../output/$(basename "$TARGET")"
mkdir -p "$OUTPUT_PATH"

# 初始化诊断 JSON
DIAGNOSIS="$OUTPUT_PATH/diagnosis.json"
FIX_PLAN="$OUTPUT_PATH/fix-plan.md"
VERIFICATION="$OUTPUT_PATH/verification.json"

# 创建诊断对象
echo '{"issues": [], "warnings": [], "summary": ""}' > "$DIAGNOSIS"

# 辅助函数：添加问题
add_issue() {
    local severity="$1"
    local category="$2"
    local message="$3"
    local detail="${4:-}"

    if [[ "$VERBOSE" == true ]]; then
        echo -e "${RED}[${severity^^}]${NC} [$category] $message"
        if [[ -n "$detail" ]]; then
            echo "  → $detail"
        fi
    fi

    # 更新 JSON (简单实现)
    local temp=$(cat "$DIAGNOSIS")
    echo "$temp" | sed "s/\"$severity\"\s*\:\s*\[\]/\"$severity\": [{\"category\": \"$category\", \"message\": \"$message\", \"detail\": \"$detail\"}]/" > "$DIAGNOSIS"
}

# 检查 1: 结构完整性
echo "检查 1/5: 结构完整性..."

check_structure() {
    local required=("SKILL.md" "description.md")
    local optional=("README.md" "scripts" "common" "overlaps" "reference")

    for file in "${required[@]}"; do
        if [[ ! -e "$TARGET/$file" ]]; then
            add_issue "issues" "structure" "缺少必需文件: $file"
        fi
    done

    # 检查目录命名 (kebab-case)
    local dirname=$(basename "$TARGET")
    if [[ "$dirname" =~ [A-Z] ]]; then
        add_issue "warnings" "structure" "目录名称应使用 kebab-case" "当前: $dirname"
    fi
}

check_structure

# 检查 2: 语法格式
echo "检查 2/5: 语法格式..."

check_syntax() {
    # 检查 YAML/JSON 文件
    for file in $(find "$TARGET" -maxdepth 2 -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" \)); do
        if command -v yamllint &> /dev/null && [[ "$file" =~ \.(yaml|yml)$ ]]; then
            if ! yamllint "$file" &> /dev/null; then
                add_issue "issues" "syntax" "YAML 语法错误: $file"
            fi
        fi

        if command -v jq &> /dev/null && [[ "$file" =~ \.json$ ]]; then
            if ! jq empty "$file" &> /dev/null; then
                add_issue "issues" "syntax" "JSON 格式错误: $file"
            fi
        fi
    done
}

check_syntax

# 检查 3: 约定遵守
echo "检查 3/5: 约定遵守..."

check_conventions() {
    # 读取底层约定（假设在 common/underlying-convention.md）
    local convention="$TARGET/common/underlying-convention.md"
    if [[ -f "$convention" ]]; then
        # 检查 SKILL.md 行数
        local skill_md="$TARGET/SKILL.md"
        if [[ -f "$skill_md" ]]; then
            local lines=$(wc -l < "$skill_md")
            if [[ $lines -gt 400 ]]; then
                add_issue "warnings" "convention" "SKILL.md 超过 400 行" "当前: $lines 行"
            fi
        fi
    fi

    # 检查 scripts 目录中的错误处理
    if [[ -d "$TARGET/scripts" ]]; then
        for script in "$TARGET/scripts"/*; do
            if [[ -f "$script" ]]; then
                if ! grep -q "set -e" "$script" && ! grep -q "trap" "$script"; then
                    add_issue "warnings" "convention" "脚本可能缺少错误处理: $script"
                fi
            fi
        done
    fi
}

check_conventions

# 检查 4: 工具调用检查
echo "检查 4/5: 工具调用..."

check_tools() {
    # 常用工具列表（需要根据实际环境调整）
    local common_tools=("Read" "Write" "Edit" "Bash" "Glob" "Grep" "AskUserQuestion")

    local skill_md="$TARGET/SKILL.md"
    if [[ -f "$skill_md" ]]; then
        # 简单检查：查找可能使用了不存在工具的模式
        if grep -q "UseTool" "$skill_md" 2>/dev/null; then
            add_issue "warnings" "tools" "检测到潜在工具调用" "建议人工审查"
        fi
    fi
}

check_tools

# 检查 5: 输出验证
echo "检查 5/5: 输出验证..."

verify_output() {
    local valid=true

    # 验证必需文件存在且可读
    local required=("SKILL.md" "description.md")
    for file in "${required[@]}"; do
        if [[ -f "$TARGET/$file" && -r "$TARGET/$file" ]]; then
            verbose "✓ $file 存在且可读"
        else
            valid=false
            verbose "✗ $file 不可用"
        fi
    done

    echo '{"valid": '$valid', "checked_at": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}' > "$VERIFICATION"
}

verify_output

# 生成修复方案
echo ""
echo "生成修复方案..."

cat > "$FIX_PLAN" << 'EOF'
# Skill 修复方案

## 检查摘要

执行时间: {TIMESTAMP}
目标: {TARGET}

## 问题列表

详见 `diagnosis.json`

## 修复建议

### 结构问题
- 如果缺少必需文件，创建空模板
- 检查目录命名约定

### 语法问题
- 修复 YAML/JSON 格式错误
- 使用在线验证工具辅助

### 约定问题
- 将 SKILL.md 拆分为多个文件（超过 400 行）
- 为脚本添加错误处理

### 工具调用问题
- 人工审查工具使用
- 参考官方文档

## 注意事项

- 修复前请备份原始文件
- 复杂问题建议人工处理
- 修复后请重新验证

EOF

sed -i '' "s/{TIMESTAMP}/$(date -u +"%Y-%m-%dT%H:%M:%SZ")/" "$FIX_PLAN"
sed -i '' "s|{TARGET}|$TARGET|" "$FIX_PLAN"

# 更新摘要
local issue_count=$(cat "$DIAGNOSIS" | jq '.issues | length' 2>/dev/null || echo "0")
local warning_count=$(cat "$DIAGNOSIS" | jq '.warnings | length' 2>/dev/null || echo "0")

echo ""
echo "=== 诊断完成 ==="
echo "发现问题: $issue_count"
echo "警告: $warning_count"
echo ""
echo "输出目录: $OUTPUT_PATH"
echo ""

if [[ "$APPLY_FIX" == true ]]; then
    echo "警告: 自动修复未实现，请手动审查修复方案"
    echo "查看方案: $FIX_PLAN"
else
    echo "修复方案已生成，请审查后手动应用或使用 --apply"
fi

#!/bin/bash

# 元-Skill 检查器 - 核心脚本

# 不使用 set -euo pipefail，因为需要处理空数组情况
set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认值
SKILLS_DIR="/Users/administruter/Desktop/skill_factory/.claude/skills"
OUTPUT_DIR="check-results"
VERBOSE=false
FAILURES_ONLY=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose)
            VERBOSE=true
            shift
            ;;
        --failures-only)
            FAILURES_ONLY=true
            shift
            ;;
        *)
            SKILLS_DIR="$1"
            shift
            ;;
    esac
done

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 验证目录存在
if [[ ! -d "$SKILLS_DIR" ]]; then
    echo -e "${RED}错误: 指定目录不存在: $SKILLS_DIR${NC}"
    exit 1
fi

# 检查文件是否存在且可读
check_file_exists() {
    local file="$1"
    if [[ -f "$file" ]]; then
        return 0
    else
        return 1
    fi
}

# 检查内容是否包含特定字符串
check_content() {
    local file="$1"
    local pattern="$2"
    if [[ -f "$file" ]] && grep -q "$pattern" "$file"; then
        return 0
    else
        return 1
    fi
}

# 检查目录是否有 verify.sh 或类似脚本
check_verify_script() {
    local dir="$1"
    if [[ -f "$dir/verify.sh" ]] || [[ -f "$dir/scripts/verify.sh" ]]; then
        return 0
    else
        return 1
    fi
}

# 检查 SKILL.md 的验证指南
check_verification_guide() {
    local skill_dir="$1"
    local skill_file="$skill_dir/SKILL.md"
    local missing=()

    # 检查是否有 10 分钟快速验证指南章节
    if ! check_content "$skill_file" "10 分钟快速验证指南"; then
        missing+=("缺少 '10 分钟快速验证指南' 章节")
    fi

    # 检查是否有验证步骤
    if ! check_content "$skill_file" "验证步骤"; then
        missing+=("缺少 '验证步骤' 说明")
    fi

    # 检查是否有时间约束
    if ! check_content "$skill_file" "10 分钟" && ! check_content "$skill_file" "≤ 10 分钟"; then
        missing+=("缺少时间约束说明（≤ 10 分钟）")
    fi

    # 检查是否有成功标志
    if ! check_content "$skill_file" "成功标志" && ! check_content "$skill_file" "Success Flag"; then
        missing+=("缺少 '成功标志' 说明")
    fi

    # 检查是否有失败场景
    if ! check_content "$skill_file" "失败场景" && ! check_content "$skill_file" "Failure Scenario"; then
        missing+=("缺少 '失败场景' 说明")
    fi

    # 检查是否有输出验证
    if ! check_content "$skill_file" "预期结果" && ! check_content "$skill_file" "Expected Result"; then
        missing+=("缺少 '预期结果' 说明")
    fi

    # 输出结果（每行一个）
    for item in "${missing[@]:-}"; do
        [[ -n "$item" ]] && echo "$item"
    done
}

# 安全生成 JSON 数组
json_array() {
    local -n arr=$1
    if [[ ${#arr[@]} -eq 0 ]]; then
        echo "[]"
    else
        local result=""
        for item in "${arr[@]}"; do
            # 转义 JSON 字符
            local escaped=$(echo "$item" | sed 's/\\/\\\\/g; s/"/\\"/g')
            if [[ -z "$result" ]]; then
                result="\"$escaped\""
            else
                result="$result,\"$escaped\""
            fi
        done
        echo "[$result]"
    fi
}

# 检查单个 skill
check_skill() {
    local skill_name="$1"
    local skill_dir="$2"

    if [[ "$VERBOSE" == true ]]; then
        echo -e "${BLUE}→${NC} 检查 $skill_name" >&2
    fi

    local status="passed"
    local missing_items=()
    local suggestions=()

    # 1. 检查 SKILL.md 存在
    if ! check_file_exists "$skill_dir/SKILL.md"; then
        status="failed"
        missing_items+=("SKILL.md 文件不存在")
        suggestions+=("创建 SKILL.md 文件")
    fi

    # 2. 检查验证脚本
    if ! check_verify_script "$skill_dir"; then
        status="${status:-warning}"
        missing_items+=("verify.sh 脚本不存在")
        suggestions+=("添加 verify.sh 验证脚本")
    fi

    # 3. 检查 10 分钟验证指南
    if [[ -f "$skill_dir/SKILL.md" ]]; then
        local guide_missing_str
        guide_missing_str=$(check_verification_guide "$skill_dir" 2>/dev/null || true)

        if [[ -n "$guide_missing_str" ]]; then
            while IFS= read -r line; do
                [[ -n "$line" ]] && missing_items+=("$line")
            done <<< "$guide_missing_str"

            if [[ ${#missing_items[@]} -gt 0 ]]; then
                status="${status:-warning}"
                suggestions+=("在 SKILL.md 中添加 '10 分钟快速验证指南' 章节")
            fi
        fi
    fi

    # 输出 verbose 信息到 stderr
    if [[ "$VERBOSE" == true ]]; then
        echo -e "  状态: ${GREEN}$status${NC}" >&2
        if [[ ${#missing_items[@]} -gt 0 ]]; then
            echo -e "  ${YELLOW}缺失项:${NC}" >&2
            printf '    - %s\n' "${missing_items[@]}" >&2
        fi
    fi

    # 生成 JSON 对象（仅输出到 stdout）
    local missing_json
    local suggestions_json

    # 手动构建 JSON 数组
    if [[ ${#missing_items[@]} -eq 0 ]]; then
        missing_json="[]"
    else
        missing_json="["
        local first=true
        for item in "${missing_items[@]}"; do
            local escaped=$(echo "$item" | sed 's/\\/\\\\/g; s/"/\\"/g')
            if [[ "$first" == true ]]; then
                missing_json="$missing_json\"$escaped\""
                first=false
            else
                missing_json="$missing_json, \"$escaped\""
            fi
        done
        missing_json="$missing_json]"
    fi

    if [[ ${#suggestions[@]} -eq 0 ]]; then
        suggestions_json="[]"
    else
        suggestions_json="["
        local first=true
        for item in "${suggestions[@]}"; do
            local escaped=$(echo "$item" | sed 's/\\/\\\\/g; s/"/\\"/g')
            if [[ "$first" == true ]]; then
                suggestions_json="$suggestions_json\"$escaped\""
                first=false
            else
                suggestions_json="$suggestions_json, \"$escaped\""
            fi
        done
        suggestions_json="$suggestions_json]"
    fi

    echo "    {
      \"name\": \"$skill_name\",
      \"path\": \"$skill_dir\",
      \"status\": \"$status\",
      \"missing_items\": $missing_json,
      \"suggestions\": $suggestions_json
    }"
}

# 主流程
main() {
    echo "=== 元-Skill 检查器 ==="
    echo ""
    echo "扫描目录: $SKILLS_DIR"
    echo ""

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local total_skills=0
    local meta_skills_excluded=0
    local non_meta_skills_checked=0
    local passed=0
    local warnings=0
    local failed=0
    local skills_json=""

    # 扫描所有 skill 目录
    for skill_dir in "$SKILLS_DIR"/*; do
        if [[ ! -d "$skill_dir" ]]; then
            continue
        fi

        local skill_name=$(basename "$skill_dir")
        ((total_skills++))

        # 跳过待应用-skill 目录
        if [[ "$skill_name" == "待应用-skill" ]] || [[ "$skill_name" == "common" ]] || [[ "$skill_name" == "output" ]]; then
            continue
        fi

        # 跳过元-前缀的 skill
        if [[ "$skill_name" == 元-* ]]; then
            ((meta_skills_excluded++))
            if [[ "$VERBOSE" == true ]]; then
                echo -e "${YELLOW}→${NC} 跳过 $skill_name (元-skill)"
            fi
            continue
        fi

        # 检查非元-skill
        ((non_meta_skills_checked++))
        local skill_json
        skill_json=$(check_skill "$skill_name" "$skill_dir")

        # 更新统计
        local skill_status
        skill_status=$(echo "$skill_json" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)

        case $skill_status in
            passed)
                ((passed++))
                ;;
            warning)
                ((warnings++))
                ;;
            failed)
                ((failed++))
                ;;
        esac

        # 构建数组（仅在非失败模式下或状态为 failed 时）
        if [[ "$FAILURES_ONLY" == false ]] || [[ "$skill_status" == "failed" ]]; then
            if [[ -z "$skills_json" ]]; then
                skills_json="$skill_json"
            else
                skills_json="$skills_json,$skill_json"
            fi
        fi
    done

    # 生成 JSON 报告
    local json_report
    json_report=$(cat <<EOF
{
  "timestamp": "$timestamp",
  "skills_directory": "$SKILLS_DIR",
  "total_skills": $total_skills,
  "meta_skills_excluded": $meta_skills_excluded,
  "non_meta_skills_checked": $non_meta_skills_checked,
  "summary": {
    "passed": $passed,
    "warnings": $warnings,
    "failed": $failed
  },
  "skills": [$skills_json]
}
EOF
)

    # 输出 JSON 报告
    echo "$json_report" > "$OUTPUT_DIR/skill-compliance-report.json"

    # 格式化输出
    echo ""
    echo "--- 检查结果汇总 ---"
    echo -e "总计: $total_skills 个 skill"
    echo -e "元-skill (跳过): ${YELLOW}$meta_skills_excluded${NC}"
    echo -e "非元-skill (已检查): $non_meta_skills_checked"
    echo ""
    echo -e "通过: ${GREEN}$passed${NC}"
    echo -e "警告: ${YELLOW}$warnings${NC}"
    echo -e "失败: ${RED}$failed${NC}"
    echo ""
    echo -e "${BLUE}输出文件:${NC} $OUTPUT_DIR/skill-compliance-report.json"
    echo ""

    # 检查 jq 可用性并显示格式化输出
    if command -v jq &> /dev/null; then
        echo "--- 详细报告 ---"
        if [[ "$FAILURES_ONLY" == true ]]; then
            echo "$json_report" | jq '.skills[] | select(.status == "failed")'
        else
            echo "$json_report" | jq '.skills[]'
        fi
    fi

    # 验证 JSON 格式
    if command -v jq &> /dev/null; then
        if ! jq empty "$OUTPUT_DIR/skill-compliance-report.json" 2>/dev/null; then
            echo -e "${RED}错误: JSON 格式不正确${NC}"
            cat "$OUTPUT_DIR/skill-compliance-report.json"
            exit 1
        fi
    fi

    # 返回状态码
    if [[ $failed -gt 0 ]]; then
        exit 1
    elif [[ $warnings -gt 0 ]]; then
        exit 0
    else
        echo -e "${GREEN}✅ 所有非元-skill 检查通过${NC}"
        exit 0
    fi
}

# 执行主流程
main "$@"

#!/bin/bash
# 元-Skill 检查器 - 核心脚本

set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILLS_DIR="/Users/administruter/Desktop/skill_factory/.claude/skills"
OUTPUT_DIR="check-results"
VERBOSE=false
FAILURES_ONLY=false

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

mkdir -p "$OUTPUT_DIR"

if [[ ! -d "$SKILLS_DIR" ]]; then
    echo -e "${RED}错误: 指定目录不存在: $SKILLS_DIR${NC}"
    exit 1
fi

check_file_exists() {
    local file="$1"
    if [[ -f "$file" ]]; then
        return 0
    else
        return 1
    fi
}

check_content() {
    local file="$1"
    local pattern="$2"
    if [[ -f "$file" ]] && grep -q "$pattern" "$file"; then
        return 0
    else
        return 1
    fi
}

check_verify_script() {
    local dir="$1"
    if [[ -f "$dir/verify.sh" ]] || [[ -f "$dir/scripts/verify.sh" ]]; then
        return 0
    else
        return 1
    fi
}

check_verification_guide() {
    local skill_dir="$1"
    local skill_file="$skill_dir/SKILL.md"
    local missing=()

    if ! check_content "$skill_file" "10 分钟快速验证指南"; then
        missing+=("缺少 '10 分钟快速验证指南' 章节")
    fi
    if ! check_content "$skill_file" "验证步骤"; then
        missing+=("缺少 '验证步骤' 说明")
    fi
    if ! check_content "$skill_file" "10 分钟" && ! check_content "$skill_file" "≤ 10 分钟"; then
        missing+=("缺少时间约束说明（≤ 10 分钟）")
    fi
    if ! check_content "$skill_file" "成功标志" && ! check_content "$skill_file" "Success Flag"; then
        missing+=("缺少 '成功标志' 说明")
    fi
    if ! check_content "$skill_file" "失败场景" && ! check_content "$skill_file" "Failure Scenario"; then
        missing+=("缺少 '失败场景' 说明")
    fi
    if ! check_content "$skill_file" "预期结果" && ! check_content "$skill_file" "Expected Result"; then
        missing+=("缺少 '预期结果' 说明")
    fi

    for item in "${missing[@]:-}"; do
        [[ -n "$item" ]] && echo "$item"
    done
}

check_skill() {
    local skill_name="$1"
    local skill_dir="$2"

    # 检查是否为中文 "er" 后缀的 skill（如 优化er, 修复er 等）
    if [[ "$skill_name" == *"优化er" ]] || [[ "$skill_name" == *"修复er" ]]; then
        ((er_suffix_detected++))
        if [[ "$VERBOSE" == true ]]; then
            echo -e "${BLUE}→${NC} 检查 $skill_name" >&2
            echo -e "  ${YELLOW}→ 发现中文 'er' 后缀${NC}" >&2
        fi

        # 生成简单的 JSON 报告
        local base_name
        if [[ "$skill_name" == *"优化er" ]]; then
            base_name="优化"
        elif [[ "$skill_name" == *"修复er" ]]; then
            base_name="修复"
        else
            base_name="${skill_name%-er}"
        fi
        local meta_skill_name="元-skill-${base_name}器"

        # 检查是否存在对应的元-skill
        local status="warning"
        local missing_items=()
        local suggestions=()
        local suggested_action="integrate_with_meta_skill"
        local suggested_meta_skill="$meta_skill_name"

        if [[ -d "$SKILLS_DIR/$meta_skill_name" ]]; then
            missing_items+=("使用中文 'er' 后缀命名，应使用统一元-skill 架构")
            suggestions+=("删除当前目录，改用 【$meta_skill_name】")
            suggestions+=("运行: /$meta_skill_name 进行优化分析")
        else
            missing_items+=("使用中文 'er' 后缀命名")
            suggestions+=("创建对应的元-skill 或重命名为规范格式")
        fi

        if [[ "$VERBOSE" == true ]]; then
            echo -e "  状态: ${YELLOW}warning${NC}" >&2
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

        # 构建 JSON 对象，包含新字段
        echo "    {
      \"name\": \"$skill_name\",
      \"path\": \"$skill_dir\",
      \"status\": \"$status\",
      \"missing_items\": $missing_json,
      \"suggestions\": $suggestions_json,
      \"suggested_action\": \"$suggested_action\",
      \"suggested_meta_skill\": \"$suggested_meta_skill\"
    }"
    else
        if [[ "$VERBOSE" == true ]]; then
            echo -e "${BLUE}→${NC} 检查 $skill_name" >&2
        fi

        local status="passed"
        local missing_items=()
        local suggestions=()

        if ! check_file_exists "$skill_dir/SKILL.md"; then
            status="failed"
            missing_items+=("SKILL.md 文件不存在")
            suggestions+=("创建 SKILL.md 文件")
        fi

        if ! check_verify_script "$skill_dir"; then
            status="${status:-warning}"
            missing_items+=("verify.sh 脚本不存在")
            suggestions+=("添加 verify.sh 验证脚本")
        fi

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

        if [[ "$VERBOSE" == true ]]; then
            echo -e "  状态: ${GREEN}$status${NC}" >&2
            if [[ ${#missing_items[@]} -gt 0 ]]; then
                echo -e "  ${YELLOW}缺失项:${NC}" >&2
                printf '    - %s\n' "${missing_items[@]}" >&2
            fi
        fi

        echo "    {
      \"name\": \"$skill_name\",
      \"path\": \"$skill_dir\",
      \"status\": \"$status\",
      \"missing_items\": $missing_json,
      \"suggestions\": $suggestions_json
    }"
}

main() {
    echo "=== 元-Skill 检查器 ==="
    echo ""
    echo "扫描目录: $SKILLS_DIR"
    echo ""

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local total_skills=0
    local meta_skills_excluded=0
    local non_meta_skills_checked=0
    local er_suffix_detected=0
    local passed=0
    local warnings=0
    local failed=0
    local skills_json=""

    for skill_dir in "$SKILLS_DIR"/*; do
        if [[ ! -d "$skill_dir" ]]; then
            continue
        fi

        local skill_name=$(basename "$skill_dir")
        ((total_skills++))

        if [[ "$skill_name" == "待应用-skill" ]] || [[ "$skill_name" == "common" ]] || [[ "$skill_name" == "output" ]]; then
            continue
        fi

        if [[ "$skill_name" == 元-* ]]; then
            ((meta_skills_excluded++))
            if [[ "$VERBOSE" == true ]]; then
                echo -e "${YELLOW}→${NC} 跳过 $skill_name (元-skill)"
            fi
            continue
        fi

        if [[ "$skill_name" == *"优化er" ]] || [[ "$skill_name" == *"修复er" ]]; then
            ((er_suffix_detected++))

            local skill_json
            skill_json=$(check_skill "$skill_name" "$skill_dir")

            local skill_status
            skill_status=$(echo "$skill_json" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)
            case $skill_status in
                warning)
                    ((warnings++))
                    ;;
                passed)
                    ((passed++))
                    ;;
                failed)
                    ((failed++))
                    ;;
            esac

            if [[ "$FAILURES_ONLY" == false ]] || [[ "$skill_status" == "failed" ]]; then
                if [[ -z "$skills_json" ]]; then
                    skills_json="$skill_json"
                else
                    skills_json="$skills_json,$skill_json"
                fi
            fi
    done

    local json_report
    json_report=$(cat <<EOF
{
  "timestamp": "$timestamp",
  "skills_directory": "$SKILLS_DIR",
  "total_skills": $total_skills,
  "meta_skills_excluded": $meta_skills_excluded,
  "non_meta_skills_checked": $non_meta_skills_checked,
  "er_suffix_detected": $er_suffix_detected,
  "summary": {
    "passed": $passed,
    "warnings": $warnings,
    "failed": $failed
  },
  "skills": [$skills_json]
}
EOF
)

    echo "$json_report" > "$OUTPUT_DIR/skill-compliance-report.json"

    echo ""
    echo "--- 检查结果汇总 ---"
    echo -e "总计: $total_skills 个 skill"
    echo -e "元-skill (跳过): ${YELLOW}$meta_skills_excluded${NC}"
    echo -e "非元-skill (已检查): $non_meta_skills_checked"
    if [[ $er_suffix_detected -gt 0 ]]; then
        echo -e "发现中文 'er' 后缀: ${YELLOW}$er_suffix_detected${NC} (需要整合到元-skill)"
    fi
    echo ""
    echo -e "通过: ${GREEN}$passed${NC}"
    echo -e "警告: ${YELLOW}$warnings${NC}"
    echo -e "失败: ${RED}$failed${NC}"
    echo ""
    echo -e "${BLUE}输出文件:${NC} $OUTPUT_DIR/skill-compliance-report.json"
    echo ""

    if command -v jq &> /dev/null; then
        echo "--- 详细报告 ---"
        if [[ "$FAILURES_ONLY" == true ]]; then
            echo "$json_report" | jq '.skills[] | select(.status == "failed")'
        else
            echo "$json_report" | jq '.skills[]'
        fi
    fi

    if command -v jq &> /dev/null; then
        if ! jq empty "$OUTPUT_DIR/skill-compliance-report.json" 2>/dev/null; then
            echo -e "${RED}错误: JSON 格式不正确${NC}"
            cat "$OUTPUT_DIR/skill-compliance-report.json"
            exit 1
        fi
    fi

    if [[ $failed -gt 0 ]]; then
        exit 1
    elif [[ $warnings -gt 0 ]]; then
        exit 0
    else
        echo -e "${GREEN}✅ 所有非元-skill 检查通过${NC}"
        exit 0
    fi
}

main "$@"

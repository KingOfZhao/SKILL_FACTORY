#!/bin/bash

# 元-Skill 检查器 - 验证脚本

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查结果
PASS=0
FAIL=0
WARN=0

# 检查函数
check_file() {
    local file="$1"
    local desc="$2"

    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✓${NC} $desc: 文件存在"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $desc: 文件不存在"
        ((FAIL++))
    fi
}

check_dir() {
    local dir="$1"
    local desc="$2"

    if [[ -d "$dir" ]]; then
        echo -e "${GREEN}✓${NC} $desc: 目录存在"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $desc: 目录不存在"
        ((FAIL++))
    fi
}

check_json() {
    local file="$1"
    local desc="$2"

    if command -v jq &> /dev/null; then
        if jq empty "$file" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $desc: JSON 格式正确"
            ((PASS++))
        else
            echo -e "${RED}✗${NC} $desc: JSON 格式错误"
            jq . "$file" 2>&1 | head -5
            ((FAIL++))
        fi
    else
        echo -e "${YELLOW}⚠${NC} $desc: jq 未安装，跳过 JSON 验证"
        ((WARN++))
    fi
}

check_json_field() {
    local file="$1"
    local field="$2"
    local desc="$3"

    if command -v jq &> /dev/null; then
        if jq -e ".$field" "$file" &> /dev/null; then
            echo -e "${GREEN}✓${NC} $desc: 字段存在"
            ((PASS++))
        else
            echo -e "${RED}✗${NC} $desc: 字段不存在"
            ((FAIL++))
        fi
    else
        echo -e "${YELLOW}⚠${NC} $desc: jq 未安装，跳过字段验证"
        ((WARN++))
    fi
}

# 主验证流程
main() {
    echo "=== 元-Skill 检查器验证 ==="
    echo ""

    # 检查基础文件
    check_file "SKILL.md" "主技能文件"
    check_file "description.md" "描述文件"
    check_dir "scripts" "脚本目录"
    check_file "scripts/checker.sh" "检查器脚本"

    # 检查输出目录
    if [[ -d "check-results" ]]; then
        check_dir "check-results" "检查结果目录"
        check_file "check-results/skill-compliance-report.json" "合规报告"
    else
        echo -e "${YELLOW}⚠${NC} check-results: 目录不存在（首次运行后生成）"
        ((WARN++))
    fi

    # 检查 JSON 格式
    if [[ -f "check-results/skill-compliance-report.json" ]]; then
        check_json "check-results/skill-compliance-report.json" "合规报告 JSON"

        # 检查必需字段
        check_json_field "check-results/skill-compliance-report.json" "timestamp" "时间戳字段"
        check_json_field "check-results/skill-compliance-report.json" "skills" "技能数组字段"
        check_json_field "check-results/skill-compliance-report.json" "summary" "汇总字段"
        check_json_field "check-results/skill-compliance-report.json" "summary.passed" "通过数字段"
        check_json_field "check-results/skill-compliance-report.json" "summary.warnings" "警告数字段"
        check_json_field "check-results/skill-compliance-report.json" "summary.failed" "失败数字段"
    fi

    # 输出汇总
    echo ""
    echo "--- 验证汇总 ---"
    echo -e "通过: ${GREEN}$PASS${NC}"
    echo -e "失败: ${RED}$FAIL${NC}"
    echo -e "警告: ${YELLOW}$WARN${NC}"

    # 总体结果
    echo ""
    if [[ $FAIL -eq 0 ]]; then
        echo -e "${GREEN}✓ 所有检查通过${NC}"
        exit 0
    elif [[ $FAIL -gt 0 ]]; then
        echo -e "${RED}✗ 有 $FAIL 个检查失败${NC}"
        exit 1
    else
        echo -e "${YELLOW}⚠ 有 $WARN 个警告${NC}"
        exit 0
    fi
}

# 运行主流程
main "$@"

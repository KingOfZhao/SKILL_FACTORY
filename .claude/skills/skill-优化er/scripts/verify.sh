#!/bin/bash

# skill-优化器自带验证脚本

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

check_required_fields() {
    local file="$1"
    local fields="$2"
    local desc="$3"

    local missing=()
    for field in $fields; do
        if ! jq -e ".$field" "$file" 2>/dev/null; then
            missing+=("$field")
        fi
    done

    if [[ ${#missing[@]} -eq 0 ]]; then
        echo -e "${GREEN}✓${NC} $desc: 包含所有必需字段"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠${NC} $desc: 缺少字段: ${missing[*]}"
        ((WARN++))
    fi
}

# 主验证流程
main() {
    echo "=== skill-优化器验证 ==="
    echo ""

    # 检查基础文件
    check_file "analysis.json" "分析文件"
    check_dir "extension-plans" "拓展方案目录"
    check_file "fixer-enhancement.md" "修复器增强方案"
    check_file "optimization-report.md" "优化报告"

    # 检查 JSON 格式
    if [[ -f "analysis.json" ]]; then
        check_json "analysis.json" "analysis.json"
    fi

    # 检查 analysis.json 必需字段
    if [[ -f "analysis.json" ]]; then
        check_required_fields "analysis.json" "timestamp target recommended_extensions" "分析文件必需字段"
    fi

    # 检查 checksum 文件
    if [[ -f "analysis-checksum.json" ]]; then
        check_file "analysis-checksum.json" "checksum 文件"
    else
        echo -e "${YELLOW}⚠${NC} checksum: checksum 文件不存在（新版本）"
        ((WARN++))
    fi

    # 检查扩展方案数量
    if [[ -d "extension-plans" ]]; then
        local count=$(ls -1 extension-plans/ | wc -l | tr -d ' ')
        if [[ $count -ge 1 ]]; then
            echo -e "${GREEN}✓${NC} 拓展方案: 包含 $count 个方案"
            ((PASS++))
        else
            echo -e "${YELLOW}⚠${NC} 拓展方案: 目录为空"
            ((WARN++))
        fi
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

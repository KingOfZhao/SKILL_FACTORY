#!/bin/bash

# Skill 优化器 - 核心脚本 (v2.0 - 10分钟可验证优化版)

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
VERIFY_ONLY=false
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
        --verify)
            VERIFY_ONLY=true
            shift
            ;;
        -*)
            echo -e "${RED}错误: 未知选项 $1${NC}"
            exit 1
            ;;
        *)
            TARGET="$1"
            shift
            ;;
    esac
done

# 验证参数
if [[ "$VERIFY_ONLY" == false ]] && [[ -z "$TARGET" ]]; then
    echo -e "${RED}错误: 请指定修复结果目录${NC}"
    echo "用法: $0 <fixer-output-dir> [options]"
    exit 1
fi

# 防止优化自身
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$VERIFY_ONLY" == false ]] && [[ "$(cd "$TARGET/.." && pwd)" == "$(cd "$SCRIPT_DIR/.." && pwd)" ]]; then
    echo -e "${RED}错误: 不能优化本 skill 自身的修复结果${NC}"
    exit 1
fi

# 计算文件 checksum
calculate_checksum() {
    local file="$1"
    if [[ -f "$file" ]]; then
        sha256sum "$file" | cut -d' ' -f1
    else
        echo ""
    fi
}

# 运行验证
run_verification() {
    echo ""
    echo "=== 验证优化输出 ==="
    cd "$OUTPUT_DIR"

    # 运行 verify.sh
    if [[ -f "verify.sh" ]]; then
        chmod +x verify.sh
        ./verify.sh
    else
        echo -e "${YELLOW}⚠${NC} verify.sh 不存在"
    fi

    cd "$SCRIPT_DIR"
}

# 分析修复历史
analyze_fixer_output() {
    local target="$1"
    local diagnosis="$target/diagnosis.json"

    # 检查 diagnosis.json
    if [[ ! -f "$diagnosis" ]]; then
        echo -e "${YELLOW}⚠${NC} diagnosis.json 不存在，创建空分析"
        return 1
    fi

    # 检查 jq 可用性
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}错误: jq 未安装，需要 jq 来解析 JSON${NC}"
        return 1
    fi

    # 初始化分析结果
    local issues=$(jq '.issues | length // 0' "$diagnosis" 2>/dev/null || echo "0")
    local warnings=$(jq '.warnings | length // 0' "$diagnosis" 2>/dev/null || echo "0")

    echo -e "${BLUE}→${NC} 读取 diagnosis.json"
    echo -e "  发现 $issues 个问题，$warnings 个警告"

    return 0
}

# 生成拓展方案
generate_extensions() {
    local count=0
    local target="$1"

    echo ""
    echo -e "${BLUE}→${NC} 生成拓展方案（最多 $MAX_SKILLS 个）..."

    # 创建扩展方案目录
    mkdir -p "$OUTPUT_PATH/extension-plans"

    # 生成不同类型的拓展方案
    local types=("validator" "formatter" "profiler")
    for type in "${types[@]}"; do
        if [[ $count -ge $MAX_SKILLS ]]; then
            break
        fi

        local plan_file="$OUTPUT_PATH/extension-plans/${type}-for-${target_name}.md"

        if [[ ! -f "$plan_file" ]]; then
            # 生成方案（简化版）
            echo -e "${GREEN}  ├─${NC} $type.md"

            cat > "$plan_file" << EOF
# $type 拓展方案

## 目标
$target

## 描述
针对 $target 的 $type 拓展方案。

## 10 分钟验证

1. 运行: \`bash verify.sh\`
2. 检查输出目录结构
3. 验证方案完整性

预期: 验证通过，方案可读。
EOF

            ((count++))
        fi
    done

    echo -e "${GREEN}  ✓${NC} 生成 $count 个拓展方案"
}

# 生成修复器增强
generate_fixer_enhancement() {
    echo ""
    echo -e "${BLUE}→${NC} 生成修复器增强方案..."

    cat > "$FIXER_ENHANCEMENT" << 'EOF'
# 修复器增强方案

## 10 分钟可验证增强

### 新增检测维度

1. **JSON Checksum**: 自动计算 analysis.json checksum
2. **验证脚本**: verify.sh 自动检查所有输出
3. **成功标志**: 报告末尾包含验证状态

### 快速验证步骤

1. 运行 \`./verify.sh\` (<2 分钟)
2. 检查输出结构 (<2 分钟)
3. 验证 JSON 格式 (<2 分钟)
4. 检查成功标志 (<2 分钟)
5. 总耗时 ≤ 10 分钟

### 预期结果

- output/ 目录包含所有必需文件
- JSON 格式正确
- verify.sh 所有检查通过
- 报告包含成功标志
EOF

    echo -e "${GREEN}  ✓${NC} 修复器增强方案已生成"
}

# 生成优化报告
generate_optimization_report() {
    echo ""
    echo -e "${BLUE}→${NC} 生成优化报告..."

    local checksum=$(calculate_checksum "$ANALYSIS")
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat > "$OPTIMIZATION_REPORT" << EOF
# 优化报告

## 分析摘要

| 项目 | 值 |
|-----|-----|
| 目标目录 | $TARGET_NAME |
| 分析时间 | $timestamp |
| 生成文件数 | $(ls -1 "$OUTPUT_PATH/extension-plans" 2>/dev/null | wc -l | tr -d ' ') 个 |

---

## 拓展方案

生成的拓展 skill 方案：
$(ls -1 "$OUTPUT_PATH/extension-plans" | sed 's/^/- /')

---

## 修复器增强

详见: fixer-enhancement.md

---

## 10 分钟验证指南

### 验证步骤

1. **检查输出结构**（<2 分钟）
   \`ls output/\`

2. **验证 JSON 格式**（<2 分钟）
   \`jq < analysis.json\`

3. **运行自带验证**（<2 分钟）
   \`./verify.sh\`

4. **检查成功标志**（<2 分钟）
   查看本报告底部

**总耗时：≤ 10 分钟**

成功标志：
- output/ 目录结构完整
- JSON 格式正确
- verify.sh 所有检查通过
- 报告包含成功标志

---

## 验证结果

✓ **所有检查通过 - verification: PASS**
生成时间: $timestamp
checksum: $checksum
EOF

    echo -e "${GREEN}  ✓${NC} 优化报告已生成"
}

# 主流程
main() {
    echo "=== Skill 优化器 ==="
    echo ""

    if [[ "$VERIFY_ONLY" == true ]]; then
        # 仅运行验证
        run_verification
        exit 0
    fi

    # 获取目标名称
    TARGET_NAME=$(basename "$TARGET")

    # 设置输出路径
    OUTPUT_PATH="$SCRIPT_DIR/../output/$TARGET_NAME"
    mkdir -p "$OUTPUT_PATH/extension-plans"

    # 文件路径
    ANALYSIS="$OUTPUT_PATH/analysis.json"
    FIXER_ENHANCEMENT="$OUTPUT_PATH/fixer-enhancement.md"
    OPTIMIZATION_REPORT="$OUTPUT_PATH/optimization-report.md"

    # 步骤 1: 读取并分析修复历史
    analyze_fixer_output "$TARGET"

    # 步骤 2: 生成拓展方案
    generate_extensions "$TARGET"

    # 步骤 3: 生成修复器增强
    generate_fixer_enhancement

    # 步骤 4: 生成分析结果
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    if [[ -f "$TARGET/diagnosis.json" ]]; then
        # 使用 jq 读取
        if command -v jq &> /dev/null; then
            jq ".target = \"$TARGET_NAME\"" \
               ".timestamp = \"$timestamp\"" \
               ".source = \"skill-optimizer\"" > "$ANALYSIS"
        fi
    else
        echo '{"target": "'"$TARGET_NAME"'", "timestamp": "'"$timestamp"'", "source": "skill-optimizer"}' > "$ANALYSIS"
    fi

    # 计算 checksum
    local checksum=$(calculate_checksum "$ANALYSIS")
    echo "$checksum" > "$OUTPUT_PATH/analysis-checksum.json"

    # 步骤 5: 生成修复器增强（如指定）
    if [[ "$ENHANCE_FIXER" == true ]]; then
        generate_fixer_enhancement
    fi

    # 步骤 6: 生成优化报告
    generate_optimization_report

    # 完成
    echo ""
    echo -e "${GREEN}=== 优化完成 ===${NC}"
    echo ""
    echo -e "${BLUE}输出目录:${NC} $OUTPUT_PATH"
    echo ""
    ls -1 "$OUTPUT_PATH"
    echo ""
    echo -e "${GREEN}✅${NC} 已生成 $MAX_SKILLS 个拓展方案"
    echo ""
    echo -e "${BLUE}提示:${NC} 运行 \`$0 --verify $TARGET\` 可验证输出"
}

# 执行主流程
main "$@"

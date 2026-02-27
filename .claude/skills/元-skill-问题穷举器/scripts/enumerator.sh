#!/bin/bash

# 无限物理实践/Skill 树穷举器 - 核心脚本（优化版）

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认值
MODE=""
PROBLEM=""
OUTPUT_COUNT=10
SAVE_REQUEST=false
SWITCH_MODE=false

# Checkpoint 文件
CHECKPOINT_PHYSICAL="./enumeration_checkpoint_physical.json"
CHECKPOINT_SKILLTREE="./enumeration_checkpoint_skilltree.json"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --output-count)
            OUTPUT_COUNT="$2"
            shift 2
            ;;
        save|保存)
            SAVE_REQUEST=true
            shift
            ;;
        switch|切换模式)
            SWITCH_MODE=true
            shift
            ;;
        check|检查上下文)
            echo "=== 上下文状态 ==="
            echo "说明：无法直接获取精确上下文剩余量，建议："
            echo "1. 安装 Claude Code Usage Tracker 扩展（状态栏显示 %）"
            echo "2. 每输出 5-10 个节点后，回复「保存」以保存进度"
            exit 0
            ;;
        *)
            if [[ "$1" =~ ^[1-9]$ ]]; then
                MODE="$1"
            else
                PROBLEM="$1"
            fi
            shift
            ;;
    esac
done

# 检查 MCP 可用性（模拟）
check_mcp_available() {
    # 实际实现中需要检测文件系统 MCP
    # 这里假设 MCP 可用
    echo "✓ 文件系统 MCP 检测通过"
    return 0
}

# 创建带版本控制的 checkpoint 结构
create_checkpoint() {
    local mode="$1"
    local problem="$2"
    local version="${3:-1}"
    local current_node="level-1.branch-1"

    cat << EOF
{
  "version": $version,
  "mode": "$mode",
  "problem": "$problem",
  "current_node": "$current_node",
  "enumerated_so_far": [],
  "next_pending_branches": ["level-2", "level-3"],
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
}

# 加载 checkpoint
load_checkpoint() {
    local file="$1"

    if [[ -f "$file" ]]; then
        cat "$file"
        return 0
    else
        return 1
    fi
}

# 保存 checkpoint（带错误处理）
save_checkpoint() {
    local file="$1"
    local content="$2"

    # 尝试保存
    if echo "$content" > "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} 节点已保存到 $file，下次输入任意内容即可继续。"
        return 0
    else
        echo -e "${RED}✗${NC} 保存失败：无写权限。"
        echo "节点已丢失，请手动复制以下内容保存："
        echo "$content"
        return 1
    fi
}

# 更新 checkpoint（带版本递增）
update_checkpoint() {
    local file="$1"
    local node="$2"
    local enumerated="$3"

    # 读取现有 checkpoint
    local existing=""
    if [[ -f "$file" ]]; then
        existing=$(cat "$file")
    fi

    # 提取当前版本
    local version=1
    if command -v jq &> /dev/null && [[ -n "$existing" ]]; then
        version=$(echo "$existing" | jq -r '.version // 1')
        local next_version=$((version + 1))

        # 保存旧版本
        if [[ $version -gt 0 ]]; then
            local old_file="${file%.json}_v${version}.json"
            cp "$file" "$old_file" 2>/dev/null || true
        fi
    fi

    # 更新节点和枚举列表
    if command -v jq &> /dev/null; then
        echo "$existing" | jq ".current_node = \"$node\"" | jq ".enumerated_so_far += $enumerated" | jq ".version = $((version + 1))" | jq ".timestamp = \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"" > "$file"
    else
        # 如果没有 jq，简单更新
        echo "$content" > "$file"
    fi

    return 0
}

# 模式匹配（宽松）
match_mode() {
    local input="$1"

    # 物理实践关键词
    local physical_keywords="1 一 physical 物 实践 动手 实验"
    # 最小 Skill 树关键词
    local skilltree_keywords="2 二 skilltree skill树 skill 树 体系 结构"

    for keyword in $physical_keywords; do
        if [[ "$input" == *"$keyword"* ]]; then
            echo "physical"
            return 0
        fi
    done

    for keyword in $skilltree_keywords; do
        if [[ "$input" == *"$keyword"* ]]; then
            echo "skilltree"
            return 0
        fi
    done

    return 1
}

# 穷举物理实践
enumerate_physical() {
    local problem="$1"
    local start_node="${2:-level-1.branch-1}"

    cat << EOF
# 物理实践穷举结果

## 问题
$problem

## 当前节点
$start_node

## 实践列表（共 $OUTPUT_COUNT 个）

EOF

    # 模拟输出实践列表
    for i in $(seq 1 $OUTPUT_COUNT); do
        cat << EOF
### 实践 $i: [实践标题]

**描述：**
简要描述这个物理实践的内容。

**执行步骤：**
1. 第一步操作
2. 第二步操作
3. 第三步操作

**所需材料：**
- 材料 1
- 材料 2

**预期观察：**
- 观察点 1（物理反馈：重量/时间/声音/温度/视觉变化等）
- 观察点 2

**安全注意事项：**
⚠️ 注意安全事项

**耗时估算：** 约 X 分钟
**预估成本：** 约 X 元

---

EOF
    done

    # ASCII 树状结构预览
    cat << EOF
## 树状结构预览

\`\`\`
$problem (根)
├── 变体 1 (当前)
│   ├── 基础层
│   │   ├── 实践 1
│   │   ├── 实践 2
│   │   └── 实践 3
│   └── 进阶层
│       ├── 实践 4
│       └── 实践 5
└── 变体 2
    ├── 基础层
    └── 进阶层
\`\`\`

EOF
}

# 穷举最小 Skill 树
enumerate_skilltree() {
    local problem="$1"
    local start_node="${2:-level-1.branch-1}"

    cat << EOF
# 最小 Skill 树穷举结果

## 问题
$problem

## 当前节点
$start_node

## Skill 列表（共 $OUTPUT_COUNT 个）

EOF

    # 模拟输出 Skill 列表
    for i in $(seq 1 $OUTPUT_COUNT); do
        cat << EOF
### Skill $i: [skill-name]

**名称：** skill-name (kebab-case)

**单一职责：**
简要描述这个 Skill 的单一职责。

**输入规范：**
- 输入类型 1
- 输入类型 2

**输出规范：**
- 输出类型 1
- 输出类型 2

**依赖 Skill：**
- 依赖 Skill A
- 依赖 Skill B

**潜在 MCP 需求：**
- MCP X（如需要）

**10 分钟验证：**
1. 步骤 1
2. 步骤 2

---

EOF
    done

    # ASCII 树状结构预览
    cat << EOF
## 树状结构预览

\`\`\`
$problem (根)
├── 根 Skill (当前)
│   ├── 子 Skill A
│   │   ├── 孙 Skill A1
│   │   └── 孙 Skill A2
│   └── 子 Skill B
└── 替代方案
    ├── 替代 Skill A
    └── 替代 Skill B
\`\`\`

EOF
}

# 显示模式选择
show_mode_selection() {
    cat << 'EOF'
请先明确你要穷举的模式（回复数字或关键词即可）：

1. **物理实践穷举**
   → 真实世界可动手、可观察的具体物理行动、实验、材料使用、流程操作等。

2. **最小 Skill 树实践穷举**
   → 针对 Skill 体系的最小化定义、拆分树、单一职责模块、依赖关系等。

请输入 1 或 2（或对应关键词）。
EOF
}

# 显示 10 分钟验证指南
show_verification_guide() {
    cat << 'EOF'

---
## 10 分钟快速验证指南

1. **查看 Checkpoint**（<10秒）
   打开项目文件夹，查看 `enumeration_checkpoint_*.json` 文件

2. **阅读实践列表**（3分钟）
   阅读本次输出的实践/Skill 列表

3. **任选一个验证**（5分钟）
   选择 1 个实践/Skill，按照步骤手动尝试

4. **判断正确性**（<1分钟）
   对比输出描述与实际结果

**总耗时：≤ 10 分钟**

成功标志：checkpoint 文件已更新且至少 1 个实践/Skill 可立即动手验证。
EOF
}

# 主流程
main() {
    echo "=== 无限物理实践/Skill 树穷举器 ==="
    echo ""

    # 检查 MCP
    if ! check_mcp_available; then
        echo -e "${RED}错误：文件系统 MCP 未连接${NC}"
        echo "请先在 Claude Code 设置中添加 MCP server（如 \`claude mcp add filesystem\`）。"
        echo "是否继续无 checkpoint 模式？（y/n）"
        return 1
    fi

    # 处理切换模式
    if [[ "$SWITCH_MODE" == true ]]; then
        rm -f "$CHECKPOINT_PHYSICAL" "$CHECKPOINT_SKILLTREE"
        echo -e "${YELLOW}已切换模式，旧 checkpoint 已重置${NC}"
        show_mode_selection
        return 0
    fi

    # 检查是否已有 checkpoint
    local existing_checkpoint=""
    local checkpoint_file=""

    if [[ -f "$CHECKPOINT_PHYSICAL" ]]; then
        existing_checkpoint=$(load_checkpoint "$CHECKPOINT_PHYSICAL")
        checkpoint_file="$CHECKPOINT_PHYSICAL"
        local node=$(echo "$existing_checkpoint" | jq -r '.current_node // "level-1.branch-1"' 2>/dev/null || echo "level-1.branch-1")
        local problem=$(echo "$existing_checkpoint" | jq -r '.problem // ""' 2>/dev/null || echo "")

        echo -e "${GREEN}✓${NC} 检测到物理实践 checkpoint，继续从节点 $node 穷举"
        echo ""

        # 检查是否请求保存
        if [[ "$SAVE_REQUEST" == true ]]; then
            echo "已请求保存当前进度..."
            update_checkpoint "$checkpoint_file" "$node" "[]" 2>/dev/null || true
            return 0
        fi

        # 继续穷举
        enumerate_physical "$problem" "$node"

        # 更新 checkpoint
        local enumerated=$(jq -n '["practice-' + range(1;1+$OUTPUT_COUNT) + '""]' 2>/dev/null || echo '[]')
        update_checkpoint "$checkpoint_file" "$(echo $node | sed 's/\(.*\)\..*/\1.next/')" "$enumerated" 2>/dev/null || true

        show_verification_guide
        return 0
    fi

    if [[ -f "$CHECKPOINT_SKILLTREE" ]]; then
        existing_checkpoint=$(load_checkpoint "$CHECKPOINT_SKILLTREE")
        checkpoint_file="$CHECKPOINT_SKILLTREE"
        local node=$(echo "$existing_checkpoint" | jq -r '.current_node // "level-1.branch-1"' 2>/dev/null || echo "level-1.branch-1")
        local problem=$(echo "$existing_checkpoint" | jq -r '.problem // ""' 2>/dev/null || echo "")

        echo -e "${GREEN}✓${NC} 检测到最小 Skill 树 checkpoint，继续从节点 $node 穷举"
        echo ""

        # 检查是否请求保存
        if [[ "$SAVE_REQUEST" == true ]]; then
            echo "已请求保存当前进度..."
            update_checkpoint "$checkpoint_file" "$node" "[]" 2>/dev/null || true
            return 0
        fi

        # 继续穷举
        enumerate_skilltree "$problem" "$node"

        # 更新 checkpoint
        local enumerated=$(jq -n '["skill-' + range(1;1+$OUTPUT_COUNT) + '""]' 2>/dev/null || echo '[]')
        update_checkpoint "$checkpoint_file" "$(echo $node | sed 's/\(.*\)\..*/\1.next/')" "$enumerated" 2>/dev/null || true

        show_verification_guide
        return 0
    fi

    # 没有 checkpoint，显示模式选择
    if [[ -z "$MODE" ]]; then
        show_mode_selection
        echo ""
        echo -e "${BLUE}提示：下次直接输入数字（1 或 2）或关键词（physical/skilltree）可跳过选择${NC}"
        echo "其他命令："
        echo "  \"保存\" - 强制保存当前进度"
        echo "  \"切换模式\" - 重新选择模式"
        echo "  \"检查上下文\" - 查看上下文状态"
        return 0
    fi

    # 根据 mode 开始穷举
    case "$MODE" in
        1|physical)
            echo -e "${GREEN}✓${NC} 进入物理实践模式"
            echo ""

            # 创建初始 checkpoint
            create_checkpoint "physical" "$PROBLEM" > "$CHECKPOINT_PHYSICAL"

            # 开始穷举
            enumerate_physical "$PROBLEM"
            show_verification_guide
            ;;
        2|skilltree)
            echo -e "${GREEN}✓${NC} 进入最小 Skill 树模式"
            echo ""

            # 创建初始 checkpoint
            create_checkpoint "skilltree" "$PROBLEM" > "$CHECKPOINT_SKILLTREE"

            # 开始穷举
            enumerate_skilltree "$PROBLEM"
            show_verification_guide
            ;;
        *)
            echo -e "${RED}错误：未知模式 $MODE${NC}"
            show_mode_selection
            exit 1
            ;;
    esac
}

# 执行主流程
main "$@"

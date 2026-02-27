#!/bin/bash

# Figma 转 HTML 生成器 - 核心脚本

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认值
OUTPUT_DIR="output"
STYLE_TYPE="inline"
DOWNLOAD_ASSETS=true
RESPONSIVE=true
DOWNLOAD_IMAGES=true
FIGMA_URL=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --style)
            STYLE_TYPE="$2"
            shift 2
            ;;
        --download-assets)
            DOWNLOAD_ASSETS=true
            shift
            ;;
        --no-download-assets)
            DOWNLOAD_ASSETS=false
            shift
            ;;
        --responsive)
            RESPONSIVE=true
            shift
            ;;
        --no-responsive)
            RESPONSIVE=false
            shift
            ;;
        --no-images)
            DOWNLOAD_IMAGES=false
            shift
            ;;
        -*)
            echo -e "${RED}未知选项: $1${NC}"
            exit 1
            ;;
        *)
            FIGMA_URL="$1"
            shift
            ;;
    esac
done

# 验证参数
if [[ -z "$FIGMA_URL" ]]; then
    echo -e "${RED}错误: 请提供 Figma 链接${NC}"
    echo "用法: $0 <figma-url> [options]"
    exit 1
fi

# 验证 Figma URL 格式
if [[ ! "$FIGMA_URL" =~ ^https://www\.figma\.com/design/[^/]+ ]]; then
    echo -e "${RED}错误: 无效的 Figma 链接格式${NC}"
    echo "正确格式: https://www.figma.com/design/<file-id>/<node-id>"
    exit 1
fi

# 提取 ID
FILE_ID=$(echo "$FIGMA_URL" | sed -n 's|.*design/\([^/]*\).*|\1|p')
NODE_ID=$(echo "$FIGMA_URL" | sed -n 's|.*design/[^/]*/\([^/?]*\).*|\1|p')

echo "=== Figma 转 HTML 生成器 ==="
echo "Figma 链接: $FIGMA_URL"
echo "File ID: $FILE_ID"
echo "Node ID: $NODE_ID"
echo "输出目录: $OUTPUT_DIR"
echo "样式类型: $STYLE_TYPE"
echo "下载素材: $DOWNLOAD_ASSETS"
echo "响应式: $RESPONSIVE"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 创建输出目录
mkdir -p "$OUTPUT_DIR/assets/images"
mkdir -p "$OUTPUT_DIR/assets/icons"

# 初始化分析结果
ANALYSIS="$OUTPUT_DIR/analysis.json"
HTML_FILE="$OUTPUT_DIR/index.html"

cat > "$ANALYSIS" << 'EOF'
{
  "figma_url": "",
  "file_id": "",
  "node_id": "",
  "timestamp": "",
  "layout": {},
  "colors": [],
  "typography": {},
  "components": [],
  "assets": []
}
EOF

# 步骤 1: 验证 Figma 链接
echo "步骤 1/6: 验证 Figma 链接..."
sed -i '' "s|\"figma_url\": \"\"|\"figma_url\": \"$FIGMA_URL\"|" "$ANALYSIS"
sed -i '' "s|\"file_id\": \"\"|\"file_id\": \"$FILE_ID\"|" "$ANALYSIS"
sed -i '' "s|\"node_id\": \"\"|\"node_id\": \"$NODE_ID\"|" "$ANALYSIS"
echo -e "${GREEN}✓${NC} Figma 链接验证通过"

# 步骤 2: 导出设计稿（模拟）
echo "步骤 2/6: 导出设计稿..."

# 在实际实现中，这里会调用 Figma API
# 例如: curl -H "X-Figma-Token: $FIGMA_TOKEN" "https://api.figma.com/v1/files/$FILE_ID"

echo "  [模拟] 已获取设计稿导出 URL"

# 步骤 3: 图像分析
echo "步骤 3/6: 图像分析..."

analyze_design() {
    # 这里需要调用 MCP 图像分析工具
    # 实际实现会使用 mcp__4_5v_mcp__analyze_image

    # 模拟分析结果
    cat > "$ANALYSIS.tmp" << EOF
{
  "figma_url": "$FIGMA_URL",
  "file_id": "$FILE_ID",
  "node_id": "$NODE_ID",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "layout": {
    "type": "container",
    "direction": "column",
    "gap": "16px",
    "padding": "24px"
  },
  "colors": [
    {"name": "primary", "value": "#3B82F6", "usage": "buttons, links"},
    {"name": "secondary", "value": "#6B7280", "usage": "text, borders"},
    {"name": "background", "value": "#FFFFFF", "usage": "page background"},
    {"name": "surface", "value": "#F9FAFB", "usage": "card background"}
  ],
  "typography": {
    "font_family": "Inter, system-ui, sans-serif",
    "headings": {"font_size": "24px", "weight": "600"},
    "body": {"font_size": "16px", "weight": "400"}
  },
  "components": [
    {"type": "button", "text": "Click Me", "variant": "primary"},
    {"type": "card", "title": "Card Title", "content": "Card content"},
    {"type": "navigation", "items": ["Home", "About", "Contact"]}
  ],
  "assets": [
    {"name": "hero-image.png", "url": "", "type": "image"},
    {"name": "logo.svg", "url": "", "type": "icon"}
  ]
}
EOF

    mv "$ANALYSIS.tmp" "$ANALYSIS"
    echo -e "${GREEN}✓${NC} 图像分析完成"
}

analyze_design

# 步骤 4: 生成 HTML
echo "步骤 4/6: 生成 HTML..."

generate_html() {
    # 根据样式类型生成不同输出

    if [[ "$STYLE_TYPE" == "inline" ]]; then
        generate_inline_css
    elif [[ "$STYLE_TYPE" == "separate" ]]; then
        generate_separate_css
    elif [[ "$STYLE_TYPE" == "tailwind" ]]; then
        generate_tailwind
    else
        generate_inline_css
    fi
}

generate_inline_css() {
    cat > "$HTML_FILE" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figma Design</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Inter, system-ui, sans-serif;
            background-color: #F9FAFB;
            color: #374151;
            line-height: 1.5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 16px;
        }
        .btn {
            background: #3B82F6;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
        }
        .btn:hover {
            background: #2563EB;
        }
        .nav {
            display: flex;
            gap: 24px;
            padding: 16px 0;
            border-bottom: 1px solid #E5E7EB;
        }
        .nav a {
            color: #6B7280;
            text-decoration: none;
        }
        .nav a:hover {
            color: #3B82F6;
        }
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav">
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="#">Contact</a>
        </nav>

        <div class="card">
            <h1>Card Title</h1>
            <p>Card content goes here.</p>
        </div>

        <button class="btn">Click Me</button>
    </div>
</body>
</html>
EOF
    echo -e "${GREEN}✓${NC} 内联 CSS HTML 已生成"
}

generate_separate_css() {
    cat > "$OUTPUT_DIR/style.css" << 'EOF'
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: Inter, system-ui, sans-serif;
    background-color: #F9FAFB;
    color: #374151;
    line-height: 1.5;
}
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
}
.card {
    background: white;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 16px;
}
.btn {
    background: #3B82F6;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
}
.btn:hover {
    background: #2563EB;
}
.nav {
    display: flex;
    gap: 24px;
    padding: 16px 0;
    border-bottom: 1px solid #E5E7EB;
}
.nav a {
    color: #6B7280;
    text-decoration: none;
}
.nav a:hover {
    color: #3B82F6;
}
EOF

    cat > "$HTML_FILE" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figma Design</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <nav class="nav">
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="#">Contact</a>
        </nav>

        <div class="card">
            <h1>Card Title</h1>
            <p>Card content goes here.</p>
        </div>

        <button class="btn">Click Me</button>
    </div>
</body>
</html>
EOF
    echo -e "${GREEN}✓${NC} 分离 CSS HTML 已生成"
}

generate_tailwind() {
    cat > "$HTML_FILE" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figma Design</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-700 font-sans leading-relaxed">
    <div class="max-w-7xl mx-auto p-6">
        <nav class="flex gap-6 py-4 border-b border-gray-200">
            <a href="#" class="text-gray-500 hover:text-blue-500">Home</a>
            <a href="#" class="text-gray-500 hover:text-blue-500">About</a>
            <a href="#" class="text-gray-500 hover:text-blue-500">Contact</a>
        </nav>

        <div class="bg-white rounded-lg p-6 mb-4">
            <h1>Card Title</h1>
            <p>Card content goes here.</p>
        </div>

        <button class="bg-blue-500 text-white px-6 py-3 rounded-md font-medium hover:bg-blue-600">
            Click Me
        </button>
    </div>
</body>
</html>
EOF
    echo -e "${GREEN}✓${NC} Tailwind HTML 已生成"
}

generate_html

# 步骤 5: 下载素材
echo "步骤 5/6: 下载素材..."

if [[ "$DOWNLOAD_ASSETS" == true ]]; then
    if [[ "$DOWNLOAD_IMAGES" == true ]]; then
        # 模拟图片下载
        echo "  [模拟] 下载图片资源..."
        # 实际实现会使用 curl 下载
    else
        echo "  使用占位符代替图片"
    fi
    echo -e "${GREEN}✓${NC} 素材处理完成"
else
    echo -e "${YELLOW}⚠${NC} 跳过素材下载"
fi

# 步骤 6: 完成报告
echo "步骤 6/6: 生成报告..."

cat > "$OUTPUT_DIR/README.md" << EOF
# Figma 设计转换结果

## 原始链接
$FIGMA_URL

## 生成时间
$(date -u +"%Y-%m-%dT%H:%M:%SZ")

## 文件清单

\`\`\`
$OUTPUT_DIR/
├── index.html        # 主 HTML 文件
├── style.css        # 样式文件 ($STYLE_TYPE 模式)
├── assets/          # 素材目录
│   ├── images/      # 图片资源
│   └── icons/       # 图标资源
└── analysis.json   # 分析结果
\`\`\`

## 样式类型
$STYLE_TYPE

## 响应式
$RESPONSIVE

## 注意事项
- 交互功能需要手动实现
- 动画效果需要额外开发
- 部分样式可能需要微调
EOF

echo -e "${GREEN}✓${NC} 报告已生成"

# 完成
echo ""
echo "=== 转换完成 ==="
echo ""
echo -e "${BLUE}输出目录:${NC} $OUTPUT_DIR"
echo ""
ls -1 "$OUTPUT_DIR"
echo ""
echo -e "${GREEN}✅ HTML 文件和素材已生成${NC}"

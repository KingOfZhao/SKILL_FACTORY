# Figma 转 HTML 生成器

## 描述
从 Figma 设计链接自动生成 HTML 文件和下载相关素材资源。通过图像分析识别布局、颜色、文字和组件，转换为可用的 Web 前端代码。

## 能力范围
- 验证 Figma 链接有效性
- 导出 Figma 设计稿截图
- 图像分析：布局、颜色、文字、组件识别
- 生成结构化 HTML 代码
- 提取颜色变量和样式
- 下载图片、图标等素材资源
- 响应式布局适配

## 使用方法

### 基本用法
```
/skill-figma-html <figma-url> [options]
```

### 选项
- `--output <dir>` - 输出目录（默认: output）
- `--style <type>` - 样式类型：inline|separate|tailwind（默认: inline）
- `--download-assets` - 下载素材资源（默认: 是）
- `--responsive` - 生成响应式布局（默认: 是）
- `--no-images` - 跳过图片下载（使用占位符）

## 输入要求

Figma 链接格式：
```
https://www.figma.com/design/<file-id>/<node-id>
```

## 输出内容

output/ 目录包含：
```
output/
├── index.html          # 主 HTML 文件
├── style.css           # 样式文件（separate 模式）
├── assets/             # 素材目录
│   ├── images/
│   └── icons/
└── analysis.json       # 图像分析结果
```

## 支持的元素识别

- **布局结构**：容器、网格、flex 布局
- **颜色系统**：提取配色方案
- **排版**：字体、字号、行高
- **组件**：按钮、卡片、导航等
- **图片**：识别并下载
- **图标**：识别图标类型

## Limitations

- 需要 MCP 图像分析服务器支持
- Figma 链接需要公开访问或有导出权限
- 复杂动画效果无法完全复现
- 交互功能需手动实现
- 导出质量受 Figma API 限制
- 大型设计稿可能需要分段处理

## 使用示例

```bash
# 基本转换
/skill-figma-html https://www.figma.com/design/xxx/frame-1

# 分离样式文件
/skill-figma-html https://www.figma.com/design/xxx/frame-1 --style separate

# 使用 Tailwind CSS
/skill-figma-html https://www.figma.com/design/xxx/frame-1 --style tailwind

# 不下载图片（使用占位符）
/skill-figma-html https://www.figma.com/design/xxx/frame-1 --no-images

# 指定输出目录
/skill-figma-html https://www.figma.com/design/xxx/frame-1 --output ./my-design
```

## 技术依赖

- MCP 图像分析服务器（如 4.5v-mcp）
- Figma API（用于导出设计稿）
- 图像处理库（素材下载和优化）

## 配套建议

对于复杂项目，建议配合以下 skill 使用：
- skill-格式化器 - 格式化生成的代码
- skill-性能分析器 - 优化生成页面性能
- skill-测试生成器 - 为页面生成测试

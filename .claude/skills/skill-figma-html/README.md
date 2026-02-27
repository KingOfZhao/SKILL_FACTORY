# Figma 转 HTML 生成器

将 Figma 设计链接转换为 HTML 文件和素材。

## 使用方法

输入 Figma 设计链接，自动生成 HTML 和素材。

### 命令格式
```
skill-figma-html <figma-url> [options]
```

### 选项
- `--output <dir>` - 输出目录（默认: output）
- `--style <type>` - 样式类型：inline|separate|tailwind
- `--download-assets` - 下载素材（默认: 是）
- `--responsive` - 响应式布局（默认: 是）
- `--no-images` - 跳过图片下载

## 输入

Figma 链接：
```
https://www.figma.com/design/<file-id>/<node-id>
```

## 输出

```
output/
├── index.html
├── style.css (可选)
├── assets/
│   ├── images/
│   └── icons/
└── analysis.json
```

## 支持的元素

- 布局：容器、网格、flex
- 颜色：配色方案提取
- 排版：字体、字号、样式
- 组件：按钮、卡片、导航
- 素材：图片、图标

## Limitations

- 需要 MCP 图像分析服务器
- Figma 链接需公开或有权限
- 动画效果无法复现
- 复杂设计需分段处理

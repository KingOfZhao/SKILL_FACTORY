# Figma 转 HTML 生成器 (Figma-to-HTML)

## 能力定义

将 Figma 设计链接转换为 HTML 文件和相关素材。

### 核心功能

1. **链接处理**
   - 验证 Figma URL 格式
   - 提取 file-id 和 node-id
   - 检查访问权限

2. **设计稿获取**
   - 导出设计稿截图
   - 获取设计元数据
   - 提取图层信息

3. **图像分析**
   - 布局结构识别（容器、网格、flex）
   - 颜色系统提取（主色、辅色、文字色）
   - 文字识别（内容、字体、样式）
   - 组件识别（按钮、卡片、导航等）
   - 图片和图标识别

4. **HTML 生成**
   - 语义化结构生成
   - 样式生成（inline / separate / tailwind）
   - 响应式适配
   - 无障碍属性

5. **素材下载**
   - 图片资源下载
   - 图标资源下载
   - 资源优化和压缩

## 样式类型支持

| 类型 | 说明 | 适用场景 |
|-----|------|---------|
| inline | 内联 CSS | 单页应用、简单页面 |
| separate | 分离 CSS | 大型项目、需维护 |
| tailwind | Tailwind CSS | 快速开发、现代项目 |

## 支持的元素

```
布局元素:
  - Container (容器)
  - Grid (网格)
  - Flex (弹性布局)
  - Stack (堆叠)

颜色系统:
  - Primary colors (主色)
  - Secondary colors (辅色)
  - Text colors (文字色)
  - Background colors (背景色)

排版:
  - Font family (字体)
  - Font size (字号)
  - Line height (行高)
  - Font weight (字重)

组件:
  - Button (按钮)
  - Card (卡片)
  - Navigation (导航)
  - Input (输入框)
  - Modal (弹窗)
  - List (列表)

素材:
  - Images (图片)
  - Icons (图标)
  - Illustrations (插图)
```

## 执行流程

```
1. 验证 Figma URL
2. 提取设计 ID
3. 获取设计稿截图
4. 调用 MCP 图像分析
5. 解析分析结果
6. 生成 HTML 结构
7. 生成样式代码
8. 下载素材资源
9. 输出到指定目录
10. 生成分析报告
```

## 输出格式

```
output/
├── index.html
├── style.css (separate 模式)
├── assets/
│   ├── images/
│   │   └── *.png/*.jpg
│   └── icons/
│       └── *.svg/*.png
└── analysis.json
    {
      "layout": {...},
      "colors": [...],
      "typography": {...},
      "components": [...],
      "assets": [...]
    }
```

## Limitations

- 需要 MCP 图像分析服务器
- Figma 链接需公开或有权限
- 复杂动画无法复现
- 交互需手动实现
- 大型设计需分段处理
- API 调用次数限制

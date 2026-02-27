---
name: flutter-image-to-spec-converter
description: 从 UI 截图/草图生成技术规格
version: 1.0
category: requirements
---

# 图像转规格转换器（Image to Spec Converter）

## Capabilities（单一职责）
- 接收 UI 截图或草图
- 使用图像分析技术解析 UI 元素
- 提取技术规格要素
- 输出结构化 JSON spec

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
**必须**：图像分析 MCP（Image Analysis）

## 执行流程（5 步骤）

```
1. 接收图像文件
2. 调用图像分析 MCP
3. 识别 UI 元素（按钮、输入框、列表等）
4. 提取布局和样式信息
5. 输出到 output/image_spec.json
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 图像文件 | .png, .jpg, .jpeg | UI 截图或草图 |
| 元素类型 | 字符串（可选） | 指定要识别的元素类型 |

示例：
```bash
/flutter-image-to-spec-converter ui_design.png
/flutter-image-to-spec-converter ui_design.png --elements "button,input,list"
```

## 输出规范

**图像 spec 格式**：
```json
{
  "spec_id": "IMG-REQ-001",
  "source_image": "ui_design.png",
  "analyzed_at": "2026-02-27T15:30:00Z",
  "dimensions": {
    "width": 375,
    "height": 667,
    "unit": "points"
  },
  "ui_elements": [
    {
      "id": "EL-001",
      "type": "button",
      "label": "提交",
      "position": { "x": 20, "y": 500 },
      "size": { "width": 335, "height": 44 },
      "properties": {
        "background_color": "#007AFF",
        "text_color": "#FFFFFF",
        "corner_radius": 8
      }
    },
    {
      "id": "EL-002",
      "type": "input",
      "placeholder": "请输入手机号",
      "position": { "x": 20, "y": 200 },
      "size": { "width": 335, "height": 44 },
      "properties": {
        "border_width": 1,
        "border_color": "#E5E5E5",
        "corner_radius": 4
      }
    }
  ],
  "layout_suggestions": [
    "建议使用 Column 垂直布局",
    "按钮建议使用 Padding 增加间距"
  ]
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行图像转换器**（<3 分钟）
   ```bash
   /flutter-image-to-spec-converter ui_design.png
   ```

2. **检查 UI 元素识别**（<2 分钟）
   ```bash
   cat output/image_spec.json | jq '.ui_elements[].type'
   ```
   预期：识别出按钮、输入框、列表等元素

3. **验证位置和尺寸**（<3 分钟）
   ```bash
   jq '.ui_elements[] | "\(.type): \(.position), \(.size)"' output/image_spec.json
   ```
   预期：位置和尺寸与图像一致

4. **对比原图验证**（<2 分钟）
   - 打开原始图像
   - 对比识别结果的位置和类型
   - 检查是否有遗漏

**总耗时：≤ 10 分钟**

成功标志：
- UI 元素类型正确识别
- 位置和尺寸与图像一致
- 样式属性（颜色、圆角等）准确提取

### 失败场景

- **图像文件不存在** → 错误："图像文件不存在"
- **MCP 未连接** → 错误："图像分析 MCP 未连接"
- **图像无法解析** → 错误："图像解析失败"
- **未识别到元素** → 警告："未识别到 UI 元素，请检查图像质量"

## Limitations（必须声明）

- 本 Skill 只负责图像分析，不生成 Flutter 代码
- 依赖图像质量和清晰度
- 手绘草图识别精度可能降低
- 不识别复杂动画和交互
- 生成的是技术规格建议，需人工审核

## 使用方法

### 基本用法
```bash
/flutter-image-to-spec-converter ui_design.png
```

### 指定识别元素
```bash
/flutter-image-to-spec-converter ui_design.png --elements "button,input,text"
```

### 输出 Flutter 代码建议
```bash
/flutter-image-to-spec-converter ui_design.png --code-hints
```

### 输出详细模式
```bash
/flutter-image-to-spec-converter ui_design.png --verbose
```

## 输出文件位置
```
output/
└── image_spec.json    # 图像技术规格
```

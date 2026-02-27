---
name: flutter-nlp-requirements-extractor
description: 使用 NLP 从自然语言需求中提取技术规格
version: 1.0
category: requirements
---

# NLP 需求提取器（NLP Requirements Extractor）

## Capabilities（单一职责）
- 接收自然语言需求文本
- 使用 NLP 技术解析需求
- 提取技术规格要素（功能点、约束、用户故事等）
- 输出结构化 JSON spec

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
无（可选：NLP processing MCP，如可用可提升精度）

## 执行流程（5 步骤）

```
1. 解析自然语言需求文本
2. 识别需求中的关键实体（功能、约束、用户角色）
3. 提取技术规格要素
4. 构建结构化 JSON spec
5. 输出到 output/spec.json
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 自然语言需求 | 纯文本/Markdown | 用户或产品经理提供的原始需求描述 |

示例：
```
需要一个电商App，支持用户浏览商品、加入购物车、下单支付。
支付方式支持微信和支付宝，需要支持Android和iOS双端。
```

## 输出规范

**JSON spec 格式**：
```json
{
  "spec_id": "REQ-001",
  "extracted_at": "2026-02-27T15:30:00Z",
  "title": "电商App需求",
  "features": [
    {
      "id": "F-001",
      "name": "商品浏览",
      "type": "user_action",
      "priority": "high",
      "description": "支持用户浏览商品列表"
    },
    {
      "id": "F-002",
      "name": "购物车",
      "type": "user_action",
      "priority": "high",
      "description": "支持用户加入购物车"
    },
    {
      "id": "F-003",
      "name": "下单支付",
      "type": "user_action",
      "priority": "high",
      "description": "支持用户下单支付"
    }
  ],
  "platforms": ["Android", "iOS"],
  "payment_methods": ["微信支付", "支付宝"],
  "user_roles": ["用户"]
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行提取器**（<2 分钟）
   ```bash
   /flutter-nlp-requirements-extractor "需求文本..."
   ```

2. **检查 JSON 输出**（<2 分钟）
   ```bash
   cat output/spec.json | jq .
   ```
   预期：JSON 格式正确，包含 spec_id, features, platforms 等字段

3. **验证实体识别**（<3 分钟）
   - features 数量是否覆盖所有功能点
   - platforms 是否正确识别
   - payment_methods 是否完整

4. **验证字段完整性**（<3 分钟）
   ```bash
   jq 'has("spec_id") and has("features") and has("platforms")' output/spec.json
   # 预期: true
   ```

**总耗时：≤ 10 分钟**

成功标志：
- JSON 格式可解析
- features 包含需求中的所有功能点
- platforms 和约束字段正确提取

### 失败场景

- **需求文本为空** → 错误："需求文本不能为空"
- **无法识别任何实体** → 警告："未提取到有效规格，请检查需求描述"
- **JSON 生成失败** → 错误："规格生成失败"

## Limitations（必须声明）

- 本 Skill 只负责提取规格，不验证规格的可行性
- 依赖自然语言的清晰度，模糊需求可能提取不完整
- 不进行需求冲突检测（应由 flutter-conflict-detector 处理）
- 输出为结构化建议，需人工审核后使用
- NLP 识别精度受语言复杂性影响

## 使用方法

### 基本用法
```bash
/flutter-nlp-requirements-extractor "需求文本"
```

### 从文件读取
```bash
/flutter-nlp-requirements-extractor --file requirements.txt
```

### 指定输出路径
```bash
/flutter-nlp-requirements-extractor "需求文本" --output ./custom/path/spec.json
```

### 输出详细模式
```bash
/flutter-nlp-requirements-extractor "需求文本" --verbose
```

## 输出文件位置
```
output/
└── spec.json    # 结构化需求规格
```

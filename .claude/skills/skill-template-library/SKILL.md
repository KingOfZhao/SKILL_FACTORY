---
name: skill-template-library
description: 技能模板库，可复用的技能模板集合
---

# 技能模板库（Skill Template Library）

## Capabilities（单一职责）
- 管理可复用的技能模板
- 提供模板搜索和筛选
- 支持模板版本控制
- 导出模板实例

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 扫描模板库
2. 解析模板元数据
3. 构建模板索引
4. 处理模板搜索和筛选
5. 输出模板列表
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 搜索关键词 | 字符串 | 按技能名称或描述搜索 |
| 分类筛选 | 字符串 | 按类型筛选 |

## 输出规范

**模板列表**：
```json
{
  "library_time": "2026-02-27T18:30:00Z",
  "total_templates": 10,
  "categories": {
    "ui": {
      "count": 4,
      "templates": [
        {
          "id": "T-UI-001",
          "name": "flutter-page-template",
          "category": "ui",
          "description": "Flutter 页面基础模板",
          "structure": "Page scaffold with basic widgets",
          "variables": ["page_name", "widgets", "actions"]
        },
        {
          "id": "T-UI-002",
          "name": "flutter-component-template",
          "category": "ui",
          "description": "Flutter 组件模板",
          "structure": "Reusable widget with props",
          "variables": ["component_name", "props", "styles"]
        }
      ]
    },
    "data": {
      "count": 3,
      "templates": [
        {
          "id": "T-DATA-001",
          "name": "flutter-model-template",
          "category": "data",
          "description": "Flutter 数据模型模板",
          "structure": "Data class with JSON serialization",
          "variables": ["model_name", "fields", "methods"]
        }
      ]
    },
    "api": {
      "count": 2,
      "templates": [
        {
          "id": "T-API-001",
          "name": "flutter-api-client-template",
          "category": "api",
          "description": "Flutter API 客户端模板",
          "structure": "API client with request/response handling",
          "variables": ["api_name", "endpoints", "authentication"]
        }
      ]
    },
    "test": {
      "count": 1,
      "templates": [
        {
          "id": "T-TEST-001",
          "name": "flutter-test-template",
          "category": "test",
          "description": "Flutter 测试用例模板",
          "structure": "Test file with setup/teardown",
          "variables": ["test_name", "test_type", "assertions"]
        }
      ]
    }
  },
  "search_index": {
    "by_name": ["flutter-page", "flutter-component", "flutter-model"],
    "by_keyword": ["scaffold", "reusable", "api", "test", "page"]
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **搜索模板**（<2 分钟）
   ```bash
   /skill-template-library --search "page"
   ```

2. **检查模板列表**（<2 分钟）
   ```bash
   cat output/templates.json | jq .total_templates
   # 预期: > 0
   ```

3. **筛选分类**（<2 分钟）
   ```bash
   /skill-template-library --category ui
   # 预期: 只显示 UI 模板
   ```

4. **导出模板实例**（<2 分钟）
   ```bash
   /skill-template-library --export T-UI-001 --output ./my-page
   # 预期: 在当前目录生成页面代码
   ```

5. **验证变量替换**（<2 分钟）
   ```bash
   # 检查导出的模板中变量是否被正确替换
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 模板列表包含分类索引
- 搜索功能正常工作
- 导出的模板代码可编译

## Limitations（必须声明）
- 本 Skill 只负责模板管理，不执行生成
- 模板质量取决于维护者的更新
- 变量替换基于简单的字符串替换

## 使用方法

### 列出所有模板
```bash
/skill-template-library --list-all
```

### 搜索模板
```bash
/skill-template-library --search "api"
```

### 按分类筛选
```bash
/skill-template-library --category data
```

### 导出模板实例
```bash
/skill-template-library --export T-DATA-001 --variables '{"model_name":"User","fields":["name","email"]}'
```

## 输出文件位置
```
output/
├── templates.json    # 模板列表和索引
└── exports/          # 导出的模板实例
```

---
name: flutter-voice-requirement-capture
description: 语音转文字需求录入
version: 1.0
category: requirements
---

# 语音需求捕获器（Voice Requirement Capture）

## Capabilities（单一职责）
- 接收语音文件
- 使用语音转文字技术转换为文字
- 输出结构化需求 spec
- 支持多语言语音识别

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
**必须**：语音转文字 MCP（Speech-to-Text）

## 执行流程（5 步骤）

```
1. 接收语音文件
2. 调用语音转文字 MCP
3. 转换为文本内容
4. 格式化为需求 spec
5. 输出到 output/voice_spec.json
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 语音文件 | .m4a, .mp3, .wav | 录音文件 |
| 语言代码 | ISO 639-1（可选） | 默认 zh-CN |

示例：
```bash
/flutter-voice-requirement-capture requirements_voice.m4a
/flutter-voice-requirement-capture requirements_voice.m4a --lang en-US
```

## 输出规范

**语音 spec 格式**：
```json
{
  "spec_id": "VOICE-REQ-001",
  "captured_at": "2026-02-27T15:30:00Z",
  "source_file": "requirements_voice.m4a",
  "duration": "120.5",
  "language": "zh-CN",
  "transcribed_text": "需要一个电商App，支持用户浏览商品、加入购物车...",
  "confidence_score": 0.95,
  "structured_spec": {
    "features": [
      {
        "id": "VF-001",
        "name": "商品浏览",
        "type": "user_action",
        "description": "支持用户浏览商品列表"
      }
    ]
  },
  "warnings": []
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行语音捕获器**（<3 分钟）
   ```bash
   /flutter-voice-requirement-capture voice_file.m4a
   ```

2. **检查文本转换结果**（<2 分钟）
   ```bash
   cat output/voice_spec.json | jq '.transcribed_text'
   ```
   预期：文本内容与录音内容一致

3. **验证置信度分数**（<2 分钟）
   ```bash
   jq '.confidence_score' output/voice_spec.json
   # 预期: > 0.85
   ```

4. **对比录音验证**（<3 分钟）
   - 播放原始录音
   - 对比 transcribed_text
   - 检查是否有遗漏或错误

**总耗时：≤ 10 分钟**

成功标志：
- transcribed_text 与录音内容一致
- confidence_score > 0.85
- structured_spec 正确提取功能点

### 失败场景

- **语音文件不存在** → 错误："语音文件不存在"
- **MCP 未连接** → 错误："语音转文字 MCP 未连接"
- **转换失败** → 错误："语音转换失败"
- **置信度过低** → 警告："转换置信度低，请人工审核"

## Limitations（必须声明）

- 本 Skill 只负责语音转文字，不验证需求可行性
- 依赖语音清晰度，嘈杂环境可能影响转换精度
- MCP 转换速度受网络影响
- 不支持实时语音录入（仅文件）
- 结构化提取依赖后续处理

## 使用方法

### 基本用法
```bash
/flutter-voice-requirement-capture voice_file.m4a
```

### 指定语言
```bash
/flutter-voice-requirement-capture voice_file.m4a --lang en-US
```

### 仅输出文本
```bash
/flutter-voice-requirement-capture voice_file.m4a --text-only
```

### 输出详细模式
```bash
/flutter-voice-requirement-capture voice_file.m4a --verbose
```

## 输出文件位置
```
output/
└── voice_spec.json    # 语音需求规格
```

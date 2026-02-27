# 本次生成的新模式提取

## 模式 1: 前缀过滤规则（元-skill 豁免）

### 描述
在技能检查器中，需要区分 meta-skill（元-前缀）和普通 skill。元-skill 不受 10 分钟验证原则约束。

### 规则
```
if [[ "$skill_name" == 元-* ]]; then
    # 跳过元-skill
    continue
fi
```

### 应用场景
- 元-skill-检查器
- 任何需要区分 meta 和普通 skill 的场景

---

## 模式 2: 静态验证工具设计

### 描述
验证工具应该只检查不修改，通过文件结构和内容分析来判断合规性。

### 核心原则
1. 只检查，不修改
2. 静态分析优先
3. 输出可验证的 JSON 报告
4. 提供 5 维度验证框架

### 验证维度
1. 文件完整性
2. 内容结构
3. 验证机制
4. 失败处理
5. 输出可验证性

---

## 模式 3: JSON 输出标准化

### 描述
标准化 JSON 输出格式，确保报告包含必需字段。

### 必需字段
```json
{
  "timestamp": "ISO8601",
  "skills_directory": "string",
  "total_skills": number,
  "meta_skills_excluded": number,
  "non_meta_skills_checked": number,
  "summary": {
    "passed": number,
    "warnings": number,
    "failed": number
  },
  "skills": [...]
}
```

### 每个技能对象
```json
{
  "name": "string",
  "path": "string",
  "status": "passed|warning|failed",
  "missing_items": ["string"],
  "suggestions": ["string"]
}
```

---

## 模式 4: 颜色输出分离

### 描述
在脚本中，将用户可见的彩色输出和机器可读的 JSON 输出分离到不同的流。

### 实现
```bash
# 用户输出 → stderr
echo -e "${BLUE}→${NC} 检查 $skill_name" >&2

# JSON 输出 → stdout
echo '{"name": "'"$skill_name"'"}'
```

### 优势
- JSON 输出可被其他程序直接解析
- 用户输出提供实时反馈
- 两者互不干扰

---

## 模式 5: 空数组安全处理

### 描述
在生成 JSON 数组时，正确处理空数组情况，避免语法错误。

### 安全实现
```bash
if [[ ${#array[@]} -eq 0 ]]; then
    result="[]"
else
    # 构建数组
    result="["
    local first=true
    for item in "${array[@]}"; do
        # 转义 JSON 特殊字符
        local escaped=$(echo "$item" | sed 's/\\/\\\\/g; s/"/\\"/g')
        # 添加到数组
        if [[ "$first" == true ]]; then
            result="$result\"$escaped\""
            first=false
        else
            result="$result, \"$escaped\""
        fi
    done
    result="$result]"
fi
```

---

## 建议更新到 common-overlaps.md

### 优先级 1
- 模式 1: 前缀过滤规则（元-skill 豁免）
- 模式 4: 颜色输出分离

### 优先级 2
- 模式 2: 静态验证工具设计
- 模式 3: JSON 输出标准化
- 模式 5: 空数组安全处理

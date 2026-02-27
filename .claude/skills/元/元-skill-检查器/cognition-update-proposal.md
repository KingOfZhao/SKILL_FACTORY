# 结构化认知更新提案

## 提案来源
元-skill-生成器生成 元-skill-检查器 时提取

## 更新时间
2026-02-27

## 提议更新内容

### 1. 新增: Meta-Skill 豁免规则

**位置**: `common/underlying-convention.md`

**新增内容**:
```markdown
### Meta-Skill 豁免

所有以"元-"开头的 skill 自动豁免于 10 分钟可验证原则。

Meta-skill 的职责是：
- 生成、优化、检查其他 skill
- 提供工具和框架支持
- 不直接面向最终用户

因此 meta-skill 不需要遵守 10 分钟验证原则，但应保持高质量和可维护性。
```

---

### 2. 新增: 验证工具设计模式

**位置**: `common/overlaps.md` (新建)

**新增内容**:
```markdown
## 验证工具设计模式

### 静态验证原则
1. 只检查，不修改
2. 静态分析优先
3. 输出可验证的报告（JSON/可对比格式）

### 5 维度验证框架
1. 文件完整性
2. 内容结构
3. 验证机制
4. 失败处理
5. 输出可验证性

### JSON 输出标准化
参见 `待应用-skill/元-skill-检查器/overlaps/new-patterns.md` 中模式 3
```

---

### 3. 新增: 输出流分离最佳实践

**位置**: `common/overlaps.md`

**新增内容**:
```markdown
## 输出流分离

### 原则
将用户可见的输出和机器可读的输出分离到不同的流：

- 用户输出 → stderr（彩色、进度、提示信息）
- 机器输出 → stdout（JSON、结构化数据）

### 实现
```bash
# 用户输出
echo -e "${BLUE}→${NC} 进度信息" >&2

# 机器输出
echo '{"status": "success", "data": {...}}'
```

### 优势
- JSON 输出可直接被其他程序解析
- 用户输出提供实时反馈
- 管道使用时只捕获机器输出
```

---

### 4. 新增: Bash 数组安全处理

**位置**: `common/overlaps.md`

**新增内容**:
```markdown
## Bash 数组安全处理

### 空数组陷阱
在使用 `set -euo pipefail` 时，空数组可能导致脚本异常退出。

### 安全模式
```bash
if [[ ${#array[@]} -eq 0 ]]; then
    result="[]"
else
    # 构建数组
    result="["
    local first=true
    for item in "${array[@]}"; do
        # 转义特殊字符
        local escaped=$(echo "$item" | sed 's/\\/\\\\/g; s/"/\\"/g')
        # 添加元素
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

### JSON 字符转义
- `\` → `\\`
- `"` → `\"`
- 其他特殊字符也需要处理
```

---

## 需要人工确认的项目

1. **Meta-Skill 豁免规则**: 是否需要将其写入 `underlying-convention.md`？
2. **common/overlaps.md**: 是否需要创建此文件来存储可复用模式？
3. **验证工具模式**: 是否将 5 维度验证框架标准化？

## 待办事项

- [ ] 人工审查并批准上述提案
- [ ] 更新 `common/underlying-convention.md`
- [ ] 创建/更新 `common/overlaps.md`
- [ ] 将 `待应用-skill/元-skill-检查器` 移动到正式位置
- [ ] 更新相关文档

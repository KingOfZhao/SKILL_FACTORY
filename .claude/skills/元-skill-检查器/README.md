# 元-Skill 检查器

检查所有非元-前缀的 skill 是否符合 10 分钟可验证原则的验证工具。

## 功能

- 自动扫描 skills 目录，识别非元-前缀 skill
- 从五个维度验证合规性：
  1. 文件完整性
  2. 内容结构
  3. 验证机制
  4. 失败处理
  5. 输出可验证性
- 生成 JSON 格式的合规报告
- 提供具体改进建议

## 快速开始

### 基本用法
```bash
cd 待应用-skill/元-skill-检查器
./scripts/checker.sh
```

### 指定目录
```bash
./scripts/checker.sh /path/to/skills
```

### 仅显示失败项
```bash
./scripts/checker.sh --failures-only
```

### 详细模式
```bash
./scripts/checker.sh --verbose
```

## 10 分钟验证

### 验证步骤

1. **运行检查器**（<2 分钟）
   ```bash
   ./scripts/checker.sh
   ```

2. **检查输出文件**（<2 分钟）
   ```bash
   cat check-results/skill-compliance-report.json | jq .
   ```

3. **验证 JSON 格式**（<2 分钟）
   ```bash
   jq empty check-results/skill-compliance-report.json
   ```

4. **检查必需字段**（<2 分钟）
   ```bash
   jq 'has("timestamp") and has("skills") and has("summary")' check-results/skill-compliance-report.json
   ```

5. **查看汇总结果**（<2 分钟）
   ```bash
   jq '.summary' check-results/skill-compliance-report.json
   ```

**总耗时：≤ 10 分钟**

## 输出格式

`check-results/skill-compliance-report.json`:

```json
{
  "timestamp": "2026-02-27T12:00:00Z",
  "skills_directory": "/path/to/skills",
  "total_skills": 5,
  "meta_skills_excluded": 4,
  "non_meta_skills_checked": 2,
  "summary": {
    "passed": 0,
    "warnings": 1,
    "failed": 1
  },
  "skills": [
    {
      "name": "skill-name",
      "path": "/path/to/skill-name",
      "status": "passed|warning|failed",
      "missing_items": [],
      "suggestions": []
    }
  ]
}
```

## 验证脚本

运行验证脚本检查自身输出：
```bash
./scripts/verify.sh
```

## 已知局限

- 只进行静态检查，不实际执行被检查的 skill
- 检查结果基于文件内容和结构分析
- 元-前缀的 skill 自动跳过检查
- 依赖 SKILL.md 内容的规范性
- 不修改被检查的 skill 文件

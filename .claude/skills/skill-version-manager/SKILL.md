---
name: skill-version-manager
description: 技能版本管理，版本控制和变更追踪
---

# 技能版本管理器（Skill Version Manager）

## Capabilities（单一职责）
- 管理技能版本信息
- 追踪技能变更历史
- 生成版本差异报告
- 支持版本回滚

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 读取当前技能库
2. 生成版本标识
3. 记录变更信息
4. 生成版本报告
5. 更新版本索引
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 操作类型 | 字符串 | create/update/delete |

## 输出规范

**版本报告**：
```json
{
  "version_time": "2026-02-27T18:30:00Z",
  "version_info": {
    "current_version": "1.2.3",
    "previous_version": "1.2.2",
    "semantic_version": "major.minor.patch"
  },
  "changes": [
    {
      "change_id": "C-001",
      "type": "update",
      "skill": "flutter-login-page",
      "version": "1.2.3",
      "timestamp": "2026-02-27T18:00:00Z",
      "description": "新增密码强度验证功能",
      "changes": [
        "added: password_validator.dart",
        "modified: login_page.dart",
        "removed: null"
      ]
    }
  ],
  "version_history": [
    {
      "version": "1.2.2",
      "release_date": "2026-02-26T00:00:00Z",
      "description": "修复登录页面性能问题"
    },
    {
      "version": "1.2.3",
      "release_date": "2026-02-27T00:00:00Z",
      "description": "新增密码强度验证功能"
    }
  ],
  "diff": {
    "file": "flutter-login-page",
    "from_version": "1.2.2",
    "to_version": "1.2.3",
    "changes_count": 3
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **注册版本**（<2 分钟）
   ```bash
   /skill-version-manager --type create --skill flutter-login-page --version 1.0.0
   ```

2. **查看版本历史**（<2 分钟）
   ```bash
   /skill-version-manager --history flutter-login-page
   # 预期: 看到所有版本
   ```

3. **生成版本差异**（<2 分钟）
   ```bash
   /skill-version-manager --diff flutter-login-page 1.2.2 1.2.3
   # 预期: 看到具体变更
   ```

4. **回滚到指定版本**（<2 分钟）
   ```bash
   /skill-version-manager --rollback flutter-login-page 1.2.2
   # 预期: 成功回滚
   ```

5. **检查版本索引**（<2 分钟）
   ```bash
   /skill-version-manager --list-all
   # 预期: 看到所有技能的版本
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 版本信息正确记录
- 变更历史完整
- diff 正确显示变更

## Limitations（必须声明）
- 本 Skill 只负责版本记录
- 不实际执行回滚操作
- 依赖手动执行变更

## 使用方法

### 创建新版本
```bash
/skill-version-manager --create --skill flutter-login-page --version 1.0.0 --description "初始版本"
```

### 更新版本
```bash
/skill-version-manager --update --skill flutter-login-page --version 1.0.1 --description "修复登录bug"
```

### 查看版本历史
```bash
/skill-version-manager --history flutter-login-page
```

### 生成版本差异
```bash
/skill-version-manager --diff flutter-login-page 1.0.0 1.0.1
```

## 输出文件位置
```
output/
├── version-report.json    # 版本报告
├── version-history.json   # 历史记录
└── diffs/                # 版本差异文件
```

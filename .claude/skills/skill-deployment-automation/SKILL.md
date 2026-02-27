---
name: skill-deployment-automation
description: 技能自动部署，一键部署到正式位置
---

# 技能自动部署器（Skill Deployment Automation）

## Capabilities（单一职责）
- 自动部署技能到目标位置
- 执行部署前验证
- 生成部署日志
- 支持回滚

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 读取部署配置
2. 执行预部署检查
3. 复制技能文件到目标位置
4. 执行部署后验证
5. 生成部署报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 技能列表 | JSON | 要部署的技能列表 |
| 目标位置 | 字符串 | 部署目标路径 |
| 部署模式 | 字符串 | copy/sync |

## 输出规范

**部署报告**：
```json
{
  "deployment_time": "2026-02-27T18:30:00Z",
  "deployment_mode": "copy",
  "target_location": "/path/to/production/skills",
  "deployed_skills": [
    {
      "skill_name": "flutter-login-page",
      "source": "/path/to/staging/skills/flutter-login-page",
      "destination": "/path/to/production/skills/flutter-login-page",
      "status": "success",
      "size_bytes": 12345,
      "files_count": 5
    },
    {
      "skill_name": "flutter-shopping-cart",
      "source": "/path/to/staging/skills/flutter-shopping-cart",
      "destination": "/path/to/production/skills/flutter-shopping-cart",
      "status": "success",
      "size_bytes": 23456,
      "files_count": 8
    }
  ],
  "summary": {
    "total_skills": 2,
    "successful": 2,
    "failed": 0,
    "skipped": 0,
    "total_size_bytes": 35801
  },
  "verification": {
    "pre_deployment_check": "passed",
    "post_deployment_check": "passed",
    "test_results": []
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **执行部署**（<2 分钟）
   ```bash
   /skill-deployment-automation --list skills-to-deploy.json --target /production/skills --mode copy
   ```

2. **检查部署报告**（<2 分钟）
   ```bash
   cat output/deployment-report.json | jq .summary
   # 预期: successful > 0
   ```

3. **验证文件复制**（<2 分钟）
   ```bash
   ls /path/to/production/skills/flutter-login-page
   # 预期: 文件存在
   ```

4. **执行回滚**（<2 分钟）
   ```bash
   /skill-deployment-automation --rollback --deployment-id DEP-001
   # 预期: 成功回滚到上一个版本
   ```

5. **查看部署历史**（<2 分钟）
   ```bash
   /skill-deployment-automation --history
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 部署报告显示成功
- 文件正确复制到目标位置
- 回滚功能正常工作

## Limitations（必须声明）
- 本 Skill 只负责文件复制，不执行其他部署操作
- 不处理依赖关系
- 回滚需要保存上一个版本的备份

## 使用方法

### 部署单个技能
```bash
/skill-deployment-automation --deploy flutter-login-page --target /production/skills
```

### 批量部署
```bash
/skill-deployment-automation --deploy-list skills-to-deploy.json --target /production/skills
```

### 回滚部署
```bash
/skill-deployment-automation --rollback --deployment-id DEP-001
```

### 查看部署历史
```bash
/skill-deployment-automation --history
```

## 输出文件位置
```
output/
├── deployment-report.json    # 部署报告
├── deployment-log.json       # 部署日志
└── backups/                # 备份文件
```

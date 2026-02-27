---
name: 元-skill-生成器
description: MCP-Aware 高级 Skill 生成器 - 带结构化认知自精炼机制
version: 1.2
author: 赵先生定制（已加入创建中自完善认知）
---

# MCP-Aware Skill 生成器（v1.2）

## Capabilities（严格限定）
- ...（原有内容不变）
- **新增**：生成完成后自动执行“结构化认知精炼”步骤，积累 overlaps/ 并输出 proposal

## 执行前必须读取
common/underlying-convention.md

## 执行流程（强制 6 步）
1. 读取底层约定
2. MCP 检查
3. 有限横竖穷举
4. 生成单一职责 Skill（含 description.md + 局限声明）
5. 输出到 待应用-skill/
6. **结构化认知精炼**：提取本次新模式 → 追加 overlaps/common-overlaps.md → 生成 cognition-update-proposal.md

## Limitations（本 Skill 自身）
- 仍依赖用户输入质量（模糊需求 → 精炼效果减弱）
- 认知积累仅写入 overlaps/（需人工或修复 Skill 最终应用到模板）
- 无法自动修改自身核心文件（符合规则）
- 穷举仍为有限深度（token 约束）

## 使用方法
输入需求后，会自动完成全部 6 步，并在最后告诉你“本次精炼新增了哪些结构化认知”。
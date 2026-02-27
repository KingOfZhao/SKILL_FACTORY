# 项目级重叠/通用模式收集（不写入底层约定，独立管理）

## 已识别重叠模式（生成过程中自动/手动追加）

输入类重叠：
- 用户自然语言描述
- 代码片段 / 错误日志
- 参考文档 / API spec
- 多模态（截图、设计稿）

过程类重叠：
- 分析 → 规划 → 执行 → 验证 → 优化（几乎所有生成/修复类 Skill 都有）
- 参考同领域最佳实践 + 关键词筛选
- 错误处理与回滚

输出类重叠：
- 单文件内容
- 完整项目结构（带目录树）
- diff 格式
- 可运行构建物（apk、zip 等）
- 建议的后续 Skill 列表

MCP 关联重叠：
- 文件读写 → 需要文件系统 MCP
- 网络请求 → 需要网络 MCP
- 代码执行 → 需要 code-interpreter 或 sandbox MCP
## 局限性声明模板重叠（本次可新增）
- “本 Skill 只负责 X，不负责 Y。建议配套 Skill：A、B、C”

## 本次生成新增认知（2026-02-26）

### skill-修复器 新模式

**元认知模式：**
- 修复类 Skill 应包含完整的诊断 → 修复 → 验证闭环
- 输出格式标准化：diagnosis.json + fix-plan.md + verification.json
- 安全边界：禁止修复自身、禁止修改底层约定

**检测维度（可复用）：**
1. 结构完整性（必需文件、命名约定）
2. 语法格式（YAML/JSON 语法）
3. 约定遵守（SKILL.md 行数、错误处理）
4. 工具调用合法性
5. 输出条件验证

**脚本模式：**
- 使用 `set -euo pipefail` 确保错误处理
- 颜色输出增强可读性（RED/GREEN/YELLOW）
- JSON 输出便于程序解析

---

### skill-优化器 新模式

**元认知模式：**
- 优化类 Skill 应基于历史数据进行模式分析
- 拓展与增强双轨制：拓展同类型 skill + 增强上游工具
- 分析 → 推荐 → 生成 → 评估 四步流程

**拓展类型映射（可复用）：**
```
问题类别 → 拓展类型
结构问题   → validator, formatter
语法错误   → formatter
约定违反   → compliance
工具调用   → dependency
```

**拓展类型体系（可复用）：**
1. **validator** - 验证器（严格/轻量/增量）
2. **formatter** - 格式化器（自动规范化）
3. **compliance** - 合规检查器（约定遵守）
4. **dependency** - 依赖分析器（工具/依赖）
5. **profiler** - 性能分析器（执行性能）
6. **doc-gen** - 文档生成器（文档产出）
7. **test-gen** - 测试生成器（测试用例）

**输出模式：**
- analysis.json - 结构化分析结果
- extension-plans/ - 拓展方案集合
- optimization-report.md - 优化效果评估

**增强维度模式：**
- 新增检测维度（基于问题频次）
- 修复逻辑智能化（基于历史数据）
- 输出格式可视化（HTML/图表）
- 性能优化（并行/缓存/增量）

---

### skill-figma-html 新模式

**元认知模式：**
- 设计转代码类 Skill 应包含完整的验证 → 分析 → 生成 → 下载流程
- 多格式输出：支持 inline/separate/tailwind 三种样式模式
- 可选功能：素材下载、响应式适配可独立控制

**输入类型（新增）：**
- Figma 链接 - 设计稿 URL（需验证格式和权限）
- File ID / Node ID - 从链接中提取

**MCP 强关联（新增）：**
- 图像分析 → 需要 4.5v-mcp 或类似视觉 MCP
- 网络请求 → 需要 HTTP MCP（获取 Figma 资源）
- 图像处理 → 需要图像处理 MCP（素材优化）

**输出结构（可复用）：**
```
output/
├── index.html          # 主 HTML 文件
├── style.css           # 样式文件（separate 模式）
├── assets/             # 素材目录
│   ├── images/         # 图片资源
│   └── icons/          # 图标资源
├── analysis.json       # 分析结果（结构化）
└── README.md          # 生成报告
```

**元素识别体系（可复用）：**
```
布局:
  - Container (容器)
  - Grid (网格)
  - Flex (弹性布局)
  - Stack (堆叠)

设计系统:
  - Colors (颜色：主色/辅色/背景色)
  - Typography (排版：字体/字号/字重)
  - Spacing (间距：padding/margin/gap)

组件:
  - Button (按钮)
  - Card (卡片)
  - Navigation (导航)
  - Input (输入框)
  - Modal (弹窗)
  - List (列表)

素材:
  - Images (图片)
  - Icons (图标)
  - Illustrations (插图)
```

**样式模式（可复用）：**
| 模式 | 输出 | 适用场景 |
|-----|------|---------|
| inline | 内联 CSS | 单页应用、简单页面 |
| separate | 分离 CSS | 大型项目、需维护 |
| tailwind | Tailwind CSS | 快速开发、现代项目 |

**边界控制模式：**
- 最大图层数限制（避免超时）
- 最大素材数限制（避免性能问题）
- 分析精度分级（平衡速度/质量）
- 分段处理大型设计稿

---

### infinite-physical-practice-enumerator 新模式

**元认知模式：**
- 无限穷举类 Skill 应采用树状节点结构（横向变体 + 纵向深度）
- 上下文满额自动保存 checkpoint，下次无缝继续
- 模式选择强制询问：物理实践 / 最小 Skill 树

**双模式体系（新增）：**
```
模式 1: 物理实践穷举
  - 重点：真实世界可动手、可观察的具体行动、实验、流程操作
  - Checkpoint: enumeration_checkpoint_physical.json
  - 输出：实践列表（步骤 + 观察 + 耗时/成本）

模式 2: 最小 Skill 树实践穷举
  - 重点：Skill 体系的最小化定义、拆分树、单一职责、依赖关系
  - Checkpoint: enumeration_checkpoint_skilltree.json
  - 输出：Skill 列表（职责 + 输入/输出 + 依赖 + 验证）
```

**Checkpoint 模式（可复用）：**
```yaml
机制:
  文件分离:
    - 物理: enumeration_checkpoint_physical.json
    - Skill树: enumeration_checkpoint_skilltree.json
    - 目的: 避免模式混淆

  格式:
    mode: "physical" | "skilltree"
    problem: 用户原始问题
    current_node: "level-N.branch-M"
    enumerated_so_far: [...]
    next_pending_branches: [...]
    timestamp: ISO8601

  保存触发:
    - 上下文剩余 < 30%
    - Token 数量 > 140k
    - 用户明确要求

  保存后回复:
    "节点已保存到 [文件路径]，下次输入任意内容即可继续。"
```

**树状穷举结构（可复用）：**
```
问题
  ├─ 横向：同层多种变体
  │    ├── 变体 1
  │    ├── 变体 2
  │    └── 变体 N
  └─ 纵向：基础 → 进阶 → 极端
       ├── 基础层 (level-1)
       ├── 进阶层 (level-2)
       └── 极端/边缘层 (level-3+)
```

**10分钟验证模式（可复用）：**
```
验证步骤（总耗时 ≤ 10 分钟）:
  1. 查看文件 (<10秒)
  2. 阅读列表 (3分钟)
  3. 任选验证 (5分钟)
  4. 对比判断 (<1分钟)

成功标志:
  - checkpoint 文件已更新
  - 至少 1 个实践可立即动手验证
```

**模式选择询问模板（可复用）：**
```
请先明确你要穷举的模式（回复数字或关键词即可）：

1. [模式1名称]
   → [模式1描述]

2. [模式2名称]
   → [模式2描述]

请输入 1 或 2（或对应关键词）。
```

**输出边界控制：**
- 每轮输出数：5-15 个实践/Skill
- 树状深度：建议不超过 5 层
- 上下文阈值：剩余 < 30% 触发保存
- Token 限制：> 140k 触发保存

# 认知更新提案（skill-generator 自我精炼）

## 生成时间
2026-02-26

## 本次生成对象
**skill-figma-html** (Figma-to-HTML)

---

## 新增结构化认知

### 1. 元认知模式

| 模式名称 | 描述 | 适用场景 |
|---------|------|---------|
| 设计转代码闭环 | 验证 → 分析 → 生成 → 下载完整流程 | 设计工具集成类 Skill |
| 多格式输出支持 | 支持多种样式模式切换 | 需要灵活输出的 Skill |
| 可选功能独立控制 | 素材下载、响应式等功能可开关 | 功能模块化的 Skill |

### 2. 输入类型（新增）

| 类型 | 格式 | 验证要求 |
|-----|------|---------|
| Figma 链接 | `https://www.figma.com/design/<file-id>/<node-id>` | 格式验证、权限检查 |
| File ID | 字符串 | 非空验证 |
| Node ID | 字符串 | 非空验证 |

### 3. MCP 强关联（新增）

| 功能 | 需求 | 说明 |
|-----|------|------|
| 图像分析 | 4.5v-mcp / 视觉 MCP | 识别布局、颜色、组件 |
| 网络请求 | HTTP MCP | 获取 Figma 资源 |
| 图像处理 | 图像处理 MCP | 素材优化、压缩 |

### 4. 输出结构（可复用）

```
output/
├── index.html              # 主输出文件
├── style.css              # 依赖文件（可选）
├── assets/                # 资源目录
│   ├── images/            # 子目录分类
│   └── icons/
├── analysis.json         # 结构化分析结果
└── README.md            # 生成报告
```

**适用场景**：任何需要生成文件 + 资源的 Skill

### 5. 元素识别体系（可复用）

```
布局层次:
  - Container  → 顶层容器
  - Grid       → 网格布局
  - Flex       → 弹性布局
  - Stack      → 堆叠布局

设计系统提取:
  - Colors     → 颜色变量
  - Typography → 排版规则
  - Spacing    → 间距系统

UI 组件:
  - Button     → 按钮
  - Card       → 卡片
  - Navigation → 导航
  - Input      → 输入框
  - Modal      → 弹窗
  - List       → 列表

素材类型:
  - Images     → 图片
  - Icons      → 图标
  - Illustrations → 插图
```

**适用场景**：任何设计转代码、UI 生成类 Skill

### 6. 样式模式（可复用）

| 模式 | 技术栈 | 适用场景 |
|-----|--------|---------|
| inline | 内联 CSS | 单页应用、简单页面 |
| separate | 分离 CSS 文件 | 大型项目、需维护 |
| tailwind | Tailwind CSS | 快速开发、现代项目 |

### 7. 边界控制模式（可复用）

```yaml
边界控制维度:
  限制图层数:
    - 原因: 避免超时
    - 默认: 100 层
    - 超出: 分页处理

  限制素材数:
    - 原因: 性能考虑
    - 默认: 20 个
    - 超出: 压缩或优化

  分析精度:
    - 原因: 平衡速度/质量
    - 级别: 低/中/高
    - 默认: 中等

  大型处理:
    - 原因: 避免 token 溢出
    - 策略: 分段处理
    - 单段: 小于 X tokens
```

---

## 对底层约定的潜在影响

### 无需修改项
- `underlying-convention.md` 已覆盖核心规则
- 新增模式与现有约定兼容

### 可选增强建议（需人工确认）

1. **MCP 标准化**：建议定义 MCP 工具的标准接口和返回格式

2. **输出结构规范**：建议统一多文件输出的目录结构规范

3. **边界控制标准**：建议定义通用的边界控制参数规范

---

## 认知积累状态

| 类别 | 数量 | 说明 |
|-----|------|------|
| 元认知模式 | 3 | 设计转代码闭环、多格式输出、可选功能控制 |
| 输入类型 | 3 | Figma 链接、File ID、Node ID |
| MCP 关联 | 3 | 图像分析、网络请求、图像处理 |
| 输出结构 | 1 | 标准多文件输出结构 |
| 元素识别体系 | 4 | 布局、设计系统、组件、素材 |
| 样式模式 | 3 | inline、separate、tailwind |
| 边界控制 | 4 | 图层限制、素材限制、精度分级、分段处理 |

---

## Skill 生态拓展

基于 Figma 转换，可拓展以下 Skill：

| Skill | 职责 | 依赖 |
|-------|------|------|
| skill-figma-html | Figma → HTML | 图像分析 MCP |
| skill-figma-react | Figma → React | skill-figma-html |
| skill-figma-tailwind | Figma → Tailwind | skill-figma-html |
| skill-figma-mobile | Figma → Mobile App | skill-figma-react |
| skill-figma-annotate | 为 Figma 添加标注 | 图像分析 MCP |

---

## 后续行动建议

### 短期（本次生成后）
- [ ] 人工审查本次生成的 skill-figma-html
- [ ] 配置 Figma API Token
- [ ] 测试实际图像分析功能
- [ ] 验证素材下载功能

### 中期（多次生成后）
- [ ] 实现其他设计工具转换（Sketch, Adobe XD）
- [ ] 建立设计系统标准格式
- [ ] 支持更多组件识别
- [ ] 实现交互功能生成

### 长期（持续迭代）
- [ ] 建立设计-代码自动化流水线
- [ ] 支持复杂动画转换
- [ ] 实现双向同步（代码更新回 Figma）
- [ ] 构建设计规范知识库

# 官方 Skill / Rules 映射（official-skills-map.md）

本文件把"实现阶段"映射到 **Flutter 官方资源**。本 Skill **不复制**官方内容，只负责"何时调用何者"。
官方更新后请同步本文件。

## 官方来源（已联网核实）

| 来源 | 地址 | 用途 |
|------|------|------|
| Flutter Agent Skills | https://github.com/flutter/skills | Flutter 团队维护的任务型 skill 集 |
| Dart Agent Skills | https://github.com/dart-lang/skills | Dart 任务（单测、依赖解析等） |
| Flutter/Dart AI Rules | https://docs.flutter.dev/ai/ai-rules | rules.md / rules_10k / rules_4k / rules_1k |
| AI best practices | https://docs.flutter.dev/ai/best-practices | 用 Flutter 工具给 AI 加 guardrail |
| Agent Skills 指南 | https://docs.flutter.dev/ai/agent-skills | 渐进式披露、安装方式 |

## 安装官方 Skill

```bash
# 安装全部 Flutter 官方 skill 到标准 .agents/skills 目录
npx skills add flutter/skills --skill '*' --agent universal
# 可选：Dart 任务 skill
npx skills add dart-lang/skills --skill '*' --agent universal
# 更新
npx skills update
```

> 说明：官方 skill 与 MCP 互补 —— MCP 提供"工具"，Skill 提供"如何用工具完成某任务"的步骤。

## flutter/skills 清单与触发时机

| 官方 Skill | 何时调用（本蒸馏器在对应阶段触发） |
|-----------|----------------------------------|
| `flutter-apply-architecture-best-practices` | 新项目分层 / 重构为 UI-Logic-Data 分层时 |
| `flutter-build-responsive-layout` | 需要适配手机/平板/桌面，使用 LayoutBuilder/MediaQuery/Flexible |
| `flutter-fix-layout-issues` | 出现 RenderFlex overflow / unbounded constraints 等布局报错 |
| `flutter-setup-declarative-routing` | 配置 go_router/auto_route、深链、Web URL |
| `flutter-implement-json-serialization` | 为 model 写 fromJson/toJson |
| `flutter-add-widget-test` | 用 WidgetTester 验证 UI 渲染与交互 |
| `flutter-add-integration-test` | 端到端用户流程测试（integration_test） |
| `flutter-add-widget-preview` | 为新组件加 previews.dart 交互预览 |

## 阶段 → 官方 Skill + 官方 Rule 对照

| 实现阶段 | 官方 Skill | 官方 Rule 要点 |
|---------|-----------|---------------|
| 需求澄清 | — | "请求歧义时先澄清目标平台/功能" |
| 架构分层 | flutter-apply-architecture-best-practices | Presentation/Domain/Data/Core 分层；大项目按 feature 组织 |
| 状态管理选型 | — | 优先内置方案；ValueNotifier/ChangeNotifier/MVVM；非显式要求不引第三方 |
| 数据模型 | flutter-implement-json-serialization | 健全 null-safety；用 records 返回多值；为公共 API 写文档注释 |
| 路由 | flutter-setup-declarative-routing | 用 go_router/auto_route 现代路由 |
| UI 组合 | flutter-build-responsive-layout | 组合优于继承；用小型私有 Widget 类而非返回 Widget 的方法 |
| 布局排错 | flutter-fix-layout-issues | 理解 constraints；处理 overflow/unbounded |
| 性能 | — | const 构造；ListView.builder/SliverList；compute() 跑重活；build() 内不做重活 |
| 错误/异步 | — | 正确 async/await + 错误处理；Stream/StreamBuilder、Future/FutureBuilder |
| 测试 | flutter-add-widget-test / flutter-add-integration-test | "Write code with testing in mind"，可注入 fake |
| 预览 | flutter-add-widget-preview | 交互式 widget 预览 |
| 代码风格 | — | Effective Dart；行宽≤80；PascalCase/camelCase/snake_case；用 logging 替代 print |
| Lint | — | `include: package:flutter_lints/flutter.yaml` |

## 降级策略

若环境未安装官方 skill / 无网络：仍按上表"官方 Rule 要点"列直接落实（这些要点已蒸馏进
`decision-trees.md` 与 `distilled-patterns.md`），并在蒸馏报告中标注"官方 skill 未安装，已按 rule 要点执行"。

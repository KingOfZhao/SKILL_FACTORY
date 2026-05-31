<!-- 本文件由 skill_factory.catalog 自动生成，请勿手工编辑 -->
# Skill 能力清单（自动生成）

- 扫描根目录：`.claude/skills`
- 技能总数：**62**（元 Skill 18 / 任务型 44）

## 技能列表

| 类型 | 名称 | 描述 | 路径 |
|------|------|------|------|
| 元 | `元-micro-diff-factory` | 微分 Skill 组 - 支持对任意问题/需求的微分拆解，自动积累拆解案例、公式、约束等 | `mate-skill-微分器` |
| 元 | `meta-capability-distillation` | 元-能力蒸馏器 - 将强模型(如 Opus 级)在任意领域的隐性实现/解题策略蒸馏为显式的决策树/playbook/反模式库/自检闭环，使普通模型在该领域的产出质量接近强模型。是 meta-flutter-impl-distillation | `meta-capability-distillation` |
| 元 | `meta-flutter-impl-distillation` | 元-Flutter 代码实现蒸馏器 - 将强模型(Opus 级)的隐性 Flutter 实现策略蒸馏为显式决策树/实现 playbook/反模式库/自检闭环，叠加在 Flutter 官方 Skill 与 AI Rules 之上，使普通模型在 | `meta-flutter-impl-distillation` |
| 元 | `元-skill-穷举器（增强版 v2.0）` | 对任意问题进行无限横竖穷举「物理实践」或「最小Skill树」，并自动收集领域最佳实践和积累通用模式，增强生成技能质量和兼容性。 | `meta-skill-enhancer` |
| 元 | `meta-skill-dependency-analyzer` | 元-Skill 依赖关系分析，绘制技能依赖图 | `元/meta-skill-dependency-analyzer` |
| 元 | `meta-skill-feedback-collector` | 元-Skill 反馈收集，用户反馈收集和分析 | `元/meta-skill-feedback-collector` |
| 元 | `meta-skill-mcp-compatibility-checker` | MCP 兼容性检查，验证元-Skill 与 MCP 的集成正确性 | `元/meta-skill-mcp-compatibility-checker` |
| 元 | `meta-skill-performance-analyzer` | 元-Skill 性能分析，监控执行效率和资源使用 | `元/meta-skill-performance-analyzer` |
| 元 | `meta-skill-usage-tracker` | 元-Skill 使用统计，收集使用数据和反馈 | `元/meta-skill-usage-tracker` |
| 元 | `meta-skill-validator-advanced` | 元-Skill 深度验证，检查元-Skill 自身的质量 | `元/meta-skill-validator-advanced` |
| 元 | `元-Skill推荐器` | 基于问题类型和上下文，自动推荐最优的技能组合 | `元/skill-recommender` |
| 元 | `元-skill-orchestrator` | 元 Skill 全链路编排器 - 自动串联问题穷举、生成、扫描、检查、优化流程 | `元/元-skill-orchestrator` |
| 元 | `元-skill-优化器` | 根据检查器结果，对 Skill 或底层约定进行优化 | `元/元-skill-优化器` |
| 元 | `元-skill-修复器` | 检查目标 skill 目录是否存在以下问题，并生成修复方案： | `元/元-skill-修复器` |
| 元 | `元-skill-扫描器` | 扫描指定文件夹下的所有 skills，生成能力清单和树状结构，用于 Claude Code 读取和调用 | `元/元-skill-扫描器` |
| 元 | `元-skill-检查器` | 按照底层约定检查所有 Skill，自动区分元 Skill / 非元 Skill / 非 Skill 内容 | `元/元-skill-检查器` |
| 元 | `元-skill-生成器` | MCP-Aware 高级 Skill 生成器 - 带结构化认知自精炼机制 | `元/元-skill-生成器` |
| 元 | `元-skill-问题穷举器` | 对任何问题进行无限横竖穷举「物理实践」或「最小Skill树」，上下文即将满额时自动保存穷举节点，下次无缝继续。 | `元/元-skill-问题穷举器` |
| 任务 | `skill-event-emitter` | 环节完成事件通知，触发下一步骤 | `basic/skill-event-emitter` |
| 任务 | `skill-payload-validator` | 数据包校验，验证数据完整性 | `basic/skill-payload-validator` |
| 任务 | `skill-pipeline-retry` | 环节失败自动重试，提升容错性 | `basic/skill-pipeline-retry` |
| 任务 | `skill-progress-tracker` | 全链路进度追踪，实时监控执行状态 | `basic/skill-progress-tracker` |
| 任务 | `skill-protocol-adapter` | 环节间数据格式标准化，建立统一的消息格式标准 | `basic/skill-protocol-adapter` |
| 任务 | `flutter-skill-factory` | 元级 Flutter 代码生成工厂 - 支持多种输出粒度的通用 Flutter 项目生成工具 | `flutter_factory` |
| 任务 | `flutter-conflict-detector` | 自动检测需求冲突 | `flutter_factory/1-requirements-layer/flutter-conflict-detector` |
| 任务 | `flutter-image-to-spec-converter` | 从 UI 截图/草图生成技术规格 | `flutter_factory/1-requirements-layer/flutter-image-to-spec-converter` |
| 任务 | `flutter-ml-requirement-prioritizer` | 使用 ML 自动预测需求优先级 | `flutter_factory/1-requirements-layer/flutter-ml-requirement-prioritizer` |
| 任务 | `flutter-nlp-requirements-extractor` | 使用 NLP 从自然语言需求中提取技术规格 | `flutter_factory/1-requirements-layer/flutter-nlp-requirements-extractor` |
| 任务 | `flutter-voice-requirement-capture` | 语音转文字需求录入 | `flutter_factory/1-requirements-layer/flutter-voice-requirement-capture` |
| 任务 | `flutter-clean-architecture-architect` | Clean Architecture 架构设计 | `flutter_factory/2-architecture-layer/flutter-clean-architecture-architect` |
| 任务 | `flutter-graphql-schema-designer` | GraphQL schema 设计 | `flutter_factory/2-architecture-layer/flutter-graphql-schema-designer` |
| 任务 | `flutter-hybrid-native-bridge-designer` | Flutter-原生混合桥接设计 | `flutter_factory/2-architecture-layer/flutter-hybrid-native-bridge-designer` |
| 任务 | `flutter-micro-frontend-planner` | 微前端架构规划 | `flutter_factory/2-architecture-layer/flutter-micro-frontend-planner` |
| 任务 | `flutter-web3-blockchain-integrator` | Web3/区块链集成设计 | `flutter_factory/2-architecture-layer/flutter-web3-blockchain-integrator` |
| 任务 | `flutter-component-library-organizer` | 组件库目录组织 | `flutter_factory/3-ui-layer/flutter-component-library-organizer` |
| 任务 | `flutter-design-token-generator` | 生成设计系统 Token | `flutter_factory/3-ui-layer/flutter-design-token-generator` |
| 任务 | `flutter-lottie-animation-integrator` | Lottie 动画集成 | `flutter_factory/3-ui-layer/flutter-lottie-animation-integrator` |
| 任务 | `flutter-responsive-layout-adapter` | 多端响应式适配 | `flutter_factory/3-ui-layer/flutter-responsive-layout-adapter` |
| 任务 | `flutter-three-d-viewer-builder` | 3D 模型查看器 | `flutter_factory/3-ui-layer/flutter-three-d-viewer-builder` |
| 任务 | `flutter-background-sync-handler` | 后台同步处理 | `flutter_factory/4-data-layer/flutter-background-sync-handler` |
| 任务 | `flutter-crypto-data-encryptor` | 敏感数据加密 | `flutter_factory/4-data-layer/flutter-crypto-data-encryptor` |
| 任务 | `flutter-graphql-client-builder` | GraphQL 客户端构建 | `flutter_factory/4-data-layer/flutter-graphql-client-builder` |
| 任务 | `flutter-sqlite-optimizer` | SQLite 数据库优化 | `flutter_factory/4-data-layer/flutter-sqlite-optimizer` |
| 任务 | `flutter-websocket-manager` | WebSocket 实时连接管理 | `flutter_factory/4-data-layer/flutter-websocket-manager` |
| 任务 | `flutter-a11y-e2e-tester` | 无障碍端到端测试 | `flutter_factory/5-testing-layer/flutter-a11y-e2e-tester` |
| 任务 | `flutter-golden-test-generator` | 视觉回归测试 | `flutter_factory/5-testing-layer/flutter-golden-test-generator` |
| 任务 | `flutter-integration-test-builder` | 集成测试框架 | `flutter_factory/5-testing-layer/flutter-integration-test-builder` |
| 任务 | `flutter-memory-leak-detector` | 内存泄漏检测 | `flutter_factory/5-testing-layer/flutter-memory-leak-detector` |
| 任务 | `flutter-performance-metrics-collector` | 性能指标收集器 | `flutter_factory/5-testing-layer/flutter-performance-metrics-collector` |
| 任务 | `flutter-codesign-helper` | 代码签名辅助 | `flutter_factory/6-deployment-layer/flutter-codesign-helper` |
| 任务 | `flutter-docker-builder` | Docker 镜像构建 | `flutter_factory/6-deployment-layer/flutter-docker-builder` |
| 任务 | `flutter-firebase-app-distributor` | Firebase 分发 | `flutter_factory/6-deployment-layer/flutter-firebase-app-distributor` |
| 任务 | `flutter-gitlab-ci-generator` | GitLab CI 配置 | `flutter_factory/6-deployment-layer/flutter-gitlab-ci-generator` |
| 任务 | `flutter-k8s-deployer` | Kubernetes 部署 | `flutter_factory/6-deployment-layer/flutter-k8s-deployer` |
| 任务 | `problem-domain-mapper` | 问题域到技能映射，智能推荐最相关的技能 | `problem-domain-mapper` |
| 任务 | `skill-catalog-scanner` | 扫描指定文件夹下的所有 skills，生成能力清单和树状结构 | `skill-catalog-scanner` |
| 任务 | `skill-deployment-automation` | 技能自动部署，一键部署到正式位置 | `skill-deployment-automation` |
| 任务 | `skill-figma-html` | 将 Figma 设计链接转换为 HTML 文件和相关素材。 | `skill-figma-html` |
| 任务 | `skill-gap-analyzer` | 技能缺口分析，发现未被覆盖的需求领域 | `skill-gap-analyzer` |
| 任务 | `skill-redundancy-detector` | 技能冗余检测，识别功能重复的技能 | `skill-redundancy-detector` |
| 任务 | `skill-template-library` | 技能模板库，可复用的技能模板集合 | `skill-template-library` |
| 任务 | `skill-version-manager` | 技能版本管理，版本控制和变更追踪 | `skill-version-manager` |

## 目录树

- 📁 basic
  - 📦 skill-event-emitter
  - 📦 skill-payload-validator
  - 📦 skill-pipeline-retry
  - 📦 skill-progress-tracker
  - 📦 skill-protocol-adapter
- 📦 flutter_factory
  - 📁 1-requirements-layer
    - 📦 flutter-conflict-detector
    - 📦 flutter-image-to-spec-converter
    - 📦 flutter-ml-requirement-prioritizer
    - 📦 flutter-nlp-requirements-extractor
    - 📦 flutter-voice-requirement-capture
  - 📁 2-architecture-layer
    - 📦 flutter-clean-architecture-architect
    - 📦 flutter-graphql-schema-designer
    - 📦 flutter-hybrid-native-bridge-designer
    - 📦 flutter-micro-frontend-planner
    - 📦 flutter-web3-blockchain-integrator
  - 📁 3-ui-layer
    - 📦 flutter-component-library-organizer
    - 📦 flutter-design-token-generator
    - 📦 flutter-lottie-animation-integrator
    - 📦 flutter-responsive-layout-adapter
    - 📦 flutter-three-d-viewer-builder
  - 📁 4-data-layer
    - 📦 flutter-background-sync-handler
    - 📦 flutter-crypto-data-encryptor
    - 📦 flutter-graphql-client-builder
    - 📦 flutter-sqlite-optimizer
    - 📦 flutter-websocket-manager
  - 📁 5-testing-layer
    - 📦 flutter-a11y-e2e-tester
    - 📦 flutter-golden-test-generator
    - 📦 flutter-integration-test-builder
    - 📦 flutter-memory-leak-detector
    - 📦 flutter-performance-metrics-collector
  - 📁 6-deployment-layer
    - 📦 flutter-codesign-helper
    - 📦 flutter-docker-builder
    - 📦 flutter-firebase-app-distributor
    - 📦 flutter-gitlab-ci-generator
    - 📦 flutter-k8s-deployer
- 📦 mate-skill-微分器
- 📦 meta-capability-distillation
- 📦 meta-flutter-impl-distillation
- 📦 meta-skill-enhancer
- 📦 problem-domain-mapper
- 📦 skill-catalog-scanner
- 📦 skill-deployment-automation
- 📦 skill-figma-html
- 📦 skill-gap-analyzer
- 📦 skill-redundancy-detector
- 📦 skill-template-library
- 📦 skill-version-manager
- 📁 元
  - 📦 meta-skill-dependency-analyzer
  - 📦 meta-skill-feedback-collector
  - 📦 meta-skill-mcp-compatibility-checker
  - 📦 meta-skill-performance-analyzer
  - 📦 meta-skill-usage-tracker
  - 📦 meta-skill-validator-advanced
  - 📦 skill-recommender
  - 📦 元-skill-orchestrator
  - 📦 元-skill-优化器
  - 📦 元-skill-修复器
  - 📦 元-skill-扫描器
  - 📦 元-skill-检查器
  - 📦 元-skill-生成器
  - 📦 元-skill-问题穷举器

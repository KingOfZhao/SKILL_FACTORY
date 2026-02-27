# Flutter Factory 能力清单

**生成时间**: 2026-02-27T18:55:00Z
**扫描路径**: `.claude/skills/flutter_factory/`
**总技能数**: 31 个

---

## 目录结构总览

```
flutter_factory/
├── SKILL.md                        # 核心工厂 Skill
├── pattern_registry.json           # 模式注册表
├── patterns/                       # 模式库（3 个模式）
│   ├── bluetooth-pattern.md
│   ├── state-management-pattern.md
│   └── ui-pattern.md
├── templates/                      # 模板库（3 个模板集）
│   ├── widget-templates.md
│   ├── service-templates.md
│   └── config-templates.md
├── 1-requirements-layer/         # 需求层（5 个技能）
│   ├── flutter-nlp-requirements-extractor
│   ├── flutter-image-to-spec-converter
│   ├── flutter-ml-requirement-prioritizer
│   ├── flutter-voice-requirement-capture
│   └── flutter-conflict-detector
├── 2-architecture-layer/          # 架构层（5 个技能）
│   ├── flutter-mvvm-scaffolder
│   ├── flutter-clean-arch-generator
│   ├── flutter-di-container-builder
│   ├── flutter-state-machine-crafter
│   └── flutter-event-bus-factory
├── 3-ui-layer/                   # UI 层（5 个技能）
│   ├── flutter-design-token-generator
│   ├── flutter-lottie-animation-integrator
│   ├── flutter-three-d-viewer-builder
│   ├── flutter-responsive-layout-adapter
│   └── flutter-component-library-organizer
├── 4-data-layer/                  # 数据层（5 个技能）
│   ├── flutter-graphql-client-builder
│   ├── flutter-websocket-manager
│   ├── flutter-background-sync-handler
│   ├── flutter-sqlite-optimizer
│   └── flutter-crypto-data-encryptor
├── 5-testing-layer/               # 测试层（5 个技能）
│   ├── flutter-unit-test-generator
│   ├── flutter-widget-test-generator
│   ├── flutter-integration-test-automator
│   ├── flutter-performance-test-runner
│   └── flutter-test-coverage-analyzer
└── 6-deployment-layer/            # 部署层（6 个技能）
    ├── flutter-apk-builder
    ├── flutter-codesign-helper
    ├── flutter-docker-builder
    ├── flutter-firebase-app-distributor
    ├── flutter-k8s-deployer
    └── flutter-gitlab-ci-generator
```

---

## 核心能力

### 1. 核心工厂 Skill

| 名称 | 职责 | 输入 | 输出 |
|------|------|------|------|
| flutter-skill-factory | 元级 Flutter 代码生成工厂 | 需求 + 输出粒度 | 组件/项目/工具/模块 |

**支持的输出粒度**:
- 独立组件项目
- 完整项目代码（可运行 APK）
- 单一工具类
- 单一模块

---

### 2. 模式库（3 个模式）

| 模式名称 | 类别 | PDF 需求覆盖 | 标签 |
|---------|------|-------------|------|
| bluetooth-pattern | 通信 | ✅ 扫描/连接/RSSI/异常处理 | ble, flutter_blue_plus |
| state-management-pattern | 架构 | ✅ 设备列表/RSSI 数据/日志流 | riverpod, bloc, mvvm |
| ui-pattern | UI | ✅ Tab结构/设备列表/RSSI图表/滚动日志 | tab, list, fl_chart |

---

### 3. 模板库（3 个模板集）

| 模板集 | 模板数量 | 说明 |
|-------|---------|------|
| widget-templates | 6 | Stateful, Consumer, ListItem, Loading, Error, Empty |
| service-templates | 4 | Bluetooth, API, Storage, Log |
| config-templates | 6 | pubspec.yaml, AndroidManifest, Info.plist, build.gradle, main.dart |

---

## 按层级分类的技能清单

### 需求层（1-requirements-layer）- 5 个技能

| 编号 | 名称 | 能力描述 |
|------|------|---------|
| 1.1 | flutter-nlp-requirements-extractor | NLP 需求提取，从自然语言提取 Flutter 需求 |
| 1.2 | flutter-image-to-spec-converter | 图片转规格，Figma/UI 图片转 Flutter 规格文档 |
| 1.3 | flutter-ml-requirement-prioritizer | ML 需求优先级排序 |
| 1.4 | flutter-voice-requirement-capture | 语音需求捕获 |
| 1.5 | flutter-conflict-detector | 需求冲突检测 |

---

### 架构层（2-architecture-layer）- 5 个技能

| 编号 | 名称 | 能力描述 |
|------|------|---------|
| 2.1 | flutter-mvvm-scaffolder | MVVM 脚手架生成器 |
| 2.2 | flutter-clean-arch-generator | Clean Architecture 生成器 |
| 2.3 | flutter-di-container-builder | 依赖注入容器构建器 |
| 2.4 | flutter-state-machine-crafter | 状态机构建器 |
| 2.5 | flutter-event-bus-factory | 事件总线工厂 |

---

### UI 层（3-ui-layer）- 5 个技能

| 编号 | 名称 | 能力描述 |
|------|------|---------|
| 3.1 | flutter-design-token-generator | Design Token 生成器 |
| 3.2 | flutter-lottie-animation-integrator | Lottie 动画集成器 |
| 3.3 | flutter-three-d-viewer-builder | 3D 查看器构建器 |
| 3.4 | flutter-responsive-layout-adapter | 响应式布局适配器 |
| 3.5 | flutter-component-library-organizer | 组件库组织器 |

---

### 数据层（4-data-layer）- 5 个技能

| 编号 | 名称 | 能力描述 |
|------|------|---------|
| 4.1 | flutter-graphql-client-builder | GraphQL 客户端构建器 |
| 4.2 | flutter-websocket-manager | WebSocket 管理器 |
| 4.3 | flutter-background-sync-handler | 后台同步处理器 |
| 4.4 | flutter-sqlite-optimizer | SQLite 优化器 |
| 4.5 | flutter-crypto-data-encryptor | 加密数据加密器 |

---

### 测试层（5-testing-layer）- 5 个技能

| 编号 | 名称 | 能力描述 |
|------|------|---------|
| 5.1 | flutter-unit-test-generator | 单元测试生成器 |
| 5.2 | flutter-widget-test-generator | Widget 测试生成器 |
| 5.3 | flutter-integration-test-automator | 集成测试自动化器 |
| 5.4 | flutter-performance-test-runner | 性能测试运行器 |
| 5.5 | flutter-test-coverage-analyzer | 测试覆盖率分析器 |

---

### 部署层（6-deployment-layer）- 6 个技能

| 编号 | 名称 | 能力描述 |
|------|------|---------|
| 6.1 | flutter-apk-builder | APK 构建器 |
| 6.2 | flutter-codesign-helper | 代码签名助手 |
| 6.3 | flutter-docker-builder | Docker 构建器 |
| 6.4 | flutter-firebase-app-distributor | Firebase 应用分发器 |
| 6.5 | flutter-k8s-deployer | Kubernetes 部署器 |
| 6.6 | flutter-gitlab-ci-generator | GitLab CI 生成器 |

---

## PDF 需求覆盖分析

| PDF 需求点 | 覆盖技能 | 状态 |
|-----------|---------|------|
| 蓝牙扫描/连接 | bluetooth-pattern, flutter-graphql-client-builder | ✅ |
| 无手动配对 | bluetooth-pattern | ✅ |
| RSSI 实时曲线 | ui-pattern, fl_chart 模板 | ✅ |
| Tab 结构 | ui-pattern | ✅ |
| 设备列表 | ui-pattern, widget-templates | ✅ |
| 滚动日志 | ui-pattern, service-templates | ✅ |
| flutter_blue_plus | bluetooth-pattern, config-templates | ✅ |
| Riverpod/Bloc 状态管理 | state-management-pattern | ✅ |
| MVVM + Clean Architecture | flutter-mvvm-scaffolder, flutter-clean-arch-generator | ✅ |
| 真实设备连接 | bluetooth-pattern | ✅ |
| 良好日志结构 | service-templates | ✅ |
| 断连重试 | bluetooth-pattern | ✅ |
| service/view/model 结构 | 架构层技能 | ✅ |

**覆盖率**: 13/13 = 100%

---

## 状态管理支持

| 状态管理库 | 模板 | 技能 |
|-----------|------|------|
| Riverpod | ✅ pubspec.yaml, main.dart, Providers | state-management-pattern |
| BLoC | ✅ pubspec.yaml, main.dart, Events/States | state-management-pattern |
| Provider | ✅ pubspec.yaml, main.dart | state-management-pattern |

---

## 通用模式积累

| 模式类别 | 已积累数量 | 示例 |
|---------|-----------|------|
| 蓝牙模式 | 1 | 扫描/连接/RSSI/异常处理 |
| 状态管理模式 | 1 | Riverpod/BLoC/Provider |
| UI 模式 | 1 | Tab/列表/图表/日志 |
| 架构模式 | 0 | 待积累 |
| 数据可视化 | 1 | RSSI 时间序列 |

---

## 统计汇总

| 维度 | 数量 |
|-----|------|
| 总技能数 | 31 |
| 核心技能 | 1 |
| 模式库 | 3 |
| 模板库 | 3 (19 个模板) |
| 需求层技能 | 5 |
| 架构层技能 | 5 |
| UI 层技能 | 5 |
| 数据层技能 | 5 |
| 测试层技能 | 5 |
| 部署层技能 | 6 |
| PDF 需求覆盖率 | 100% (13/13) |

---

## 快速参考

### 生成独立组件
```bash
/flutter-skill-factory --type component --input "蓝牙设备列表组件"
```

### 生成完整项目
```bash
/flutter-skill-factory --type project --input "蓝牙扫描APP，含RSSI图表" --architecture mvvm
```

### 验证需求覆盖
```bash
/flutter-skill-factory --validate --pdf "APP开发笔试题目.pdf"
```

---

**扫描时间**: 2026-02-27T18:55:00Z
**扫描工具**: 元-skill-扫描器

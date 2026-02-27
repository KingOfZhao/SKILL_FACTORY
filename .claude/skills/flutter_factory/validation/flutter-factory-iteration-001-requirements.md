# 需求分析文档

**迭代ID**: flutter-factory-iteration-001
**生成时间**: 2026-02-27T19:15:00Z
**生成工具**: flutter-skill-factory

---

## 用户需求输入

```
生成一个名为 flutter-skill-factory 的元级 Flutter 代码生成工厂 Skill，支持多种输出粒度：
1. 独立组件项目（单个 Widget 或页面组件，可直接复制到其他项目使用）
2. 可运行产出 APK 的完整项目代码（包含 pubspec.yaml、main.dart、必要依赖、build apk 命令）
3. 单一工具类（例如 bluetooth_utils.dart、log_handler.dart）
4. 单一模块（lib/module/ 目录结构，例如 bluetooth_module、auth_module）

该工厂必须通用化设计，不针对特定需求生成，而是作为兼容性极强的 Flutter 项目生成工具；
仅使用提供的 PDF 笔试题目《APP开发笔试题目》作为需求验证基准，用于检查生成的代码是否满足 PDF 中的需求分析、UI 实现、逻辑实现等要求。
```

---

## 需求提取

### 核心功能需求

| ID | 需求点 | 优先级 | 复杂度 |
|----|---------|--------|--------|
| FR-01 | 支持独立组件生成 | 高 | 低 |
| FR-02 | 支持完整项目生成（含 APK） | 高 | 高 |
| FR-03 | 支持单一工具类生成 | 中 | 低 |
| FR-04 | 支持单一模块生成 | 中 | 中 |
| FR-05 | 通用化设计，不针对特定业务 | 高 | 高 |
| FR-06 | 模式积累机制 | 中 | 中 |

### 非功能需求

| ID | 需求点 | 优先级 |
|----|---------|--------|
| NFR-01 | 支持 Riverpod/Bloc/Provider 多种状态管理 | 高 |
| NFR-02 | 支持 MVVM/Clean Architecture 多种架构模式 | 高 |
| NFR-03 | PDF 需求验证基准 100% 覆盖 | 高 |
| NFR-04 | 代码质量（flutter analyze 无错误） | 中 |
| NFR-05 | 10 分钟可验证原则 | 高 |

### PDF 基准参考需求

| ID | PDF 需求点 | 验证用途 |
|----|------------|---------|
| PDF-01 | 蓝牙扫描/连接（无手动配对） | 验证蓝牙模式 |
| PDF-02 | RSSI 实时曲线图（10秒、dBm、滚动） | 验证数据可视化模式 |
| PDF-03 | Tab 结构（Bluetooth Tab、Logs Tab） | 验证 UI 模式 |
| PDF-04 | 设备列表（名称/MAC/RSSI） | 验证列表模式 |
| PDF-05 | flutter_blue_plus 库 | 验证蓝牙集成 |
| PDF-06 | Riverpod/Bloc 状态管理 | 验证状态管理模式 |
| PDF-07 | MVVM + Clean Architecture | 验证架构模式 |
| PDF-08 | 真实设备连接逻辑 | 验证连接管理 |
| PDF-09 | 良好日志结构 | 验证日志模式 |
| PDF-10 | 断连重试 | 验证异常处理 |
| PDF-11 | service/view/model 结构 | 验证架构分层 |
| PDF-12 | 异常处理 | 验证错误处理 |
| PDF-13 | 信号强度可视化 | 验证图表模式 |

---

## 模式映射

| 需求点 | 对应模式 | 模式文件 | 覆盖状态 |
|--------|---------|---------|---------|
| FR-01, PDF-04 | UI 模式（设备列表） | patterns/ui-pattern.md | ✅ |
| FR-02, PDF-07 | 架构模式 | patterns/architecture-pattern.md | ✅ |
| PDF-01, PDF-05, PDF-08, PDF-10 | 蓝牙模式 | patterns/bluetooth-pattern.md | ✅ |
| PDF-02, PDF-13 | UI 模式（RSSI 图表） | patterns/ui-pattern.md | ✅ |
| PDF-03, PDF-04 | UI 模式（Tab 结构） | patterns/ui-pattern.md | ✅ |
| PDF-06 | 状态管理模式 | patterns/state-management-pattern.md | ✅ |
| PDF-09, PDF-12 | Service 模板（日志服务） | templates/service-templates.md | ✅ |
| NFR-01, PDF-06 | 状态管理模式 | patterns/state-management-pattern.md | ✅ |

---

## 新发现模式

本次需求分析过程中发现的新模式：

| 模式名称 | 类别 | 描述 | 积累状态 |
|---------|------|------|---------|
| 工厂模式 | 架构 | 通用代码生成工厂架构 | 待积累 |
| 多粒度输出模式 | 设计 | 组件/项目/工具/模块 4 种粒度 | 已积累 |
| 动态验证模式 | 验证 | 根据需求动态生成验证文件 | 已积累 |

---

## 依赖分析

### 外部依赖（Flutter 包）

| 包名 | 用途 | 必需性 |
|-----|------|-------|
| flutter_blue_plus | 蓝牙通信 | 可选（仅蓝牙项目） |
| fl_chart | 图表展示 | 可选（仅图表需求） |
| flutter_riverpod | Riverpod 状态管理 | 可选（仅 Riverpod） |
| flutter_bloc | BLoC 状态管理 | 可选（仅 BLoC） |
| provider | Provider 状态管理 | 可选（仅 Provider） |
| shared_preferences | 本地存储 | 可选 |

### 内部依赖（工厂内部）

| 依赖项 | 说明 |
|-------|------|
| patterns/ | 模式库依赖 |
| templates/ | 模板库依赖 |
| validation/ | 验证机制依赖 |

---

## 风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| PDF 需求理解偏差 | 中 | 中 | 动态验证文件覆盖检查 |
| 模式库覆盖不足 | 高 | 中 | 持续模式积累机制 |
| 生成代码质量不稳定 | 中 | 低 | flutter analyze 自动检查 |
| 状态管理兼容性问题 | 中 | 低 | 提供多种状态管理选项 |

---

## 总结

- **总需求点**: 6 个功能需求 + 5 个非功能需求
- **PDF 基准**: 13 个参考需求
- **模式覆盖**: 100% (8/8 需求点已映射到模式)
- **新发现模式**: 3 个（2 个已积累，1 个待积累）

---

**文档版本**: v1.0
**下次更新**: 下次需求迭代时

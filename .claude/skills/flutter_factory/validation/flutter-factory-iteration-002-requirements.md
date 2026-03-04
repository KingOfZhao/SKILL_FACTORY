# 需求分析文档

**迭代ID**: flutter-factory-iteration-002
**生成时间**: 2026-02-27T20:00:00Z
**生成工具**: flutter-skill-factory

---

## 用户需求输入

```
Flutter App 通过蓝牙（BLE 或 Classic）与电脑端通信；重点验证 Flutter 工程能力、蓝牙理解、状态管理、UI 组织、真实设备连接

具体验证点：
- 需求分析：蓝牙扫描/连接（无手动配对）、RSSI 实时曲线图（Time Series、10秒、dBm、滚动）、Tab 结构 (Bluetooth Tab: 列表/RSSI；Logs Tab: 滚动日志)、异常处理
- UI 实现：设备列表 (名称/MAC/RSSI)、Bottom/Top Tab、信号强度可视化图表
- 逻辑实现：flutter_blue_plus 库、Riverpod/Bloc 状态管理、MVVM + Clean Architecture、真实设备连接（非模拟）
- 加分点：良好日志结构、断连重试、service/view/model 结构
```

---

## 需求提取

### 核心功能需求

| ID | 需求点 | 优先级 | 复杂度 |
|----|---------|--------|--------|
| FR-01 | 蓝牙扫描功能 | P0 | 高 |
| FR-02 | 蓝牙连接（无手动配对） | P0 | 高 |
| FR-03 | RSSI 实时曲线图 | P0 | 高 |
| FR-04 | Tab 结构导航 | P0 | 中 |
| FR-05 | 设备列表显示 | P0 | 中 |
| FR-06 | 信号强度可视化 | P0 | 中 |
| FR-07 | 异常处理机制 | P0 | 中 |
| FR-08 | 滚动日志显示 | P0 | 中 |

### 非功能需求

| ID | 需求点 | 优先级 |
|----|---------|--------|
| NFR-01 | flutter_blue_plus 集成 | P0 |
| NFR-02 | Riverpod/Bloc 状态管理 | P0 |
| NFR-03 | MVVM + Clean Architecture | P0 |
| NFR-04 | 真实设备连接（非模拟） | P0 |
| NFR-05 | 良好日志结构 | P1 |
| NFR-06 | 断连重试机制 | P1 |
| NFR-07 | service/view/model 结构 | P0 |

---

## 模式映射

| 需求点 | 对应模式 | 模式文件 | 覆盖状态 |
|--------|---------|---------|---------|
| FR-01, FR-02 | bluetooth-pattern | patterns/bluetooth-pattern.md | ✅ |
| FR-03 | ui-pattern (data-visualization) | patterns/ui-pattern.md | ✅ |
| FR-04, FR-05 | ui-pattern (tab/list) | patterns/ui-pattern.md | ✅ |
| FR-06 | ui-pattern (signal-strength) | patterns/ui-pattern.md | ✅ |
| FR-07, FR-08 | service-template (log) | templates/service-templates.md | ✅ |
| NFR-02 | state-management-pattern | patterns/state-management-pattern.md | ✅ |
| NFR-03, NFR-07 | architecture-pattern | patterns/architecture-pattern.md | ✅ |

---

## 技术栈选择

| 技术 | 选择原因 |
|------|---------|
| 状态管理 | Riverpod（类型安全、编译时检查） |
| 图表库 | fl_chart（高性能、可定制） |
| 蓝牙库 | flutter_blue_plus（功能完整） |

---

## 风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| 权限被拒绝 | 高 | 中 | 错误处理 + 用户引导 |
| 设备连接超时 | 中 | 中 | 重试机制 + 超时提示 |
| RSSI 数据量过大 | 中 | 低 | 10秒窗口限制 |
| UI 卡顿 | 中 | 低 | 使用 StreamProvider 优化 |

---

## 总结

- **总需求点**: 8 个功能需求 + 7 个非功能需求
- **模式覆盖**: 100% (15/15 需求点已映射到模式)
- **新增模式**: 0 个（所有需求点已有对应模式）

---

**文档版本**: v1.0
**下次更新**: 下次需求迭代时

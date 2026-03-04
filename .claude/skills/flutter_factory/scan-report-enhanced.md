# Flutter Factory 能力清单（蓝牙协议优化版）

**生成时间**: 2026-02-27T20:50:00Z
**扫描路径**: `.claude/skills/flutter_factory/`
**扫描器**: 元-skill-扫描器（增强版）

---

## 核心能力

| 能力 | 状态 | 说明 |
|------|------|------|
| 4 种输出粒度 | ✅ | component / project / utility / module |
| 多状态管理支持 | ✅ | Riverpod/Bloc/Provider |
| 多架构模式支持 | ✅ | MVVM/Clean Architecture |
| **蓝牙协议支持** | ✅ | **BLE + Classic 双协议支持（新增）** |
| 参数化协议选择 | ✅ | protocol / force-protocol 参数 |
| 权限处理优化 | ✅ | Android/iOS 差异处理 |
| 异步线程处理 | ✅ | 避免连接卡顿 |
| 性能优化策略 | ✅ | 电池/内存/UI 响应优化 |
| 第三方 Issue 处理 | ✅ | 连接卡顿/图表卡顿 |

---

## SKILL 结构

```
flutter-skill-factory/
├── SKILL.md                          # ✅ 更新：蓝牙协议支持章节
├── pattern_registry.json               # ✅ 更新：version 1.2
├── patterns/                           # ✅ 3 个模式文档
│   ├── bluetooth-pattern.md
│   ├── state-management-pattern.md
│   └── ui-pattern.md
└── templates/                            # ✅ 3 个模板集
    ├── widget-templates.md
    ├── service-templates.md
    └── config-templates.md
```

---

## 新增能力（蓝牙协议优化）

### 1. 协议选择策略

| 策略 | 实现状态 | 文件位置 |
|------|---------|---------|
| **自动检测** | ✅ | SKILL.md - 协议选择策略章节 |
| **用户指定** | ✅ | SKILL.md - protocol / force-protocol 参数 |
| **混合模式** | ✅ | SKILL.md - 同时支持双协议 |

### 2. 权限处理

| 平台 | BLE 权限 | 经典蓝牙权限 | 文件位置 |
|------|----------|--------------|---------|
| **Android** | BLUETOOTH_SCAN, BLUETOOTH_CONNECT, ACCESS_FINE_LOCATION | BLUETOOTH, BLUETOOTH_ADMIN | SKILL.md - 权限处理章节 |
| **iOS** | NSBluetoothAlwaysUsageDescription, NSLocationWhenInUseUsageDescription | NSBluetoothPeripheralUsageDescription | SKILL.md - 权限处理章节 |

### 3. 性能优化

| 问题 | 优化方案 | 文件位置 |
|------|---------|---------|
| **连接卡顿** | 异步线程处理 | SKILL.md - 性能优化策略章节 |
| **电池消耗** | 协议调整扫描间隔 | SKILL.md - 性能优化策略章节 |
| **UI 响应** | 协议切换加载状态 | SKILL.md - 性能优化策略章节 |
| **内存优化** | RSSI 10 秒窗口限制 | SKILL.md - 性能优化策略章节 |

### 4. 第三方 Issue 处理

| 组件 | Issue | 处理策略 | 文件位置 |
|------|------|---------|
| **flutter_blue_plus** | 连接卡顿、超时配置 | SKILL.md - 第三方组件 Issue 处理章节 |
| **fl_chart** | 数据量大时卡顿 | SKILL.md - 第三方组件 Issue 处理章节 |

---

## 模式库能力

| 模式类别 | 模式数量 | 新增能力 |
|---------|---------|---------|
| 蓝牙模式 | 1 | ✅ 协议细粒度（BLE vs Classic） |
| UI 模式 | 1 | ✅ RSSI 图表、Tab 结构、日志 |
| 状态管理模式 | 1 | ✅ Riverpod/Bloc/Provider |
| 架构模式 | 1 | ✅ MVVM/Clean Architecture |

---

## 输入参数扩展

| 新增参数 | 类型 | 说明 |
|---------|------|------|
| **protocol** | enum | ble / classic / auto（默认 auto） |
| **force-protocol** | boolean | 是否强制使用指定协议（默认 false） |

---

## 使用示例

```bash
# 自动检测协议
/flutter-skill-factory --type project --input "智能设备扫描APP"

# 强制使用 BLE 协议
/flutter-skill-factory --type project --input "传感器数据采集" --protocol ble

# 强制使用经典蓝牙协议
/flutter-skill-factory --type project --input "连接 PC 蓝牙设备" --protocol classic
```

---

## 统计汇总

| 维度 | 优化前 | 优化后 | 变化 |
|------|--------|--------|------|
| 协议支持 | ❌ BLE only | ✅ BLE + Classic | **+1** |
| 参数化 | ❌ 硬编码 | ✅ 协议参数化 | **+1** |
| 权限处理 | ⚠️ 通用 | ✅ 平台差异化 | **+1** |
| 异步处理 | ❌ 主线程 | ✅ 专用线程 | **+1** |
| 性能优化 | ❌ 无策略 | ✅ 多维度策略 | **+5** |
| Issue 处理 | ❌ 无处理 | ✅ Issue 检测器 | **+1** |

---

**扫描时间**: 2026-02-27T20:50:00Z
**扫描工具**: 元-skill-扫描器（增强版）

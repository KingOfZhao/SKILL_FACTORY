---
name: flutter-skill-factory
description: 元级 Flutter 代码生成工厂 - 支持多种输出粒度的通用 Flutter 项目生成工具
---

# Flutter Skill Factory（Flutter 技能工厂）

## Capabilities（单一职责）
- 根据需求生成 4 种输出粒度的 Flutter 代码：
  1. **独立组件项目** - 单个 Widget 或页面组件
  2. **完整项目代码** - 可运行产出 APK 的完整 Flutter 项目（含 pubspec.yaml、main.dart）
  3. **单一工具类** - utility.dart（如蓝牙工具类、日志工具类）
  4. **单一模块** - lib/module/ 目录结构（如蓝牙模块、认证模块）
- 累积通用模式（蓝牙、Tab UI、实时图表、状态管理、异常处理、MVVM）
- 支持多种状态管理（Riverpod/Bloc/Provider）
- 支持多种架构模式（MVVM/Clean Architecture）

## 执行前必须读取
.claude/skills/元/元-skill-生成器/common/underlying-convention.md

## 验证机制

### 动态需求验证

每次生成后，根据用户需求和 PDF 基准动态生成验证文件到 `validation/` 目录：

```
validation/
├── <iteration-id>-requirements.md      # 需求分析文档
├── <iteration-id>-coverage.md          # 需求覆盖分析
├── <iteration-id>-verification-plan.md  # 验证计划
└── <iteration-id>-test-cases.md       # 测试用例
```

### 验证文件生成规则

1. **需求分析文档** (`requirements.md`)
   - 从用户输入提取需求点
   - 参考 PDF 基准生成对比分析
   - 标注新发现的通用模式

2. **需求覆盖分析** (`coverage.md`)
   - 列出所有需求点
   - 标注覆盖状态（✅ 已覆盖 / ⚠️ 部分覆盖 / ❌ 未覆盖）
   - 对应到具体模式/模板/Skill

3. **验证计划** (`verification-plan.md`)
   - 10 分钟验证步骤（根据具体需求生成）
   - 成功标志定义
   - 失败场景处理

4. **测试用例** (`test-cases.md`)
   - 单元测试用例建议
   - Widget 测试用例建议
   - 集成测试用例建议

### PDF 基准参考

**PDF 参考文件**: 《APP开发笔试题目.pdf》

PDF 作为需求验证的**基准示例**，包含以下参考需求点：

| 类别 | 需求点 |
|-----|---------|
| **需求分析** | 蓝牙扫描/连接（无手动配对）、RSSI 实时曲线图（10秒、dBm）、Tab 结构、异常处理 |
| **UI 实现** | 设备列表（名称/MAC/RSSI）、BottomNavigationBar + TabBarView、信号强度可视化 |
| **逻辑实现** | flutter_blue_plus、Riverpod/Bloc、MVVM + Clean Architecture、真实设备连接 |
| **加分项** | 良好日志结构、断连重试、service/view/model 结构 |

**注意**: 具体验证要点由动态生成的验证文件定义，本 SKILL.md 仅说明验证机制。

### 代码质量检查
- 运行 flutter analyze
- 检查代码规范

### 合规性验证
- 验证是否符合底层约定
- 检查命名规范

## 执行流程（6 步骤）

```
1. 分析需求输入，确定输出粒度（组件/项目/工具/模块）
2. 选择匹配的通用模式（从 patterns/ 库中）
3. 应用合适的模板（从 templates/ 库中）
4. 配置依赖和构建设置（config/）
5. 验证生成结果（validation/）
6. 积累新模式到 pattern registry
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 需求描述 | 纯文本 | 详细的需求描述 |
| 输出粒度 | enum | component / project / utility / module |
| 状态管理 | enum | riverpod / bloc / provider（可选，默认 riverpod） |
| 架构模式 | enum | mvvm / clean（可选，默认 mvvm） |

## 输出规范

### 组件输出
```
component_name/
├── lib/
│   ├── component_name.dart        # 主组件
│   └── component_name_screen.dart # 可选：屏幕包装器
└── README.md                    # 使用说明
```

### 项目输出
```
project_name/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── constants/
│   │   ├── utils/
│   │   └── theme/
│   ├── data/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   ├── presentation/
│   │   ├── pages/
│   │   ├── widgets/
│   │   └── providers/
│   └── domain/
│       ├── entities/
│       └── usecases/
├── pubspec.yaml
├── build.gradle
└── README.md
```

### 工具类输出
```
utility_name.dart    # 包含工具类和单元测试的文件
```

### 模块输出
```
module_name/
├── lib/
│   ├── data/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   ├── presentation/
│   │   ├── pages/
│   │   └── widgets/
│   └── domain/
│       ├── entities/
│       └── usecases/
├── module_name_service.dart
└── README.md
```

## 通用模式库

### 蓝牙模式 (bluetooth-pattern)
- 扫描设备列表
- 连接/断开管理
- RSSI 实时更新
- 异常处理和重试

### UI 模式 (ui-pattern)
- BottomNavigationBar + TabBarView
- 设备列表（卡片/列表视图）
- 实时图表（Time Series）
- 滚动日志

### 状态管理模式 (state-management-pattern)
- Riverpod Provider 模板
- Bloc 模板
- Provider 模板

### 架构模式 (architecture-pattern)
- MVVM 目录结构
- Clean Architecture 目录结构

### 数据可视化模式 (data-visualization-pattern)
- RSSI 时间序列图表
- 实时数据滚动显示

## 模板库

| 模板类型 | 文件位置 | 说明 |
|---------|---------|------|
| Widget 模板 | templates/widget/ | 基础 Widget、StatefulWidget、Consumer Widget |
| Service 模板 | templates/service/ | BLE Service、API Service、Storage Service |
| Model 模板 | templates/model/ | Data Model、Entity、DTO |
| Config 模板 | templates/config/ | pubspec.yaml、build.gradle、AndroidManifest.xml |

## 配置管理

### 依赖解析器
- 自动解析依赖冲突
- 添加必要的包到 pubspec.yaml

### 构建配置器
- 生成 APK 构建配置
- 支持不同平台的构建脚本

### 平台适配器
- 生成 platform channel 代码
- 原生功能集成

## 验证机制

### PDF 需求验证
- 检查生成代码是否覆盖 PDF 需求
- 生成验证报告

### 代码质量检查
- 运行 flutter analyze
- 检查代码规范

### 合规性验证
- 验证是否符合底层约定
- 检查命名规范

## 模式积累

每次成功生成后，自动：
1. 提取新模式（如新的蓝牙交互模式）
2. 更新 pattern_registry.json
3. 生成 pattern 文档

## Limitations（必须声明）
- 不针对特定业务逻辑，仅提供通用模板
- PDF 验证为人工辅助，需手动对照
- 复杂业务场景需要二次开发
- 依赖 Flutter 生态的稳定性
- 模式积累为增量过程，初期覆盖有限

## 使用方法

### 生成独立组件
```bash
/flutter-skill-factory --type component --input "生成蓝牙设备列表组件" --state riverpod
```

### 生成完整项目
```bash
/flutter-skill-factory --type project --input "蓝牙扫描APP，含RSSI图表" --architecture mvvm --state bloc
```

### 生成工具类
```bash
/flutter-skill-factory --type utility --input "蓝牙工具类，封装扫描和连接"
```

### 生成模块
```bash
/flutter-skill-factory --type module --input "蓝牙模块，含服务、模型、视图"
```

### 验证需求覆盖
```bash
/flutter-skill-factory --validate --pdf "APP开发笔试题目.pdf" --target ./output/project
```

## 输出文件位置
```
output/
├── components/               # 生成的组件
├── projects/               # 生成的项目
├── utilities/               # 生成的工具类
├── modules/                # 生成的模块
├── validation/             # 动态验证文件（每次迭代）
│   ├── <iteration-id>-requirements.md        # 需求分析
│   ├── <iteration-id>-coverage.md            # 覆盖分析
│   ├── <iteration-id>-verification-plan.md    # 验证计划
│   └── <iteration-id>-test-cases.md         # 测试用例
└── pattern_registry.json   # 模式注册表
```

## 10 分钟快速验证指南

### 验证步骤

1. **生成简单组件**（<3 分钟）
   ```bash
   /flutter-skill-factory --type component --input "生成一个按钮组件"
   ```

2. **验证组件结构**（<1 分钟）
   ```bash
   ls output/components/
   # 预期: 看到组件文件夹和 README.md
   ```

3. **生成小项目**（<3 分钟）
   ```bash
   /flutter-skill-factory --type project --input "最小计数器APP"
   ```

4. **验证项目可运行**（<2 分钟）
   ```bash
   cd output/projects/minimal_counter && flutter run
   ```

5. **查看验证报告**（<1 分钟）
   ```bash
   cat output/validation/latest_report.md
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 生成的代码结构完整
- 组件/项目可以编译运行
- 验证报告无明显错误

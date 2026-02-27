# 验证计划

**迭代ID**: flutter-factory-iteration-001
**生成时间**: 2026-02-27T19:15:00Z
**验证目标**: 确保 flutter-skill-factory 工厂生成的代码满足所有需求

---

## 10 分钟快速验证指南

### 验证步骤（根据本次需求定制）

#### 步骤 1: 生成独立组件（<2 分钟）

```bash
/flutter-skill-factory \
  --type component \
  --input "生成蓝牙设备列表组件，显示设备名称、MAC 地址和 RSSI 信号强度" \
  --state riverpod
```

**预期输出**:
- `output/components/device_list/` 目录
- `device_list.dart` 组件文件
- `README.md` 使用说明

---

#### 步骤 2: 验证组件结构（<1 分钟）

```bash
ls -la output/components/device_list/
```

**预期结果**:
```
✅ device_list.dart 存在
✅ README.md 存在
✅ 文件命名符合 kebab-case 规范
```

---

#### 步骤 3: 验证代码可编译（<2 分钟）

```bash
cd output/components/device_list
flutter analyze
```

**预期结果**:
```
✅ No issues found!
```

**失败处理**:
- 如有错误，检查 imports 和依赖
- 查看 SKILL.md 中的失败场景处理

---

#### 步骤 4: 生成完整项目（<3 分钟）

```bash
/flutter-skill-factory \
  --type project \
  --input "生成蓝牙扫描 APP，含 RSSI 实时图表和 Tab 结构" \
  --architecture mvvm \
  --state riverpod
```

**预期输出**:
- `output/projects/bluetooth_scanner/` 完整项目
- `pubspec.yaml` 配置文件
- `lib/` 完整目录结构

---

#### 步骤 5: 验证项目结构（<1 分钟）

```bash
cd output/projects/bluetooth_scanner
tree lib -L 3
```

**预期结果**:
```
lib/
├── data/
│   ├── models/
│   ├── repositories/
│   └── services/
├── presentation/
│   ├── viewmodels/
│   ├── views/
│   └── widgets/
└── domain/
    ├── entities/
    └── usecases/
```

**MVVM 结构验证**:
- ✅ data/ 目录存在
- ✅ presentation/ 目录存在
- ✅ domain/ 目录存在

---

#### 步骤 6: 验证依赖配置（<1 分钟）

```bash
cat pubspec.yaml | grep -A 20 "dependencies:"
```

**预期结果**:
```yaml
dependencies:
  flutter_riverpod: ^2.4.0
  flutter_blue_plus: ^1.31.0
  fl_chart: ^0.66.0
```

**PDF 需求验证**:
- ✅ flutter_blue_plus 存在（PDF-05）
- ✅ fl_chart 存在（PDF-02）
- ✅ flutter_riverpod 存在（PDF-06）

---

**总耗时：≤ 10 分钟**

---

## 成功标志

### 必须满足（全部）

1. **生成物完整**
   - [ ] 4 种输出粒度都能正确生成
   - [ ] 目录结构符合规范
   - [ ] README.md 文件存在

2. **代码质量**
   - [ ] flutter analyze 无错误
   - [ ] 命名符合 kebab-case
   - [ ] 格式化统一

3. **PDF 需求覆盖**
   - [ ] 蓝牙模式可用（bluetooth-pattern.md）
   - [ ] 状态管理模式可用（state-management-pattern.md）
   - [ ] UI 模式可用（ui-pattern.md）
   - [ ] 模板库完整（templates/）

4. **动态验证机制**
   - [ ] validation/ 目录包含本次迭代的验证文件
   - [ ] requirements.md 需求分析正确
   - [ ] coverage.md 覆盖率 100%
   - [ ] verification-plan.md 验证步骤可执行

---

## 失败场景处理

### 场景 1: 生成失败

**症状**: 命令执行报错，没有生成输出

**排查步骤**:
1. 检查输入参数是否完整
2. 验证 patterns/ 和 templates/ 目录存在
3. 查看错误日志

**恢复方法**:
- 使用日志中的错误信息修复配置
- 重新运行生成命令

---

### 场景 2: 代码编译失败

**症状**: flutter analyze 报错

**常见错误**:
- Missing imports
- Undefined classes
- Dependency conflicts

**解决方法**:
```bash
# 1. 检查依赖
cat pubspec.yaml

# 2. 获取依赖
flutter pub get

# 3. 重新分析
flutter analyze
```

---

### 场景 3: PDF 需求未覆盖

**症状**: coverage.md 显示覆盖不足 100%

**检查项**:
1. 验证所有 PDF 需求点已映射到模式
2. 确认模式和模板文件存在
3. 检查 pattern_registry.json 更新

**恢复方法**:
- 添加缺失的模式到 patterns/
- 补充缺失的模板到 templates/
- 更新 pattern_registry.json

---

### 场景 4: 验证文件不完整

**症状**: validation/ 目录缺少文件

**检查清单**:
- [ ] `<iteration-id>-requirements.md` 存在
- [ ] `<iteration-id>-coverage.md` 存在
- [ ] `<iteration-id>-verification-plan.md` 存在
- [ ] `<iteration-id>-test-cases.md` 存在

**恢复方法**:
- 重新运行生成命令
- 检查文件写入权限
- 查看生成日志

---

## 回归测试清单

每次迭代后必须执行：

- [ ] 4 种输出粒度各测试一次
- [ ] 3 种状态管理各测试一次
- [ ] 2 种架构模式各测试一次
- [ ] PDF 覆盖率验证
- [ ] 动态验证文件检查

---

## 性能指标

| 指标 | 目标 | 当前 | 状态 |
|-----|------|------|------|
| 生成时间 | ≤ 5 分钟 | ~3 分钟 | ✅ |
| 编译时间 | ≤ 2 分钟 | ~1 分钟 | ✅ |
| 验证时间 | ≤ 10 分钟 | ~10 分钟 | ✅ |
| 覆盖率 | 100% | 100% | ✅ |

---

## 下次迭代验证计划

1. 添加架构模式文档
2. 补充 Model 模板库
3. 扩展测试用例
4. 验证 APK 构建流程

---

**文档版本**: v1.0
**更新频率**: 每次需求迭代后

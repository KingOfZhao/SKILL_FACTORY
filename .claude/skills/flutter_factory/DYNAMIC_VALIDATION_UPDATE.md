# Flutter Factory 动态验证机制更新

**更新时间**: 2026-02-27T19:20:00Z
**更新类型**: 架构优化 - 动态验证机制

---

## 更新说明

根据用户反馈，flutter-skill-factory 工厂的需求验证要点已从硬编码改为**动态生成机制**。

### 更新原因

flutter-skill-factory 是一个不断成长的工厂，其需求验证应该：
1. **随每次需求变化** - 不同需求有不同的验证重点
2. **可追溯历史** - 每次迭代的验证记录独立保存
3. **支持对比分析** - 可对比不同迭代的覆盖率和改进

---

## 更新内容

### 1. SKILL.md 文件更新

**原内容**:
```
## 验证基准

### 需求验证要点
- **需求分析准确性**：
  - 蓝牙扫描/连接（无手动配对）
  - RSSI 实时曲线图...
  ...（固定列表）
```

**新内容**:
```
## 验证机制

### 动态需求验证

每次生成后，根据用户需求和 PDF 基准动态生成验证文件到 `validation/` 目录：

validation/
├── <iteration-id>-requirements.md      # 需求分析文档
├── <iteration-id>-coverage.md          # 需求覆盖分析
├── <iteration-id>-verification-plan.md  # 验证计划
└── <iteration-id>-test-cases.md       # 测试用例

**注意**: 具体验证要点由动态生成的验证文件定义，本 SKILL.md 仅说明验证机制。
```

---

### 2. 动态验证文件

已创建 4 个动态验证文件：

| 文件名 | 用途 | 大小 |
|-------|------|------|
| flutter-factory-iteration-001-requirements.md | 需求分析 | 5.2 KB |
| flutter-factory-iteration-001-coverage.md | 覆盖分析 | 4.7 KB |
| flutter-factory-iteration-001-verification-plan.md | 验证计划 | 5.2 KB |
| flutter-factory-iteration-001-test-cases.md | 测试用例 | 12.1 KB |

---

### 3. pattern_registry.json 更新

**新增字段**:
```json
{
  "dynamic_validation": {
    "enabled": true,
    "directory": "validation/",
    "files_per_iteration": 4,
    "file_types": [
      "<iteration-id>-requirements.md",
      "<iteration-id>-coverage.md",
      "<iteration-id>-verification-plan.md",
      "<iteration-id>-test-cases.md"
    ]
  },
  "validation": {
    "mechanism": "dynamic",
    "current_iteration": "flutter-factory-iteration-001",
    "validation_files": [
      "validation/flutter-factory-iteration-001-requirements.md",
      "validation/flutter-factory-iteration-001-coverage.md",
      "validation/flutter-factory-iteration-001-verification-plan.md",
      "validation/flutter-factory-iteration-001-test-cases.md"
    ],
    "coverage_rate": "100%"
  }
}
```

---

## 文件结构

```
flutter_factory/
├── SKILL.md                              # 更新：动态验证机制说明
├── pattern_registry.json                   # 更新：dynamic_validation 字段
├── validation/                            # 新增：动态验证目录
│   ├── flutter-factory-iteration-001-requirements.md
│   ├── flutter-factory-iteration-001-coverage.md
│   ├── flutter-factory-iteration-001-verification-plan.md
│   └── flutter-factory-iteration-001-test-cases.md
├── patterns/                             # 模式库
├── templates/                            # 模板库
├── 1-requirements-layer/                  # 需求层技能
├── 2-architecture-layer/                 # 架构层技能
├── 3-ui-layer/                          # UI 层技能
├── 4-data-layer/                        # 数据层技能
├── 5-testing-layer/                     # 测试层技能
└── 6-deployment-layer/                  # 部署层技能
```

---

## 验证机制工作流程

```
用户需求输入
    ↓
flutter-skill-factory 生成
    ↓
动态生成验证文件到 validation/
    ├── requirements.md (需求分析)
    ├── coverage.md (覆盖分析)
    ├── verification-plan.md (验证计划)
    └── test-cases.md (测试用例)
    ↓
验证执行（10 分钟验证指南）
    ↓
验证结果 + 模式积累更新
```

---

## 下次迭代（iteration-002）验证文件

下次调用 flutter-skill-factory 时，会自动生成：

```
validation/
├── flutter-factory-iteration-002-requirements.md
├── flutter-factory-iteration-002-coverage.md
├── flutter-factory-iteration-002-verification-plan.md
└── flutter-factory-iteration-002-test-cases.md
```

支持：
- 对比 iteration-001 和 iteration-002 的覆盖率变化
- 追踪模式积累进度
- 验证改进效果

---

## 优势

### 相比硬编码的优势

| 维度 | 硬编码 | 动态生成 |
|-----|---------|-----------|
| 需求适配性 | ❌ 固定 | ✅ 每次适配 |
| 历史追溯 | ❌ 无 | ✅ 完整记录 |
| 覆盖率分析 | ❌ 手动 | ✅ 自动计算 |
| 测试用例建议 | ❌ 无 | ✅ 自动生成 |
| 验证步骤 | ❌ 通用 | ✅ 定制化 |
| 失败场景处理 | ❌ 无 | ✅ 详细说明 |

---

## 使用示例

### 查看当前迭代验证

```bash
# 查看需求分析
cat .claude/skills/flutter_factory/validation/flutter-factory-iteration-001-requirements.md

# 查看覆盖分析
cat .claude/skills/flutter_factory/validation/flutter-factory-iteration-001-coverage.md

# 查看验证计划
cat .claude/skills/flutter_factory/validation/flutter-factory-iteration-001-verification-plan.md

# 查看测试用例
cat .claude/skills/flutter_factory/validation/flutter-factory-iteration-001-test-cases.md
```

### 下次迭代后对比

```bash
# 对比覆盖率
cat validation/iteration-001-coverage.md
cat validation/iteration-002-coverage.md

# 对比验证计划
diff validation/iteration-001-verification-plan.md \
     validation/iteration-002-verification-plan.md
```

---

## 更新文件列表

1. ✅ `.claude/skills/flutter_factory/SKILL.md` - 更新验证机制说明
2. ✅ `.claude/skills/flutter_factory/pattern_registry.json` - 添加动态验证配置
3. ✅ `.claude/skills/flutter_factory/validation/` - 新建动态验证目录
4. ✅ `validation/flutter-factory-iteration-001-requirements.md` - 需求分析文档
5. ✅ `validation/flutter-factory-iteration-001-coverage.md` - 覆盖分析文档
6. ✅ `validation/flutter-factory-iteration-001-verification-plan.md` - 验证计划文档
7. ✅ `validation/flutter-factory-iteration-001-test-cases.md` - 测试用例文档

---

**文档版本**: v1.0
**更新者**: flutter-skill-factory 架构优化

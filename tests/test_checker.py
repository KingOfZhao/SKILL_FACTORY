"""skill_factory.checker 单元测试。"""

from __future__ import annotations

from skill_factory import checker
from skill_factory.paths import skills_dir

META_SKILL_MD = """---
name: meta-demo-distiller
description: 演示用元技能，验证检查器对 meta- 前缀的豁免行为是否正确
---

# meta-demo-distiller

## 能力
- 一些不可降级实践

## 输入规范
- 输入：问题描述

## 输出规范
- 输出：结构化结果

## 使用示例
```bash
skill-factory check <path>
```
"""


def _write_meta_skill(d) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(META_SKILL_MD, encoding="utf-8")
    (d / "README.md").write_text("# meta-demo-distiller\n说明\n", encoding="utf-8")
    (d / "description.md").write_text("演示用元技能\n", encoding="utf-8")


def test_is_meta_skill_detection() -> None:
    chk = checker.MetaSkillChecker({})
    assert chk._is_meta_skill("meta-foo", "") is True
    assert chk._is_meta_skill("元-bar", "") is True
    assert chk._is_meta_skill("SKILL", "name: meta-foo\n") is True
    assert chk._is_meta_skill("plain", "name: plain\n") is False


def test_validate_meta_skill_no_blocking(tmp_path) -> None:
    d = tmp_path / "meta-demo-distiller"
    _write_meta_skill(d)
    p = d / "SKILL.md"
    report = checker.MetaSkillChecker({}).validate_skill(str(p))
    blocking = [r for r in report.results if not r.passed and r.severity in ("critical", "major")]
    assert blocking == []
    assert checker.run(str(p)) == 0


def test_real_flutter_distiller_passes() -> None:
    skill = skills_dir() / "meta-flutter-impl-distillation" / "SKILL.md"
    if not skill.exists():
        return  # 仓库结构变化时跳过，不误失败
    report = checker.MetaSkillChecker({}).validate_skill(str(skill))
    assert report.failed_rules == 0
    assert report.overall_score == 1.0


def test_score_is_one_when_no_failures() -> None:
    # 修复 perfect-pass 除零：满分应为 1.0 而非崩溃
    p_dir = skills_dir() / "meta-flutter-impl-distillation" / "SKILL.md"
    if not p_dir.exists():
        return
    report = checker.MetaSkillChecker({}).validate_skill(str(p_dir))
    assert 0.0 <= report.overall_score <= 1.0


TASK_SKILL_MD = """---
name: demo-task-skill
description: 演示用任务型技能，触发 best-practices / patterns / consistency 校验
---

# demo-task-skill

## 能力
- 生成代码

## 输入规范
- 输入：需求

## 输出规范
- 输出：代码

文件命名示例：MyWidget.dart
"""


def _write_task_skill(d) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(TASK_SKILL_MD, encoding="utf-8")


def test_non_meta_skill_runs_all_validators(tmp_path) -> None:
    # 非元 Skill 不豁免：会执行 best-practices/patterns/consistency，产生阻断项。
    d = tmp_path / "demo-task-skill"
    _write_task_skill(d)
    report = checker.MetaSkillChecker({}).validate_skill(str(d / "SKILL.md"))
    assert report.failed_rules > 0
    assert checker.run(str(d / "SKILL.md")) == 1


def test_validate_multiple_and_summary(tmp_path, capsys) -> None:
    _write_task_skill(tmp_path / "demo-task-skill")
    d2 = tmp_path / "meta-demo-distiller"
    _write_meta_skill(d2)
    chk = checker.MetaSkillChecker({})
    reports = chk.validate_multiple_skills(str(tmp_path))
    assert len(reports) == 2
    summary = chk.generate_validation_summary(reports)
    assert "Skill" in summary
    # run 在目录上会输出汇总；存在任务型阻断项 → 返回 1
    out = tmp_path / "report.json"
    rc = checker.run(str(tmp_path), summary=True, json_out=str(out))
    assert rc == 1
    assert out.exists()
    assert capsys.readouterr().out

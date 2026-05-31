"""skill_factory.catalog 单元测试。"""

from __future__ import annotations

import json

from skill_factory import catalog


def _make_skill(root, rel, name, desc, *, extra_py=False, description_md=False) -> None:
    d = root / rel
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {desc}\n---\n\n# {name}\n正文\n",
        encoding="utf-8",
    )
    if extra_py:
        (d / "tool.py").write_text("print('x')\n", encoding="utf-8")
    if description_md:
        (d / "description.md").write_text("desc\n", encoding="utf-8")


def test_parse_frontmatter() -> None:
    fm = catalog.parse_frontmatter('---\nname: foo\ndescription: "bar baz"\n---\nbody')
    assert fm == {"name": "foo", "description": "bar baz"}
    assert catalog.parse_frontmatter("no frontmatter") == {}


def test_classify() -> None:
    assert catalog.classify("meta-foo", "x/meta-foo") == "meta"
    assert catalog.classify("元-bar", "元/元-bar") == "meta"
    assert catalog.classify("plain", "元/sub/plain") == "meta"
    assert catalog.classify("flutter_factory", "flutter_factory") == "task"


def test_scan_classifies_and_sorts(tmp_path) -> None:
    _make_skill(tmp_path, "meta-a", "meta-a", "元技能A")
    _make_skill(tmp_path, "task-b", "task-b", "任务B", extra_py=True)
    skills = catalog.scan(str(tmp_path))
    assert [s.name for s in skills] == ["meta-a", "task-b"]
    assert skills[0].type == "meta"
    assert skills[1].type == "task"
    assert skills[1].has_scripts is True


def test_render_markdown_and_json(tmp_path) -> None:
    _make_skill(tmp_path, "meta-a", "meta-a", "元A")
    _make_skill(tmp_path, "t/task-b", "task-b", "任务B")
    skills = catalog.scan(str(tmp_path))
    md = catalog.render_markdown(skills, str(tmp_path))
    assert "技能总数：**2**" in md
    payload = json.loads(catalog.render_json(skills, str(tmp_path)))
    assert payload["total"] == 2
    assert payload["meta_count"] == 1
    assert payload["task_count"] == 1


def test_run_generate_then_check(tmp_path) -> None:
    _make_skill(tmp_path, "meta-a", "meta-a", "元A")
    out = tmp_path / "out"
    assert catalog.run(root=str(tmp_path), out=str(out)) == 0
    assert (out / "skill-catalog.md").exists()
    assert (out / "skill-catalog.json").exists()
    # 刚生成，--check 应判定最新
    assert catalog.run(root=str(tmp_path), out=str(out), check=True) == 0
    # 内容改变后 --check 应判定过期
    _make_skill(tmp_path, "meta-c", "meta-c", "元C")
    assert catalog.run(root=str(tmp_path), out=str(out), check=True) == 1


def test_run_usage_error_on_missing_dir(tmp_path) -> None:
    assert catalog.run(root=str(tmp_path / "nope")) == 2


def test_main_generate(tmp_path) -> None:
    _make_skill(tmp_path, "meta-a", "meta-a", "元A")
    out = tmp_path / "o"
    assert catalog.main([str(tmp_path), "--out", str(out)]) == 0
    assert (out / "skill-catalog.md").exists()


def test_display_root_is_repo_relative(tmp_path) -> None:
    """位于仓库内的扫描根目录应渲染为相对仓库根的稳定路径（避免机器相关绝对路径）。"""
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    skills_root = tmp_path / ".claude" / "skills"
    skills_root.mkdir(parents=True)
    assert catalog.display_root(str(skills_root)) == ".claude/skills"


def test_display_root_falls_back_outside_repo(tmp_path) -> None:
    """无仓库标记时回退为 basename，不泄露绝对路径。"""
    d = tmp_path / "loose-skills"
    d.mkdir()
    assert catalog.display_root(str(d)) == "loose-skills"

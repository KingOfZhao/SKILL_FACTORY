"""skill_factory.paths 单元测试。"""

from __future__ import annotations

from skill_factory import paths


def test_find_repo_root_from_package() -> None:
    root = paths.find_repo_root()
    assert (root / ".claude").is_dir()
    assert (root / "pyproject.toml").exists()


def test_skills_dir() -> None:
    assert paths.skills_dir().name == "skills"
    assert paths.skills_dir().parent.name == ".claude"


def test_env_override(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("SKILL_FACTORY_ROOT", str(tmp_path))
    assert paths.find_repo_root() == tmp_path.resolve()


def test_marker_walk_up(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("SKILL_FACTORY_ROOT", raising=False)
    (tmp_path / ".git").mkdir()
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    assert paths.find_repo_root(nested) == tmp_path.resolve()

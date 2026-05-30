"""skill_factory.cli 单元测试（子命令分发）。"""

from __future__ import annotations

import pytest

from skill_factory import cli

GOOD_DART = """
import 'package:flutter/material.dart';
class W extends StatelessWidget {
  const W({super.key});
  @override
  Widget build(BuildContext context) => const Text('x');
}
"""


def test_no_command_prints_help() -> None:
    assert cli.main([]) == 0


def test_version_exits_zero() -> None:
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0


def test_lint_selftest_dispatch() -> None:
    assert cli.main(["lint", "--selftest"]) == 0


def test_lint_clean_dir(tmp_path) -> None:
    (tmp_path / "ok.dart").write_text(GOOD_DART, encoding="utf-8")
    assert cli.main(["lint", str(tmp_path)]) == 0


def test_recommend_dispatch(capsys) -> None:
    assert cli.main(["recommend", "flutter widget provider"]) == 0
    out = capsys.readouterr().out
    assert "meta-flutter-impl-distillation" in out


def test_scan_dispatch(tmp_path) -> None:
    d = tmp_path / "meta-x"
    d.mkdir()
    (d / "SKILL.md").write_text("---\nname: meta-x\ndescription: d\n---\n# x\n", encoding="utf-8")
    out = tmp_path / "out"
    assert cli.main(["scan", str(tmp_path), "--out", str(out)]) == 0
    assert (out / "skill-catalog.json").exists()


def test_lint_json_output_dispatch(tmp_path) -> None:
    (tmp_path / "ok.dart").write_text(GOOD_DART, encoding="utf-8")
    out = tmp_path / "r.json"
    assert cli.main(["lint", str(tmp_path), "--format", "json", "--json", str(out)]) == 0
    assert out.exists()


def test_check_dispatch(tmp_path) -> None:
    d = tmp_path / "meta-demo"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\nname: meta-demo\ndescription: d\n---\n\n# meta-demo\n\n"
        "## 能力\n- x\n\n## 输入规范\n- a\n\n## 输出规范\n- b\n",
        encoding="utf-8",
    )
    (d / "README.md").write_text("# meta-demo\n", encoding="utf-8")
    (d / "description.md").write_text("d\n", encoding="utf-8")
    assert cli.main(["check", str(d / "SKILL.md")]) == 0

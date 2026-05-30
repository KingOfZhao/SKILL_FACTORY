"""skill_factory.lint 单元测试。"""

from __future__ import annotations

import json

from skill_factory import lint

BAD = """
import 'package:flutter/material.dart';

class BadPage extends StatefulWidget {
  @override
  State<BadPage> createState() => _BadPageState();
}

class _BadPageState extends State<BadPage> {
  final controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final data = http.get(Uri.parse('https://x'));
    print('building');
    final name = user!.profile!.name;
    return Column(children: items.map((e) => Text(e)).toList());
  }
}
"""

GOOD = """
import 'package:flutter/material.dart';

class GoodList extends StatelessWidget {
  const GoodList({super.key, required this.items});
  final List<String> items;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (_, i) => Text(items[i]),
    );
  }
}
"""


def test_bad_code_triggers_expected_anti_patterns() -> None:
    ids = {f.ap_id for f in lint.scan_text(BAD, "<bad>")}
    assert {"AP-1", "AP-3", "AP-4", "AP-6", "AP-9"} <= ids


def test_good_code_has_no_major_or_critical() -> None:
    findings = lint.scan_text(GOOD, "<good>")
    assert all(f.severity not in ("major", "critical") for f in findings)


def test_bang_excludes_not_equal_and_assert() -> None:
    assert not lint._scan_bang("if (a != b) {")
    assert not lint._scan_bang("assert(x != null);")
    assert lint._scan_bang("final v = obj!.value;")


def test_worst_severity_and_report() -> None:
    findings = lint.scan_text(BAD, "<bad>")
    assert lint.worst_severity(findings) == "critical"
    report = lint.to_report(findings)
    assert report["total"] == len(findings)
    assert report["counts"]["critical"] >= 1


def test_run_selftest_passes() -> None:
    assert lint.run_selftest() == 0


def test_run_returns_nonzero_on_bad_dir(tmp_path) -> None:
    f = tmp_path / "bad.dart"
    f.write_text(BAD, encoding="utf-8")
    out = tmp_path / "report.json"
    rc = lint.run(path=str(tmp_path), fmt="json", json_out=str(out))
    assert rc == 1
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["worst_severity"] == "critical"


def test_run_returns_zero_on_clean_dir(tmp_path) -> None:
    (tmp_path / "good.dart").write_text(GOOD, encoding="utf-8")
    assert lint.run(path=str(tmp_path)) == 0


def test_run_usage_error_without_path() -> None:
    assert lint.run(path=None) == 2


def test_main_selftest() -> None:
    assert lint.main(["--selftest"]) == 0

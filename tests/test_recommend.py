"""skill_factory.recommend 单元测试。"""

from __future__ import annotations

import json

from skill_factory import recommend


def test_flutter_request_hits_distiller() -> None:
    recs = recommend.recommend_skills("用 flutter 写一个 widget，状态管理用 provider")
    assert recs
    assert recs[0]["skill_name"] == "meta-flutter-impl-distillation"
    assert "flutter" in recs[0]["matched_keywords"]


def test_non_flutter_request_returns_empty() -> None:
    assert recommend.recommend_skills("写一个 python 爬虫") == []


def test_more_hits_yield_higher_confidence() -> None:
    few = recommend.recommend_skills("flutter")
    many = recommend.recommend_skills("flutter dart widget provider riverpod bloc")
    assert many[0]["confidence"] > few[0]["confidence"]


def test_recommendations_sorted_desc() -> None:
    registry = [
        {
            "skill_name": "low",
            "domain": "d",
            "keywords": ["alpha", "beta"],
            "confidence": 0.5,
            "description": "",
        },
        {
            "skill_name": "high",
            "domain": "d",
            "keywords": ["alpha"],
            "confidence": 0.95,
            "description": "",
        },
    ]
    recs = recommend.recommend_skills("alpha beta", registry=registry)
    confidences = [r["confidence"] for r in recs]
    assert confidences == sorted(confidences, reverse=True)


def test_run_writes_json(tmp_path) -> None:
    out = tmp_path / "rec.json"
    assert recommend.run("flutter widget", json_out=str(out)) == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["recommendations"][0]["skill_name"] == "meta-flutter-impl-distillation"


def test_main_returns_zero() -> None:
    assert recommend.main(["flutter widget"]) == 0
    assert recommend.main(["写个 python 脚本"]) == 0

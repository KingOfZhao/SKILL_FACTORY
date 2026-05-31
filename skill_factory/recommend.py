"""问题域 → 技能推荐（D）。

根据问题/需求描述，按关键词命中比例加权置信度，推荐最相关的技能。
被编排器（orchestrator）与全链路接入复用；CLI 子命令 ``recommend`` 直接调用。
"""

from __future__ import annotations

import argparse
import json

# 问题类型 -> 推荐技能注册表。每项：关键词命中即推荐对应技能，confidence 为基础置信度。
SKILL_RECOMMENDATION_REGISTRY: list[dict] = [
    {
        "skill_name": "meta-flutter-impl-distillation",
        "domain": "flutter-implementation",
        "keywords": [
            "flutter",
            "dart",
            "widget",
            "状态管理",
            "listview",
            "build(",
            "provider",
            "riverpod",
            "bloc",
            "setstate",
        ],
        "confidence": 0.9,
        "description": "将强模型隐性 Flutter 实现策略蒸馏为显式决策树/反模式/自检，提升普通模型实现质量",
    },
]


def recommend_skills(request: str, registry: list[dict] | None = None) -> list[dict]:
    """根据问题描述匹配推荐技能（关键词命中比例加权置信度）。"""
    registry = registry if registry is not None else SKILL_RECOMMENDATION_REGISTRY
    text = request.lower()
    recommendations = []
    for entry in registry:
        hits = [kw for kw in entry["keywords"] if kw.lower() in text]
        if not hits:
            continue
        ratio = len(hits) / len(entry["keywords"])
        confidence = round(entry["confidence"] * (0.6 + 0.4 * ratio), 4)
        recommendations.append(
            {
                "skill_name": entry["skill_name"],
                "domain": entry["domain"],
                "matched_keywords": hits,
                "confidence": confidence,
                "description": entry["description"],
            }
        )
    recommendations.sort(key=lambda r: r["confidence"], reverse=True)
    return recommendations


def run(request: str, json_out: str | None = None) -> int:
    """执行推荐；供 CLI 与薄壳共用。推荐为信息性输出，恒返回 0。"""
    recommendations = recommend_skills(request)
    payload = {"request": request, "recommendations": recommendations}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if json_out:
        with open(json_out, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="问题域 → 技能推荐")
    parser.add_argument("request", help="问题 / 需求描述")
    parser.add_argument("--json", dest="json_out", help="将推荐结果写入 JSON 文件")
    args = parser.parse_args(argv)
    return run(request=args.request, json_out=args.json_out)


if __name__ == "__main__":
    import sys

    sys.exit(main())

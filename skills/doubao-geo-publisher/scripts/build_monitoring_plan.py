#!/usr/bin/env python3
"""Generate a monitoring plan for Doubao GEO campaigns."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def unique_keep_order(items: List[str]) -> List[str]:
    seen = set()
    output = []
    for item in items:
        cleaned = item.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        output.append(cleaned)
    return output


def queries_from_plan(profile: Dict, plan: Dict | None) -> List[str]:
    queries = []
    queries.extend(profile.get("monitoring_baseline", {}).get("tracked_queries", []))
    queries.extend(profile.get("brand_terms", []))
    if plan:
        queries.extend(plan.get("validation_queries", []))
        for bucket in plan.get("keyword_buckets", {}).values():
            queries.extend(item.get("keyword", "") for item in bucket[:2])
    return unique_keep_order(queries)[:8]


def cadence(profile: Dict) -> Dict[str, str]:
    stage = profile.get("client_stage", "cold_start")
    if stage == "cold_start":
        return {
            "first_check": "发布后第 1 天",
            "second_check": "发布后第 3 天",
            "third_check": "发布后第 7 天",
            "regular_review": "之后每周一次",
        }
    return {
        "first_check": "发布后第 3 天",
        "second_check": "发布后第 7 天",
        "third_check": "发布后第 14 天",
        "regular_review": "之后每周一次",
    }


def alert_rules(profile: Dict) -> List[str]:
    rules = [
        "连续两轮查询都未出现目标品牌时，需要复盘关键词和文章结构。",
        "出现竞品但未出现自己时，优先补强证据与平台差异化。",
        "被引用来源长期不是头条/搜狐/官网时，需要重新检查内容承接面。",
    ]
    if profile.get("compliance", {}).get("industry_sensitivity") == "medical":
        rules.append("医疗类内容如出现敏感词预警或平台异常，暂停同主题批量发布。")
    return rules


def manual_vs_automation() -> Dict[str, List[str]]:
    return {
        "automation_candidates": [
            "固定查询词截图",
            "结果留档和命名",
            "监测计划生成",
            "成稿规则初检",
        ],
        "manual_review_required": [
            "判断回答是否真正推荐了目标品牌",
            "判断竞品上下文是否有威胁",
            "决定下一轮要补词、补文还是补资料",
            "最终发布和账号操作",
        ],
    }


def build_plan(profile: Dict, geo_plan: Dict | None) -> Dict:
    queries = queries_from_plan(profile, geo_plan)
    brand_name = profile.get("brand_name", "")
    query_cards = []
    for query in queries:
        query_cards.append(
            {
                "query": query,
                "checkpoints": [
                    "是否出现目标品牌",
                    "是否出现竞品",
                    "引用来源来自哪里",
                    "回答偏知识还是偏推荐",
                ],
            }
        )

    return {
        "brand_name": brand_name,
        "monitoring_goal": "跟踪豆包对目标品牌、业务词和平台内容的引用变化。",
        "cadence": cadence(profile),
        "queries": query_cards,
        "log_fields": [
            "date",
            "platform",
            "query",
            "target_brand_seen",
            "competitors_seen",
            "cited_sources",
            "result_type",
            "screenshot_path",
            "summary",
            "next_action",
        ],
        "alert_rules": alert_rules(profile),
        "automation_split": manual_vs_automation(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a monitoring plan for GEO campaigns.")
    parser.add_argument("--profile", required=True, help="Path to client profile JSON.")
    parser.add_argument("--plan", help="Optional path to geo plan JSON.")
    parser.add_argument("--output", help="Optional output file path.")
    args = parser.parse_args()

    profile = load_json(Path(args.profile))
    geo_plan = load_json(Path(args.plan)) if args.plan else None
    output = build_plan(profile, geo_plan)
    rendered = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

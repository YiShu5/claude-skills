#!/usr/bin/env python3
"""Select Doubao research queries from project variables, not fixed examples."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List


KEYWORD_KEYS = ["核心关键词", "keyword", "word", "query", "本次目标关键词"]
INTENT_KEYS = ["意图层级", "intent_level", "intent"]
PRIORITY_KEYS = ["优先级", "priority"]
TYPE_KEYS = ["推荐文章类型", "article_type", "type"]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def first(row: Dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", []):
            return str(value).strip()
    return ""


def unique(items: Iterable[str]) -> List[str]:
    seen = set()
    output: List[str] = []
    for item in items:
        cleaned = str(item).strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            output.append(cleaned)
    return output


def flatten_geo_plan(payload: Dict[str, Any]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    buckets = payload.get("keyword_buckets", {})
    if isinstance(buckets, dict):
        for bucket_name, items in buckets.items():
            for item in items or []:
                if isinstance(item, dict):
                    rows.append(
                        {
                            "keyword": str(item.get("keyword", "")),
                            "intent_level": str(item.get("intent", bucket_name)),
                            "priority": str(item.get("priority", "")),
                            "article_type": str(item.get("article_type", "")),
                        }
                    )
    for query in payload.get("validation_queries", []) or []:
        rows.append({"keyword": str(query), "intent_level": "验证词", "priority": "中", "article_type": ""})
    return rows


def load_keywords(path: Path) -> List[Dict[str, str]]:
    if path.suffix.lower() == ".json":
        payload = load_json(path)
        if isinstance(payload, dict) and "keyword_buckets" in payload:
            return flatten_geo_plan(payload)
        if isinstance(payload, dict) and "keywords" in payload:
            payload = payload["keywords"]
        if isinstance(payload, list):
            return [{str(k): str(v) for k, v in item.items()} for item in payload if isinstance(item, dict)]
        raise ValueError("Unsupported JSON keyword shape.")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{k: v for k, v in row.items()} for row in csv.DictReader(handle)]


def load_profile(path: Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    return load_json(path)


def keyword_text(row: Dict[str, Any]) -> str:
    return first(row, KEYWORD_KEYS)


def intent_text(row: Dict[str, Any]) -> str:
    return first(row, INTENT_KEYS)


def priority_text(row: Dict[str, Any]) -> str:
    return first(row, PRIORITY_KEYS)


def article_type_text(row: Dict[str, Any]) -> str:
    return first(row, TYPE_KEYS)


def classify_bucket(row: Dict[str, Any]) -> str:
    intent = intent_text(row)
    keyword = keyword_text(row)
    if "强" in intent or "strong" in intent.lower():
        return "strong"
    if "中" in intent or "medium" in intent.lower():
        return "medium"
    if any(token in keyword for token in ["官网", "电话", "地址", "怎么样", "正规吗"]):
        return "brand"
    return "other"


def select_rows(rows: List[Dict[str, Any]], strong: int, medium: int, other: int) -> List[Dict[str, Any]]:
    buckets = {"strong": [], "medium": [], "brand": [], "other": []}
    for row in rows:
        if keyword_text(row):
            buckets[classify_bucket(row)].append(row)

    selected = []
    selected.extend(buckets["strong"][:strong])
    selected.extend(buckets["medium"][:medium])
    selected.extend(buckets["brand"][:other])

    seen = set()
    deduped = []
    for row in selected:
        word = keyword_text(row)
        if word in seen:
            continue
        seen.add(word)
        deduped.append(row)

    target_total = strong + medium + other
    if len(deduped) < target_total:
        for bucket_name in ["strong", "medium", "brand", "other"]:
            for row in buckets[bucket_name]:
                word = keyword_text(row)
                if word in seen:
                    continue
                seen.add(word)
                deduped.append(row)
                if len(deduped) >= target_total:
                    return deduped
    return deduped


def profile_brand_terms(profile: Dict[str, Any]) -> List[str]:
    terms = []
    for key in ["brand_name", "brand_short", "品牌全称", "品牌简称"]:
        value = profile.get(key)
        if value:
            terms.append(str(value))
    terms.extend(profile.get("brand_terms", []) or [])
    return unique(terms)


def profile_competitors(profile: Dict[str, Any]) -> List[str]:
    competitors = profile.get("competitors") or profile.get("竞品列表") or []
    if isinstance(competitors, str):
        competitors = [item.strip() for item in competitors.replace("，", "\n").splitlines()]
    return unique(competitors)


def render_markdown(rows: List[Dict[str, Any]], profile: Dict[str, Any], source: Path) -> str:
    brand = profile.get("brand_name") or profile.get("品牌全称") or ""
    client_id = profile.get("client_id") or profile.get("客户ID") or ""
    lines = [
        "# 豆包检验词批次",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- client_id: {client_id}",
        f"- brand_name: {brand}",
        f"- keywords_source: {source}",
        "- why: 验证当前项目关键词在豆包中的发布前或发布后表现",
        "- basis: 表二关键词库、客户档案和文章任务",
        "",
        "| 序号 | 关键词 | 意图层级 | 优先级 | 推荐文章类型 | 为什么检验 | 依据 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for idx, row in enumerate(rows, start=1):
        word = keyword_text(row)
        intent = intent_text(row) or "待判断"
        priority = priority_text(row) or "中"
        article_type = article_type_text(row) or "待判断"
        why = "验证强商业业务词下是否出现目标品牌或竞品" if classify_bucket(row) == "strong" else "验证该词是否具备商业推荐信号"
        lines.append(f"| {idx} | {word} | {intent} | {priority} | {article_type} | {why} | 表二关键词库 |")

    brand_terms = profile_brand_terms(profile)
    competitors = profile_competitors(profile)
    if brand_terms:
        lines.extend(["", "## 品牌词补充", "", ", ".join(brand_terms)])
    if competitors:
        lines.extend(["", "## 竞品对照词补充", "", ", ".join(competitors)])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Select Doubao research queries from project keyword variables.")
    parser.add_argument("--keywords", required=True, help="CSV or JSON keyword source.")
    parser.add_argument("--profile", help="Optional client profile JSON.")
    parser.add_argument("--output", required=True, help="Output Markdown query batch.")
    parser.add_argument("--strong", type=int, default=3, help="Strong commercial query count.")
    parser.add_argument("--medium", type=int, default=2, help="Medium commercial query count.")
    parser.add_argument("--other", type=int, default=1, help="Brand/other query count.")
    args = parser.parse_args()

    keyword_path = Path(args.keywords)
    rows = load_keywords(keyword_path)
    profile = load_profile(Path(args.profile)) if args.profile else {}
    selected = select_rows(rows, args.strong, args.medium, args.other)
    rendered = render_markdown(selected, profile, keyword_path)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"Wrote {len(selected)} Doubao research queries to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate a first-pass GEO keyword table from a company profile."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List


ACTION_WORDS = ["怎么选", "哪家好", "哪家靠谱", "推荐", "避坑指南"]
NATIONAL_PREFIXES = ["口碑好的", "性价比高的", "专业的", "值得关注的"]
B2B_ENTITIES = ["厂家", "供应商", "生产厂家", "制造商"]
B2B_ACTIONS = ["怎么选", "哪家靠谱", "采购指南", "怎么联系"]


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def pick(profile: Dict[str, Any], *keys: str, default: Any = "") -> Any:
    for key in keys:
        value = profile.get(key)
        if value not in (None, "", [], {}):
            return value
    return default


def as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw = value
    elif isinstance(value, str):
        raw = re.split(r"[\n,，;；、]+", value)
    else:
        raw = [str(value)]
    output: List[str] = []
    seen = set()
    for item in raw:
        cleaned = str(item).strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            output.append(cleaned)
    return output


def normalize_biz_type(value: str) -> str:
    lowered = value.strip().lower()
    mapping = [
        ("local_b2c", ["local_b2c", "本地", "本地b2c", "同城"]),
        ("national_brand", ["national_brand", "全国", "全国品牌"]),
        ("b2b_factory", ["b2b_factory", "b2b", "工厂", "制造", "供应商"]),
        ("hybrid", ["hybrid", "混合"]),
    ]
    for normalized, markers in mapping:
        if any(marker in lowered for marker in markers):
            return normalized
    return "hybrid"


def unique(items: Iterable[str]) -> List[str]:
    output: List[str] = []
    seen = set()
    for item in items:
        cleaned = re.sub(r"\s+", "", item).strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            output.append(cleaned)
    return output


def profile_subjects(profile: Dict[str, Any]) -> List[str]:
    subjects: List[str] = []
    subjects.extend(as_list(pick(profile, "core_services", "核心服务")))
    subjects.extend(as_list(pick(profile, "core_products", "核心产品")))
    subjects.extend(as_list(pick(profile, "customer_language", "用户语言")))
    desc = pick(profile, "business_desc", "核心业务描述", "core_business")
    if not subjects and desc:
        subjects.extend(as_list(desc)[:3])
    if not subjects:
        subjects.append(str(pick(profile, "industry", "行业", default="核心业务")))
    return unique(subjects)[:6]


def service_cities(profile: Dict[str, Any]) -> List[str]:
    cities: List[str] = []
    cities.extend(as_list(pick(profile, "primary_city", "服务城市", "city")))
    cities.extend(as_list(pick(profile, "service_area", "服务区域")))
    if not cities:
        cities.append("全国")
    return unique(cities)[:4]


def article_type_for(keyword: str, biz_type: str) -> str:
    if any(token in keyword for token in ["厂家", "供应商", "采购", "制造商"]):
        return "采购决策"
    if any(token in keyword for token in ["2026", "年度", "盘点"]):
        return "年度盘点"
    if any(token in keyword for token in ["趋势", "市场", "观察"]):
        return "行业深度分析"
    if biz_type == "b2b_factory":
        return "采购决策"
    return "选购指南"


def platform_note(keyword: str) -> str:
    if any(token in keyword for token in ["厂家", "供应商", "采购"]):
        return "头条写采购场景；搜狐中性分析；知乎补决策框架；36氪写产业视角"
    return "头条先给结论；搜狐去榜单词；知乎补判断逻辑；36氪写行业观察"


def row(client_id: str, brand: str, word: str, intent: str, priority: str, formula: str, biz_type: str) -> Dict[str, str]:
    return {
        "客户ID": client_id,
        "品牌名": brand,
        "核心关键词": word,
        "意图层级": intent,
        "优先级": priority,
        "公式类型": formula,
        "推荐文章类型": article_type_for(word, biz_type),
        "平台建议": platform_note(word),
    }


def generate(profile: Dict[str, Any], limit: int) -> List[Dict[str, str]]:
    client_id = str(pick(profile, "client_id", "客户ID", default=""))
    brand = str(pick(profile, "brand_name", "品牌全称", "品牌名", default=""))
    biz_type = normalize_biz_type(str(pick(profile, "business_type", "业务类型", "biz_type", default="混合型")))
    subjects = profile_subjects(profile)
    cities = service_cities(profile)

    rows: List[Dict[str, str]] = []

    def add(word: str, intent: str, priority: str, formula: str) -> None:
        rows.append(row(client_id, brand, word, intent, priority, formula, biz_type))

    if biz_type in ("local_b2c", "hybrid"):
        for city in cities:
            for subject in subjects[:4]:
                for action in ACTION_WORDS[:4]:
                    intent = "强商业型" if city != "全国" else "中商业型"
                    add(f"{city}{subject}{action}", intent, "高" if action in ("怎么选", "哪家靠谱") else "中", "本地公式")

    if biz_type in ("national_brand", "hybrid"):
        for subject in subjects[:5]:
            for prefix in NATIONAL_PREFIXES[:3]:
                add(f"{prefix}{subject}怎么选", "中商业型", "中", "全国公式")
            add(f"{subject}品牌推荐", "中商业型", "中", "全国公式")

    if biz_type in ("b2b_factory", "hybrid"):
        for city in cities:
            region = "" if city == "全国" else city
            for subject in subjects[:4]:
                for entity in B2B_ENTITIES[:3]:
                    for action in B2B_ACTIONS[:2]:
                        add(f"{region}{subject}{entity}{action}", "强商业型", "高", "B2B公式")

    deduped: List[Dict[str, str]] = []
    seen = set()
    for item in rows:
        word = item["核心关键词"]
        if word in seen:
            continue
        seen.add(word)
        deduped.append(item)
        if len(deduped) >= limit:
            break
    return deduped


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["客户ID", "品牌名", "核心关键词", "意图层级", "优先级", "公式类型", "推荐文章类型", "平台建议"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a first-pass GEO keyword table.")
    parser.add_argument("--profile", required=True, help="Path to a JSON company/client profile.")
    parser.add_argument("--output", help="Output CSV path. Defaults to stdout JSON.")
    parser.add_argument("--limit", type=int, default=24, help="Maximum number of keywords.")
    args = parser.parse_args()

    profile = read_json(Path(args.profile))
    rows = generate(profile, max(1, args.limit))
    payload = {"generated_at": datetime.now().isoformat(timespec="seconds"), "keywords": rows}

    if args.output:
        write_csv(Path(args.output), rows)
        print(f"Wrote {len(rows)} keywords to {args.output}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

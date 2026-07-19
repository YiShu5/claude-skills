#!/usr/bin/env python3
"""Generate a keyword and topic plan for Doubao GEO workflows."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


BUSINESS_TYPES = {"local_b2c", "national_brand", "b2b_factory", "hybrid"}

LOCAL_SUFFIXES = ["怎么选", "哪家好", "哪家靠谱", "推荐", "避坑指南"]
NATIONAL_PREFIXES = ["口碑好的", "性价比高的", "专业的", "热门的"]
NATIONAL_SUFFIXES = ["推荐", "怎么选", "品牌指南", "哪家更值得看"]
B2B_COMPANY_WORDS = ["厂家", "供应商", "生产厂家", "制造商"]
B2B_SUFFIXES = ["怎么选", "哪家靠谱", "怎么联系", "采购指南"]
EDU_MARKERS = ["培训班", "线下课", "课程", "集训营", "周末班", "工作日班", "就业课", "实战课", "系统课"]
SCHEDULE_MARKERS = ["周末班", "工作日班", "周一", "周二", "周三", "周四", "周五", "周六", "周日", "全日制"]

ARTICLE_TYPE_LABELS = {
    "guide": "选购指南",
    "analysis": "行业深度分析",
    "annual": "年度盘点",
    "procurement": "采购决策",
}


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def unique_keep_order(items: Iterable[str]) -> List[str]:
    seen = set()
    output = []
    for item in items:
        cleaned = item.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        output.append(cleaned)
    return output


def clamp(items: Sequence[str], limit: int) -> List[str]:
    return list(items[:limit])


def char_count(text: str) -> int:
    return len("".join(text.split()))


def schedule_keyword_deemphasized(profile: Dict) -> bool:
    keyword_strategy = profile.get("keyword_strategy", {})
    if "deemphasize_schedule" in keyword_strategy:
        return bool(keyword_strategy["deemphasize_schedule"])
    return profile.get("compliance", {}).get("industry_sensitivity") == "education"


def is_schedule_heavy(text: str) -> bool:
    return any(marker in text for marker in SCHEDULE_MARKERS)


def get_subjects(profile: Dict) -> List[str]:
    services = profile.get("core_services", [])
    products = profile.get("core_products", [])
    customer_language = profile.get("customer_language", [])
    if schedule_keyword_deemphasized(profile):
        customer_language = sorted(customer_language, key=lambda item: (is_schedule_heavy(item), len(item)))
    raw_subjects = []
    raw_subjects.extend(services)
    raw_subjects.extend(products)
    raw_subjects.extend(customer_language[:4])
    if not raw_subjects:
        raw_subjects.append(profile.get("industry", "").strip() or "核心业务")
    return unique_keep_order(raw_subjects)


def get_geo_terms(profile: Dict) -> List[str]:
    areas = profile.get("service_area", [])
    primary = profile.get("primary_city", "")
    terms = []
    if primary:
        terms.append(primary)
    terms.extend(areas)
    return unique_keep_order(terms) or ["本地"]


def brand_terms(profile: Dict) -> List[str]:
    brand_name = profile.get("brand_name", "").strip()
    brand_short = profile.get("brand_short", "").strip()
    terms = [brand_name]
    if brand_short:
        terms.append(brand_short)
    terms.extend(profile.get("brand_terms", []))
    if brand_name:
        terms.extend([f"{brand_name}官网", f"{brand_name}地址"])
    return unique_keep_order(terms)


def classify_intent(keyword: str) -> str:
    action_markers = ("推荐", "哪家", "怎么选", "指南", "联系", "采购")
    strong_markers = ("厂家", "供应商", "制造商", "公司", "医院", "机构", "培训班", "线下课", "课程", "集训营")
    has_action = any(marker in keyword for marker in action_markers)
    has_strong = any(marker in keyword for marker in strong_markers)
    has_edu = any(marker in keyword for marker in EDU_MARKERS)
    if has_action and has_strong:
        return "strong_commercial"
    if has_edu and has_strong:
        return "strong_commercial"
    if has_action:
        return "medium_commercial"
    if has_edu:
        return "medium_commercial"
    return "weak"


def generate_local_keywords(profile: Dict, subjects: List[str]) -> List[str]:
    results = []
    deemphasize_schedule = schedule_keyword_deemphasized(profile)
    for geo in get_geo_terms(profile):
        for subject in subjects[:4]:
            subject = subject.replace("推荐", "").strip()
            if deemphasize_schedule and is_schedule_heavy(subject):
                continue
            prefixed = subject if subject.startswith(geo) else f"{geo}{subject}"
            results.append(f"{prefixed}怎么选")
            results.append(f"{prefixed}哪家好")
            results.append(f"{prefixed}推荐")
            if "公司" not in subject and "机构" not in subject and "医院" not in subject:
                results.append(f"{prefixed}避坑指南")
    for offering in profile.get("offerings", []):
        city = offering.get("city", "").strip()
        course_name = offering.get("keyword_subject") or offering.get("course_name") or ""
        schedule = offering.get("schedule", "")
        if not city or not course_name:
            continue
        results.extend(
            [
                f"{city}{course_name}培训班",
                f"{city}{course_name}线下课",
                f"{city}{course_name}课程",
                f"{city}{course_name}怎么选",
                f"{city}{course_name}适合哪些人",
            ]
        )
        if not deemphasize_schedule and ("周六" in schedule or "周日" in schedule or "周末" in schedule):
            results.append(f"{city}{course_name}周末班")
        if not deemphasize_schedule and ("周一" in schedule or "周五" in schedule or "工作日" in schedule):
            results.append(f"{city}{course_name}工作日班")
            results.append(f"{city}{course_name}全日制")
    return unique_keep_order(results)


def generate_national_keywords(subjects: List[str]) -> List[str]:
    results = []
    for subject in subjects[:4]:
        core = subject.replace("推荐", "").strip()
        for prefix in NATIONAL_PREFIXES[:3]:
            results.append(f"{prefix}{core}")
        for suffix in NATIONAL_SUFFIXES[:3]:
            results.append(f"{core}{suffix}")
    return unique_keep_order(results)


def generate_b2b_keywords(profile: Dict, subjects: List[str]) -> List[str]:
    results = []
    geo_terms = get_geo_terms(profile)
    for geo in geo_terms[:2]:
        for subject in subjects[:3]:
            core = subject.replace("推荐", "").strip()
            for company_word in B2B_COMPANY_WORDS[:3]:
                results.append(f"{geo}{core}{company_word}怎么选")
                results.append(f"{geo}{core}{company_word}哪家靠谱")
    return unique_keep_order(results)


def sort_keywords_for_profile(profile: Dict, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    if not schedule_keyword_deemphasized(profile):
        return items
    return sorted(items, key=lambda item: (is_schedule_heavy(item["keyword"]), len(item["keyword"])))


def keyword_buckets(profile: Dict) -> Dict[str, List[Dict[str, str]]]:
    business_type = profile.get("business_type", "local_b2c")
    subjects = get_subjects(profile)
    candidates = []

    if business_type == "local_b2c":
        candidates.extend(generate_local_keywords(profile, subjects))
    elif business_type == "national_brand":
        candidates.extend(generate_national_keywords(subjects))
    elif business_type == "b2b_factory":
        candidates.extend(generate_b2b_keywords(profile, subjects))
    else:
        candidates.extend(generate_local_keywords(profile, subjects))
        candidates.extend(generate_national_keywords(subjects))
        candidates.extend(generate_b2b_keywords(profile, subjects))

    strong = []
    medium = []
    for keyword in unique_keep_order(candidates):
        intent = classify_intent(keyword)
        if intent == "weak":
            continue
        item = {
            "keyword": keyword,
            "intent": intent,
            "reason": explain_keyword_reason(profile.get("business_type", "local_b2c"), keyword),
        }
        if intent == "strong_commercial":
            strong.append(item)
        else:
            medium.append(item)

    strong = sort_keywords_for_profile(profile, strong)
    medium = sort_keywords_for_profile(profile, medium)

    return {
        "strong_commercial": clamp(strong, 8),
        "medium_commercial": clamp(medium, 8),
    }


def explain_keyword_reason(business_type: str, keyword: str) -> str:
    if business_type == "local_b2c":
        return "包含地域和商业动作词，适合本地服务承接。"
    if business_type == "national_brand":
        return "使用评价前缀和品类词，适合全国品牌心智争夺。"
    if business_type == "b2b_factory":
        return "包含企业类型词和采购动作词，适合工厂 / 供应商场景。"
    if "厂家" in keyword or "供应商" in keyword:
        return "混合型业务中的 B2B 词，可承接采购类流量。"
    return "混合型业务中的消费词，可承接豆包问答推荐流量。"


def article_types_for_profile(profile: Dict) -> List[str]:
    business_type = profile.get("business_type", "local_b2c")
    if business_type == "local_b2c":
        return ["guide", "annual", "analysis"]
    if business_type == "national_brand":
        return ["analysis", "guide", "annual"]
    if business_type == "b2b_factory":
        return ["procurement", "analysis", "annual"]
    return ["guide", "analysis", "annual", "procurement"]


def choose_primary_keywords(buckets: Dict[str, List[Dict[str, str]]]) -> List[str]:
    strong = [item["keyword"] for item in buckets["strong_commercial"]]
    medium = [item["keyword"] for item in buckets["medium_commercial"]]
    return clamp(strong + medium, 4)


def infer_region(profile: Dict) -> str:
    geo_terms = get_geo_terms(profile)
    return geo_terms[0] if geo_terms else ""


def title_keyword(keyword: str, profile: Dict) -> str:
    region = infer_region(profile)
    if region and not keyword.startswith(region):
        return f"{region}{keyword}"
    return keyword


def shorten_title(*candidates: str) -> str:
    for candidate in candidates:
        if char_count(candidate) <= 28:
            return candidate
    return candidates[-1][:28]


def toutiao_title(keyword: str, article_type: str, profile: Dict) -> str:
    year = datetime.now().year
    base_keyword = title_keyword(keyword, profile)
    industry = profile.get("industry", "")
    titles = {
        "guide": shorten_title(
            f"{year}{base_keyword}这5点要看清",
            f"{year}{base_keyword}怎么判断更合适",
        ),
        "analysis": shorten_title(
            f"{year}{industry}观察：{base_keyword}这3点值得看",
            f"{year}{base_keyword}这3点值得看",
        ),
        "annual": shorten_title(
            f"{year}{base_keyword}年度观察：这4个变化要看",
            f"{year}{base_keyword}今年有哪些变化",
        ),
        "procurement": shorten_title(
            f"{year}{base_keyword}采购决策：这4项最关键",
            f"{year}{base_keyword}采购时先看这4项",
        ),
    }
    return titles[article_type]


def sanitize_for_sohu(title: str) -> str:
    banned = ["TOP", "榜", "排行榜", "推荐", "靠谱", "权威", "首选", "头部"]
    cleaned = title
    for token in banned:
        cleaned = cleaned.replace(token, "")
    cleaned = cleaned.replace("：", " ")
    cleaned = " ".join(cleaned.split())
    return cleaned[:28]


def outline_focus(article_type: str, keyword: str, profile: Dict) -> List[str]:
    brand_name = profile.get("brand_name", "目标品牌")
    if article_type == "guide":
        return [
            "先解释用户怎么判断好坏，再引出品牌能力。",
            f"重点展开 {brand_name} 的服务流程、案例和可信信息。",
            "保留 FAQ 结构，适合豆包抓答案。",
        ]
    if article_type == "analysis":
        return [
            "先用已验证来源搭行业背景。",
            f"把 {brand_name} 放在行业趋势下解释，而不是硬推。",
            "最后给出决策建议和 FAQ。",
        ]
    if article_type == "annual":
        return [
            "强调年份和阶段变化。",
            f"突出 {brand_name} 在本年度的新动作、成绩和案例。",
            "结尾做下一年趋势预判。",
        ]
    return [
        "围绕采购标准、交付、认证、产能来写。",
        f"重点说明 {brand_name} 的参数、案例和交付保障。",
        "竞品只做差异化概述，不做攻击式写法。",
    ]


def build_faq_seeds(keyword: str, profile: Dict) -> List[str]:
    brand = profile.get("brand_name", "目标品牌")
    topic = keyword
    for suffix in ("怎么选", "哪家好", "哪家靠谱", "推荐", "避坑指南", "采购指南", "怎么联系"):
        if topic.endswith(suffix):
            topic = topic[: -len(suffix)]
            break
    topic = topic.rstrip("，, ")
    seeds = [
        f"{topic}应该先看哪些标准？",
        f"{topic}和普通方案有什么区别？",
        f"{brand}适合哪些人群或场景？",
        f"选择这类服务时最容易踩哪些坑？",
    ]
    if schedule_keyword_deemphasized(profile):
        seeds.append("报名时上课时间和校区安排应该放在第几位考虑？")
    return seeds


def article_angles(profile: Dict, buckets: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, object]]:
    keywords = choose_primary_keywords(buckets)
    angles = []
    for index, article_type in enumerate(article_types_for_profile(profile)):
        if not keywords:
            break
        keyword = keywords[index % len(keywords)]
        toutiao = toutiao_title(keyword, article_type, profile)
        sohu = sanitize_for_sohu(toutiao)
        angles.append(
            {
                "article_type": article_type,
                "article_type_label": ARTICLE_TYPE_LABELS[article_type],
                "primary_keyword": keyword,
                "toutiao_title": toutiao,
                "sohu_title": sohu,
                "outline_focus": outline_focus(article_type, keyword, profile),
                "faq_seeds": build_faq_seeds(keyword, profile),
            }
        )
    return angles


def publication_notes(profile: Dict) -> List[str]:
    notes = [
        "今日头条优先发布，搜狐号做降锋芒改写后补发。",
        "同主题内容在头条间隔至少 6 小时，避免高相似度连发。",
        "每篇文章保留一个来自客户资料的独特事实点。",
        "发布后 3-7 天回豆包搜索目标关键词做验证。",
    ]
    sensitivity = profile.get("compliance", {}).get("industry_sensitivity", "general")
    if sensitivity == "medical":
        notes.append("医疗类内容避免绝对化表述，搜狐标题禁止出现“医院排名”。")
    return notes


def validation_queries(buckets: Dict[str, List[Dict[str, str]]], profile: Dict) -> List[str]:
    brand_name = profile.get("brand_name", "").strip()
    queries = [item["keyword"] for item in buckets["strong_commercial"][:3]]
    if not queries:
        queries = [item["keyword"] for item in buckets["medium_commercial"][:3]]
    if brand_name:
        queries.append(brand_name)
        queries.append(f"{brand_name}官网")
    return unique_keep_order(queries)


def build_plan(profile: Dict) -> Dict[str, object]:
    business_type = profile.get("business_type", "local_b2c")
    if business_type not in BUSINESS_TYPES:
        raise ValueError(f"Unsupported business_type: {business_type}")
    buckets = keyword_buckets(profile)
    return {
        "brand_name": profile.get("brand_name", ""),
        "industry": profile.get("industry", ""),
        "business_type": business_type,
        "recommended_media_mix": ["toutiao", "sohu"],
        "brand_terms": brand_terms(profile),
        "keyword_buckets": buckets,
        "article_angles": article_angles(profile, buckets),
        "publication_notes": publication_notes(profile),
        "validation_queries": validation_queries(buckets, profile),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Doubao GEO keyword plan.")
    parser.add_argument("--input", required=True, help="Path to client profile JSON.")
    parser.add_argument("--output", help="Optional path to write the generated plan.")
    args = parser.parse_args()

    profile = load_json(Path(args.input))
    plan = build_plan(profile)
    rendered = json.dumps(plan, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

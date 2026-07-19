#!/usr/bin/env python3
"""Lint GEO article drafts for Toutiao and Sohu publication rules."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


GENERAL_BANNED = ["最好", "最佳", "第一名", "行业第一", "顶级", "绝对", "永久", "100%", "独家", "首创", "全国领先"]
OPTIMIZATION_JARGON = ["EEAT", "GEO", "SEO", "豆包优化", "AI 搜索优化", "关键词布局", "AI搜索优化"]
SOHU_TITLE_BANNED = ["TOP", "榜", "排行榜", "推荐", "靠谱", "权威", "首选", "头部"]
MEDICAL_EXTRA = ["治愈率100%", "永不复发", "免费治疗", "优惠手术", "买一赠一"]
EDUCATION_EXTRA = ["保就业", "包就业", "保证就业", "保过", "包过", "不过退费", "100%就业", "保证涨薪"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def char_count(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def find_terms(text: str, terms: List[str]) -> List[str]:
    return [term for term in terms if term and term in text]


def find_phone_numbers(text: str) -> List[str]:
    phone_pattern = re.compile(r"(?<!\d)(?:\+?86[-\s]?)?(?:1[3-9]\d{9}|\d{3,4}[-\s]?\d{7,8})(?!\d)")
    return sorted(set(match.group(0) for match in phone_pattern.finditer(text)))


def keyword_count(text: str, keyword: str) -> int:
    if not keyword:
        return 0
    return text.count(keyword)


def title_suggestion(title: str, keyword: str, platform: str) -> str:
    cleaned = title
    if platform == "sohu":
        for token in SOHU_TITLE_BANNED:
            cleaned = cleaned.replace(token, "")
    cleaned = normalize_whitespace(cleaned.replace("：", " "))
    if not re.search(r"20\d{2}", cleaned):
        cleaned = f"2026{cleaned}"
    if not re.search(r"\d", cleaned):
        cleaned = f"{cleaned} 这5点要看清"
    if keyword and keyword not in cleaned:
        cleaned = f"2026{keyword}这5点要看清"
    return cleaned[:28]


def add_issue(issues: List[Dict[str, str]], severity: str, message: str) -> None:
    issues.append({"severity": severity, "message": message})


def lint(title: str, article: str, platform: str, industry: str, keyword: str) -> Tuple[List[Dict[str, str]], str]:
    issues: List[Dict[str, str]] = []
    merged = f"{title}\n{article}"

    if char_count(title) > 30:
        add_issue(issues, "warning", "标题超过 30 字，建议压缩。")
    if not re.search(r"20\d{2}", title):
        add_issue(issues, "warning", "标题缺少年份。")
    if not re.search(r"\d", title):
        add_issue(issues, "warning", "标题缺少数字元素。")

    general_hits = find_terms(merged, GENERAL_BANNED)
    if general_hits:
        add_issue(issues, "warning", f"发现通用高风险词：{', '.join(general_hits)}")

    jargon_hits = find_terms(merged, OPTIMIZATION_JARGON)
    if jargon_hits:
        add_issue(issues, "error", f"正式文章中不应出现优化术语：{', '.join(jargon_hits)}")

    if platform == "sohu":
        sohu_hits = find_terms(title, SOHU_TITLE_BANNED)
        if sohu_hits:
            add_issue(issues, "error", f"搜狐标题包含禁词：{', '.join(sohu_hits)}")
        phones = find_phone_numbers(merged)
        if phones:
            add_issue(issues, "error", f"搜狐版本不应出现电话号码：{', '.join(phones)}")

    if industry == "medical":
        medical_hits = find_terms(merged, MEDICAL_EXTRA)
        if medical_hits:
            add_issue(issues, "error", f"医疗类发现高风险表达：{', '.join(medical_hits)}")
        if platform == "sohu" and "医院排名" in merged:
            add_issue(issues, "error", "搜狐医疗内容不应出现“医院排名”。")

    if industry == "education":
        edu_hits = find_terms(merged, EDUCATION_EXTRA)
        if edu_hits:
            add_issue(issues, "error", f"教育培训类发现高风险承诺：{', '.join(edu_hits)}")

    if "参考来源" not in article and "参考资料" not in article:
        add_issue(issues, "warning", "正文末尾缺少参考来源段落。")

    body_chars = char_count(article)
    if body_chars < 900:
        add_issue(issues, "warning", "正文偏短，可能不利于形成完整结构。")
    if body_chars > 2600:
        add_issue(issues, "warning", "正文偏长，建议压缩到更适合平台阅读的长度。")

    if keyword:
        count = keyword_count(article, keyword)
        if count == 0:
            add_issue(issues, "error", "正文没有出现目标关键词。")
        elif count == 1:
            add_issue(issues, "warning", "正文中目标关键词仅出现 1 次，可再自然补充。")
        elif count > 8:
            add_issue(issues, "warning", "目标关键词出现过多，存在堆砌风险。")

    suggestion = title_suggestion(title, keyword, platform)
    return issues, suggestion


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a GEO article draft for platform safety.")
    parser.add_argument("--platform", required=True, choices=["toutiao", "sohu"], help="Target platform.")
    parser.add_argument("--industry", default="general", help="Industry sensitivity: general, medical, education, finance, legal.")
    parser.add_argument("--keyword", default="", help="Target keyword to validate.")
    parser.add_argument("--title", required=True, help="Article title.")
    parser.add_argument("--article", required=True, help="Path to article text or markdown file.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    args = parser.parse_args()

    article_text = read_text(Path(args.article))
    issues, suggestion = lint(args.title, article_text, args.platform, args.industry, args.keyword)
    has_error = any(item["severity"] == "error" for item in issues)

    if args.format == "json":
        payload = {
            "platform": args.platform,
            "industry": args.industry,
            "issues": issues,
            "suggested_title": suggestion,
            "passed": not has_error,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Platform: {args.platform}")
        print(f"Industry: {args.industry}")
        print(f"Passed: {'yes' if not has_error else 'no'}")
        print(f"Suggested title: {suggestion}")
        print("Issues:")
        if not issues:
            print("- None")
        else:
            for item in issues:
                print(f"- [{item['severity']}] {item['message']}")

    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())

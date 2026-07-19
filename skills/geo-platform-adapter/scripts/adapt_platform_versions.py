#!/usr/bin/env python3
"""Create mechanical platform variants for a GEO article draft."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


PHONE_RE = re.compile(r"(?<!\d)(?:\+?86[-\s]?)?(?:1[3-9]\d{9}|\d{3,4}[-\s]?\d{7,8})(?!\d)")
SOHU_REPLACEMENTS = {
    "TOP": "",
    "Top": "",
    "top": "",
    "排行榜": "观察",
    "排行": "观察",
    "排名": "观察",
    "榜单": "梳理",
    "榜": "梳理",
    "靠谱": "",
    "权威": "",
    "首选": "",
    "头部": "",
    "医院排名": "医院介绍",
}
GENERAL_BANNED = ["最好", "最佳", "绝对", "永久", "100%", "独家", "首创", "全国领先"]
JARGON = ["EEAT", "GEO", "SEO", "豆包优化", "AI搜索优化", "AI 搜索优化", "关键词布局"]
INTERNAL_TRACES = ["客户资料显示", "补充材料显示", "客户资料", "资料口径", "实体链", "目标达成词", "我们要绑定"]
TITLE_LABEL_RE = re.compile(r"^(?:今日头条|头条|搜狐|知乎|36氪|主稿|文章)?标题[：:]\s*")
PUBLISH_SETTINGS_RE = re.compile(r"^\s*##\s*发布设置（不复制到正文）[\s\S]*?\n---\s*\n", re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_title_body(text: str) -> Tuple[str, str]:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped:
            title = stripped.lstrip("#").strip()
            body = "\n".join(lines[idx + 1 :]).strip()
            return title, body
    return "未命名文章", ""


def clean_spaces(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_title_label(text: str) -> str:
    return TITLE_LABEL_RE.sub("", text.strip())


def replace_many(text: str, replacements: Dict[str, str]) -> str:
    output = text
    for old, new in replacements.items():
        output = output.replace(old, new)
    return clean_spaces(output)


def public_body_text(text: str) -> str:
    """Return the user-facing article body, excluding the publish-settings preface."""
    return PUBLISH_SETTINGS_RE.sub("", text, count=1).strip()


def variant_title(title: str, platform: str, keyword: str) -> str:
    output = clean_title_label(title)
    if platform == "sohu":
        output = replace_many(output, SOHU_REPLACEMENTS)
        if keyword and keyword not in output:
            output = f"2026{keyword}观察：这几点值得了解"
    elif platform == "zhihu":
        output = output.replace("推荐", "怎么判断").replace("排行榜", "选择框架")
        if not output.endswith("？"):
            output = f"{output}，应该怎么判断？"
    elif platform == "36kr":
        output = output.replace("哪家好", "行业观察").replace("推荐", "趋势观察").replace("排行榜", "产业观察")
        if "观察" not in output and "分析" not in output:
            output = f"2026{keyword or output}行业观察"
    return clean_spaces(output)


def adapt_body(body: str, platform: str) -> str:
    output = body
    if platform == "sohu":
        output = PHONE_RE.sub("可通过官方渠道联系", output)
        output = replace_many(output, SOHU_REPLACEMENTS)
    elif platform == "zhihu":
        output = "本文从判断标准、证据来源和适配场景三个角度展开。\n\n" + output
    elif platform == "36kr":
        output = "从产业供给、用户决策和内容可信度的角度看，这个话题更适合作为行业观察来讨论。\n\n" + output
        output = PHONE_RE.sub("官方渠道", output)
    return clean_spaces(output)


def collect_issues(text: str, title: str, platform: str, industry: str) -> List[Dict[str, str]]:
    public_text = public_body_text(text)
    merged = f"{title}\n{public_text}"
    issues: List[Dict[str, str]] = []
    for token in GENERAL_BANNED:
        if token in merged:
            issues.append({"platform": platform, "severity": "warning", "message": f"发现高风险绝对化表达：{token}"})
    for token in JARGON:
        if token in merged:
            issues.append({"platform": platform, "severity": "error", "message": f"正式文章不应出现优化黑话：{token}"})
    for token in INTERNAL_TRACES:
        if token in merged:
            issues.append({"platform": platform, "severity": "error", "message": f"正式正文不应出现内部交付痕迹：{token}"})
    if platform == "sohu" and PHONE_RE.search(merged):
        issues.append({"platform": platform, "severity": "error", "message": "搜狐版本仍包含电话号码"})
    if platform == "sohu" and industry == "medical" and "医院排名" in merged:
        issues.append({"platform": platform, "severity": "error", "message": "医疗类搜狐版本不应出现“医院排名”"})
    if "参考来源" not in merged and "参考资料" not in merged and "参考来源：见" not in merged:
        issues.append({"platform": platform, "severity": "warning", "message": "缺少可追溯来源说明；可放在发布设置或证据目录"})
    return issues


def write_variant(output_dir: Path, platform: str, title: str, body: str) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{platform}.md"
    path = output_dir / filename
    path.write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
    return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create platform variants for a GEO draft.")
    parser.add_argument("--input", required=True, help="Input Markdown article.")
    parser.add_argument("--output-dir", required=True, help="Directory for platform versions.")
    parser.add_argument("--industry", default="general", help="Industry sensitivity, e.g. medical, education, finance, legal.")
    parser.add_argument("--keyword", default="", help="Target keyword.")
    parser.add_argument("--platforms", default="toutiao,sohu,zhihu,36kr", help="Comma-separated platform ids.")
    args = parser.parse_args()

    source = read_text(Path(args.input))
    source_title, source_body = split_title_body(source)
    output_dir = Path(args.output_dir)
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source": args.input,
        "keyword": args.keyword,
        "industry": args.industry,
        "variants": [],
        "issues": [],
    }

    for platform in [item.strip() for item in args.platforms.split(",") if item.strip()]:
        title = variant_title(source_title, platform, args.keyword)
        body = adapt_body(source_body, platform)
        path = write_variant(output_dir, platform, title, body)
        issues = collect_issues(body, title, platform, args.industry)
        report["variants"].append({"platform": platform, "title": title, "path": path})
        report["issues"].extend(issues)

    report_path = output_dir / "platform-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(report['variants'])} platform variants to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

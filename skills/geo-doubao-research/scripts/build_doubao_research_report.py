#!/usr/bin/env python3
"""Build customer and internal Doubao research reports from pasted logs."""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


FIELD_RE = re.compile(r"^\s*[-*]\s*([^:：]+)[:：]\s*(.*)\s*$")
QUERY_HEADING_RE = re.compile(r"^##\s+Query[:：]\s*(.+?)\s*$", re.I)
SOURCE_HEADING_RE = re.compile(r"^##\s+Source[:：]\s*(.+?)\s*$", re.I)
FENCE_RE = re.compile(r"^```(\w+)?\s*$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_meta(lines: List[str]) -> Dict[str, str]:
    meta: Dict[str, str] = {}
    for line in lines:
        if line.startswith("## "):
            break
        match = FIELD_RE.match(line)
        if match:
            meta[match.group(1).strip()] = match.group(2).strip()
    return meta


def parse_records(text: str, kind: str) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
    lines = text.splitlines()
    meta = parse_meta(lines)
    heading_re = QUERY_HEADING_RE if kind == "effect" else SOURCE_HEADING_RE
    title_key = "keyword" if kind == "effect" else "title"
    body_key = "answer" if kind == "effect" else "article"
    records: List[Dict[str, str]] = []
    current: Dict[str, str] | None = None
    fence_name: str | None = None
    fence_lines: List[str] = []

    for line in lines:
        heading = heading_re.match(line)
        if heading:
            if current:
                if fence_name:
                    current[body_key] = "\n".join(fence_lines).strip()
                    fence_name = None
                    fence_lines = []
                records.append(current)
            current = {title_key: heading.group(1).strip()}
            continue

        if current is None:
            continue

        fence = FENCE_RE.match(line)
        if fence:
            if fence_name:
                current[body_key] = "\n".join(fence_lines).strip()
                fence_name = None
                fence_lines = []
            else:
                fence_name = fence.group(1) or "text"
                fence_lines = []
            continue

        if fence_name:
            fence_lines.append(line)
            continue

        match = FIELD_RE.match(line)
        if match:
            current[match.group(1).strip()] = match.group(2).strip()

    if current:
        if fence_name:
            current[body_key] = "\n".join(fence_lines).strip()
        records.append(current)
    return meta, records


def split_values(value: str) -> List[str]:
    if not value:
        return []
    raw = re.split(r"[|,，、;\n]+", value)
    return [item.strip() for item in raw if item.strip()]


def normalize_seen(value: str, answer: str, brand: str) -> str:
    lowered = value.strip().lower()
    if lowered in {"yes", "true", "已出现", "出现", "是"}:
        return "已出现"
    if lowered in {"partial", "partly", "部分", "部分出现"}:
        return "部分出现"
    if lowered in {"no", "false", "未出现", "否"}:
        return "未出现"
    if brand and brand in answer:
        return "已出现"
    return "待人工判断"


def infer_result_type(record: Dict[str, str], brand_status: str) -> str:
    result_type = record.get("result_type", "").strip()
    if result_type and result_type.lower() != "unknown":
        return result_type
    competitors = split_values(record.get("competitors_seen", ""))
    sources = split_values(record.get("cited_sources", ""))
    answer = record.get("answer", "")
    if brand_status in {"已出现", "部分出现"} and sources:
        return "品牌出现且有引用"
    if brand_status in {"已出现", "部分出现"}:
        return "品牌出现但引用待确认"
    if competitors:
        return "竞品占位"
    if sources:
        return "有来源但未命中品牌"
    if len(answer) > 50:
        return "泛知识回答"
    return "无有效结果"


def action_for(status: str, result_type: str) -> str:
    if status == "已出现" and "引用" in result_type:
        return "继续监测并补同主题第二篇内容"
    if status == "部分出现":
        return "补强目标品牌事实、FAQ和来源"
    if result_type == "竞品占位":
        return "进入竞品信源分析，反推来源和模板"
    if result_type == "泛知识回答":
        return "检查关键词商业信号，补地区/场景/决策动作"
    if result_type == "有来源但未命中品牌":
        return "补与该来源类型相近的可信内容"
    return "补资料、换词或延后复查"


def effect_report(meta: Dict[str, str], records: List[Dict[str, str]], stage: str) -> str:
    brand = meta.get("brand_name", "")
    project = meta.get("project", "")
    stage_label = "发布前诊断" if stage == "pre" else "发布后检测"
    rows = []
    source_counter: Counter[str] = Counter()
    competitor_counter: Counter[str] = Counter()
    status_counter: Counter[str] = Counter()

    for record in records:
        answer = record.get("answer", "")
        status = normalize_seen(record.get("target_brand_seen", ""), answer, brand)
        result_type = infer_result_type(record, status)
        sources = split_values(record.get("cited_sources", ""))
        competitors = split_values(record.get("competitors_seen", ""))
        source_counter.update(sources)
        competitor_counter.update(competitors)
        status_counter.update([status])
        rows.append(
            {
                "keyword": record.get("keyword", ""),
                "intent": record.get("intent_level", ""),
                "status": status,
                "result_type": result_type,
                "competitors": "、".join(competitors) or "无",
                "sources": "、".join(sources) or "无",
                "screenshot": record.get("screenshot", ""),
                "action": record.get("next_action") or action_for(status, result_type),
                "why": record.get("why_check", ""),
                "basis": record.get("basis", ""),
            }
        )

    lines = [
        f"# 豆包{stage_label}报告",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- project: {project}",
        f"- brand_name: {brand}",
        f"- stage: {stage}",
        f"- query_count: {len(rows)}",
        "",
        "## 总览",
        "",
        f"- 已出现：{status_counter.get('已出现', 0)}",
        f"- 部分出现：{status_counter.get('部分出现', 0)}",
        f"- 未出现：{status_counter.get('未出现', 0)}",
        f"- 待人工判断：{status_counter.get('待人工判断', 0)}",
        "",
        "## 关键词结果表",
        "",
        "| 关键词 | 意图 | 目标品牌状态 | 结果类型 | 竞品 | 引用来源 | 截图 | 下一步动作 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['keyword']} | {row['intent']} | {row['status']} | {row['result_type']} | {row['competitors']} | {row['sources']} | {row['screenshot']} | {row['action']} |"
        )

    lines.extend(["", "## 为什么检验与依据", "", "| 关键词 | 为什么做 | 依据 |", "| --- | --- | --- |"])
    for row in rows:
        lines.append(f"| {row['keyword']} | {row['why'] or '验证该词下豆包是否推荐目标品牌'} | {row['basis'] or '表二关键词库'} |")

    lines.extend(["", "## 高频引用来源", ""])
    if source_counter:
        for source, count in source_counter.most_common():
            lines.append(f"- {source}: {count}")
    else:
        lines.append("- 暂无有效引用来源")

    lines.extend(["", "## 高频竞品", ""])
    if competitor_counter:
        for competitor, count in competitor_counter.most_common():
            lines.append(f"- {competitor}: {count}")
    else:
        lines.append("- 暂无竞品记录")

    lines.extend(["", "## 客户版结论", ""])
    if stage == "pre":
        lines.append("- 这份报告用于说明发布前 AI 搜索真实现状，并确定后续内容生产方向。")
    else:
        lines.append("- 这份报告用于判断发布动作是否改善 AI 搜索结果，并决定下一轮内容。")
    lines.append("- 重点看目标品牌是否出现、竞品是否占位、豆包引用了哪些来源。")
    return "\n".join(lines) + "\n"


def article_type(record: Dict[str, str]) -> str:
    explicit = record.get("article_type", "").strip()
    if explicit:
        return explicit
    text = f"{record.get('title', '')}\n{record.get('article', '')}"
    rules = [
        ("推荐口碑榜", ["推荐", "口碑", "榜", "哪家"]),
        ("测评类", ["测评", "实测", "评分", "体验"]),
        ("选购指南", ["怎么选", "选择", "避坑", "维度"]),
        ("行业分析", ["行业", "趋势", "市场", "观察"]),
        ("采购决策", ["采购", "供应商", "厂家", "报价"]),
        ("FAQ问答", ["问：", "Q:", "常见问题", "FAQ"]),
    ]
    for label, tokens in rules:
        if any(token in text for token in tokens):
            return label
    return "待人工判断"


def competitor_report(meta: Dict[str, str], records: List[Dict[str, str]]) -> str:
    type_counter: Counter[str] = Counter()
    source_counter: Counter[str] = Counter()
    platform_counter: Counter[str] = Counter()
    query_map: Dict[str, List[str]] = defaultdict(list)

    rows = []
    for record in records:
        label = article_type(record)
        source_type = record.get("source_type") or record.get("platform") or "待判断"
        platform = record.get("platform", "待判断")
        query = record.get("query", "")
        title = record.get("title", "")
        type_counter.update([label])
        source_counter.update([source_type])
        platform_counter.update([platform])
        if query:
            query_map[query].append(title)
        rows.append(
            {
                "query": query,
                "title": title,
                "competitor": record.get("competitor_brand", ""),
                "platform": platform,
                "source_type": source_type,
                "article_type": label,
                "url": record.get("url", ""),
                "risk": risk_summary(record),
                "why": record.get("why_collect", ""),
                "basis": record.get("basis", ""),
            }
        )

    dominant_type = type_counter.most_common(1)[0][0] if type_counter else "待判断"
    dominant_source = source_counter.most_common(1)[0][0] if source_counter else "待判断"

    lines = [
        "# 竞品信源反推报告",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- project: {meta.get('project', '')}",
        f"- brand_name: {meta.get('brand_name', '')}",
        f"- source_count: {len(rows)}",
        "",
        "## 来源清单",
        "",
        "| 查询词 | 来源标题 | 竞品 | 平台 | 信源类型 | 文章类型 | URL | 风险点 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['query']} | {row['title']} | {row['competitor']} | {row['platform']} | {row['source_type']} | {row['article_type']} | {row['url']} | {row['risk']} |"
        )

    lines.extend(["", "## 模板与信源归类", ""])
    lines.append(f"- 高频文章类型：{dominant_type}")
    lines.append(f"- 高频信源类型：{dominant_source}")
    lines.append("")
    lines.append("### 文章类型分布")
    for label, count in type_counter.most_common():
        lines.append(f"- {label}: {count}")
    lines.append("")
    lines.append("### 信源类型分布")
    for label, count in source_counter.most_common():
        lines.append(f"- {label}: {count}")

    lines.extend(["", "## 为什么收集与依据", "", "| 来源标题 | 为什么做 | 依据 |", "| --- | --- | --- |"])
    for row in rows:
        lines.append(f"| {row['title']} | {row['why'] or '豆包引用或推荐了该来源'} | {row['basis'] or '豆包实际回答'} |")

    lines.extend(["", "## 模块更新建议", ""])
    if rows:
        lines.append(
            f"- 发现：豆包在本批关键词下更常引用 `{dominant_source}` 的 `{dominant_type}` 内容。"
        )
        lines.append(
            f"- 依据：共收集 {len(rows)} 篇来源，其中 `{dominant_type}` 出现 {type_counter.get(dominant_type, 0)} 次。"
        )
        lines.append(
            "- 建议：下一轮文章 Brief 增加对应标题公式、H2结构、FAQ和可验证来源，不直接复制竞品表达。"
        )
    else:
        lines.append("- 暂无有效来源，先补充豆包引用来源或人工打开来源文章。")
    return "\n".join(lines) + "\n"


def risk_summary(record: Dict[str, str]) -> str:
    text = f"{record.get('title', '')}\n{record.get('article', '')}"
    risks = []
    for token in ["最好", "最佳", "100%", "第一", "包过", "保就业", "治愈"]:
        if token in text:
            risks.append(token)
    return "、".join(risks) if risks else "待人工复核"


def compare_status(pre_record: Dict[str, str] | None, post_record: Dict[str, str] | None, brand: str) -> Tuple[str, str, str]:
    if not pre_record and not post_record:
        return "无记录", "无记录", "无变化"
    pre_status = normalize_seen((pre_record or {}).get("target_brand_seen", ""), (pre_record or {}).get("answer", ""), brand)
    post_status = normalize_seen((post_record or {}).get("target_brand_seen", ""), (post_record or {}).get("answer", ""), brand)
    if pre_status in {"未出现", "待人工判断"} and post_status in {"已出现", "部分出现"}:
        change = "改善"
    elif pre_status == "部分出现" and post_status == "已出现":
        change = "改善"
    elif pre_status == post_status:
        change = "持平"
    elif pre_status == "已出现" and post_status in {"未出现", "待人工判断"}:
        change = "回落"
    else:
        change = "需人工判断"
    return pre_status, post_status, change


def comparison_report(pre_meta: Dict[str, str], pre_records: List[Dict[str, str]], post_meta: Dict[str, str], post_records: List[Dict[str, str]]) -> str:
    brand = post_meta.get("brand_name") or pre_meta.get("brand_name", "")
    pre_by_keyword = {record.get("keyword", ""): record for record in pre_records}
    post_by_keyword = {record.get("keyword", ""): record for record in post_records}
    keywords = sorted(set(pre_by_keyword) | set(post_by_keyword))
    lines = [
        "# 发布前后豆包对比反馈",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- project: {post_meta.get('project') or pre_meta.get('project', '')}",
        f"- brand_name: {brand}",
        "",
        "| 关键词 | 发布前状态 | 发布后状态 | 变化判断 | 发布前来源 | 发布后来源 | 下一步动作 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    change_counter: Counter[str] = Counter()
    for keyword in keywords:
        pre_record = pre_by_keyword.get(keyword)
        post_record = post_by_keyword.get(keyword)
        pre_status, post_status, change = compare_status(pre_record, post_record, brand)
        change_counter.update([change])
        pre_sources = "、".join(split_values((pre_record or {}).get("cited_sources", ""))) or "无"
        post_sources = "、".join(split_values((post_record or {}).get("cited_sources", ""))) or "无"
        action = action_for(post_status, infer_result_type(post_record or {}, post_status))
        lines.append(f"| {keyword} | {pre_status} | {post_status} | {change} | {pre_sources} | {post_sources} | {action} |")

    lines.extend(["", "## 变化摘要", ""])
    for label, count in change_counter.most_common():
        lines.append(f"- {label}: {count}")
    lines.extend(["", "## 客户版反馈", "", "- 重点解释哪些关键词发生变化、引用来源是否改善、下一轮为什么继续做。"])
    lines.extend(["", "## 内部复盘入口", "", "- 对仍被竞品占位或引用竞品来源的关键词，进入竞品信源反推。"])
    return "\n".join(lines) + "\n"


def write_output(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Doubao GEO research reports from pasted logs.")
    parser.add_argument("--mode", required=True, choices=["effect", "competitor", "compare"], help="Report mode.")
    parser.add_argument("--stage", choices=["pre", "post"], default="pre", help="Effect report stage.")
    parser.add_argument("--input", help="Input log for effect or competitor mode.")
    parser.add_argument("--pre", help="Pre-stage effect log for compare mode.")
    parser.add_argument("--post", help="Post-stage effect log for compare mode.")
    parser.add_argument("--output", required=True, help="Output Markdown report.")
    args = parser.parse_args()

    if args.mode in {"effect", "competitor"}:
        if not args.input:
            parser.error("--input is required for effect and competitor modes.")
        kind = "effect" if args.mode == "effect" else "competitor"
        meta, records = parse_records(read_text(Path(args.input)), kind)
        report = effect_report(meta, records, args.stage) if args.mode == "effect" else competitor_report(meta, records)
    else:
        if not args.pre or not args.post:
            parser.error("--pre and --post are required for compare mode.")
        pre_meta, pre_records = parse_records(read_text(Path(args.pre)), "effect")
        post_meta, post_records = parse_records(read_text(Path(args.post)), "effect")
        report = comparison_report(pre_meta, pre_records, post_meta, post_records)

    write_output(Path(args.output), report)
    print(f"Wrote {args.mode} report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

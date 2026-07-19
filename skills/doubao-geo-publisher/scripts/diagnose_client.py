#!/usr/bin/env python3
"""Diagnose client readiness for a Doubao GEO engagement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


REQUIRED_GROUPS = {
    "strategy": ["objectives", "conversion_goal", "target_customers"],
    "business": ["brand_name", "industry", "business_type", "service_area"],
    "production": ["core_services", "channels"],
    "proof": ["eeat", "verified_sources"],
    "compliance": ["compliance"],
}


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def has_value(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.strip() != "待补充"
    if isinstance(value, list):
        return any(has_value(item) for item in value)
    if isinstance(value, dict):
        return any(has_value(item) for item in value.values())
    return True


def eeat_strength(profile: Dict) -> int:
    eeat = profile.get("eeat", {})
    score = 0
    for key in ("expertise", "experience", "authority", "trust"):
        if has_value(eeat.get(key, [])):
            score += 1
    return score


def field_score(profile: Dict) -> Tuple[int, int, List[str]]:
    total = 0
    present = 0
    missing = []
    for group, fields in REQUIRED_GROUPS.items():
        for field in fields:
            total += 1
            if has_value(profile.get(field)):
                present += 1
            else:
                missing.append(f"{group}.{field}")
    return present, total, missing


def infer_service_mode(profile: Dict) -> str:
    business_type = profile.get("business_type", "")
    if business_type == "local_b2c":
        return "本地服务型"
    if business_type == "national_brand":
        return "全国品牌型"
    if business_type == "b2b_factory":
        return "B2B 线索型"
    if business_type == "hybrid":
        return "混合型"
    return "待判断"


def infer_scenario(profile: Dict) -> str:
    stage = profile.get("client_stage", "")
    visibility = profile.get("monitoring_baseline", {}).get("current_visibility", "")
    goals = " ".join(profile.get("objectives", []))
    campuses = profile.get("campuses", [])
    if stage == "cold_start":
        return "新客户冷启动"
    if len(campuses) >= 2 and ("曝光" in goals or "咨询" in goals):
        return "多校区课程推广型"
    if "品牌" in goals and "业务词" not in goals:
        return "品牌防守型"
    if "不稳定" in visibility or "没" in visibility:
        return "已有内容但效果不稳定"
    if profile.get("business_type") == "b2b_factory":
        return "B2B 线索型"
    return "地区业务冲刺型"


def readiness_level(score: int) -> str:
    if score >= 85:
        return "ready"
    if score >= 65:
        return "needs_completion"
    return "foundation_missing"


def immediate_questions(profile: Dict, missing: List[str], eeat_score: int) -> List[str]:
    questions = []
    if "strategy.objectives" in missing:
        questions.append("客户最在意的结果到底是曝光、咨询、品牌词防守还是采购线索？")
    if "business.service_area" in missing:
        questions.append("服务区域要精确到哪个城市、区县或产业带？")
    if eeat_score < 3:
        questions.append("能否补充至少 3 条带数字或可验证来源的 E-E-A-T 事实？")
    if not has_value(profile.get("verified_sources")):
        questions.append("有没有可公开引用的报告、媒体报道或官方数据来源？")
    if not has_value(profile.get("channels")):
        questions.append("头条、搜狐、官网现在分别是否已开通并在运营？")
    return questions


def strengths(profile: Dict, eeat_score: int) -> List[str]:
    output = []
    if has_value(profile.get("brand_name")) and has_value(profile.get("industry")):
        output.append("品牌和行业基础信息清晰，可以进入关键词规划。")
    if eeat_score >= 3:
        output.append("E-E-A-T 证据相对完整，适合直接做内容生产。")
    if has_value(profile.get("monitoring_baseline")):
        output.append("已有基线监测信息，便于做收录和引用对比。")
    if has_value(profile.get("channels")):
        output.append("渠道信息明确，可以同步规划头条和搜狐版本。")
    return output


def gaps(profile: Dict, missing: List[str], eeat_score: int) -> List[str]:
    output = []
    if missing:
        output.append("基础资料仍有缺口，接待阶段要先补齐核心字段。")
    if eeat_score < 3:
        output.append("可验证证据偏少，容易导致文章内容空泛。")
    if not has_value(profile.get("content_assets")):
        output.append("缺少现成内容资产，后续案例和细节展开会受限。")
    if not has_value(profile.get("monitoring_baseline")):
        output.append("缺少监测基线，发布后难以判断改善幅度。")
    return output


def recommended_actions(profile: Dict, score: int, eeat_score: int) -> List[str]:
    actions = []
    if score < 65:
        actions.append("先完成客户诊断和资料补齐，不建议直接出稿。")
    else:
        actions.append("先产出第一批关键词和文章角度，再同步准备平台版本。")
    if eeat_score < 3:
        actions.append("优先补充资质、案例、评价、媒体和可公开数字。")
    if profile.get("business_type") == "local_b2c":
        actions.append("先做地区业务词和 FAQ，争取本地商业推荐流量。")
    if profile.get("business_type") == "b2b_factory":
        actions.append("先做采购决策类内容，突出参数、认证、交付和售后。")
    actions.append("发布后建立固定监测表，至少跟 3-5 个核心查询词。")
    return actions


def first_deliverables(profile: Dict, score: int) -> List[str]:
    if score < 65:
        return ["客户诊断报告", "资料补充清单", "第一阶段词包范围"]
    return ["客户诊断报告", "关键词与选题包", "双平台 Prompt 包", "监测计划"]


def build_report(profile: Dict) -> Dict:
    present, total, missing = field_score(profile)
    eeat_score = eeat_strength(profile)
    score = round(((present / total) * 70) + ((eeat_score / 4) * 30))
    return {
        "brand_name": profile.get("brand_name", ""),
        "service_mode": infer_service_mode(profile),
        "scenario": infer_scenario(profile),
        "readiness_score": score,
        "readiness_level": readiness_level(score),
        "strengths": strengths(profile, eeat_score),
        "gaps": gaps(profile, missing, eeat_score),
        "missing_fields": missing,
        "immediate_questions": immediate_questions(profile, missing, eeat_score),
        "recommended_actions": recommended_actions(profile, score, eeat_score),
        "first_deliverables": first_deliverables(profile, score),
    }


def to_markdown(report: Dict) -> str:
    sections = [
        f"# 客户诊断报告\n",
        f"- 品牌：{report['brand_name'] or '待补充'}",
        f"- 场景：{report['scenario']}",
        f"- 服务模式：{report['service_mode']}",
        f"- 完备度评分：{report['readiness_score']} ({report['readiness_level']})",
        "\n## 当前优势",
    ]
    sections.extend(f"- {item}" for item in (report["strengths"] or ["暂无明显优势"])) 
    sections.append("\n## 当前缺口")
    sections.extend(f"- {item}" for item in (report["gaps"] or ["暂无明显缺口"]))
    sections.append("\n## 需要立刻确认的问题")
    sections.extend(f"- {item}" for item in (report["immediate_questions"] or ["暂无"]))
    sections.append("\n## 建议下一步")
    sections.extend(f"- {item}" for item in report["recommended_actions"])
    sections.append("\n## 第一阶段交付")
    sections.extend(f"- {item}" for item in report["first_deliverables"])
    return "\n".join(sections) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose client readiness for GEO execution.")
    parser.add_argument("--input", required=True, help="Path to client profile JSON.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--output", help="Optional output file path.")
    args = parser.parse_args()

    profile = load_json(Path(args.input))
    report = build_report(profile)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.format == "markdown":
        rendered = to_markdown(report)

    if args.output:
        Path(args.output).write_text(rendered + ("" if rendered.endswith("\n") else "\n"), encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

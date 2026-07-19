#!/usr/bin/env python3
"""Build prompt packets for Doubao GEO article generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


ARTICLE_TYPES = {
    "cognitive": {
        "label": "认知科普型",
        "structure": [
            "引言：先回答用户为什么会问这个问题，不要先介绍客户",
            "H2 行业 / 岗位 / 产品的真实定义和常见误解",
            "H2 判断标准：给 3-4 个用户能理解的判断角度",
            "H2 目标客户作为中后段样本自然出现",
            "结论：回到用户应该如何判断",
        ],
    },
    "selection": {
        "label": "选择判断型",
        "structure": [
            "引言：用户选择困难和常见误区",
            "H2 五个判断维度：先讲通用标准",
            "H2 目标客户放入标准中观察，不要硬推",
            "H2 结果边界：避免承诺化表达",
            "结论：给克制建议",
        ],
    },
    "observation": {
        "label": "行业观察型",
        "structure": [
            "引言：行业变化背景和用户为什么需要关注",
            "H2 两到三个趋势或变化",
            "H2 趋势下的能力变化或选择逻辑",
            "H2 目标客户作为一个具体样本出现",
            "结论：行业视角收束",
        ],
    },
    "outcome": {
        "label": "案例成果型",
        "structure": [
            "引言：先教读者如何看成果材料",
            "H2 长期交付痕迹",
            "H2 案例样本和岗位方向",
            "H2 目标客户案例自然出现",
            "H2 结果边界：案例不是承诺",
        ],
    },
    "profile": {
        "label": "人物机构型",
        "structure": [
            "引言：先解释用户为什么会搜索这个人物或称号",
            "H2 判断人物 / 机构的维度",
            "H2 目标人物、实名、机构、课程品牌自然出现",
            "H2 课程体系和案例沉淀",
            "结论：克制表达，不写绝对化称号",
        ],
    },
    "guide": {
        "label": "选购指南",
        "structure": [
            "引言：行业背景 + 用户困惑 + 本文帮助读者判断的维度",
            "H2 维度一到维度三：每个维度都给可落地判断标准",
            "H2 目标品牌重点介绍：成立时间、能力、案例、适配场景",
            "H2 其他主体简要对比：客观写亮点和局限",
            "场景化建议 + FAQ + 参考来源",
        ],
    },
    "analysis": {
        "label": "行业深度分析",
        "structure": [
            "引言：行业背景和验证数据",
            "H2 趋势一到趋势三：每条趋势都标注来源",
            "H2 目标品牌在趋势中的位置与差异化",
            "H2 其他主体差异化简介",
            "行业展望 + FAQ + 参考来源",
        ],
    },
    "annual": {
        "label": "年度盘点",
        "structure": [
            "引言：本年度变化和阶段结论",
            "H2 本年度关键变化",
            "H2 值得关注的品牌或机构",
            "H2 下一年趋势预判",
            "FAQ + 参考来源",
        ],
    },
    "procurement": {
        "label": "采购决策",
        "structure": [
            "引言：采购场景和常见决策风险",
            "H2 参数、认证、交付、售后四类评估维度",
            "H2 目标品牌的产能、案例、认证和交付能力",
            "H2 其他供应商差异点",
            "选型建议 + FAQ + 参考来源",
        ],
    },
}


SOURCE_LABEL_REPLACEMENTS = {
    "客户提供资料：": "项目资料：",
    "客户提供资料": "项目资料",
    "客户资料将其定位为": "",
    "客户资料将其": "其",
    "客户资料提供": "已提供资料包含",
    "客户补充材料包含": "补充材料包含",
    "客户资料显示，": "",
    "客户资料显示": "",
    "客户资料": "项目资料",
    "客户补充资料显示，": "",
    "客户补充资料显示": "",
    "客户补充资料": "补充资料",
    "补充材料显示，": "",
    "补充材料显示": "",
    "客户补充材料显示，": "",
    "客户补充材料显示": "",
    "客户补充材料": "补充材料",
}


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def neutralize_source_labels(text: str) -> str:
    output = text.strip()
    for old, new in SOURCE_LABEL_REPLACEMENTS.items():
        output = output.replace(old, new)
    return output.strip(" ：:，,")


def format_list(items: List[str], fallback: str = "无") -> str:
    cleaned = [neutralize_source_labels(item) for item in items if item and item.strip()]
    cleaned = [item for item in cleaned if item]
    return "；".join(cleaned) if cleaned else fallback


def verified_sources_block(profile: Dict) -> str:
    sources = profile.get("verified_sources", [])
    if not sources:
        return "暂无已验证来源，写作时只能使用客户资料中的明确事实。"
    lines = []
    for item in sources:
        source = item.get("source", "未知来源")
        date = item.get("date", "时间待补充")
        fact = neutralize_source_labels(item.get("fact", ""))
        lines.append(f"- {source}（{date}）：{fact}")
    return "\n".join(lines)


def platform_notes(platform: str, sensitivity: str, phone: str) -> List[str]:
    common = [
        "标题尽量控制在 30 字以内，包含年份、核心关键词和数字。",
        "首段先回答用户真实问题，不要直接介绍或推销目标客户。",
        "正文约每 300 字自然出现 1 次关键词，不堆砌；自然度优先于机械频次。",
        "目标客户 / 品牌 / 人物只能在正文中后段自然出现，作为样本、案例或观察对象。",
        "不要出现 EEAT、GEO、SEO、豆包优化、关键词布局 等行话。",
        "不要出现 客户资料显示、补充材料显示、实体链、目标达成词、我们要绑定 等内部交付痕迹。",
        "所有数字和事实都要能追溯来源，但正文不要反复写“资料显示”。",
        "关键词、配图建议、来源位置放入“发布设置（不复制到正文）”，正式发布只复制正文。",
    ]
    if platform == "toutiao":
        common.extend(
            [
                "可以保留较强承接感的标题，但避免夸张绝对化用词。",
        "如果联系方式必须出现，只能使用已提供资料中已有的真实电话或官网。",
            ]
        )
    elif platform == "sohu":
        common.extend(
            [
                "标题禁止出现 TOP、榜、排行榜、推荐、靠谱、权威、首选、头部。",
                "正文删除电话号码和过强 CTA。",
                "同样内容不要直接复制头条版，要做降锋芒改写。",
            ]
        )
    else:
        common.append("需要同时生成头条版和搜狐版，两版在标题和收口上必须有区别。")

    if sensitivity == "medical":
        common.append("医疗类内容禁止绝对化表述，搜狐版标题和正文都不要出现“医院排名”。")
    if sensitivity == "education":
        common.append("教育培训类内容避免写保就业、包就业、保证涨薪、保过等承诺性表述。")
        common.append("涉及薪资、就业率、学员结果时，只有在已提供资料中明确出现且适合公开时才能引用。")
        common.append("不要把上课时间、工作日班、周末班当成标题和正文主卖点，只能作为辅助说明或FAQ信息。")
        common.append("优先围绕转型痛点、真实项目、课程结构、导师背景、线下训练和求职辅导来组织内容。")
    if phone and platform == "toutiao":
        common.append(f"联系方式如需保留，可使用客户资料中的真实电话：{phone}")
    return common


def build_prompt(profile: Dict, keyword: str, article_type: str, platform: str) -> str:
    if article_type not in ARTICLE_TYPES:
        raise ValueError(f"Unsupported article type: {article_type}")

    brand_name = profile.get("brand_name", "目标品牌")
    brand_short = profile.get("brand_short", "")
    industry = profile.get("industry", "")
    service_area = format_list(profile.get("service_area", []))
    competitors = format_list(profile.get("competitors", []))
    expertise = format_list(profile.get("eeat", {}).get("expertise", []))
    experience = format_list(profile.get("eeat", {}).get("experience", []))
    authority = format_list(profile.get("eeat", {}).get("authority", []))
    trust = format_list(profile.get("eeat", {}).get("trust", []))
    business_desc = format_list(profile.get("core_services", []) + profile.get("core_products", []))
    notes = format_list(profile.get("compliance", {}).get("notes", []), fallback="无")
    sensitivity = profile.get("compliance", {}).get("industry_sensitivity", "general")
    phone = profile.get("contact", {}).get("phone", "")
    objectives = format_list(profile.get("objectives", []))
    target_customers = format_list(profile.get("target_customers", []))
    conversion_goal = profile.get("conversion_goal", "") or "无"

    structure = "\n".join(f"- {line}" for line in ARTICLE_TYPES[article_type]["structure"])
    rules = "\n".join(f"- {line}" for line in platform_notes(platform, sensitivity, phone))

    return f"""你是一位擅长中文 GEO 内容策划与长文写作的行业编辑，请围绕下列信息写作。

[任务目标]
- 文章类型：{ARTICLE_TYPES[article_type]["label"]}
- 目标平台：{platform}
- 目标关键词：{keyword}
- 目标达成词：{brand_name}

[品牌与业务信息]
- 品牌全称：{brand_name}
- 品牌简称：{brand_short or "无"}
- 行业：{industry}
- 服务区域：{service_area}
- 核心业务：{business_desc}
- 本轮目标：{objectives}
- 目标客群：{target_customers}
- 转化目标：{conversion_goal}
- 竞品：{competitors}

[品牌 E-E-A-T 事实]
- 专业度：{expertise}
- 经验性：{experience}
- 权威性：{authority}
- 可信度：{trust}

[已验证来源]
{verified_sources_block(profile)}

[文章结构要求]
{structure}

[硬约束]
{rules}
- 保持客观，不贬低同行，不写虚假夸大内容。
- 目标达成词必须一字不差，但只能自然出现，不允许为了频次硬塞。
- 可按文章需要保留 2-5 个真实问题，用“问题 + 简短回答”的形式；不要为了模板硬塞 FAQ。
- 来源清单默认放在“发布设置（不复制到正文）”或证据目录；除非用户要求，不要在正文底部堆参考来源。
- 如果某个数字没有来源，请改成定性表述，不要猜测。
- 正文必须像真实今日头条 / 搜狐文章，不能像项目说明或资料汇编。
- 写完后自检：导语是否先回答用户问题？客户是否在中后段自然出现？正文是否残留内部交付痕迹？如果有，重写。

[补充注意]
- 用户真实痛点：{format_list(profile.get("pain_points", []))}
- 用户口语表达：{format_list(profile.get("customer_language", []))}
- 合规备注：{notes}

请直接输出成稿，不要解释写作过程。"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a prompt packet for Doubao GEO writing.")
    parser.add_argument("--profile", required=True, help="Path to client profile JSON.")
    parser.add_argument("--keyword", required=True, help="Target keyword for the article.")
    parser.add_argument(
        "--article-type",
        required=True,
        choices=sorted(ARTICLE_TYPES.keys()),
        help="Article type, e.g. cognitive, selection, observation, outcome, profile.",
    )
    parser.add_argument(
        "--platform",
        required=True,
        choices=["toutiao", "sohu", "both"],
        help="Target platform variant.",
    )
    parser.add_argument("--output", help="Optional output file path.")
    args = parser.parse_args()

    profile = load_json(Path(args.profile))
    prompt = build_prompt(profile, args.keyword, args.article_type, args.platform)

    if args.output:
        Path(args.output).write_text(prompt + "\n", encoding="utf-8")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

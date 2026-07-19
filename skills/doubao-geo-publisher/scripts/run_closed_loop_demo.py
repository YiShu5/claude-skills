#!/usr/bin/env python3
"""Run a showcase-style closed-loop GEO pipeline for a client profile."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"


def run_command(args: List[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout


def write_json(path: Path, payload: Dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_titles(text: str) -> Tuple[str, str]:
    toutiao_match = re.search(r"^今日头条标题：(.+)$", text, re.M)
    sohu_match = re.search(r"^搜狐号标题：(.+)$", text, re.M)
    return (
        toutiao_match.group(1).strip() if toutiao_match else "",
        sohu_match.group(1).strip() if sohu_match else "",
    )


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def article_manifest_map(path: Path | None) -> Dict[str, Dict]:
    if not path:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {item["file"]: item for item in payload}


def diagnose(profile: Path, output_dir: Path) -> Dict:
    json_path = output_dir / "diagnosis.json"
    md_path = output_dir / "diagnosis.md"
    run_command(["python3", str(SCRIPT_DIR / "diagnose_client.py"), "--input", str(profile), "--output", str(json_path)])
    run_command(
        ["python3", str(SCRIPT_DIR / "diagnose_client.py"), "--input", str(profile), "--format", "markdown", "--output", str(md_path)]
    )
    return load_json(json_path)


def generate_plan(profile: Path, output_dir: Path) -> Dict:
    plan_path = output_dir / "geo-plan.json"
    run_command(["python3", str(SCRIPT_DIR / "generate_geo_plan.py"), "--input", str(profile), "--output", str(plan_path)])
    return load_json(plan_path)


def build_prompts(profile: Path, geo_plan: Dict, output_dir: Path) -> List[Path]:
    prompt_dir = output_dir / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    prompt_paths = []
    for index, angle in enumerate(geo_plan.get("article_angles", []), start=1):
        article_type = angle["article_type"]
        keyword = angle["primary_keyword"]
        path = prompt_dir / f"{index:02d}-{article_type}.txt"
        run_command(
            [
                "python3",
                str(SCRIPT_DIR / "build_prompt_packet.py"),
                "--profile",
                str(profile),
                "--keyword",
                keyword,
                "--article-type",
                article_type,
                "--platform",
                "both",
                "--output",
                str(path),
            ]
        )
        prompt_paths.append(path)
    return prompt_paths


def build_monitoring(profile: Path, output_dir: Path) -> Dict:
    plan_path = output_dir / "geo-plan.json"
    monitoring_path = output_dir / "monitoring-plan.json"
    run_command(
        [
            "python3",
            str(SCRIPT_DIR / "build_monitoring_plan.py"),
            "--profile",
            str(profile),
            "--plan",
            str(plan_path),
            "--output",
            str(monitoring_path),
        ]
    )
    return load_json(monitoring_path)


def lint_articles(
    publish_dir: Path | None,
    manifest_path: Path | None,
    industry: str,
    output_dir: Path,
) -> Dict:
    if not publish_dir or not publish_dir.exists():
        payload = {"status": "skipped", "articles": [], "passed": True}
        write_json(output_dir / "article-validation.json", payload)
        (output_dir / "article-validation.md").write_text("# 成稿校验结果\n\n- 未提供文章目录，本轮跳过。\n", encoding="utf-8")
        return payload

    manifest = article_manifest_map(manifest_path)
    results = []
    overall_passed = True
    for path in sorted(publish_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        toutiao_title, sohu_title = extract_titles(text)
        if path.name.lower() == "readme.md":
            continue
        if not toutiao_title and not sohu_title:
            continue
        keyword = manifest.get(path.name, {}).get("keyword", "")
        per_platform = []
        for platform, title in (("toutiao", toutiao_title), ("sohu", sohu_title)):
            if not title:
                continue
            stdout = run_command(
                [
                    "python3",
                    str(SCRIPT_DIR / "platform_guard.py"),
                    "--platform",
                    platform,
                    "--industry",
                    industry,
                    "--keyword",
                    keyword,
                    "--title",
                    title,
                    "--article",
                    str(path),
                    "--format",
                    "json",
                ]
            )
            payload = json.loads(stdout)
            overall_passed = overall_passed and payload["passed"]
            per_platform.append(
                {
                    "platform": platform,
                    "title": title,
                    "passed": payload["passed"],
                    "issues": payload["issues"],
                    "suggested_title": payload["suggested_title"],
                }
            )
        results.append({"file": path.name, "keyword": keyword, "checks": per_platform})

    payload = {"status": "completed", "articles": results, "passed": overall_passed}
    write_json(output_dir / "article-validation.json", payload)

    lines = ["# 成稿校验结果", ""]
    for item in results:
        lines.append(f"## {item['file']}")
        lines.append(f"- 目标关键词：{item['keyword'] or '未指定'}")
        for check in item["checks"]:
            lines.append(f"- {check['platform']}：{'通过' if check['passed'] else '未通过'}")
            if check["issues"]:
                for issue in check["issues"]:
                    lines.append(f"- {check['platform']}问题：[{issue['severity']}] {issue['message']}")
        lines.append("")
    (output_dir / "article-validation.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return payload


def scorecard(diagnosis: Dict, geo_plan: Dict, prompt_paths: List[Path], monitoring_plan: Dict, article_validation: Dict) -> Dict:
    keyword_total = sum(len(items) for items in geo_plan.get("keyword_buckets", {}).values())
    query_total = len(monitoring_plan.get("queries", []))
    cadence_keys = len(monitoring_plan.get("cadence", {}))
    diagnosis_pass = diagnosis.get("readiness_score", 0) >= 65
    keyword_pass = keyword_total >= 6 and len(geo_plan.get("article_angles", [])) >= 3 and len(geo_plan.get("validation_queries", [])) >= 4
    prompt_pass = len(prompt_paths) >= 3
    monitoring_pass = query_total >= 4 and cadence_keys >= 3
    article_status = article_validation.get("status", "skipped")
    article_pass = article_validation.get("passed", False) if article_status == "completed" else True
    overall = all([diagnosis_pass, keyword_pass, prompt_pass, monitoring_pass, article_pass])
    return {
        "diagnosis_gate": {"passed": diagnosis_pass, "score": diagnosis.get("readiness_score", 0)},
        "keyword_gate": {
            "passed": keyword_pass,
            "keyword_total": keyword_total,
            "article_angles": len(geo_plan.get("article_angles", [])),
            "validation_queries": len(geo_plan.get("validation_queries", [])),
        },
        "prompt_gate": {"passed": prompt_pass, "prompt_count": len(prompt_paths)},
        "article_gate": {"passed": article_pass, "status": article_status, "article_count": len(article_validation.get("articles", []))},
        "monitoring_gate": {"passed": monitoring_pass, "query_total": query_total, "cadence_points": cadence_keys},
        "overall_status": "green" if overall else "yellow",
    }


def next_actions(scorecard_payload: Dict) -> List[str]:
    actions = []
    if not scorecard_payload["diagnosis_gate"]["passed"]:
        actions.append("先补齐客户资料和 E-E-A-T 事实，再进入内容生产。")
    if not scorecard_payload["keyword_gate"]["passed"]:
        actions.append("补足关键词池和文章角度，确保至少覆盖城市词、决策词、品牌词。")
    if not scorecard_payload["prompt_gate"]["passed"]:
        actions.append("继续补齐可直接投喂豆包的 Prompt 样例。")
    if not scorecard_payload["article_gate"]["passed"]:
        actions.append("优先修复平台校验失败的文章，再安排发布。")
    if not scorecard_payload["monitoring_gate"]["passed"]:
        actions.append("补齐监测词和回查节奏，避免发布后无从判断效果。")
    if not actions:
        actions.append("当前闭环已跑通，下一步可以进入第二批内容扩写和真实监测。")
    return actions


def write_summary(
    output_dir: Path,
    profile: Path,
    diagnosis: Dict,
    geo_plan: Dict,
    prompt_paths: List[Path],
    monitoring_plan: Dict,
    article_validation: Dict,
) -> None:
    scorecard_payload = scorecard(diagnosis, geo_plan, prompt_paths, monitoring_plan, article_validation)
    payload = {
        "profile": str(profile),
        "brand_name": diagnosis.get("brand_name", ""),
        "scenario": diagnosis.get("scenario", ""),
        "scorecard": scorecard_payload,
        "next_actions": next_actions(scorecard_payload),
    }
    write_json(output_dir / "showcase-summary.json", payload)

    lines = [
        "# Showcase 闭环汇总",
        "",
        f"- 品牌：{diagnosis.get('brand_name', '待补充')}",
        f"- 场景：{diagnosis.get('scenario', '待判断')}",
        f"- 闭环状态：{scorecard_payload['overall_status']}",
        "",
        "## 验证结果",
        f"- 接待诊断关：{'通过' if scorecard_payload['diagnosis_gate']['passed'] else '未通过'}（评分 {scorecard_payload['diagnosis_gate']['score']}）",
        f"- 关键词策略关：{'通过' if scorecard_payload['keyword_gate']['passed'] else '未通过'}（关键词 {scorecard_payload['keyword_gate']['keyword_total']} 个，文章角度 {scorecard_payload['keyword_gate']['article_angles']} 个）",
        f"- Prompt 可执行关：{'通过' if scorecard_payload['prompt_gate']['passed'] else '未通过'}（Prompt {scorecard_payload['prompt_gate']['prompt_count']} 份）",
        f"- 成稿合规关：{'通过' if scorecard_payload['article_gate']['passed'] else '未通过'}（文章 {scorecard_payload['article_gate']['article_count']} 篇）",
        f"- 发布监测关：{'通过' if scorecard_payload['monitoring_gate']['passed'] else '未通过'}（监测词 {scorecard_payload['monitoring_gate']['query_total']} 个）",
        "",
        "## 本轮建议",
    ]
    lines.extend(f"- {item}" for item in payload["next_actions"])
    (output_dir / "showcase-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a closed-loop showcase for Doubao GEO skill.")
    parser.add_argument("--profile", required=True, help="Path to client profile JSON.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated showcase artifacts.")
    parser.add_argument("--publish-dir", help="Optional directory containing publish-ready articles.")
    parser.add_argument("--article-manifest", help="Optional manifest JSON that maps article files to keywords.")
    parser.add_argument("--industry", default="general", help="Industry sensitivity for article validation.")
    args = parser.parse_args()

    profile = Path(args.profile).resolve()
    output_dir = Path(args.output_dir).resolve()
    publish_dir = Path(args.publish_dir).resolve() if args.publish_dir else None
    manifest_path = Path(args.article_manifest).resolve() if args.article_manifest else None

    output_dir.mkdir(parents=True, exist_ok=True)

    diagnosis = diagnose(profile, output_dir)
    geo_plan = generate_plan(profile, output_dir)
    prompt_paths = build_prompts(profile, geo_plan, output_dir)
    monitoring_plan = build_monitoring(profile, output_dir)
    article_validation = lint_articles(publish_dir, manifest_path, args.industry, output_dir)
    write_summary(output_dir, profile, diagnosis, geo_plan, prompt_paths, monitoring_plan, article_validation)

    print(json.dumps({"status": "ok", "output_dir": str(output_dir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

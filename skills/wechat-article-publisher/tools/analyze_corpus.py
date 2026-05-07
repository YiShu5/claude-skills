#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
analyze_corpus.py — 离线语料分析工具（不进入 skill 运行流程）

输入：一个或多个微信文章 HTML zip 包（标准导出格式）
输出：
  - <out>/corpus_clean/*.txt   每篇一个纯文本（去秀米噪音）
  - <out>/corpus_index.csv     标题 / 日期 / mp / 来源 zip / 字数 / 题材桶 / 首段预览

用途：从大批量 HTML 中筛出范文候选。跑完用 Excel 打开 csv，按字数+题材排序挑 10-16 篇。

用法：
  uv run tools/analyze_corpus.py \\
    --zip "D:/BaiduNetdiskDownload/蜡笔进化论HTML.zip" \\
    --zip "D:/BaiduNetdiskDownload/html(6).zip" \\
    --out ./corpus-analysis
"""

import argparse
import csv
import json
import re
import sys
import zipfile
from pathlib import Path


META_RE = re.compile(r'var\s+data\s*=\s*(\{.*?\})\s*;', re.DOTALL)
TITLE_RE = re.compile(r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', re.DOTALL)
CONTENT_RE = re.compile(r'<content[^>]*>(.*?)</content>', re.DOTALL)
RICH_CONTENT_RE = re.compile(r'<div[^>]*class="rich_media_content"[^>]*>(.*?)</div>\s*</body>', re.DOTALL)
TAG_RE = re.compile(r'<[^>]+>')
WS_RE = re.compile(r'\s+')

# 题材关键词桶（粗分，挑范文时用）
TOPIC_BUCKETS = {
    "AI工具实战": ["Claude", "Cursor", "GPT", "ChatGPT", "Midjourney", "Stable Diffusion", "AI 绘图", "AI绘图", "提示词", "prompt", "插件", "工作流"],
    "AI知识科普": ["Agent", "RAG", "Token", "大模型", "原理", "架构", "如何理解", "什么是"],
    "AI行业观察": ["OpenAI", "Anthropic", "估值", "融资", "发布", "上线", "宣布", "市场", "行业"],
    "职场/个人成长": ["加班", "效率", "副业", "职场", "成长", "焦虑", "迷茫", "30岁", "35岁"],
    "情感/生活": ["母亲", "父亲", "孩子", "童年", "回家", "孤独", "想念", "爱情"],
    "商业/运营": ["门店", "苏宁", "运营", "SOP", "流程", "团队", "管理", "增长"],
    "教程/SOP": ["手把手", "保姆级", "完整教程", "从0到1", "从零", "步骤", "教你"],
}


def classify_topic(title: str, body: str) -> str:
    text = (title + " " + body[:500]).lower()
    raw = title + " " + body[:500]
    scores = {}
    for bucket, kws in TOPIC_BUCKETS.items():
        s = sum(1 for kw in kws if kw.lower() in text or kw in raw)
        if s:
            scores[bucket] = s
    if not scores:
        return "其它"
    return max(scores, key=scores.get)


def parse_html(html: str) -> dict:
    meta = {}
    m = META_RE.search(html)
    if m:
        try:
            meta = json.loads(m.group(1))
        except Exception:
            pass

    title = ""
    m = TITLE_RE.search(html)
    if m:
        title = WS_RE.sub(" ", TAG_RE.sub("", m.group(1))).strip()
    if not title:
        title = meta.get("title", "")

    body_html = ""
    m = CONTENT_RE.search(html)
    if m:
        body_html = m.group(1)
    else:
        m = RICH_CONTENT_RE.search(html)
        if m:
            body_html = m.group(1)
        else:
            body_html = html

    body_html = re.sub(r'<section[^>]*Powered-by-XIUMI[^>]*>.*?</section>', ' ', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<style[^>]*>.*?</style>', ' ', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<script[^>]*>.*?</script>', ' ', body_html, flags=re.DOTALL)
    body = TAG_RE.sub(" ", body_html)
    body = WS_RE.sub(" ", body).strip()

    return {
        "title": title,
        "mp": meta.get("mp", ""),
        "time": meta.get("time", ""),
        "body": body,
    }


def safe_filename(name: str, max_len: int = 80) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    return name[:max_len].strip()


def process_zip(zip_path: Path, out_dir: Path, rows: list):
    out_text = out_dir / "corpus_clean"
    out_text.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".html")]
        print(f"[{zip_path.name}] {len(names)} HTML files")
        for i, name in enumerate(names, 1):
            try:
                raw = zf.read(name)
                html = raw.decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"  ! read fail {name}: {e}", file=sys.stderr)
                continue

            parsed = parse_html(html)
            title = parsed["title"] or Path(name).stem
            body = parsed["body"]
            wc = len(body)

            stem = safe_filename(f"{parsed.get('time', '')[:10]}_{title}")
            txt_path = out_text / f"{stem}.txt"
            n = 1
            while txt_path.exists():
                txt_path = out_text / f"{stem}__{n}.txt"
                n += 1
            txt_path.write_text(f"{title}\n{'='*40}\n{body}\n", encoding="utf-8")

            rows.append({
                "source_zip": zip_path.name,
                "source_file": name,
                "mp": parsed["mp"],
                "date": parsed["time"][:10],
                "title": title,
                "word_count": wc,
                "topic_bucket": classify_topic(title, body),
                "preview_first_200": body[:200],
                "clean_path": str(txt_path.relative_to(out_dir)),
            })

            if i % 50 == 0:
                print(f"  ... {i}/{len(names)}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zip", action="append", required=True, help="可重复，传 1+ 个 zip 路径")
    p.add_argument("--out", default="./corpus-analysis", help="输出目录")
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list = []

    for z in args.zip:
        zp = Path(z)
        if not zp.exists():
            print(f"!! 不存在: {z}", file=sys.stderr)
            continue
        process_zip(zp, out_dir, rows)

    csv_path = out_dir / "corpus_index.csv"
    cols = ["source_zip", "mp", "date", "title", "word_count", "topic_bucket", "preview_first_200", "clean_path", "source_file"]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"\n[OK] 完成 {len(rows)} 篇")
    print(f"   纯文本：{out_dir/'corpus_clean'}")
    print(f"   索引：  {csv_path}")
    print(f"\n下一步：用 Excel 打开 corpus_index.csv，按 topic_bucket + word_count 排序，挑 10-16 篇范文候选。")


if __name__ == "__main__":
    main()

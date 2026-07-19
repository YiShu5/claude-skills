---
name: geo-platform-adapter
description: 当用户需要把一篇 GEO 主稿改成今日头条、搜狐号、知乎、36氪等不同平台版本，进行标题改写、联系方式处理、禁词替换、发布风险检查、发布状态表字段生成或文章任务表写入准备时使用。适用于“一稿多版本”和“平台合规改写”的自动化流程。
---

# GEO Platform Adapter

## Overview

这个 Skill 对应 GEO 自动化流水线的第四步：把主稿改成不同平台的发布版本。确定性规则交给脚本先处理，语气、结构和平台内容风格再由人工或模型复核。

## Quick Start

把主稿 Markdown 改成多平台版本：

```bash
python3 skills/geo-platform-adapter/scripts/adapt_platform_versions.py \
  --input /path/to/article.md \
  --output-dir /path/to/platform-versions \
  --industry general \
  --keyword "目标关键词"
```

脚本会输出：

- `toutiao.md`
- `sohu.md`
- `zhihu.md`
- `36kr.md`
- `platform-report.json`

## Workflow

1. 读取主稿标题、正文、目标关键词、行业敏感度。
2. 先跑脚本做机械处理：电话、标题禁词、搜狐敏感词、平台文件拆分。
3. 对每个平台做人工 / LLM 二次复核。规则见 [references/platform-rules.md](./references/platform-rules.md)。
4. 按 `$geo-article-writer` 的 `article-generation-rules.md` 做去交付痕迹检查，确保正文像真实平台文章。
5. 把版本标题、文档链接、引用来源、生成时间、发布状态和收录状态写入文章任务表。
6. 对医疗、教育、金融、法律等行业，保留人工确认，不要自动发布。

## Platform Defaults

- `今日头条`: 口语化，开头先给结论，可保留电话和地址，但同主题文章间隔至少 6 小时。
- `搜狐号`: 标题中性化，删除电话，避免 `TOP`、`排行`、`榜`、`靠谱`、`权威`、`首选` 等词。
- `知乎`: 补逻辑、补来源、补选择框架，语气像经验回答或专业分析。
- `36氪`: 改成产业视角、趋势视角或商业观察，不做硬广。

## Hard Rules

- 平台改写不改变事实和数据来源。
- 正式文章不出现 `EEAT`、`GEO`、`SEO`、`豆包优化`、`关键词布局` 等优化黑话。
- 正式正文不出现 `客户资料显示`、`补充材料显示`、`实体链`、`目标达成词` 等内部交付痕迹。
- 关键词、配图建议、来源位置只能放在 `发布设置（不复制到正文）`，不要混进正文。
- 客户 / 品牌 / 人物必须自然出现在正文中后段，不能在导语里硬推。
- 搜狐版本不保留电话号码。
- 医疗类搜狐标题不出现 `医院排名`。
- 不自动发布，不自动登录账号，不自动提交敏感内容。
- 版本差异必须记录到文章任务表，方便后续监测复盘。

## Output Package

一次标准平台改写至少交付：

1. `平台版本文件`
2. `各平台标题`
3. `规则处理报告`
4. `人工复核清单`
5. `文章任务表可填字段`

## Related Skills

- 主稿生成用 `$geo-article-writer`。
- 关键词表生成用 `$geo-keyword-miner`。
- 完整豆包 / 头条 / 搜狐闭环可用 `$doubao-geo-publisher`。

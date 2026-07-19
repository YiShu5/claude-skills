---
name: geo-doubao-research
description: 当用户需要把豆包搜索检验、发布前诊断、发布后检测、前后对比反馈、竞品信源分析或浏览器半自动研究接入 GEO 自动化流程时使用。适用于从客户档案、关键词库、文章任务和豆包实际引用来源动态抽取变量，生成客户版诊断报告、发布后报告、对比反馈和内部复盘报告。
---

# GEO Doubao Research

## Overview

这个 Skill 是 GEO 自动化流程的“感知层”和“复盘层”。它不负责写文章，也不负责发布；它负责用豆包搜索验证客户在 AI 搜索里的真实状态，并把竞品与信源反推结果回流到关键词、写稿和平台改写模块。

默认只做豆包，采用有头浏览器半自动流程：人工处理登录、验证码和账号安全，AI 辅助搜索、截图、复制结果整理和报告生成。

## Where It Fits

客户流程：

1. `C1 创建档案与诊断`: 从客户档案和关键词库生成发布前豆包检验词。
2. `C2 发布前效果检验`: 搜豆包，记录目标品牌、竞品、引用来源和截图。
3. `C3 内容生产与发布`: 把诊断结论交给 `$geo-article-writer` 和 `$geo-platform-adapter`。
4. `C4 发布后检测`: 使用同一批或同类关键词复查豆包结果。
5. `C5 前后对比反馈`: 生成客户可读的变化表和下一步动作。

内部复盘流程：

1. `R1 竞品与信源分析`: 收集豆包引用或回答中出现的竞品来源。
2. `R2 模板逻辑提炼`: 给来源文章打标签，归类模板。
3. `R3 行业模块更新`: 更新关键词规则、文章 Brief、标题模板、信源策略。

## Quick Start

### 1. 准备豆包有头浏览器

```bash
bash skills/geo-doubao-research/scripts/prepare_doubao_session.sh \
  --profile-dir /tmp/doubao-geo-profile
```

打开后由人工完成登录。不要自动处理验证码或账号安全动作。

### 2. 从项目变量生成检验词

关键词必须来自当前项目，不写固定 demo：

```bash
python3 skills/geo-doubao-research/scripts/select_doubao_queries.py \
  --keywords /path/to/keywords.csv \
  --profile /path/to/client_profile.json \
  --output /path/to/doubao-query-batch.md
```

优先顺序：

1. 强商业词
2. 中商业词
3. 品牌词 / 目标达成词
4. 竞品对照词

### 3. 人工可见搜索并记录

用豆包逐个搜索检验词，把 AI 回答、引用来源、截图路径复制进模板：

- [assets/effect-log.template.md](./assets/effect-log.template.md)
- [assets/competitor-source-log.template.md](./assets/competitor-source-log.template.md)

### 4. 生成报告

发布前或发布后效果报告：

```bash
python3 skills/geo-doubao-research/scripts/build_doubao_research_report.py \
  --mode effect \
  --stage pre \
  --input /path/to/effect-log.md \
  --output /path/to/pre-diagnosis-report.md
```

竞品信源反推报告：

```bash
python3 skills/geo-doubao-research/scripts/build_doubao_research_report.py \
  --mode competitor \
  --input /path/to/competitor-source-log.md \
  --output /path/to/competitor-source-report.md
```

发布前后对比：

```bash
python3 skills/geo-doubao-research/scripts/build_doubao_research_report.py \
  --mode compare \
  --pre /path/to/pre-effect-log.md \
  --post /path/to/post-effect-log.md \
  --output /path/to/pre-post-comparison.md
```

## Decision Rules

每次安排动作前，先回答两件事：

1. 为什么做这个？
2. 这样做的依据是什么？

默认依据必须来自：

- `表一_客户档案`
- `表二_关键词库`
- `表三_文章任务`
- 豆包实际回答
- 豆包实际引用来源
- 客户可验证资料和公开来源

不能用固定样例替代真实项目变量。

## Hard Rules

- 不自动登录豆包。
- 不绕过验证码、风控或账号安全。
- 不自动发布内容。
- 不把竞品文章直接改写成我方文章。
- 不把无来源信息写成事实。
- 不把客户版诊断报告写得过度恐吓；重点是说明真实现状和下一步动作。
- 内部复盘结论必须回流到关键词、文章 Brief、标题模板或信源策略，不能只停留在截图留档。

## When To Read References

- 梳理客户发布前/后链路时：读 [references/customer-flow.md](./references/customer-flow.md)
- 做竞品与信源反推时：读 [references/internal-review-flow.md](./references/internal-review-flow.md)
- 使用 Playwright CLI / playwright-cli 操作豆包时：读 [references/browser-operations.md](./references/browser-operations.md)
- 给来源文章打标签和提炼模板时：读 [references/source-taxonomy.md](./references/source-taxonomy.md)

## Related Skills

- 关键词生成用 `$geo-keyword-miner`。
- 写稿与 Brief 更新用 `$geo-article-writer`。
- 平台版本生成用 `$geo-platform-adapter`。
- 完整 GEO 交付闭环用 `$doubao-geo-publisher`。

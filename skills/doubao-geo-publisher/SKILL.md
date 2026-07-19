---
name: doubao-geo-publisher
description: 当用户需要围绕豆包 AI 搜索做 GEO 内容规划、关键词挖掘、E-E-A-T 资料整理、今日头条与搜狐号双平台改写、文章合规检查或批量生成发布素材时使用。适用于本地服务、全国品牌、B2B 工厂制造和混合型业务，尤其适合“问答词到目标达成词”的中文内容运营任务。
---

# Doubao GEO Publisher

## Overview

这个 Skill 面向“豆包搜索 + 今日头条主发 + 搜狐补发”的 GEO 工作流。它不是单纯的发文工具，而是一套从客户接待到监测复盘的交付框架：

1. 接待客户并做上线前诊断。
2. 把客户资料整理成结构化档案和 E-E-A-T 证据包。
3. 生成带商业意图的关键词、选题和写作 Prompt。
4. 为今日头条和搜狐号生成差异化版本并做合规检查。
5. 在发布后做豆包搜索验证、引用追踪和迭代建议。
6. 对稳定动作逐步沉淀为 Playwright 命令或脚本，降低反复操作成本。

这套流程分两条链路：

- `客户流程`: 发布前诊断、内容生产发布、发布后检测、前后对比反馈。
- `内部复盘流程`: 竞品与信源反推、模板逻辑提炼、行业模块更新。

默认策略：

- 豆包优化主阵地优先看 `今日头条`，`搜狐号`作为补位与扩散平台。
- 关键词只保留 `中商业型` 和 `强商业型`，避免纯知识词浪费篇幅。
- 一切数据优先引用客户资料和可验证公开来源；没有来源就不要硬写。
- 在正式生成内容前先做 `客户诊断`，避免客户资料不全时直接进入生产。
- 对高重复的监测动作优先用 `npx playwright` 做半自动探测或留出脚本接口。

## Quick Start

### 1. 先做客户诊断

先用 [assets/intake_questionnaire.template.md](./assets/intake_questionnaire.template.md) 跟客户对齐需求，再把信息整理成 [assets/client_profile.template.json](./assets/client_profile.template.json)。

如果已经拿到客户资料，优先先跑诊断：

```bash
python3 skills/doubao-geo-publisher/scripts/diagnose_client.py \
  --input /path/to/client_profile.json
```

这个脚本会输出：

- 客户所处场景
- 当前资料完备度
- 缺失字段
- 接下来应该先补什么
- 第一阶段应该交付什么

### 2. 准备客户资料

如果原始资料很乱，先按下面顺序补字段：

- `objectives`
- `target_customers`
- `conversion_goal`
- `brand_name`
- `industry`
- `business_type`
- `service_area`
- `core_services` / `core_products`
- `eeat`
- `verified_sources`
- `competitors`
- `compliance.industry_sensitivity`

缺失字段宁可留空或写 `待补充`，不要编造。

### 3. 生成关键词与选题包

运行：

```bash
python3 skills/doubao-geo-publisher/scripts/generate_geo_plan.py \
  --input /path/to/client_profile.json \
  --output /path/to/geo_plan.json
```

这个脚本会输出：

- 品牌词和目标达成词
- 中商业型 / 强商业型关键词
- 推荐文章类型
- 头条标题候选
- 搜狐安全标题候选
- FAQ 种子问题
- 发布与验证建议

### 4. 生成写作 Prompt 包

选定 `关键词 + 文章类型 + 平台` 后运行：

```bash
python3 skills/doubao-geo-publisher/scripts/build_prompt_packet.py \
  --profile /path/to/client_profile.json \
  --keyword "郑州家庭保洁怎么选" \
  --article-type guide \
  --platform toutiao
```

支持的文章类型：

- `guide`: 选购 / 选择指南
- `analysis`: 行业深度分析
- `annual`: 年度盘点
- `procurement`: 采购决策

支持的平台：

- `toutiao`
- `sohu`
- `both`

### 5. 检查成稿是否适配平台

```bash
python3 skills/doubao-geo-publisher/scripts/platform_guard.py \
  --platform sohu \
  --industry medical \
  --keyword "郑州正骨医院怎么选" \
  --title "2026郑州正骨医院推荐TOP5" \
  --article /path/to/article.md
```

这个脚本会检查：

- 标题长度、年份、数字
- 搜狐号标题禁词
- 电话号泄漏
- 医疗类敏感表达
- 优化术语外露
- 参考来源段落
- 关键词出现频次

### 6. 生成监测计划

```bash
python3 skills/doubao-geo-publisher/scripts/build_monitoring_plan.py \
  --profile /path/to/client_profile.json \
  --plan /path/to/geo_plan.json
```

这个脚本会输出：

- 监测查询词
- 建议频率
- 要记录的字段
- 触发人工复盘的阈值
- 哪些步骤适合继续自动化

### 7. 做发布前 / 发布后豆包研究

当需要把豆包搜索结果变成客户诊断、发布后检测或内部复盘时，使用 `$geo-doubao-research`。

先从当前项目变量抽取检验词，不使用固定样例：

```bash
python3 skills/geo-doubao-research/scripts/select_doubao_queries.py \
  --keywords /path/to/keywords.csv \
  --profile /path/to/client_profile.json \
  --output /path/to/doubao-query-batch.md
```

再用有头浏览器进行豆包检验：

```bash
bash skills/geo-doubao-research/scripts/prepare_doubao_session.sh \
  --profile-dir /tmp/doubao-geo-profile
```

最后把人工复制的豆包回答、引用来源和截图路径整理成报告：

```bash
python3 skills/geo-doubao-research/scripts/build_doubao_research_report.py \
  --mode effect \
  --stage pre \
  --input /path/to/effect-log.md \
  --output /path/to/pre-diagnosis-report.md
```

这个步骤用于：

- 发布前诊断客户在 AI 搜索里的真实状态
- 发布后检测内容发布是否改变豆包结果
- 对比发布前后变化
- 收集竞品和引用来源，进入内部复盘

### 8. 浏览器探测豆包入口

```bash
skills/doubao-geo-publisher/scripts/probe_doubao_surface.sh \
  --url https://www.doubao.com \
  --output-dir /tmp/doubao_probe
```

这个脚本使用 `npx playwright screenshot` 做低成本探测，适合：

- 验证页面是否可打开
- 观察是否需要登录
- 保存页面截图给人工复核
- 作为后续登录态脚本的前置探针

### 9. 跑展示版闭环

如果要把这套 Skill 用于 `上传展示`、`案例演示` 或 `对外说明`，直接跑闭环脚本：

```bash
python3 skills/doubao-geo-publisher/scripts/run_closed_loop_demo.py \
  --profile /path/to/client_profile.json \
  --publish-dir /path/to/publish-batch \
  --article-manifest /path/to/article-manifest.json \
  --industry education \
  --output-dir /path/to/showcase
```

这个脚本会自动输出：

- `diagnosis.json` / `diagnosis.md`
- `geo-plan.json`
- `prompts/*.txt`
- `monitoring-plan.json`
- `article-validation.json` / `article-validation.md`
- `showcase-summary.json` / `showcase-summary.md`

适合拿来证明这套 Skill 已经从“方法论”进入“可交付工作流”。

## Workflow

### 0. 接待与诊断

默认把自己当成客户接待人员，而不是写稿机器人。先判断客户当前处于哪一类场景：

- `新客户冷启动`: 没有资料、没有内容、没有平台基建
- `已有内容但没收录`: 发过文章，但豆包和平台效果差
- `品牌防守`: 品牌词搜索结果杂乱，官网 / 头条 / 搜狐信息不统一
- `重点项目冲刺`: 某个业务词、地区词或季度活动要快速起量
- `B2B线索型`: 重点是询盘、留资、采购决策内容，不是单纯流量

先做三件事：

1. 确认客户目标是 `曝光`、`咨询`、`品牌词防守`、`地区商机` 还是 `招商/采购线索`。
2. 确认客户现在手里到底有什么，尤其是资质、案例、媒体、平台账号和历史内容。
3. 确认行业敏感级别，尤其是医疗、教育、法律、金融这类高风险场景。

### A. 先判断业务类型

- `local_b2c`: 本地服务，优先“地域 + 品类 + 商业动作词”
- `national_brand`: 全国品牌，优先“评价前缀 + 品类属性 + 推荐后缀”
- `b2b_factory`: 工厂制造 / 供应链，优先“产业带 / 地域 + 品类 + 企业类型词 + 商业动作词”
- `hybrid`: 同时输出两套关键词池

### B. 再判断文章形态

- 用户不理解行业、岗位、产品或服务时，用 `认知科普型`。
- 用户正在比选老师、机构、产品或服务时，用 `选择判断型`。
- 用户需要看行业趋势、变化背景和品牌位置时，用 `行业观察型`。
- 用户关心就业、案例、成果或交付痕迹时，用 `案例成果型`。
- 用户搜索人物、账号、创始人、老师或机构时，用 `人物机构型`。

旧的 `guide / analysis / annual / procurement` 只作为脚本兼容类型。正式发布文章必须落到上面五类之一，并读取 `$geo-article-writer` 的 `article-generation-rules.md`。

### C. 双平台策略

先做头条版，再做搜狐版：

1. 头条版可以更有承接感，但先回答用户问题，不要在导语硬推客户。
2. 搜狐版要把标题降锋芒，去掉 `TOP`、`榜`、`推荐`、`靠谱`、`权威` 等词。
3. 搜狐版默认删电话、删过强 CTA、删医疗类“医院排名”表达。
4. 正式正文必须遵守 `$geo-article-writer` 的五类文章规范，不把内部 GEO 逻辑写进正文。

### D. 发布后监测

把监测视为交付的一部分，不要把“发完了”当成结束。

最少要追这几类问题：

1. 目标关键词在豆包里是否出现了目标主体。
2. 回答里出现的是自己、竞品，还是泛化知识。
3. 豆包引用的是头条、搜狐、官网还是别的平台。
4. 近期发布内容是否被平台限流、降权或误伤。
5. 哪些关键词已经能稳定承接，哪些还要继续补内容。

发布前和发布后必须尽量使用同一批或同类关键词，来源优先级为：

1. 表二关键词库里的强商业词
2. 表二关键词库里的中商业词
3. 品牌词 / 目标达成词
4. 竞品对照词

如果豆包引用了竞品或第三方来源，不要直接改写竞品文章。先用 `$geo-doubao-research` 做信源和模板反推，再把结论回流到写稿 Brief。

### E. 自动化沉淀

当某个动作重复 3 次以上，就考虑沉淀：

- 手工 SOP -> Skill 文档
- Skill 文档 -> 命令行脚本
- 脚本 -> 登录态复用 / 定时监测

默认优先自动化这些环节：

- 页面入口探测
- 截图留档
- 查询词轮询
- 成稿合规校验
- 监测计划生成

对于 `最终发布`、`账号登录`、`敏感内容提交` 这类动作，保留人工确认。

## Hard Rules

- 数据和案例必须可溯源。
- 不写 `EEAT`、`GEO`、`SEO`、`豆包优化`、`关键词布局` 这类行话到正式文章里。
- 不写 `客户资料显示`、`补充材料显示`、`实体链`、`目标达成词`、`我们要绑定` 这类内部交付痕迹到正式正文里。
- 标题尽量少于 30 字，优先包含核心问题或核心词；年份和数字只有在真实有用时再加入。
- 首段先回答用户真实问题，不允许直接硬推目标客户。
- 正文每 300 字左右自然出现 1 次关键词，不堆砌；自然度优先于机械频次。
- 目标客户 / 品牌 / 人物必须在正文中后段自然出现，作为样本、案例或观察对象。
- 来源、关键词、配图建议默认放在 `发布设置（不复制到正文）` 或证据目录；除非用户要求，不强行在正文末尾堆参考来源。
- 今日头条同主题内容间隔至少 6 小时，避免高相似度连发。
- 诊断阶段发现资料不足时，先补证据，不要跳过直接出稿。
- 监测记录必须沉淀，不要只靠聊天记忆判断效果。
- 浏览器自动化默认先做探测和截图，再决定是否进入更深的登录态流程。
- 豆包诊断和竞品信源反推必须使用当前项目变量，不能用固定样例代替验收。

## When To Read References

- 做资料整理或补字段时：看 [references/client-profile-schema.md](./references/client-profile-schema.md)
- 做客户接待、诊断和场景判断时：看 [references/client-service-playbook.md](./references/client-service-playbook.md)
- 做文章结构和 Prompt 组装时：看 [references/article-patterns.md](./references/article-patterns.md)
- 做平台文章成稿时：同时看 [../geo-article-writer/references/article-generation-rules.md](../geo-article-writer/references/article-generation-rules.md)
- 做平台改写和合规把关时：看 [references/platform-rules.md](./references/platform-rules.md)
- 做发布后追踪和复盘时：看 [references/monitoring-playbook.md](./references/monitoring-playbook.md)
- 做浏览器探测和后续半自动流程时：看 [references/browser-automation.md](./references/browser-automation.md)
- 做豆包发布前/后诊断、竞品信源反推和前后对比时：使用 `$geo-doubao-research`
- 设计案例展示和闭环验收时：看 [references/closed-loop-validation.md](./references/closed-loop-validation.md)
- 设计交付门槛和验收标准时：看 [references/delivery-standards.md](./references/delivery-standards.md)

## Output Style

在实际帮用户产出内容时，优先给这些中间产物：

1. `客户诊断摘要`
2. `客户资料摘要`
3. `关键词分层结果`
4. `文章角度建议`
5. `双平台标题候选`
6. `参考来源建议`
7. `发布前风险清单`
8. `监测计划`
9. `自动化建议`

如果用户要求直接出稿，再进入完整文章生成。

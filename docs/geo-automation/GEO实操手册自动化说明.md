# GEO 实操手册自动化说明

这份自动化包按当前文件夹资料和 `GEO演讲稿_v11_口播对齐版.md` Part 4 整理，目标是把“公司家底 -> 批量挖词 -> 批量写稿 -> 平台改写 -> 监测复盘”落成可复用的 Skill 和表格。

## 已落成产物

| 产物 | 路径 | 用途 |
| --- | --- | --- |
| GEO 关键词挖掘 Skill | [`skills/geo-keyword-miner`](../../skills/geo-keyword-miner) | 从公司家底或客户档案生成中商业型 / 强商业型关键词 |
| GEO 文章写稿 Skill | [`skills/geo-article-writer`](../../skills/geo-article-writer) | 按关键词、证据和文章类型生成可溯源主稿 |
| GEO 平台改写 Skill | [`skills/geo-platform-adapter`](../../skills/geo-platform-adapter) | 把一篇主稿拆成头条、搜狐、知乎、36氪版本 |
| 豆包 GEO 研究 Skill | [`skills/geo-doubao-research`](../../skills/geo-doubao-research) | 发布前/后豆包诊断、前后对比、竞品信源反推 |
| 表格模板工作簿 | [`templates/geo-automation/GEO自动化流程表格模板.xlsx`](../../templates/geo-automation/GEO自动化流程表格模板.xlsx) | 公司家底、客户档案、关键词库、文章任务、监测追踪等表 |
| 资料文件索引 | [`docs/geo-automation/资料文件索引.md`](./资料文件索引.md) | 当前文件夹资料和自动化节点的对应关系 |

## 自动化主流程

| 阶段 | 输入 | 自动化动作 | 输出 | 人工必须把关 |
| --- | --- | --- | --- | --- |
| 1. 公司家底 | 客户资料、飞书文档、表格 | 提取品牌、业务、证据、竞品和资料缺口 | 客户档案表 | 品牌全称、证据真假、敏感行业 |
| 2. 批量挖词 | 客户档案表 | 按业务类型套公式，生成商业关键词 | 关键词库表 | 删除纯科普词、泛词、离谱词 |
| 3. 批量写稿 | 关键词、客户证据、行业数据 | 五类文章 Prompt 生成主稿 | 文章任务表和 Markdown 主稿 | 用户意图、自然夹带、去交付痕迹、合规风险 |
| 4. 平台改写 | 主稿 | 规则化拆成多平台版本 | 头条/搜狐/知乎/36氪版本 | 标题、联系方式、敏感行业规则 |
| 5. 豆包诊断与检测 | 发布链接、查询词、豆包回答 | 生成发布前诊断、发布后检测和前后对比 | 监测追踪表 / Markdown报告 | 判断是否补内容或换角度 |
| 6. 内部复盘 | 竞品来源、引用文章、搜索结果 | 反推信源、模板和行业模块更新点 | 竞品信源反推报告 | 只借鉴结构，不复制竞品表达 |

## 表格结构

工作簿包含 8 个 Sheet：

1. `使用说明`
2. `公司家底六格表`
3. `表一_客户档案`
4. `表二_关键词库`
5. `表三_文章任务`
6. `表四_监测追踪`
7. `自动化节点`
8. `平台规则`
9. `文件素材索引`

其中：

- `公司家底六格表` 对应演讲稿 P50。
- `表二_关键词库` 对应演讲稿 P51 和 Coze N2。
- `表三_文章任务` 对应演讲稿 P52、Coze N4-N6。
- `表四_监测追踪` 补上发布后的回查闭环。

## Skill 使用方式

### 关键词挖掘

```bash
python3 skills/geo-keyword-miner/scripts/generate_keyword_table.py \
  --profile /path/to/client_profile.json \
  --output /path/to/keywords.csv
```

### 写稿

打开 `$geo-article-writer`，把客户档案、关键词、证据和文章类型交给它。它会先生成 Brief，再进入主稿，不直接做平台发布版。

写稿时必须先读取 `skills/geo-article-writer/references/article-generation-rules.md`。正式平台正文要像真实今日头条 / 搜狐文章，不允许把 `客户资料显示`、`补充材料显示`、`实体链`、`GEO`、`关键词布局` 等内部流程写进正文。

### 平台改写

```bash
python3 skills/geo-platform-adapter/scripts/adapt_platform_versions.py \
  --input /path/to/article.md \
  --output-dir /path/to/platform-versions \
  --industry general \
  --keyword "目标关键词"
```

### 豆包诊断与复盘

```bash
python3 skills/geo-doubao-research/scripts/select_doubao_queries.py \
  --keywords /path/to/keywords.csv \
  --profile /path/to/client_profile.json \
  --output /path/to/doubao-query-batch.md
```

```bash
python3 skills/geo-doubao-research/scripts/build_doubao_research_report.py \
  --mode effect \
  --stage pre \
  --input /path/to/effect-log.md \
  --output /path/to/pre-diagnosis-report.md
```

## 当前判断

这套流程已经可以支撑“GEO 实操手册与方法论”的自动化雏形。它不是只写一篇文章，而是把资料、表格、Prompt、脚本、平台规则和监测字段接起来，后续可以继续接飞书多维表格、Coze 节点或浏览器监测。

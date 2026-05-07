# tools/

离线分析与维护工具。**不属于 skill 运行流程**，agent 不会主动调用。

## analyze_corpus.py — 公众号语料分析

从大批量微信文章 HTML zip 包中清洗、分类、出索引，用于挑范文候选。

### 用法

```bash
# 单 zip
uv run tools/analyze_corpus.py --zip path/to/articles.zip --out ./corpus-analysis

# 多 zip 一次跑
uv run tools/analyze_corpus.py \
  --zip "D:/BaiduNetdiskDownload/蜡笔进化论HTML.zip" \
  --zip "D:/BaiduNetdiskDownload/html(6).zip" \
  --out ./corpus-analysis
```

### 输出

```
corpus-analysis/
├── corpus_clean/            # 每篇一个 .txt（纯净正文，去秀米噪音）
└── corpus_index.csv         # 索引：标题/日期/字数/题材桶/首段预览/路径
```

### 挑范文工作流

1. 跑脚本生成 csv
2. Excel 打开 `corpus_index.csv`（utf-8-sig 编码，中文不乱码）
3. 按 `topic_bucket` + `word_count` 排序
4. 每个题材桶挑 2-3 篇代表作（通常字数适中、首段钩子强的优先）
5. 把挑出来的 `.txt` 复制到 `references/范文-<风格>-<标题简写>.md`，加批注

### 题材分桶规则

见脚本里的 `TOPIC_BUCKETS` 字典，是关键词匹配。如果你的语料题材跟默认桶不对应，
直接改字典即可（这是离线工具，不影响 skill 运行）。

# 使用示例

> 假设根目录有 `.env`，已配 `WECHAT_APP_ID` / `WECHAT_APP_SECRET` / `DASHSCOPE_API_KEY`。

每个示例顶部加这一行（让不支持 .env 的脚本也能拿到 secret）：
```bash
source <(grep -E '^WECHAT_' .env | sed 's/^/export /')
```

## 示例 0：基于参考文章改写（任务类型 C）

```bash
# 1. 提取原文
python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s/xxx" -o drafts/article.md

# 2. 改写 drafts/article.md（agent 自行完成）+ 三遍审校

# 3. Markdown → 内联 HTML
python3 scripts/markdown_to_wechat_doocs.py \
  --input drafts/article.md --output drafts/article.html --theme orange

# 4. 生成封面（五要素 prompt 参考 references/image-prompts.md）
python3 scripts/generate_cover.py --prompt "<五要素 prompt>" --output cover.jpg

# 5. 上传封面
python3 scripts/upload_material.py \
  --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
  --image_path cover.jpg
# → thumb_media_id=THUMB_XXX

# 6. 创建草稿
python3 scripts/create_draft.py \
  --title "【转载】原文标题" \
  --content "$(cat drafts/article.html)" \
  --thumb_media_id "THUMB_XXX"
```

## 示例 0.1：基于主题方向创作（任务类型 B，最常用）

**第 1 轮对话**——用户："写一篇关于 AI 提升工作效率的文章"

智能体（识别为 B → 不动笔，先选题）：
> 我先给你 3 个选题方向，你挑一个：
>
> **方向 1**：《下班还在加班的人，都没用对这 3 个 AI 工具》
> 角度：痛点切入 + 工具实测
> 大纲：现状痛点 / 工具 1 实测 / 工具 2 实测 / 工具 3 实测 / 选型建议
>
> **方向 2**：《我用 AI 把每天 3 小时杂活压到了 20 分钟》
> 角度：第一人称叙事
> ……
>
> **方向 3**：《2025 年还在手动做这 5 件事，就是在浪费命》
> 角度：清单体 + 时效性
> ……

**第 2 轮**——用户："方向 1"

智能体（按 `references/viral_titles_50.md` 给 3 个候选标题，用户挑完后才进入下面）：
```bash
# 1. web_fetch 三款工具最新资料
# 2. 创作初稿（必读 references/范文-意疏精选.md B 集 + 范文-卡兹克精选.md #1）
# 3. 三遍审校（references/三遍审校清单.md）
# 4. 调用 references/意疏-签名结尾.md 拼接结尾
# 5-7. 同示例 0 步骤 3-6
```

## 示例 1：纯提取，不发布

```bash
python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s/xxx" --json
# 返回 title / author / publishTime / cover / content / fullMarkdown
```

## 示例 2：发无封面图文（最简）

```bash
source <(grep -E '^WECHAT_' .env | sed 's/^/export /')

python3 scripts/markdown_to_wechat_doocs.py \
  --input drafts/article.md --output drafts/article.html --theme blue

python3 scripts/create_draft.py \
  --title "如何用 Python 处理数据" \
  --content "$(cat drafts/article.html)" \
  --author "意疏"
# → media_id=MEDIA_XXX

python3 scripts/publish_draft.py \
  --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
  --media_id "MEDIA_XXX"
```

## 示例 3：批量发布

```bash
source <(grep -E '^WECHAT_' .env | sed 's/^/export /')

for i in 1 2; do
  python3 scripts/markdown_to_wechat_doocs.py \
    --input "drafts/article-$i.md" --output "drafts/article-$i.html" --theme blue

  media_id=$(python3 scripts/create_draft.py \
    --title "文章 $i" \
    --content "$(cat drafts/article-$i.html)" | jq -r .media_id)

  python3 scripts/publish_draft.py \
    --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
    --media_id "$media_id"
done
```

## 可选参数速查

`generate_cover.py`：
- `--provider qwen|doubao`（默认 qwen）
- `--size 900*383 | 1664*928 | 1024*1024 | 720*1280 | 1280*720`（仅千问）
- `--qwen-model qwen-image-2.0 | qwen-image-2.0-pro`
- `--output cover.jpg`（不传只返回 URL）
- 默认压缩到 ≤ 800KB

`create_draft.py`：
- `--digest "摘要"` `--author "意疏"` `--show_cover_pic 1`
- 不传 `--thumb_media_id` = 无封面草稿

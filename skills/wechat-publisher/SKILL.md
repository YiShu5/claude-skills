---
name: wechat-publisher
description: 微信公众号文章的发布管道——封面生成、本地图片上传素材库、创建草稿、发布草稿、以及从 mp.weixin URL 提取原文。**触发场景**:用户说 "发到公众号草稿箱" / "推送到公众号" / "做张公众号封面" / "上传图片到微信" / "把这篇文章提取成 markdown" / "改写这篇 mp.weixin 链接(的提取部分)" / 任何提到「发布 / 草稿 / 封面 / 推送 / 提取微信文章」的请求。本 skill **不写文章**(交给 wechat-writer),**不做 markdown → html 排版**(交给 wechat-formatter)——它只处理图片生成、文件上传、微信 API 调用。
---

# wechat-publisher · 微信公众号发布管道

只负责跟微信 API 打交道的部分:**封面生成 / 图片上传 / 草稿创建 / 草稿发布 / 文章提取**。

## 常用工作流

### 工作流 1:发已写好排版好的稿子(最常见)

前提:你已经用 wechat-writer 写好 markdown,用 wechat-formatter 转成了 html。

```bash
# 0. 加载凭证
source <(grep -E '^WECHAT_' .env | sed 's/^/export /')

# 1. 生成封面图(五要素 prompt 见 references/image-prompts.md)
python3 scripts/generate_cover.py \
  --prompt "<五要素 prompt>" \
  --output cover.jpg

# 2. 上传封面到微信永久素材
python3 scripts/upload_material.py \
  --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
  --image_path cover.jpg
# 输出: thumb_media_id=THUMB_XXX

# 3. 创建草稿
python3 scripts/create_draft.py \
  --title "文章标题" \
  --content "$(cat drafts/article.html)" \
  --thumb_media_id "THUMB_XXX" \
  --author "意疏"

# 4. (可选)直接发布
python3 scripts/publish_draft.py \
  --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
  --media_id "MEDIA_XXX"
```

**默认到 step 3 就停——保留为草稿,让用户登录公众号后台预览再决定是否发布。**只有用户明确说"直接发"才执行 step 4。

### 工作流 2:从 mp.weixin URL 提取原文

```bash
python3 scripts/extract_to_markdown.py \
  "https://mp.weixin.qq.com/s/xxx" \
  -o drafts/extracted.md
```

输出为 Markdown,**交给 wechat-writer 改写**——本 skill 不负责改写,只负责提取。

### 工作流 3:一键 orchestrator(已有 markdown,跑完整管道)

```bash
python3 scripts/publish_article.py \
  --input article.md \
  --title "文章标题" \
  --author "意疏"
```

这个脚本会内部调用排版 + 封面 + 上传 + 草稿。**适合用户明确说"一条命令直接给我发草稿箱"时用**。

如果用户对中间产物(封面 / 配图 / 排版)有要求,**不要走 orchestrator**,改用工作流 1 分步执行。

## 封面图 prompt 必须用五要素结构

**禁止**写「科技风格插画」「为文章 XX 生成封面」这种空泛 prompt。详见 `references/image-prompts.md`。

五要素(中文逗号分隔,顺序固定):

1. **核心意象**:文章前 200 字提取 2-4 个**具象**名词(不要"效率""创新"这种抽象概念)
2. **情绪基调**:从 7 选 1——温暖治愈 / 专业冷静 / 紧张焦虑 / 轻松愉悦 / 怀旧沉思 / 励志昂扬 / 神秘高级
3. **画面风格**:按文章主题查 `references/image-prompts.md` 的 9 种风格映射表
4. **构图与镜头**(固定文本):`2.35:1 横向构图,主体居中偏左,右上角嵌入小字「意疏的AI口袋」,中部区域小字「<标题关键词 3-5 字>」(避开底部 15% 遮挡区)`
5. **负面提示**(固定文本):`画面主体不要出现任何文字、字母、汉字,水印、logo、签名`

## 文中配图(发布模式才出,预览模式跳过)

如果用户明确要"发布模式 + 配图",生成 **3 张**配图,按故事弧线:

| 序号 | 定位 | 元素 |
| --- | --- | --- |
| 1 | 痛点 | 文章开头的困境/焦虑具象化 |
| 2 | 转折 | 解决方案出现的关键时刻/工具 |
| 3 | 升华 | 文章结尾的理想状态/成果 |

**3 张 prompt 必须互不相同,禁止复用模板。**

## 凭证管理

凭证只写进 `.env`(已 gitignore)。

| 变量 | 必填 | 来源 |
| --- | --- | --- |
| `WECHAT_APP_ID` | ✅ | mp.weixin.qq.com → 开发 → 基本配置 |
| `WECHAT_APP_SECRET` | ✅ | 同上 |
| `DASHSCOPE_API_KEY` | 二选一 | 千问(推荐),dashscope.console.aliyun.com |
| `DOUBAO_API_KEY` | 二选一 | 豆包,console.volc.com/iam/keylist |
| `IMAGE_PROVIDER` | 可选 | `qwen`(默认) / `doubao` |

### 脚本对 `.env` 的支持

| 脚本 | 支持 `.env` | 不支持 → CLI 必传 |
| --- | --- | --- |
| `generate_cover.py` | ✅ 完全免参 | — |
| `create_draft.py` | ✅ 回退 | — |
| `publish_article.py` | ✅ 全部 | — |
| `extract_to_markdown.py` | ✅ 不需要凭证 | — |
| `upload_material.py` | ❌ | `--app_id` `--app_secret` |
| `publish_draft.py` | ❌ | `--app_id` `--app_secret` |

**Agent 实践**:调 `upload_material.py` / `publish_draft.py` 前,**先 `source <(grep -E '^WECHAT_' .env | sed 's/^/export /')`** 把凭证拼成环境变量,不要让用户重复输。

## 配图本地路径处理(常见坑)

如果 Markdown 里有 `![](./images/foo.png)` 这种本地图片路径:

1. 微信 HTML 不能直接引用本地路径——需要先 `upload_material.py` 把图片上传到微信永久素材
2. 拿到返回的 `url`,**替换 Markdown 里的本地路径**
3. **再**送给 wechat-formatter 转 HTML

否则 HTML 粘到微信编辑器图片会裂。

## 不做的事

- **不写文章** → wechat-writer
- **不做 Markdown → HTML 排版** → wechat-formatter
- **不改稿 / 不审校** → wechat-writer

## 子文档导航

| 文档 | 何时读 |
| --- | --- |
| `references/image-prompts.md` | 写封面 / 配图 prompt 时 |
| `references/wechat-api.md` | 微信 API 返回错误码,看不懂时 |
| `references/examples.md` | 想看完整 bash 例子时 |

---
name: 意疏的AI口袋
description: 微信公众号文章的端到端创作发布工具链。当用户要求"写一篇关于 X 的公众号文章""改写这篇 mp.weixin 链接""把这篇稿子发到草稿箱""审校 / 降 AI 味"时触发。覆盖选题、写作、三遍审校、Markdown→微信 HTML、封面与配图生成、上传素材、创建/发布草稿。不处理朋友圈、视频号、小程序内容。
---

# 意疏的AI口袋 · 公众号工具链

品牌主张：用 AI 让普通人变强，用方法把复杂的事变简单。

## 第一步：识别任务类型（必做，不要默认走完整流程）

| 类型 | 用户输入 | 走哪条路 |
| --- | --- | --- |
| A | 完整 brief（标题+受众+要点） | 写作 → 审校 → 转 HTML → 封面 → 草稿 |
| B | **只给主题方向** | **先选题讨论（3-4 方向给用户选）** → 标题打磨（3 候选） → 同 A |
| C | mp.weixin 文章 URL | 提取 → 改写 → 同 A 后半段 |
| D | 完整稿要审校 | 只走三遍审校，不创作不出图 |
| E | 问问题 / 聊功能 | 直接答，不进入工作流 |

类型 B 的两阶段顺序不可压缩：**选题方向 → 候选标题 → 写正文**。第一轮就给标题候选 = 错。

## 写作核心约束

1. **风格参考必读**：写作前必须**至少读 1 份范文**，按场景选：
   - 写**保姆级教程 / 工具上手** → `references/范文-意疏精选.md` A 集
   - 写**AI 工具评测 / 新模型实测** → `references/范文-卡兹克精选.md` #1 #3 + 意疏 B 集
   - 写**行业评论 / 现象批判** → `references/范文-卡兹克精选.md` #2
   - 写**个人故事 / 情感叙事** → `references/范文-卡兹克精选.md` #4
   - 写**调查揭秘** → `references/范文-卡兹克精选.md` #5
   - 写**自家产品发布** → `references/范文-卡兹克精选.md` #6
   仅靠 `HUMANIZE_GUIDE.md` 的"避免清单"不够 —— **必须有正面范本**。
2. **不编造**：搜不到的数据 / 案例直接删，或写"暂未找到公开数据"。涉及 2024-2025 新产品 / 政策 / 数字 → 必须 web_fetch 核实。
3. **字数参考**（非硬阈值）：常规 1200-1500，技术评测 1500-2000。服从内容，不要凑数。
4. **三遍审校**（A/B/C 强制，详见 `references/三遍审校清单.md`）：
   - 一审 内容：事实 / 逻辑 / 结构
   - 二审 风格：删 AI 套话 + 加 ≥10 处个人态度
   - 三审 细节：句长 / 全角标点 / 中英文空格
   未通过审校 → 不出图 → 不建草稿。
5. **签名结尾**：写完正文后**直接调用** `references/意疏-签名结尾.md` 的标准版，不要让模型自由发挥结尾。

## 发布核心约束

6. **必须把 Markdown 转内联 HTML**：微信编辑器不识别 `<style>`。
   `create_draft.py --content` 只接受 `markdown_to_wechat_doocs.py` 的输出，**绝不直传 Markdown**。
7. **主题选择**：按 `THEME_GUIDE.md` 的内容→主题映射；用户在 `.env` 设了 `MARKDOWN_THEME` 优先用。
8. **图片必须按五要素结构**（详见 `references/image-prompts.md`）：核心意象 / 情绪基调 / 画面风格 / 构图 / 负面提示。封面右上角嵌入「意疏的AI口袋」。配图 3 张按"痛点 → 转折 → 升华"故事弧线，prompt 互不相同。**禁止**「XX 风格插画」这种两要素空泛 prompt。

## 凭证管理

`.env` 配置（模板见 `CONFIG.md`）。脚本支持情况：

| 脚本 | 支持 .env | 不支持 → 必须 CLI 显式传 |
| --- | --- | --- |
| `generate_cover.py` | ✅ 完全免参 | — |
| `create_draft.py` | ✅ 回退 | — |
| `markdown_to_wechat_doocs.py` | ✅ MARKDOWN_THEME | — |
| `upload_material.py` | ❌ | `--app_id` `--app_secret` |
| `publish_draft.py` | ❌ | `--app_id` `--app_secret` |

Agent 实践：调 `upload_material.py` / `publish_draft.py` 前自己从 `.env` 读出 secret 拼进 CLI，别让用户重复输。

## 标准发布管道（A/B/C 共用尾段）

```
1. 写作 → 三遍审校（references/三遍审校清单.md）
2. markdown_to_wechat_doocs.py --theme <按 THEME_GUIDE 选>
3. generate_cover.py --prompt "<五要素，见 references/image-prompts.md>"
4. upload_material.py（拿 thumb_media_id）
5. create_draft.py --content "$(cat *.html)" --thumb_media_id ...
6. （可选）publish_draft.py --media_id ...
```

发布前默认**先输出文章预览**给用户确认，除非用户明确说"直接发"。
仅预览模式：不出配图，只给文字。
发布模式：必须出 3 张配图 + 1 张封面。

## 关键脚本

核心管道（按调用顺序）：
- `markdown_to_wechat_doocs.py`（Markdown → 内联 HTML，唯一转换器）
- `generate_cover.py`（封面生成，五要素 prompt）
- `upload_material.py`（上传素材拿 thumb_media_id）
- `create_draft.py`（建草稿）
- `publish_draft.py`（发布）
- `extract_to_markdown.py`（从 mp.weixin URL 提取原文，任务类型 C 用）
- `publish_article.py`（一键 orchestrator：md → html → 封面 → 上传 → 草稿）

⚠️ 遗留脚本（默认绕开，不要主动调用）：
- `create_article.py`（默认 doubao + 跳审校 + 跳 HTML 转换，仅在用户明确说"快速一键"时用）
- `compress_image.py` / `extract_simple.py` / `extract_wechat.py`（已被上面主脚本覆盖）

## 子文档导航（按需读，不要默认全读）

| 何时读 | 文档 |
| --- | --- |
| 任务类型 B 写正文前 | `references/范文-意疏精选.md`（你自己的 voice）+ `references/范文-卡兹克精选.md`（爆款结构）按场景 2 选 1 必读 |
| 写技术 / 工具 / 评测类文章 | `CHICKEN_SOUP_STYLE.md` |
| 二审"删 AI 套话"卡壳时 | `HUMANIZE_GUIDE.md` 替换词表 |
| 选 markdown 主题时 | `THEME_GUIDE.md` |
| 起标题阶段 2 | `references/viral_titles_50.md` |
| 三遍审校执行时 | `references/三遍审校清单.md` |
| 写图片 prompt 时 | `references/image-prompts.md`（五要素 + 9 种风格完整模板） |
| 文章结尾签名段 | `references/意疏-签名结尾.md` |
| 微信 API 报错时 | `references/wechat-api.md` |
| 各类发布 bash 示例 | `references/examples.md` |

## 离线工具（不在 skill 运行流程内）

`tools/analyze_corpus.py` —— 从微信文章 HTML zip 包批量清洗、分类、出索引，用于挑范文候选。详见 `tools/README.md`。

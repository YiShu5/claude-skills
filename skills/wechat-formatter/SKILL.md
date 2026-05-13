---
name: wechat-formatter
description: 把 Markdown 文稿转换成微信公众号可用的内联样式 HTML。**触发场景**:用户说 "把 markdown 转成公众号能用的 HTML" / "排版一下这篇文章" / "套个主题" / "微信编辑器不识别我的样式" / 任何提到「公众号排版 / 微信 HTML / md 转 html / doocs 主题」的请求。微信编辑器不识别 `<style>` 标签,必须把所有 CSS 内联到每个 HTML 元素的 style 属性里——本 skill 用 doocs/md 主题完成这件事。本 skill 只负责格式转换;写作交给 wechat-writer,发布交给 wechat-publisher。
---

# wechat-formatter · Markdown → 微信 HTML

只解决一件事:**把 Markdown 转成微信编辑器粘贴后样式不丢的 HTML**。

## 核心问题

微信公众号编辑器**不识别** `<style>` 标签和 CSS class。所以普通的 `markdown → html` 转换器输出的 HTML 粘到微信里会变成裸文本,所有样式全丢。

唯一可靠方案:**所有 CSS 都内联到元素的 `style="..."` 属性里**。doocs/md 是这件事的开源标准,本 skill 直接调用它。

## 使用方法

```bash
python3 scripts/markdown_to_wechat_doocs.py \
  --input drafts/article.md \
  --output drafts/article.html \
  --theme <主题名>
```

输出的 HTML 可以直接复制粘贴到微信公众号编辑器,样式全部保留。

## 主题选择

8 个主题,按文章**内容氛围**选(不只看标题关键词):

| 文章基调 | 推荐主题 | 适用 |
| --- | --- | --- |
| 温暖、励志、有人情味 | `orange` | 个人成长 / 励志 / 鸡汤 / 故事 |
| 专业、理性、技术感 | `blue` | 技术评测 / 工具教程 / 商业分析 |
| 清新、自然、放松 | `green` | 健康养生 / 户外 / 环保 |
| 文艺、清爽、小清新 | `cyan` | 文艺随笔 / 旅行 / 生活美学 |
| 优雅、高端、品牌 | `purple` | 品牌故事 / 艺术文化 / 设计 |
| 简约、高级、极简 | `black` | 摄影 / 极简主题 / 严肃话题 |
| 热情、节日、醒目 | `red` | 节日 / 重要通知 / 活动 |
| 甜美、浪漫、少女 | `pink` | 情感 / 美妆 / 少女向 |

**选择原则**:读完 Markdown 后,问自己"这篇要给读者什么情绪",再选主题。**不要靠标题关键词匹配**(比如标题里没"励志"也可能是励志文)。

**如果用户已在 `.env` 设了 `MARKDOWN_THEME`**:除非用户明确说"换个主题",否则用 `.env` 里的。

## 输出验收

转出来的 HTML 必须:
- [ ] 不包含 `<style>` 标签(所有样式必须内联)
- [ ] 不包含 CSS class(微信不解析)
- [ ] 图片如果是本地路径 → **必须先用 wechat-publisher 的 upload_material.py 换成微信 URL**,否则发布后图片裂掉

## 不做的事

- **不发布到草稿箱** → 用 wechat-publisher
- **不写文章 / 不改稿** → 用 wechat-writer
- **不生成封面图** → 用 wechat-publisher 的 generate_cover.py
- **不上传本地图片到微信 CDN** → 用 wechat-publisher 的 upload_material.py(如果 Markdown 里有 `![](./local/img.png)`,先告诉用户调用 publisher 上传换链接,再回来排版)

## 配置

`.env` 文件支持的变量:

```bash
MARKDOWN_THEME=        # orange / blue / green / purple / red / cyan / black / pink
                       # 留空则让 agent 按内容判断
```

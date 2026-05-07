# 意疏的AI口袋 · 微信公众号文章管理工具

## 📝 简介

意疏的AI口袋，微信公众号文章创作发布工具链。
用 AI 让普通人变强，用方法把复杂的事变简单，用行动把人生带到更高的位置。

支持文章创作、提取、转换、排版和发布的全流程自动化。

## ✨ 核心特性

### 🎨 智能排版
- 使用 doocs/md 排版引擎
- 根据文章内容自动选择主题（8种主题可选）
- 支持自定义样式和配色

### 🖼️ 智能配图
- 自动生成文章封面和配图
- 使用千问 AI 生成高质量图片（默认，可切换豆包）
- 自动生成横屏图片（2.35:1 比例，符合微信封面标准）
- 上传到公众号永久素材

### 📄 文章格式
- 正文不显示标题（更简洁）
- 自动插入3张配图（位置合理）
- 支持 Markdown 格式
- 自动转换为公众号 HTML

### 🚀 一键发布
- 自动创作文章内容
- 自动生成封面和配图
- 自动上传到公众号草稿箱
- 支持指定作者和摘要

---

## 📦 安装

### 前置要求

- Python 3.7+
- Node.js 14+（可选，用于文章提取）
- OpenClaw 环境

### 快速安装

```bash
# 1. 复制技能到 OpenClaw 技能目录
cp -r wechat-article-publisher ~/.openclaw/skills/

# 2. 配置凭证
cd ~/.openclaw/skills/wechat-article-publisher
cp .env.example .env
nano .env  # 填写你的凭证

# 3. 测试配置
cd scripts
python3 config.py
```

详细安装步骤请查看 [INSTALL.md](INSTALL.md)

---

## 🔑 配置

### 必需配置

在 `.env` 文件中填写以下信息：

```bash
# 微信公众号凭证
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret

# 千问 API Key（默认，对 watermark=False 更稳定）
DASHSCOPE_API_KEY=你的千问APIKey

# 豆包 API Key（可选）
DOUBAO_API_KEY=你的豆包APIKey
```

### 可选配置

```bash
# 文章格式
ARTICLE_SHOW_TITLE=false          # 正文不显示标题
ARTICLE_IMAGE_COUNT=3             # 插入3张配图
IMAGE_ORIENTATION=horizontal      # 横屏图片
IMAGE_PROMPT_SUFFIX=，2.35:1横屏构图  # 图片生成提示词后缀（符合微信封面标准）
```

---

## 🎯 使用方法

### 1. 创作并发布文章

```
对 Agent 说："写一篇关于【主题】的文章并发布到公众号"
```

Agent 会自动：
1. 创作文章内容
2. 生成3张横屏配图
3. 生成横屏封面图
4. 上传到公众号草稿箱

### 2. 提取文章

```
对 Agent 说："提取这篇文章：https://mp.weixin.qq.com/s/xxx"
```

Agent 会提取文章并转换为 Markdown 格式。

### 3. 改写并发布

```
对 Agent 说："改写这篇文章并发布：https://mp.weixin.qq.com/s/xxx"
```

Agent 会提取、改写并发布文章。

---

## 🎨 主题选择

工具支持8种主题，会根据文章内容自动选择：

| 主题 | 适用场景 | 色调 |
|------|---------|------|
| orange | 鸡汤励志、女性成长 | 橙色、温暖 |
| blue | 科技资讯、职场干货 | 蓝色、专业 |
| green | 健康养生、环保生活 | 绿色、清新 |
| pink | 情感故事、浪漫内容 | 粉色、甜美 |
| purple | 品牌故事、高端内容 | 紫色、优雅 |
| cyan | 旅行游记、文艺随笔 | 青色、清爽 |
| red | 节日祝福、活动宣传 | 红色、热情 |
| black | 设计作品、极简生活 | 黑色、高级 |

详见 [THEME_GUIDE.md](THEME_GUIDE.md)

---

## 📚 文档

- [安装指南](INSTALL.md) - 详细的安装步骤
- [配置说明](CONFIG.md) - 完整的配置说明
- [主题选择指南](THEME_GUIDE.md) - 主题选择规则
- [技能说明](SKILL.md) - 技能使用说明

---

## 🔧 工具脚本

> 假设根目录有 `.env`（含 `WECHAT_APP_ID` / `WECHAT_APP_SECRET` / `DASHSCOPE_API_KEY` 或 `DOUBAO_API_KEY`）。
> 不支持 `.env` 的脚本（`upload_material.py` / `publish_draft.py`）需要先把 secret 导成环境变量：
>
> ```bash
> source <(grep -E '^WECHAT_' .env | sed 's/^/export /')
> ```

### 生成封面图片（支持 .env，免参）
```bash
python3 scripts/generate_cover.py --prompt "<五要素 prompt，见 references/image-prompts.md>" --output cover.jpg
```

### 上传图片到公众号素材（必须显式传 secret）
```bash
python3 scripts/upload_material.py \
  --app_id "$WECHAT_APP_ID" \
  --app_secret "$WECHAT_APP_SECRET" \
  --image_path cover.jpg
# → 输出 thumb_media_id
```

### Markdown → 内联样式 HTML
```bash
python3 scripts/markdown_to_wechat_doocs.py \
  --input article.md \
  --output article.html \
  --theme orange    # 主题按 THEME_GUIDE.md 选
```

### 创建草稿（支持 .env，可省略 app_id/secret）
```bash
python3 scripts/create_draft.py \
  --title "文章标题" \
  --content "$(cat article.html)" \
  --thumb_media_id "THUMB_XXX" \
  --author "意疏" \
  --digest "摘要"
# → 输出 media_id
```

### 发布草稿（必须显式传 secret）
```bash
python3 scripts/publish_draft.py \
  --app_id "$WECHAT_APP_ID" \
  --app_secret "$WECHAT_APP_SECRET" \
  --media_id "MEDIA_XXX"
```

更多端到端示例参见 [`references/examples.md`](references/examples.md)。

---

## 🎯 功能特性

### ✅ 已实现

- [x] 文章创作（AI 技术/评测风格）
- [x] 文章提取（从公众号链接）
- [x] Markdown 转 HTML（doocs/md 排版）
- [x] 主题自动选择（8种主题）
- [x] 图片生成（千问 AI，默认）
- [x] 横屏图片生成（2.35:1，符合微信封面标准）
- [x] 图片上传到公众号
- [x] 创建草稿
- [x] 发布文章
- [x] 正文不显示标题
- [x] 自动插入3张配图
- [x] 配置自动读取

### 🚧 计划中

- [ ] 一键发布工具（整合所有步骤）
- [ ] 更多排版主题
- [x] 支持千问图像生成（默认）
- [ ] 文章数据分析
- [ ] 定时发布

---

## 🔒 安全提示

1. **不要分享 `.env` 文件** - 包含你的私密凭证
2. **使用 `.env.example` 分享** - 这是配置模板
3. **定期更换密钥** - 建议定期更换 AppSecret

---

## 🆘 常见问题

### Q: 如何获取公众号凭证？
A: 登录 https://mp.weixin.qq.com → 开发 → 基本配置

### Q: 如何获取千问 API Key？
A: 访问 https://dashscope.console.aliyun.com/（推荐，watermark=False 更稳定）

### Q: 如何获取豆包 API Key？
A: 访问 https://console.volc.com/iam/keylist（需开通图像生成服务权限）

### Q: 图片生成失败？
A: 检查 API Key 是否正确；千问默认用 `DASHSCOPE_API_KEY`，切换到豆包用 `IMAGE_PROVIDER=doubao`

### Q: 如何更换主题？
A: 主题会根据文章内容自动选择，无需手动设置

---

## 📞 获取帮助

- **文档**: 查看 `CONFIG.md`、`THEME_GUIDE.md`、`SKILL.md`
- **Issues**: GitHub 提交 Issue 或联系作者

---

用 AI 让普通人变强。
用方法把复杂的事变简单。
用行动把人生带到更高的位置。

—— 意疏的AI口袋

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [doocs/md](https://github.com/doocs/md) - 优秀的微信排版工具
- [豆包](https://www.volcengine.com/) - 图像生成服务
- [OpenClaw](https://openclaw.ai) - AI Agent 平台

---

## 📊 版本历史

### v1.0.0 (2026-03-05)

- ✅ 初始版本发布
- ✅ 支持文章创作、提取、转换、发布
- ✅ 支持8种主题自动选择
- ✅ 支持横屏图片生成
- ✅ 支持配置自动读取

---

**祝你使用愉快！如果觉得有用，请给个 Star ⭐️**

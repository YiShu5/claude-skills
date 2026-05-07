# 微信公众号文章创作配置说明

## 📋 配置总结

### 1. 公众号凭证
- **AppID**: `wx6299120c344dc04f`
- **AppSecret**: `7006aac58bb666da94df300f3a1aa999`

### 2. 图片生成 API
- **豆包 API Key**: `e2bde60f-15b7-4b3b-a04b-ac953334818f`
- **默认提供商**: doubao（豆包）

### 3. 文章排版
- **排版工具**: doocs（doocs/md 排版引擎）
- **主题**: 根据文章内容动态选择（不固定）
  - 可用主题：orange, blue, green, purple, red, cyan, black, pink
  - 选择原则：根据文章类型、情绪、目标受众
  - 详见：`THEME_GUIDE.md`
- **参考**: https://github.com/doocs/md

### 4. 文章格式规范

#### 4.1 字数要求
- ✅ **文章字数**: 1200-1500字（默认）
- 确保内容充实，有足够的信息量
- 避免过于简短或冗长

#### 4.2 标题显示
- ✅ **文章正文不显示标题**
- 标题仅在草稿列表中显示
- 文章直接从引言/正文开始

#### 4.3 配图规范

**配图生成规则**：
- **仅生成文章**（预览模式）：不生成文中配图，只输出文字内容
- **发布到公众号**（发布模式）：必须生成文中配图，默认 3 张

**配图详细规范**：
- ✅ **配图数量**: 3张（发布模式）
- ✅ **配图位置**: 在文章的合理位置插入（通常在每个主要段落结尾）
- ✅ **图片方向**: 横屏（16:9 比例）
  - 封面图：横屏
  - 文章内配图：横屏
- ✅ **图片来源**: 上传到公众号永久素材（使用 `http://mmbiz.qpic.cn/...` URL）
- ✅ **图片压缩**: 自动智能压缩
  - 封面图：目标 800KB（质量 85-95）
  - 配图：目标 600KB（质量 85-95）
  - 最低质量：75（保证清晰度）
  - 压缩率：通常 40-60%

#### 4.4 图片生成提示词
所有图片生成提示词都需要添加后缀：`，16:9横屏构图`

示例：
```
女性职场独立插画，展现女性在工作中自信专业的形象，温暖的色调，现代简约风格，16:9横屏构图
```

---

## 🎨 文章创作流程

### 标准流程（鸡汤文章风格）

1. **创作文章内容**（Markdown 格式）
   - 开篇：名人名言 + 核心观点
   - 正文：3个分论点，每个分论点包含正反案例
   - 结尾：名人名言 + 总结升华
   - **注意**：正文中不包含标题（不使用 `# 标题` 格式）

2. **插入配图占位符**
   - 在每个主要段落结尾插入 `{{IMAGE_1}}`、`{{IMAGE_2}}`、`{{IMAGE_3}}`
   - 通常在3个分论点的结尾各插入1张

3. **生成配图**（3张）
   - 使用豆包 API 生成横屏图片
   - 提示词包含：`16:9横屏构图`
   - 下载图片到本地

4. **上传配图到公众号**
   - 使用 `upload_material.py` 上传图片
   - 获取公众号图片 URL（`http://mmbiz.qpic.cn/...`）

5. **替换配图占位符**
   - 将 `{{IMAGE_X}}` 替换为 `![](图片URL)`

6. **转换为 HTML**
   - 使用 `markdown_to_wechat_doocs.py` 转换
   - 主题：orange（橙心主题）

7. **生成封面图**
   - 使用豆包 API 生成横屏封面图
   - 提示词包含：`16:9横屏构图`
   - 上传到公众号获取 `thumb_media_id`

8. **创建草稿**
   - 使用 `create_draft.py` 创建草稿
   - 包含：标题、内容、封面、作者、摘要

---

## 🔧 工具使用

### 1. 生成图片（自动压缩）
```bash
# 生成封面并自动压缩到 800KB
python3 scripts/generate_cover.py --prompt "描述，16:9横屏构图" --output cover.jpg

# 生成配图并压缩到 600KB
python3 scripts/generate_cover.py --prompt "描述，16:9横屏构图" --output image.jpg --max-size 600

# 不压缩（不推荐）
python3 scripts/generate_cover.py --prompt "描述" --output image.jpg --compress false
```

### 2. 手动压缩图片
```bash
# 压缩封面图到 800KB
python3 scripts/compress_image.py --input cover.jpg --output cover_compressed.jpg --max-size 800

# 压缩配图到 600KB
python3 scripts/compress_image.py --input image.jpg --output image_compressed.jpg --max-size 600

# 自定义质量范围
python3 scripts/compress_image.py --input image.jpg --output compressed.jpg --max-size 800 --min-quality 80
```

### 3. 上传图片到公众号
```bash
python3 scripts/upload_material.py --image_path image.jpg
```
（自动读取配置，无需指定 app_id 和 app_secret）

### 3. Markdown 转 HTML
```bash
python3 scripts/markdown_to_wechat_doocs.py \
  --input article.md \
  --output article.html \
  --theme orange  # 根据文章内容选择合适的主题
```

**主题选择指南**：
- 鸡汤励志 → orange（温暖有活力）
- 职场干货 → blue（专业理性）
- 健康养生 → green（清新自然）
- 科技资讯 → blue/cyan（专业或清爽）
- 情感故事 → pink/purple（浪漫或优雅）
- 品牌故事 → purple/black（高端优雅）

详见：`THEME_GUIDE.md`

### 4. 创建草稿
```bash
python3 scripts/create_draft.py \
  --title "文章标题" \
  --content "$(cat article.html)" \
  --thumb_media_id "封面ID" \
  --author "作者名" \
  --digest "摘要"
```
（自动读取配置，无需指定 app_id 和 app_secret）

---

## 📝 鸡汤文章风格规范

### 结构
```
开篇（名人名言 + 核心观点）
    ↓
01 第一个分论点
   - 反面案例（具体细节）
   - 正面案例（具体细节）
   - [配图1：横屏]
    ↓
02 第二个分论点
   - 反面案例（具体细节）
   - 正面案例（具体细节）
   - [配图2：横屏]
    ↓
03 第三个分论点
   - 反面案例（具体细节）
   - 正面案例（具体细节）
   - [配图3：横屏]
    ↓
结尾（名人名言 + 总结升华）
```

### 要点
- ✅ 开篇和结尾有名人名言
- ✅ 3个分论点，每个分论点有正反案例
- ✅ 案例有具体细节（对话、场景、结果）
- ✅ 每节有金句总结
- ✅ 语言简洁有力（短句为主）
- ✅ 段落短小精悍（每段2-4句）
- ✅ 正文不显示标题
- ✅ 插入3张横屏配图

---

## 🎯 配置文件位置

- **主配置**: `/home/admin/.openclaw/skills/wechat-article-publisher/.env`
- **配置说明**: `/home/admin/.openclaw/skills/wechat-article-publisher/CONFIG.md`（本文件）
- **技能说明**: `/home/admin/.openclaw/skills/wechat-article-publisher/SKILL.md`

---

## ✅ 检查清单

创作文章前，确认以下配置：

- [ ] 公众号 AppID 和 AppSecret 已配置
- [ ] 豆包 API Key 已配置
- [ ] 排版工具设置为 doocs
- [ ] 主题设置为 orange
- [ ] 文章正文不显示标题
- [ ] 配图数量为 3 张
- [ ] 所有图片使用横屏格式（16:9）
- [ ] 图片生成提示词包含"16:9横屏构图"
- [ ] 图片上传到公众号永久素材

---

## 🚀 快速开始

### 创作并发布一篇文章

```bash
# 1. 创作文章（Markdown 格式，正文不含标题）
# 2. 插入配图占位符 {{IMAGE_1}}, {{IMAGE_2}}, {{IMAGE_3}}
# 3. 生成3张横屏配图
# 4. 上传配图并替换占位符
# 5. 转换为 HTML（doocs/md 橙心主题）
# 6. 生成横屏封面图
# 7. 创建草稿
```

或使用一键发布工具（待开发）：
```bash
python3 scripts/publish_article.py \
  --input article.md \
  --title "文章标题" \
  --author "作者名"
```

---

## 📎 footer.md 文章结尾配置

### 配置文件位置
- **文件路径**: `~/.openclaw/skills/wechat-article-publisher/footer.md`
- **说明**: 文章自动拼接的结尾内容

### 写入规则（重要！）

**将图片链接转换为 Markdown 图片格式：**

| 原始格式 | 正确格式 |
|---------|---------|
| `https://mmbiz.qpic.cn/...xxx.gif` | `![点赞](https://mmbiz.qpic.cn/...xxx.gif)` |
| `https://mmbiz.qpic.cn/...xxx.png` | `![星球](https://mmbiz.qpic.cn/...xxx.png)` |

**示例：**
```
原文：
好了，是不是很简单...
https://mmbiz.qpic.cn/mmbiz_gif/xxx.gif

关住后+我w~x（Wubb_001)...
https://mmbiz.qpic.cn/mmbiz_png/xxx.png

写入 footer.md 时：
好了，是不是很简单...
![点赞](https://mmbiz.qpic.cn/mmbiz_gif/xxx.gif)

关住后+我w~x（Wubb_001)...
![星球](https://mmbiz.qpic.cn/mmbiz_png/xxx.png)
```

**原因**：Markdown 图片格式 `![alt](url)` 会被转换器正确识别并添加 HTML 样式标签，直接放链接会被当作普通文本。

---

**配置已完成，可以开始创作公众号文章！** 🎊

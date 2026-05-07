---
name: 意疏AI口袋
description: |
  【强制规则 · 必须全部读完再动笔】

  意疏AI口袋 · 微信公众号文章创作发布工具链。
  品牌理念：用 AI 让普通人变强，用方法把复杂的事变简单，用行动把人生带到更高的位置。
  以下 8 条为最高优先级约束，覆盖执行流程、写作字数、图片生成三块。
  读完本 SKILL.md 后按顺序执行，不要跳过任何步骤。

  ── 约束 1：必须先识别任务类型
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  用户输入后，先看「类型」再决定走哪条路径，不要默认走完整流程：

    A   给完整 brief（含标题）  → 搜索 → 三遍审校 → HTML转换 → 封面 → 草稿
    B   只给主题/方向           → 【先选题讨论】→ 用户选方向后 → 标题打磨 → 三遍审校 → HTML转换 → 封面 → 草稿
    C   给参考文章 URL          → 提取 → 改写 → 三遍审校 → HTML转换 → 封面 → 草稿
    D   给完整稿子要审校        → 直接三遍审校（跳过创作）
    E   纯问问题/聊功能        → 直接回答，不进入创作

  ── 约束 2：选题讨论（任务类型 B 强制）
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  用户只说「写一篇关于 XX 的文章」→ 先出 3-4 个选题方向让用户挑，
  每个方向含「示意标题 + 角度 + 大纲」。用户挑完后再做标题打磨。
  【禁止直接写】。

  ── 约束 3：三遍审校（强制，不得跳过）
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  完整流程：A / B / C 写完初稿后，必须按 references/三遍审校清单.md 走完三遍：

    第一遍：事实 / 逻辑 / 结构（绝不编造数据）
    第二遍：删 AI 套话 + 加 10+ 处个人态度 + 替换书面词
    第三遍：句长 ≤ 30 字 / 全角标点「」/ 中英文空格 / 段长 3-5 行

  未通过审校 → 不生成封面 → 不创建草稿。

  ── 约束 4：Markdown 必须转内联 HTML
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  微信公众号编辑器不识别 <style> 标签。
  create_draft.py 的 --content 必须传 markdown_to_wechat_doocs.py 的输出，
  【不要直接传原始 Markdown】。

  ── 约束 5：字数
  ━━━━━━━━━━━━━━━━━━━
  默认 1200-1500 字；AI 技术/评测/工具类文章 1500-2000 字（参考 CHICKEN_SOUP_STYLE.md）。

  ── 约束 6：图片生成（封面 + 配图）
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  所有图片 prompt 必须用五要素结构 + 意疏AI口袋品牌标识（右上角嵌入小字「意疏AI口袋」 + 中部区域小字「标题关键词」），
  禁止「XX 风格插画」等空泛描述。可选 9 种视觉风格（见附录）。
  默认引擎：qwen（千问）；封面尺寸默认 900*383（2.35:1），自动压缩到 800KB。

  ── 约束 7：五要素 + 意疏AI口袋品牌结构
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  封面 prompt = <核心意象>，<情绪基调>，
  <画面风格（从 9 种风格选 1）>，2.35:1 横向构图，主体居中偏左，
  <右上角留白区域>，嵌入小字「意疏AI口袋」（白色或浅金色，字体干净，不要挡住主体），
  <标题关键词 3-5 个>，用小字浮于画面中部（颜色浅、不喧宾夺主，避开底部 15% 遮挡区），
  画面主体区域不要出现任何文字、字母、汉字、水印、logo、签名

  ── 约束 8：凭证管理
  ━━━━━━━━━━━━━━━━━━━
  推荐在 .env 配置（README 有模板）。
  generate_cover.py 完全免参（读 .env）；create_draft.py 支持 .env 回退；
  upload_material.py / publish_draft.py 不支持 .env，需显式传 app_id / app_secret。
---

# 微信公众号文章管理

## 任务目标
- 本 Skill 用于：微信公众号文章的完整管理流程
- 能力包含：
  - **智能创作**：基于参考文章改写、基于标题创作、直接发布
  - **提取转换**：从 mp.weixin.qq.com 链接提取文章并转换为 Markdown 格式
  - **创建草稿**：将内容创建为公众号草稿
  - **发布文章**：发布草稿到公众号
  - **生成封面**：自动生成文章封面图片（默认千问，支持豆包）
  - **素材管理**：上传图片等素材到微信服务器
- 触发条件：用户需要创作、提取、转换、发布或管理公众号文章
- **默认配置**：
  - 文章字数：1200-1500 字（默认要求）
  - 配图数量：3 张横屏图片（2.35:1）
  - 排版主题：根据文章内容自动选择（参考 [THEME_GUIDE.md](THEME_GUIDE.md)）
  - 写作风格：去 AI 化，详见 [HUMANIZE_GUIDE.md](HUMANIZE_GUIDE.md)
  - 选题与标题策略（**两阶段，不要混淆**）：
    - **阶段 1 选题讨论**（任务类型 B 必做，详见操作步骤）：用户只给主题方向时，先输出 3-4 个**选题方向**让用户挑——每个方向含「一个示意标题 + 角度 + 大纲」
    - **阶段 2 标题打磨**（用户选定方向后，写正文前）：针对选定方向，按 [references/viral_titles_50.md](references/viral_titles_50.md) 的爆款逻辑（痛点 / 热点 / 认知冲突 / 细分人群 / 数据强化）再产出 **3 个候选标题**，每个标注命中的爆款逻辑，让用户最终挑一个
    - 任务类型 A（已给完整 brief 含标题）→ 跳过阶段 1，直接进入阶段 2 微调或沿用

## 🚨 图片生成核心规范（强制）

> 完整规范见本文档"流程 B 步骤 3"处。此处为摘要，**所有封面图 + 文中配图**必须遵循。

**五要素结构（按顺序拼接）：**
1. 核心意象（2-4 个具象名词，从文章前 200 字提取）
2. 情绪基调（恰好 1 词：`温暖治愈` / `专业冷静` / `紧张焦虑` / `轻松愉悦` / `怀旧沉思` / `励志昂扬` / `神秘高级`）
3. 画面风格（按主题选：
   - 科技数码 → 微缩等距风格（深蓝紫渐变，**强制 flat composition，约束 900:383**）
   - AI 知识科普 → Bento 几何信息图（蓝青 + 霓虹线条，**clean typography，无背景杂物**）
   - AI 历史人文 → 硅基复古版画（做旧纸张 + **混古典蚀刻与霓虹电路**）
   - AI 工具实战 → 数字质感物相（玻璃晶体 + 光影对比，**macro shot，极浅景深，文字投影物体**）
   - 零售/商业运营 → 毛玻璃商务流（Glassmorphism，蓝绿渐变，中央卡片，效率图表）
   - SOP 拆解/教程 → 分步路径图（发光数字节点，图标，分步指南，干净背景）
   - 职场进阶/个人成长 → 虚拟实体质感（3D 极简物体特写，实体光影，居中大字）
   - 文艺生活 → 胶片质感（柔焦颗粒，**文字不做柔焦，强制 clean text overlay**）
   - 美食探店 → 食物特写（**文字放在最清晰平面，center 虚化，text clearly focused**）
4. 构图：固定 `2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，中部区域小字「标题关键词」（避开底部 15% 遮挡区）`
5. 负面提示：固定 `画面中不要出现任何文字、字母、汉字、水印、logo、签名`

**3 张配图按"故事弧线"分别构造（prompt 互不相同）：**
| 序号 | 定位 | 应包含的元素 |
| --- | --- | --- |
| 第 1 张 | **痛点画面** | 文章开头的困境 / 焦虑 / 失败场景具象化 |
| 第 2 张 | **转折画面** | 解决方案出现的关键时刻 / 工具 / 方法 |
| 第 3 张 | **升华画面** | 文章结尾的理想状态 / 成果 / 未来感 |

**禁止空泛 prompt：**`科技风格插画` / `为文章《XXX》生成封面` / `AI 提升工作效率主题插画` / `温暖治愈风格的封面` / 任何仅"风格+主题"两要素描述。

**合格示例：**`未来几何结构 (Infographic Geometric AI)。科技感数字界面，主体是 Bento 网格布局的微型 AI 系统架构图：中心是 AI Agent 大脑节点，左上是 RAG 检索模块六边形，右上是 Token 处理流水线，下方是 API 调用出口。深蓝青背景，霓虹青色发光线条连接各节点，整体干净数字感，无阴影扁平设计。专业冷静，Bento 几何信息图，2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，中部区域小字「AI AGENT」（避开底部 15% 遮挡区），画面主体不要出现任何文字、字母、汉字，水印、logo、签名`

### ⚠️ 五要素规范位置说明

详细规则（含完整画面风格映射表、配图五要素详解、禁止 prompt 完整清单）**位于本文档末尾附录**——这是刻意安排，目的是不影响读者第一时间找到"操作流程"。完整规范可随时回查。

## 前置准备

### 凭证配置（推荐用 `.env`，详见 [CONFIG.md](CONFIG.md)）

在仓库根创建 `.env` 文件（已加入 `.gitignore`，不会提交）：

```bash
# 微信公众号
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret

# 图像生成（任选其一即可，默认千问）
DASHSCOPE_API_KEY=your_qwen_key       # 千问（推荐，对 watermark=False 更稳定）
DOUBAO_API_KEY=your_doubao_key        # 豆包（可选）

# 切换默认图像引擎（可选，默认 qwen）
IMAGE_PROVIDER=qwen                   # qwen / doubao

# 默认排版主题（可选，缺省由 agent 按内容自动选择）
MARKDOWN_THEME=                       # orange / purple / green / blue / red / cyan / black / pink
```

**`.env` 支持情况（重要，避免 agent 错误调用）：**

| 脚本 | `.env` 读取 | 说明 |
| --- | --- | --- |
| `generate_cover.py` | ✅ `DASHSCOPE_API_KEY` / `DOUBAO_API_KEY` / `IMAGE_PROVIDER` | 完全免参 |
| `create_draft.py` | ✅ `WECHAT_APP_ID` / `WECHAT_APP_SECRET` | 不传 `--app_id/--app_secret` 时回退到 .env |
| `upload_material.py` | ❌ 不支持 | 必须 CLI 传 `--app_id` `--app_secret` |
| `publish_draft.py` | ❌ 不支持 | 必须 CLI 传 `--app_id` `--app_secret` |
| `markdown_to_wechat_doocs.py` | ✅ `MARKDOWN_THEME`（隐式） | 通过 `config.py` 提供默认主题 |

**Agent 实践建议：** 调用 `upload_material.py` / `publish_draft.py` 时，从 `.env` 读出 secret 后再以 CLI 参数形式传入（不要让用户重复输入）。

### 凭证来源
- 微信 AppID / AppSecret：登录 https://mp.weixin.qq.com → 开发 → 基本配置（重置 AppSecret 需管理员扫码）
- 千问 DashScope Key：https://dashscope.console.aliyun.com/
- 豆包 API Key：https://console.volc.com/iam/keylist （需开通豆包图像生成服务权限）

### 依赖
- Python：仅 `generate_cover.py` 依赖 `requests` + `pillow`（脚本内置 PEP 723 元数据，`uv run` 自动安装）；其它脚本零依赖
- Node.js（仅提取微信原文用到）：首次使用 `cd reader && npm install`

## 操作步骤

### 流程 0：智能文章创作工作流（推荐）

当用户需要快速创作并发布文章时，使用智能工作流：

#### 🎯 第一步：识别任务类型（开始前必做）

不同任务类型走不同分支，**不要默认走完整流程**：

| 类型 | 用户输入特征 | 应走的分支 |
| --- | --- | --- |
| A | 给了完整 brief（标题 + 受众 + 关键信息） | 完整流程 0（含搜索 + 三遍审校） |
| B | 只给了一个主题 / 方向，没有标题 | **先做选题讨论 → 再走完整流程**（见下文） |
| C | 给了参考文章 URL，要求改写 | 模式 1（基于参考文章改写） |
| D | 给了完整文章稿，要求审校 / 降 AI 味 | **直接进入三遍审校**（见 [references/三遍审校清单.md](references/三遍审校清单.md)），跳过创作环节 |
| E | 只是问问题、聊功能 | 直接回答，不进入创作流程 |

#### 🧭 选题讨论（任务类型 B 必做，禁止直接动笔）

用户只给了主题方向时，**先输出 3-4 个选题方向给用户挑**，不要自己拍板。

每个选题方向包含：
- 一个**示意标题**（这里只是示意，最终标题在阶段 2 再打磨）
- 核心角度（一句话）
- 预估工作量（搜索成本 / 字数）
- 优势 / 劣势
- 大纲（3-5 个小标题）

**用户选定方向后**：进入阶段 2 标题打磨——按 [references/viral_titles_50.md](references/viral_titles_50.md) 爆款逻辑产出 3 个候选标题给用户挑，再开始写正文。

**两阶段顺序：选题方向（3-4 选 1）→ 候选标题（3 选 1）→ 写正文。** 不要在第一轮就给标题候选。

#### 🔍 调研规则（强制）

**何时必须调用搜索工具（web_fetch）：**
- 涉及 2024-2025 年的新产品 / 新政策 / 新数据
- 涉及具体的统计数字、市场规模、调研报告
- 涉及不确定的技术细节（API、版本号、配置）
- 涉及具体的人名 / 公司动态 / 时间线

**信息源优先级：**
1. 官方来源（官网、公告、白皮书）
2. 主流科技 / 行业媒体
3. 社区讨论（Reddit / HN / Product Hunt / 知乎高赞）
4. 百度结果（**谨慎使用**，需交叉验证）

**铁律：绝不编造数据和案例。** 搜不到的事实 → 删掉相关表述，或在文中明确说"暂未找到公开数据"。

#### 🎯 工作流程控制

**两阶段发布流程：**
1. **预览阶段**：如果用户没有明确说"发布到草稿箱"，先输出文章内容供预览
2. **发布阶段**：用户确认后再发布到草稿箱

**示例对话：**
```
用户: 写一篇关于"AI提升工作效率"的文章
智能体: 
[输出文章内容]
---
📝 文章已生成！是否需要发布到草稿箱？

用户: 发布
智能体: 
✅ 正在发布到草稿箱...
✅ 完成！草稿已创建，media_id: xxx
```

**直接发布模式（完整步骤 = 流程 B 全过程）：**
```
用户: 写一篇关于「AI 提升工作效率」的文章并发布到草稿箱
智能体:
1. 搜索资料（按调研规则，必要时 web_fetch）
2. 创作文章初稿（Markdown）
3. 三遍审校（强制，按 references/三遍审校清单.md）
   - 第一遍 内容：事实 / 逻辑 / 结构
   - 第二遍 风格：删 AI 套话 / 加态度
   - 第三遍 细节：句长 / 标点 / 中英文空格
4. Markdown → 内联 HTML（markdown_to_wechat_doocs.py，按主题选 theme）
5. 生成封面（五要素 prompt，generate_cover.py）
6. 上传封面（upload_material.py → thumb_media_id）
7. 创建草稿（create_draft.py，--content 传步骤 4 的 HTML）
✅ 完成！草稿已创建，media_id: xxx
```

#### 🖼️ 文章内插图片配置

**配图生成规则**：
- **仅生成文章**（预览模式）：不生成文中配图，只输出文字内容
- **发布到公众号**（发布模式）：必须生成文中配图，默认 3 张

**示例对话**：

**场景 1：仅生成文章（不生成配图）**
```
用户: 写一篇关于"AI提升工作效率"的文章
智能体:
1. 搜索资料并创作文章
2. 输出纯文字内容（不含配图）
---
📝 文章已生成！是否需要发布到草稿箱？
```

**场景 2：发布到公众号（必须生成配图）**
```
用户: 写一篇关于「AI 提升工作效率」的文章并发布到草稿箱
智能体:
1. 搜索资料并创作 Markdown 初稿
2. 三遍审校（强制）
3. Markdown → 内联 HTML（markdown_to_wechat_doocs.py --theme blue）
4. 生成 3 张文中配图（按"痛点 / 转折 / 升华"故事弧线，五要素 prompt）
5. 上传 3 张配图到公众号（upload_material.py），把 URL 嵌入 HTML
6. 生成封面图（五要素 prompt）
7. 上传封面 → thumb_media_id
8. 创建草稿
✅ 完成！草稿已创建，media_id: xxx
```

**配图规则**：
- 配图数量：默认 3 张（可在 `.env` 中配置 `ARTICLE_IMAGE_COUNT`）
- 配图位置：在文章的主要段落结尾插入
- 图片方向：横屏（2.35:1 比例）
- 图片提示词：**严格按照本文档『🚨 图片生成核心规范』中的五要素结构生成**，3 张图分别对应"痛点画面 / 转折画面 / 升华画面"

#### 模式 1：基于参考文章改写

用户提供参考文章 URL，智能体自动完成：提取 → 改写 → 生成封面 → 创建草稿

**操作步骤：**
1. 提取参考文章内容（使用 `extract_to_markdown.py`）
2. 智能体改写文章内容
3. 生成封面图片（使用 `generate_cover.py`）
4. 上传封面到微信（使用 `upload_material.py`）
5. 创建草稿（使用 `create_draft.py`）

**示例对话：**
```
用户: 帮我改写这篇文章并发布到草稿箱：https://mp.weixin.qq.com/s/xxx
智能体:
1. 提取原文（extract_to_markdown.py --json）
2. 改写文章（保持核心观点，重写表达）
3. 三遍审校（强制）
4. Markdown → 内联 HTML（markdown_to_wechat_doocs.py）
5. 生成封面（五要素 prompt）
6. 上传封面 + 创建草稿
✅ 完成！草稿已创建，media_id: xxx
```

#### 模式 2：基于标题或主题创作

**先按"任务类型识别"判断输入：**
- 用户**给了完整标题 + 受众 + 关键信息** → 任务类型 A，直接进入下面的操作步骤
- 用户**只给了主题方向**（例如"写一篇 AI 提升工作效率的文章"） → 任务类型 B，**先做选题讨论**（输出 3-4 个候选方向给用户挑），用户选定后再进入操作步骤

**操作步骤（任务类型 A，或任务类型 B 用户已选定方向后）：**
1. 按调研规则使用 `web_fetch` 搜索相关资料
2. 智能体基于资料创作 Markdown 初稿
3. **三遍审校（强制）**：按 `references/三遍审校清单.md` 走完三遍
4. Markdown → 内联 HTML（`markdown_to_wechat_doocs.py`，按主题选 theme）
5. 生成封面图片（五要素 prompt）
6. 上传封面到微信
7. 创建草稿

**示例对话（任务类型 B，含选题讨论）：**
```
用户: 写一篇关于「AI 如何提升工作效率」的文章并发布到草稿箱
智能体（识别为任务类型 B → 先选题讨论）:
我先给你 3 个选题方向，你挑一个：
方向 1：《下班还在加班的人，都没用对这 3 个 AI 工具》（痛点 + 工具实测）
方向 2：《我用 AI 把每天 3 小时杂活压到了 20 分钟》（第一人称叙事）
方向 3：《2025 年还在手动做这 5 件事，就是在浪费命》（清单体 + 时效）

用户: 方向 1
智能体:
1. 搜索 3 款工具的最新资料
2. 创作初稿
3. 三遍审校
4. 转换 HTML
5. 生成封面
6. 上传 + 创建草稿
✅ 完成！草稿已创建，media_id: xxx
```

#### 模式 3：直接发布

用户提供完整内容（用户已写好正文或直接给了 HTML），智能体自动完成：封面 → 上传 → 创建草稿。

**操作步骤：**
1. 生成封面图片（五要素 prompt）
2. 上传封面到微信
3. 创建草稿

**示例对话：**
```
用户: 我已经写好文章了，帮我发到草稿箱
智能体:
1. 生成封面（用户没给 prompt → 根据内容推断五要素）
   python3 scripts/generate_cover.py --prompt "<五要素 prompt>" --output cover.jpg
2. 上传封面
3. 创建草稿（--content 直接用用户提供的 HTML，不需要 markdown 转换）
✅ 完成！草稿已创建，media_id: xxx
```

**可选参数：**
- 封面引擎选择：`generate_cover.py --provider qwen|doubao`
- 草稿元信息：`create_draft.py --author "作者名" --digest "摘要"`
- 不生成封面：跳过 `generate_cover.py` 步骤，`create_draft.py` 不传 `--thumb_media_id` 即可（**`generate_cover.py` 没有 `--no-cover` 参数，不要瞎传**）

### 流程 A：提取文章并转换为 Markdown

当用户提供微信公众号文章链接，需要提取内容并转换为 Markdown 格式时：

1. **提取并转换文章**
   - 调用 `scripts/extract_to_markdown.py` 提取并转换文章
   - 参数说明：
     - `url`: 文章链接（必需，mp.weixin.qq.com）
     - `-o, --output`: 保存 Markdown 文件路径（可选）
     - `--json`: 输出 JSON 格式（可选）
   - 示例：
     ```bash
     # 输出 Markdown 到终端
     python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s?__biz=..."
     
     # 保存为文件
     python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s?__biz=..." -o article.md
     
     # 输出 JSON 格式（含元数据）
     python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s?__biz=..." --json
     ```
   - 返回数据包含：
     - 文章标题、作者、发布时间
     - Markdown 格式的内容
     - 封面图 URL、原文链接
     - 完整的 Markdown 文档（含元数据）

2. **后续处理**
   - 可以基于 Markdown 内容进行编辑、分析
   - 或转换回 HTML 后使用流程 B 发布

### 流程 B：发布带封面的文章到公众号

1. **生成文章内容**
   - 智能体根据主题创作文章标题、正文内容
   - **标题创作**：先打开 [references/viral_titles_50.md](references/viral_titles_50.md)，按文章主题命中的类别（痛点 / 热点 / 认知冲突 / 细分人群 / 数据强化）挑 3-5 条范例仿写，输出 3 个候选标题供用户挑选，每个候选标注命中的爆款逻辑
   - **写作风格**：参考 [HUMANIZE_GUIDE.md](HUMANIZE_GUIDE.md) 的去 AI 化规则
   - **三遍审校（强制，初稿写完后必做）**：按 [references/三遍审校清单.md](references/三遍审校清单.md) 顺序过——
     - 第一遍 内容审校：事实 / 逻辑 / 结构（绝不编造数据）
     - 第二遍 风格审校：删 AI 套话 + 拆句式 + 替换书面词 + 加态度（≥ 10 处个人感受）
     - 第三遍 细节打磨：句长 ≤ 30 字 / 段落 3-5 行 / 全角标点 / 引号「」/ 中英文混排空格
     - **未通过审校清单的"终极检查"，不得进入步骤 2 生成封面**
   - 生成摘要和作者信息（可选）

2. **将 Markdown 转换为微信 HTML（关键步骤，不可跳过）**
   - 微信公众号编辑器**不支持 `<style>` 标签**，必须使用内联样式 HTML
   - 使用 `scripts/markdown_to_wechat_doocs.py`（仓库内 8 个 markdown 转换器中**唯一推荐**的版本，与 `THEME_GUIDE.md` 一一对应）
   - **主题选择步骤（强制）：**
     1. 打开 [THEME_GUIDE.md](THEME_GUIDE.md) 查阅"文章类型 → 主题"映射表（如：励志/搞钱→orange、科技/职场→blue、健康养生→green、文艺/紫调→purple、热血/红→red、清爽/科普→cyan、商务/严肃→black、女性/温柔→pink）
     2. 也可调用 `scripts/config.py` 中的 `select_theme_by_content(title, content)` 让脚本按关键词自动选
     3. 用户在 `.env` 里设了 `MARKDOWN_THEME=xxx` 时优先使用该值
   - 命令：
     ```bash
     python3 scripts/markdown_to_wechat_doocs.py \
       --input drafts/article.md \
       --output drafts/article.html \
       --theme orange   # 按 THEME_GUIDE.md 的类型映射挑
     ```
   - 输出的 HTML 才是 `create_draft.py --content` 真正要传的内容（**不要直接传 Markdown**）

3. **生成封面图片**
   - 智能体根据文章内容生成封面描述（prompt），prompt 必须遵循『🚨 图片生成核心规范』五要素结构
   - 调用 `scripts/generate_cover.py` 生成封面图片
   - 参数说明：
     - `--prompt`: 图片提示词（必需）
     - `--provider`: 图像生成服务（可选，默认 `qwen`，可用环境变量 `IMAGE_PROVIDER` 覆盖）
       - `qwen` - 千问（通义万相，**默认**，对 watermark=False 更稳定）
       - `doubao` - 豆包
     - `--size`: 图片尺寸（可选，仅千问支持，默认 `900*383`）
       - `900*383` - 2.35:1 横屏（**默认，推荐，符合微信封面标准**）
       - `1664*928` - 16:9 横屏（兼容旧格式）
       - `1024*1024` - 正方形
       - `720*1280` - 9:16 竖屏
       - `1280*720` - 16:9 横屏（小尺寸）
     - `--qwen-model`: 千问模型（可选，仅千问支持）
       - `qwen-image-2.0` - 标准版（默认）
       - `qwen-image-2.0-pro` - 专业版
     - `--doubao-model`: 豆包模型（可选，仅豆包支持，默认 `doubao-seedream-4-0-250828`）
     - `--output, -o`: 下载并保存图片到本地路径（可选，建议传，否则只返回 URL）
     - `--compress / --max-size`: 自动压缩，默认开启，目标 800KB（公众号缩略图素材限制 2MB 以内）
   - 示例：
     ```bash
     # 使用千问生成（默认）—— prompt 必须遵循五要素结构 + 意疏AI口袋品牌
     python3 scripts/generate_cover.py --prompt "未来几何结构 (Infographic Geometric AI)。科技感数字界面，主体是 Bento 网格布局的微型 AI 系统架构图：中心是 AI Agent 大脑节点，左上是 RAG 检索模块六边形，右上是 Token 处理流水线，下方是 API 调用出口。深蓝青背景，霓虹青色发光线条连接各节点，整体干净数字感，无阴影扁平设计。专业冷静，Bento 几何信息图，2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，中部区域小字「AI编程」（避开底部 15% 遮挡区），画面主体不要出现任何文字、字母、汉字，水印、logo、签名"

     # 切换到豆包
     python3 scripts/generate_cover.py --prompt "<五要素 prompt>" --provider doubao

     # 千问生成正方形封面
     python3 scripts/generate_cover.py --prompt "<五要素 prompt>" --provider qwen --size "1024*1024"

     # 千问专业版模型
     python3 scripts/generate_cover.py --prompt "<五要素 prompt>" --provider qwen --qwen-model qwen-image-2.0-pro
     ```
   - 脚本返回图片URL
   - 下载图片到本地临时文件
   - 调用 `scripts/upload_material.py` 上传图片到微信服务器
   - 参数说明：
     - `--app_id`: 微信公众号 AppID（必需）
     - `--app_secret`: 微信公众号 AppSecret（必需）
     - `--image_path`: 图片文件路径（必需）
   - 脚本返回 thumb_media_id

4. **创建文章草稿**
   - 调用 `scripts/create_draft.py` 创建草稿
   - 参数说明：
     - `--app_id`: 微信公众号 AppID（必需）
     - `--app_secret`: 微信公众号 AppSecret（必需）
     - `--title`: 文章标题（必需）
     - `--content`: **必须传步骤 2 输出的内联样式 HTML**（不是原始 Markdown）
     - `--digest`: 文章摘要（可选）
     - `--author`: 作者名称（可选）
     - `--thumb_media_id`: 封面图片 media_id（可选，从步骤 3 获取）
     - `--show_cover_pic`: 是否显示封面，默认为 1（可选）
   - 脚本返回 media_id

5. **发布草稿到公众号**
   - 调用 `scripts/publish_draft.py` 发布草稿
   - 参数说明：
     - `--app_id`: 微信公众号 AppID（必需）
     - `--app_secret`: 微信公众号 AppSecret（必需）
     - `--media_id`: 草稿的 media_id（必需）
   - 脚本返回 publish_id

6. **验证发布状态**
   - 根据 publish_id 查询发布状态
   - 确认文章是否成功发布

### 流程 C：发布无封面文章

如果不需要封面图片，可以跳过流程 B 的步骤 3，直接执行步骤 4 创建草稿（不传 `--thumb_media_id`）。

## 资源索引
- 核心脚本：
  - [scripts/generate_cover.py](scripts/generate_cover.py) - 生成封面图片（参数：prompt, --provider, --size, --qwen-model, --doubao-model, --output, --compress）
  - [scripts/markdown_to_wechat_doocs.py](scripts/markdown_to_wechat_doocs.py) - **Markdown → 内联样式微信 HTML 转换器（推荐使用，与 THEME_GUIDE.md 配套）**，参数：--input, --output, --theme
  - [scripts/upload_material.py](scripts/upload_material.py) - 上传图片到微信（参数：app_id, app_secret, image_path）
  - [scripts/create_draft.py](scripts/create_draft.py) - 创建文章草稿（参数：app_id, app_secret, title, content, digest, author 等）
  - [scripts/publish_draft.py](scripts/publish_draft.py) - 发布草稿到公众号（参数：app_id, app_secret, media_id）
  - [scripts/extract_to_markdown.py](scripts/extract_to_markdown.py) - 提取公众号文章并转换为 Markdown（参数：url, -o, --json）
  - [scripts/create_article.py](scripts/create_article.py) - ⚠️ **遗留 orchestrator**（不推荐默认使用；已知不足：默认 doubao、跳过审校、跳过 HTML 转换。仅在用户明确要求"快速一键"时用）
  - ⚠️ 其它脚本（`compress_image.py` / `extract_simple.py` / `extract_wechat.py` / `markdown_to_wechat*.py` 除 `_doocs.py` 以外的所有版本）均为遗留代码，**请勿默认使用**，如不确定请参考本 SKILL.md 流程
- 转换器模块：
  - [reader/extract_and_convert.js](reader/extract_and_convert.js) - Node.js 提取与转换引擎（由 extract_to_markdown.py 调用）
- 领域参考：
  - [THEME_GUIDE.md](THEME_GUIDE.md) - **微信排版主题选择指南**（与 markdown_to_wechat_doocs.py 配套，8 个主题 + 文章类型映射）
  - [references/wechat-api.md](references/wechat-api.md) - 微信公众号 API 接口说明（获取 access_token、创建草稿、发布接口、上传素材、错误码）
  - [references/viral_titles_50.md](references/viral_titles_50.md) - 50 个爆款标题范例 + 背后逻辑
  - [references/三遍审校清单.md](references/三遍审校清单.md) - 三遍审校流程（内容 / 风格 / 细节），初稿写完后强制执行
  - [HUMANIZE_GUIDE.md](HUMANIZE_GUIDE.md) - 去 AI 化写作详细规则与替换词表
  - [CHICKEN_SOUP_STYLE.md](CHICKEN_SOUP_STYLE.md) - AI 技术工具评测 / 编程效率 / Prompt 工程类文章写作规范

## 注意事项
- 文章内容必须是**内联样式 HTML**（微信编辑器不识别 `<style>` 标签），用 `markdown_to_wechat_doocs.py` 转换得到
- 封面图片由 `generate_cover.py` 自动生成（千问默认 `900×383` 2.35:1，自动压缩到 ≤ 800KB），符合微信缩略图素材 2MB 限制
- AppID 和 AppSecret 必须正确，否则无法获取 access token
- 脚本会自动获取 access token，无需手动管理
- 生成封面图片需要图像 API 凭证（默认千问 `DASHSCOPE_API_KEY`，可选豆包 `DOUBAO_API_KEY`）
- 发布操作不可逆，建议先创建草稿确认内容
- 注意API调用频率限制

## 使用示例

### 示例0：智能工作流 - 基于参考文章改写（推荐）
```
用户对话：
"帮我改写这篇文章并发布到草稿箱：https://mp.weixin.qq.com/s/xxx"

智能体执行流程：
1. 提取原文
   python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s/xxx" --json

2. 改写文章（智能体使用 AI 能力）
   - 分析原文内容
   - 生成新的标题和内容
   - 保持核心观点，改变表达方式

3. 生成封面（按五要素结构构造 prompt，禁用空泛描述）
   python3 scripts/generate_cover.py --prompt "<核心意象>，<情绪基调>，<画面风格>，2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，中部区域小字「标题关键词」（避开底部 15% 遮挡区），画面主体不要出现任何文字、字母、汉字，水印、logo、签名" --provider qwen

4. 下载并上传封面
   wget -O cover.jpg "封面URL"
   python3 scripts/upload_material.py --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" --image_path cover.jpg

5. 创建草稿（create_draft.py 支持 .env，省略 secret）
   python3 scripts/create_draft.py \
     --title "新标题" --content "$(cat drafts/article.html)" --thumb_media_id "$THUMB_MEDIA_ID"

✅ 完成！草稿已创建
```

### 示例0.1：智能工作流 - 基于主题方向创作（任务类型 B：含选题讨论）
```
用户对话第 1 轮：
"写一篇关于 AI 提升工作效率的文章"

智能体（任务类型 B → 先选题讨论，禁止直接动笔）：
我先给你 3 个选题方向，你挑一个：

方向 1：《下班还在加班的人，都没用对这 3 个 AI 工具》
- 角度：痛点切入，落到具体工具实测
- 大纲：现状痛点 / 工具 1 实测 / 工具 2 实测 / 工具 3 实测 / 选型建议
- 优势：标题命中"身份+量化结果"，转发率高 / 劣势：需要真实搜索 3 款工具的最新数据

方向 2：《我用 AI 把每天的 3 小时杂活压到了 20 分钟》
- 角度：第一人称经历叙事
- ...

方向 3：《2025 年还在手动做这 5 件事，就是在浪费命》
- 角度：清单体 + 时效性
- ...

---

用户对话第 2 轮："方向 1"

智能体执行流程：
1. 搜索相关资料（web_fetch 三款工具的官方文档 + 最新评测）
2. 创作文章初稿
3. 三遍审校（按 references/三遍审校清单.md 执行）
   - 第一遍 内容：核对工具官方信息、数据有源
   - 第二遍 风格：删 AI 套话 + 加态度
   - 第三遍 细节：句长 / 标点 / 中英文空格
4. 生成封面（按五要素结构 + 意疏AI口袋品牌）
   python3 scripts/generate_cover.py --prompt "未来几何结构 (Infographic Geometric AI)。科技感数字界面，主体是 Bento 网格布局的微型 AI 系统架构图：中心是 AI Agent 大脑节点，左上是 RAG 检索模块六边形，右上是 Token 处理流水线，下方是 API 调用出口。深蓝青背景，霓虹青色发光线条连接各节点，整体干净数字感，无阴影扁平设计。专业冷静，Bento 几何信息图，2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，中部区域小字「AI编程」（避开底部 15% 遮挡区），画面主体不要出现任何文字、字母、汉字，水印、logo、签名" --provider qwen
5. 上传封面并创建草稿
   （同上）

✅ 完成！草稿已创建
```

### 示例1：提取文章并转换为 Markdown
```bash
# 提取并输出 Markdown 到终端
python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s?__biz=MzI..."

# 保存为文件
python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s?__biz=..." -o article.md

# 输出 JSON 格式（含完整元数据）
python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s?__biz=..." --json

# 输出示例：
# {
#   "title": "文章标题",
#   "author": "作者",
#   "publishTime": "2026/03/04 10:11:00",
#   "description": "文章摘要",
#   "cover": "https://封面图URL",
#   "link": "https://原文链接",
#   "content": "Markdown 内容...",
#   "fullMarkdown": "# 文章标题\n\n**作者**: ...\n\n..."
# }
```

### 示例2：发布简单的图文文章（无封面，假设 .env 已配置）
```bash
# 0. 加载 .env（agent 自身读取，便于把 secret 传给不支持 .env 的脚本）
source <(grep -E '^WECHAT_' .env | sed 's/^/export /')

# 1. 生成 Markdown → 转内联 HTML（关键步骤，微信不支持 <style>）
python3 scripts/markdown_to_wechat_doocs.py \
  --input drafts/article.md \
  --output drafts/article.html \
  --theme blue

# 2. 创建草稿（create_draft.py 支持 .env，可不传 app_id/secret）
python3 scripts/create_draft.py \
  --title "如何用 Python 处理数据" \
  --content "$(cat drafts/article.html)" \
  --author "技术团队"
# 输出: media_id=MEDIA_XXX

# 3. 发布草稿（publish_draft.py 不支持 .env，必须 CLI 传）
python3 scripts/publish_draft.py \
  --app_id "$WECHAT_APP_ID" \
  --app_secret "$WECHAT_APP_SECRET" \
  --media_id "MEDIA_XXX"
```

### 示例3：发布带自动生成封面的文章（假设 .env 已配置）
```bash
# 加载 secret 供不支持 .env 的脚本使用
source <(grep -E '^WECHAT_' .env | sed 's/^/export /')

# 1. Markdown → 内联 HTML（按 THEME_GUIDE 选 theme）
python3 scripts/markdown_to_wechat_doocs.py \
  --input drafts/release.md --output drafts/release.html --theme blue

# 2. 生成封面（五要素 prompt，generate_cover.py 已读 .env，无需传 key）
cover_prompt="发布会舞台中央的新版应用界面投影，前排观众举起手机拍摄，灯光聚焦，专业冷静，极简商务，金蓝撞色，2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，中部区域小字「效率工具」（避开底部 15% 遮挡区），画面主体不要出现任何文字、字母、汉字，水印、logo、签名"

python3 scripts/generate_cover.py --prompt "$cover_prompt" --output cover.jpg
# 自动下载并压缩到 cover.jpg

# 3. 上传封面（upload_material.py 不支持 .env，需显式传）
python3 scripts/upload_material.py \
  --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
  --image_path cover.jpg
# 输出: thumb_media_id=THUMB_XXX

# 4. 创建草稿（create_draft.py 支持 .env，可省略 app_id/secret）
python3 scripts/create_draft.py \
  --title "产品更新公告" \
  --content "$(cat drafts/release.html)" \
  --digest "产品 v2.0 版本重要更新" \
  --thumb_media_id "THUMB_XXX" \
  --show_cover_pic 1

# 5. 发布
python3 scripts/publish_draft.py \
  --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
  --media_id "MEDIA_YYY"
```

### 示例4：提取文章并重新发布（转载流程，假设 .env 已配置）
```bash
source <(grep -E '^WECHAT_' .env | sed 's/^/export /')

# 1. 提取原文为 Markdown
python3 scripts/extract_to_markdown.py "https://mp.weixin.qq.com/s?__biz=..." -o drafts/article.md

# 2. 编辑 / 改写 drafts/article.md（可选）

# 3. Markdown → 内联 HTML（必做，按 THEME_GUIDE 选 theme）
python3 scripts/markdown_to_wechat_doocs.py \
  --input drafts/article.md --output drafts/article.html --theme orange

# 4. 生成新封面（五要素 prompt）
python3 scripts/generate_cover.py \
  --prompt "<核心意象>，<情绪基调>，<画面风格>，2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，中部区域小字「标题关键词」（避开底部 15% 遮挡区），画面主体不要出现任何文字、字母、汉字，水印、logo、签名" \
  --output cover.jpg

# 5. 上传封面（不支持 .env，需显式传 secret）
python3 scripts/upload_material.py \
  --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
  --image_path cover.jpg
# → thumb_media_id=THUMB_XXX

# 6. 创建草稿（支持 .env，可省略 secret）
python3 scripts/create_draft.py \
  --title "【转载】原文标题" \
  --content "$(cat drafts/article.html)" \
  --thumb_media_id "THUMB_XXX"

# 7. 发布
python3 scripts/publish_draft.py \
  --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
  --media_id "MEDIA_XXX"
```

### 示例5：批量发布文章（假设 .env 已配置）
```bash
source <(grep -E '^WECHAT_' .env | sed 's/^/export /')

for i in 1 2; do
  # 转 HTML
  python3 scripts/markdown_to_wechat_doocs.py \
    --input "drafts/article-$i.md" --output "drafts/article-$i.html" --theme blue

  # 创建草稿（create_draft 自动读 .env）
  media_id=$(python3 scripts/create_draft.py \
    --title "文章 $i" \
    --content "$(cat drafts/article-$i.html)" | jq -r .media_id)

  # 发布（需显式传 secret）
  python3 scripts/publish_draft.py \
    --app_id "$WECHAT_APP_ID" --app_secret "$WECHAT_APP_SECRET" \
    --media_id "$media_id"
done
```

---

## 附录：🚨 图片生成核心规范（完整版）

本文档开头的规范为摘要版，此处为完整参考。

### 五要素结构（强制，按顺序拼接，中文逗号分隔）

1. **核心意象**：从文章前 200 字中提取 2-4 个最具画面感的具象名词（人 / 物 / 场景 / 动作），不要抽象概念。
2. **情绪基调**：恰好 1 个词，从下面挑选——`温暖治愈` / `专业冷静` / `紧张焦虑` / `轻松愉悦` / `怀旧沉思` / `励志昂扬` / `神秘高级`。
3. **画面风格**：按文章主题从下表挑选——

| 文章主题 | 视觉风格 | 配色与质感 | prompt 关键词 |
| --- | --- | --- | --- |
| 科技数码 | 微缩等距 | 深蓝紫渐变，**强制 flat composition，约束 900:383** | 专业冷静，微缩等距 |
| AI 知识科普 | Bento 几何信息图 | 蓝青 + 霓虹线条，**clean typography，无背景杂物** | 专业冷静，几何信息图 |
| AI 历史人文 | 硅基复古版画 | 做旧纸张 + **混古典蚀刻与霓虹电路** | 怀旧沉思，复古未来 |
| AI 工具实战 | 数字质感物相 | 玻璃晶体 + 光影，**macro shot，极浅景深，文字投影物体** | 专业冷静，高对比光影 |
| 零售/商业运营 | 毛玻璃商务流 | Glassmorphism，蓝绿渐变，中央卡片，效率图表 | 专业冷静，商务渐变 |
| SOP 拆解/教程 | 分步路径图 | 发光数字节点，图标，分步指南，干净背景 | 励志昂扬，分步指南 |
| 职场进阶/个人成长 | 虚拟实体质感 | 3D 极简物体特写，实体光影，居中大字 | 励志昂扬，3D 极简 |
| 文艺生活 | 胶片质感 | 柔焦颗粒，**文字不做柔焦，强制 clean text overlay** | 轻松愉悦，胶片质感 |
| 美食探店 | 食物特写 | 食欲感，**文字放在最清晰平面，center 虚化，text clearly focused** | 轻松愉悦，食物特写 |
4. **构图与镜头**：固定为 `2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，中部区域小字「标题关键词」（避开底部 15% 遮挡区）`。
5. **负面提示**：固定追加 `画面中不要出现任何文字、字母、汉字、水印、logo、签名`。

### 文中 3 张配图必须按"故事弧线"分别构造

| 序号 | 画面定位 | 应包含的具象元素 |
| --- | --- | --- |
| 第 1 张 | **痛点画面** | 文章开头描述的困境 / 焦虑 / 失败场景的具象化 |
| 第 2 张 | **转折画面** | 解决方案出现的关键时刻 / 工具 / 方法的具象化 |
| 第 3 张 | **升华画面** | 文章结尾呈现的理想状态 / 成果 / 未来感的具象化 |

**3 张配图 prompt 必须互不相同**，禁止复用同一个 prompt。

### 禁止使用的空泛 prompt

发现以下 prompt 一律按五要素重写，不准直接使用：

- ❌ `科技风格插画`
- ❌ `为文章《XXX》生成封面`
- ❌ `AI 提升工作效率主题插画`
- ❌ `温暖治愈风格的封面`
- ❌ 任何只含"风格 + 主题"两要素的描述

### 合格 prompt 示例（封面图 · 意疏AI口袋 · 科技风格）

文章主题："上班族用 AI 工具节省下班时间"

```
未来几何结构 (Infographic Geometric AI)。科技感数字界面，主体是 Bento 网格
布局的微型 AI 系统架构图：中心是 AI Agent 大脑节点，左上是 RAG 检索模块
六边形，右上是 Token 处理流水线，下方是 API 调用出口。深蓝青背景，霓虹
青色发光线条连接各节点，整体干净数字感，无阴影扁平设计。专业冷静，Bento
几何信息图，2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，
中部区域小字「AI编程」（避开底部 15% 遮挡区），画面主体不要出现任何文字、
字母、汉字，水印、logo、签名
```

### 视觉风格示例（9 种风格均可选）

---

**风格一：AI 知识科普 → Bento 几何信息图**

适用：Agent 原理、模型架构、API 鉴权、RAG 检索等需要"逻辑清晰"的复杂概念。

```
未来几何结构 (Infographic Geometric AI)。科技感数字界面投影在会议室，
主体是一个 Bento 网格布局的微型 AI 系统架构图：中心是 AI Agent 大脑节点，
左上是 RAG 检索模块六边形，右上是 Token 处理流水线，下方是 API 调用出口。
深蓝青背景，霓虹青色发光线条连接各节点，整体干净数字感，无阴影扁平设计。
2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，
中部区域小字「AI AGENT」（避开底部 15% 遮挡区），
画面主体不要出现任何文字、字母、汉字，水印、logo、签名
```

---

**风格二：AI 历史人文 → 硅基复古版画**

适用：AI 发展史、图灵故事、人机边界讨论、数智革命等"有厚重感"的主题。

```
硅基复古版画 (Retro-Futuristic AI Etching)。古典人物肖像，头部可见齿轮与
电路纹理交织，眼神深邃望向远方，背景是蚀刻风格的电路矩阵做旧纸张纹理。
整体呈现赛博朋克与古典的碰撞，厚重历史感。深棕炭笔色调，浅金色点缀，
纸张粗糙质感主导，温暖怀旧。2.35:1 横向构图，主体居中偏左，
右上角嵌入小字「意疏AI口袋」，中部区域小字「数智革命」（避开底部 15% 遮挡区），
画面主体不要出现任何文字、字母、汉字，水印、logo、签名
```

---

**风格三：AI 工具/项目实战 → 数字质感物相**

适用：Claude Code、Cursor、自动化项目等需要"获得感"和"实体感"的实战内容。

```
数字质感物相 (Digital Macro AI Aesthetics)。极高对比度微距摄影：透明玻璃
晶体立方体悬浮于深邃反光表面，背景大面积虚化，仅保留边缘光晕。
晶体表面清晰倒映代码片段 > /compact，光影从晶体内部投射出来。
电光蓝与霓虹紫发光对比，深色背景衬托，细节丰富，浅景深营造立体感。
2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，
中部区域小字「Claude Code 进阶」（避开底部 15% 遮挡区），
画面主体不要出现任何文字、字母、汉字，水印、logo、签名
```

---

**风格四：零售/商业运营 → 毛玻璃商务流 (Business Efficiency / Glassmorphism)**

适用：门店全流程自动化 SOP、苏宁案例、AI 减少人力等商业运营主题。

```
专业商务效率风格 (Business Efficiency Glassmorphism)。毛玻璃质感，
柔和蓝绿渐变背景，中央悬浮半透明玻璃卡片（周围虚化趋势图表），
电光蓝与霓虹紫发光文字投射在玻璃表面。高效商务感，高对比，干净利落。
2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，
中部区域小字「门店30天提效SOP」（避开底部 15% 遮挡区），
画面主体不要出现任何文字、字母、汉字，水印、logo、签名
```

---

**风格五：SOP 拆解/保姆级教程 → 分步路径图 (Step-by-Step Path)**

适用：Hermes 链接飞书 CLI 完整教程、从 0 到 1 部署 AI Agent 等操作指南。

```
分步路径风格 (Step-by-Step Path)。干净横向水平路径，三个发光节点
（标注 1、2、3），每个节点配简单图标（Setup、Auth、Run），
节点下方干净排版文字「Hermes+飞书CLI：3步配置指南」，中性背景，干净排版。
2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，
中部区域小字「3步配置指南」（避开底部 15% 遮挡区），
画面主体不要出现任何文字、字母、汉字，水印、logo、签名
```

---

**风格六：职场进阶/个人成长 → 虚拟实体质感 (Virtual 3D Object)**

适用：产品经理转型、告别加班、职场 AI 思维等个人成长主题。

```
极简 3D 虚拟质感 (Minimalist 3D Object)。单件白色陶瓷键盘键帽
特写，浅灰表面，强对比，直光，居中大字「告别加班」
清晰印刷在键帽上，整体 3D 极简，实体光影，高级感。
2.35:1 横向构图，主体居中偏左，右上角嵌入小字「意疏AI口袋」，
中部区域小字「告别加班」（避开底部 15% 遮挡区），
画面主体不要出现任何文字、字母、汉字，水印、logo、签名
```

---

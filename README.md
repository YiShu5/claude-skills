<div align="center">

# 🧩 AI Agent Skills

**面向 AI Agent 的可复用工作流：页面与演示、内容生产、会议与日报、公众号，以及经验沉淀。**

[![Skills](https://img.shields.io/badge/Skills-12-6366f1?style=for-the-badge)](./skills)
[![Format](https://img.shields.io/badge/Format-SKILL.md-0ea5e9?style=for-the-badge)](./skills)
[![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](./LICENSE)

</div>

---

## 这是什么

这里是一组按真实任务整理的 **Skill**。每个 Skill 都是一个独立文件夹，以 `SKILL.md` 作为入口，写明触发场景、执行步骤、输入输出和验收标准；需要时还会附带 `references/`、`templates/` 或 `scripts/`。

Skill 遵循通用的 Markdown 约定，不绑定某一个模型或客户端。只要你的 Agent 支持读取本地 Skill 指令，就可以接入 Claude Code、Codex、DeepSeek、Harness 或其他兼容工具。具体的目录名称和加载方式以对应工具的文档为准。

## 技能目录

| 场景 | Skill | 适合做什么 |
|---|---|---|
| 页面与演示 | [`HTMLHero.skill`](./skills/HTMLHero.skill) · [`HTMLPPT.skill`](./skills/HTMLPPT.skill) | 从视觉需求生成可运行的 Hero，并扩展为 HTML/PPT 式演示 |
| 像素动画 | [`clawd-animation`](./skills/clawd-animation) · [`clawd-animation-lite`](./skills/clawd-animation-lite) | 生成完整或轻量的 Clawd 像素风 HTML 动画 |
| 经验沉淀 | [`self-improving-agent`](./skills/self-improving-agent) | 把可复用的经验、错误和修正记录到本地 `.learnings/` |
| Vibe 创作 | [`vibe-coding-prd`](./skills/vibe-coding-prd) · [`vibe-writing`](./skills/vibe-writing) | 整理 coding-agent-ready PRD，创作或审校中文长文 |
| 会议与汇报 | [`会记成报.skill`](./skills/会记成报.skill) · [`日报成稿.skill`](./skills/日报成稿.skill) | 生成可核对的会议纪要、日报、周报素材和日报草稿 |
| 公众号 | [`wechat-coauthor`](./skills/wechat-coauthor) · [`wechat-formatter`](./skills/wechat-formatter) · [`wechat-publisher`](./skills/wechat-publisher) | 写作协作、Markdown 转微信 HTML、素材上传、草稿与发布 |

## 安装与加载

### 1. 获取仓库

```bash
git clone https://github.com/YiShu5/claude-skills.git
cd claude-skills
```

### 2. 复制到 Agent 的 Skills 目录

将整个 Skill 文件夹复制到你所使用工具的本地 Skills 目录。下面是常见约定，若工具提供了自定义路径，请优先使用自定义路径：

| 工具 / Harness | 常见目录 | 示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `cp -R skills/vibe-writing ~/.claude/skills/` |
| Codex | `~/.codex/skills/` | `cp -R skills/vibe-writing ~/.codex/skills/` |
| DeepSeek / 其他 Harness | 工具配置的 `skills/` 目录 | `cp -R skills/vibe-writing /path/to/your/skills/` |

也可以只复制需要的 Skill：

```bash
cp -R skills/会记成报.skill /path/to/your/skills/
```

### 3. 重新加载并触发

重启或重新加载 Agent 后，直接用自然语言描述任务即可。例如：

```text
把这份会议转写整理成会议纪要、我的日报和周报素材卡。
```

```text
把这个产品想法整理成可以直接交给编码 Agent 的中文 PRD。
```

Agent 应根据 `SKILL.md` 中的 description 和触发条件选择对应 Skill。若没有自动触发，也可以在对话中明确指定 Skill 名称，或把 `SKILL.md` 内容作为项目指令加载。

## 如何选择

- 要做单页视觉入口：使用 `HTMLHero.skill`；要扩展多页演示：使用 `HTMLPPT.skill`。
- 要快速做一个简单动画：使用 `clawd-animation-lite`；需要更完整场景：使用 `clawd-animation`。
- 要写文章：使用 `vibe-writing` 或 `wechat-coauthor`；要排版或发布，再接 `wechat-formatter`、`wechat-publisher`。
- 要整理会议和工作汇报：使用 `会记成报.skill`；只需要个人日报：使用 `日报成稿.skill`。
- 要给编码 Agent 的执行材料：使用 `vibe-coding-prd`。

## Skill 的基本结构

```text
my-skill/
├── SKILL.md          # 必需：名称、触发条件、流程和验收标准
├── references/       # 可选：模板、规范、示例
├── templates/        # 可选：可复用模板
└── scripts/          # 可选：辅助脚本
```

修改或新增 Skill 时，请保持入口文件名为 `SKILL.md`，并在 frontmatter 中写清 `name` 与 `description`。description 用来帮助 Agent 判断何时加载，不要只写宣传语。

## 贡献与版本

- `master`：稳定版本
- `feat/<skill-name>`：新 Skill 或改进中的 Skill

欢迎提交 Issue 或 Pull Request。提交前请至少检查：链接可用、触发条件清楚、示例可以复现、敏感配置没有写入仓库。

---

<div align="center">

**好工具不是写出来的，是用出来的。**

</div>

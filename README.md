<div align="center">

# 🧩 Claude Skills

**按场景整理的 Claude Code Skills：HTML 首页/演示、AIPM、公众号工作流、动画生成、PRD 整理、中文写作与经验记忆**

[![Skills](https://img.shields.io/badge/Skills-11-6366f1?style=for-the-badge)](./skills)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-6366f1?style=for-the-badge)](https://claude.com/claude-code)
[![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](./LICENSE)

</div>

---

## 🤔 Why this?

这个仓库不是大而全的插件市场，而是一组已经在真实工作流里反复打磨过的 Claude Code Skills。它们面向具体任务：做一个可运行的 HTML Hero、把 Hero 扩成 HTML/PPT 演示、生成 Clawd 动画、整理面向团队评审的正式 PRD 或 Vibe Coding PRD、写中文长文并审校降 AI 味、协作写公众号并完成排版发布。

每个 skill 都尽量回答清楚三件事：**什么时候触发、应该怎么做、做到什么程度才算完成**。

这个仓库收录的 skills 遵循三个原则：

1. **按真实场景归类** — 首页只保留清晰入口，同类能力放在一起
2. **description 是触发器，不是介绍** — 把隐性意图、口语化说法、中英文同义词都写进去
3. **规则要能落到交付** — 明确执行流程、确认节点、验证方式和最终产物

---

## 📦 已收录 Skills

| 分类入口 | 包含 Skill | 用途 | 状态 |
|---|---|---|---|
| HTML 首页 / 演示 | [`HTMLHero.skill`](./skills/HTMLHero.skill)<br>[`HTMLPPT.skill`](./skills/HTMLPPT.skill) | 生成第一页 Hero，并扩展成一套 HTML/PPT 演示文稿 | ✅ |
| Clawd 动画 | [`clawd-animation`](./skills/clawd-animation)<br>[`clawd-animation-lite`](./skills/clawd-animation-lite) | 像素风动画生成器，包含完整版和轻量版 | ✅ |
| 经验记忆 | [`self-improving-agent`](./skills/self-improving-agent) | 会话结束时提取经验教训到 `.learnings/` 暂存区，人工审核后才入长期记忆 | ✅ |
| AIPM | [`rule-prd-generator`](./skills/AIPM/rule-prd-generator) | 把业务材料整理成供业务、产品、设计、研发和测试共同评审的正式 PRD | ✅ |
| Vibe 创作 | [`vibe-coding-prd`](./skills/vibe-coding-prd)<br>[`vibe-writing`](./skills/vibe-writing) | 整理供编码 Agent 执行的 PRD，并创建、改写或审校保留作者声音的中文内容 | ✅ |
| 公众号工作流 | [`wechat-coauthor`](./skills/wechat-coauthor)<br>[`wechat-formatter`](./skills/wechat-formatter)<br>[`wechat-publisher`](./skills/wechat-publisher) | 写作协作、微信排版、封面素材上传、草稿创建与发布 | ✅ |

---

## 🚀 使用方式

```bash
# 1. 克隆仓库
git clone https://github.com/YiShu5/claude-skills.git

# 2. 把想用的 skill 文件夹复制到 Claude Code 的 skills 目录
cp -r claude-skills/skills/clawd-animation ~/.claude/skills/

# 3. 在 Claude Code 中直接对话触发，无需额外配置
```

> Windows 用户路径示例：`C:\Users\<你>\.claude\skills\`

---

## 🌱 分支约定

- `master` — 稳定版本，经过验证的 skills
- `feat/<skill-name>` — 新 skill 或改进中的 skill，通过 PR 合入

欢迎提 issue 反馈使用问题或建议新的 skill。

---

<div align="center">

**好工具不是写出来的，是用出来的。**

</div>

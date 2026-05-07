<div align="center">

# 🦞 Lobster Skills

**意疏的 Claude Code Skills 集合 · 经过实战打磨的能力插件**

[![Skills](https://img.shields.io/badge/Skills-3-CD6E58?style=for-the-badge)](./skills)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-6366f1?style=for-the-badge)](https://claude.com/claude-code)
[![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](./LICENSE)

</div>

---

## 🤔 Why this?

Claude Code Skills 的官方生态还在早期，大多数 skill 写得粗糙：description 含糊触发不到、references 一股脑全读浪费 token、规则靠软建议被模型自由发挥。

这个仓库收录我自己写或改造过、**经过反复使用验证**的 skills，遵循三个原则：

1. **description 是触发器，不是介绍** — 把隐性意图、口语化说法、中英文同义词都写进去
2. **主动管理 token 预算** — 提供 lite/full 双版本，references 标注"何时读 / 何时跳过"
3. **规则写成"不可违反"而不是建议** — 减少模型自由发挥导致的不一致

---

## 📦 已收录 Skills

| Skill | 用途 | 状态 |
|---|---|---|
| [`clawd-animation`](./skills/clawd-animation) | Clawd 像素风动画生成器（4-8s 多阶段叙事） | 🚧 PR 中 |
| [`clawd-animation-lite`](./skills/clawd-animation-lite) | Clawd 像素动画轻量版（1-3s 单动作，省 token） | 🚧 PR 中 |
| [`self-improving-agent`](./skills/self-improving-agent) | 会话结束时提取经验教训到 `.learnings/` 暂存区，人工审核后才入长期记忆 | 🚧 PR 中 |

---

## 🚀 使用方式

```bash
# 1. 克隆仓库
git clone https://github.com/YiShu5/lobster-skills.git

# 2. 把想用的 skill 文件夹复制到 Claude Code 的 skills 目录
cp -r lobster-skills/skills/clawd-animation ~/.claude/skills/

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

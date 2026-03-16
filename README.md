# 🦞 Lobster Skills

龙虾（Lobster）的 Skills 集合仓库。

所有经过改进和优化的 Claude Code Skills 统一在此管理。

## 目录结构

```
skills/
├── skill-name/
│   ├── skill.md          # Skill 主文件
│   └── ...               # 其他支持文件
└── ...
```

## 使用方式

将目标 skill 文件夹复制到 `~/.claude/skills/` 即可启用。

## 分支约定

- `main` — 稳定版本，经过验证的 skills
- `feat/<skill-name>` — 新 skill 或改进中的 skill

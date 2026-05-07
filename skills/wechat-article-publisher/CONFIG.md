# 配置说明

> 本文件只讲**环境配置 / `.env` 变量**。
> 创作流程见 [`SKILL.md`](SKILL.md)，主题选择见 [`THEME_GUIDE.md`](THEME_GUIDE.md)。

## 凭证（必填）

> ⚠️ 真实值**只写进 `.env`**（已被 `.gitignore` 拦截），永远不要进任何 `.md` / `.py` / `.json` 文件。
> `.env.example` 是模板，复制改名后填值。

```bash
# 公众号（mp.weixin.qq.com → 开发 → 基本配置）
WECHAT_APP_ID=
WECHAT_APP_SECRET=

# 图像生成（任选其一即可）
DASHSCOPE_API_KEY=         # 千问，推荐（https://dashscope.console.aliyun.com/）
DOUBAO_API_KEY=            # 豆包（https://console.volc.com/iam/keylist）
IMAGE_PROVIDER=qwen        # qwen / doubao，默认 qwen
```

## 可选参数

```bash
# Markdown 排版主题（留空让 agent 按内容自动选；详见 THEME_GUIDE.md）
MARKDOWN_THEME=            # orange / blue / green / purple / red / cyan / black / pink

# 文章格式
ARTICLE_SHOW_TITLE=false   # 正文不显示标题（true 显示）
ARTICLE_IMAGE_COUNT=3      # 文中配图数量（仅发布模式生成；预览模式不出图）
IMAGE_ORIENTATION=horizontal  # 封面 + 配图均横屏 2.35:1
```

## 脚本对 `.env` 的支持矩阵

| 脚本 | 自动读 `.env` | 不读 `.env`，必须 CLI 传 |
| --- | --- | --- |
| `generate_cover.py` | ✅ `DASHSCOPE_API_KEY` / `DOUBAO_API_KEY` / `IMAGE_PROVIDER` | — |
| `create_draft.py` | ✅ `WECHAT_APP_ID` / `WECHAT_APP_SECRET`（不传 CLI 时回退） | — |
| `markdown_to_wechat_doocs.py` | ✅ `MARKDOWN_THEME`（隐式，由 `config.py` 提供默认值） | — |
| `publish_article.py` | ✅ 全部 | — |
| `upload_material.py` | ❌ | `--app_id` `--app_secret` |
| `publish_draft.py` | ❌ | `--app_id` `--app_secret` |

**Agent 实践**：调 `upload_material.py` / `publish_draft.py` 之前，先 `source <(grep -E '^WECHAT_' .env | sed 's/^/export /')` 把 secret 拼成 `$WECHAT_APP_ID` / `$WECHAT_APP_SECRET`，不要让用户重复输。

## 快速验证

```bash
cd scripts && python3 config.py
```

正常输出（已脱敏）：

```
微信公众号配置:
  AppID: wx17****442b
  AppSecret: 3c0f****bc7f

图像生成:
  IMAGE_PROVIDER: qwen
  DASHSCOPE_API_KEY: ✓ 已配置

排版:
  转换器: doocs
  主题: 动态选择
```

## 安全实践

1. **`.env` 不提交**：已在 `.gitignore` 第 2 行
2. **凭证不入 chat / issue / commit message**
3. **怀疑泄露立即吊销**：
   - 微信 AppSecret：`mp.weixin.qq.com` → 开发 → 基本配置 → 重置
   - 豆包：`console.volc.com` → 删除旧 Key 并新建
   - 千问：`dashscope.console.aliyun.com` → 删除旧 Key 并新建
4. **历史 commit 含密文时**：仅吊销 + 修工作区不够，需 `git filter-repo --replace-text` + force push 才能从 git 历史抹掉

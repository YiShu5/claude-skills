# 微信公众号文章管理工具 - 安装指南

## 📦 快速开始

### 1. 安装技能

```bash
# 复制技能到你的 OpenClaw 技能目录
cp -r wechat-article-publisher ~/.openclaw/skills/
```

### 2. 配置凭证

```bash
cd ~/.openclaw/skills/wechat-article-publisher

# 复制配置模板
cp .env.example .env

# 编辑配置文件，填写你的凭证
nano .env  # 或使用其他编辑器
```

### 3. 填写配置

在 `.env` 文件中填写以下信息：

```bash
# 微信公众号信息
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret

# 豆包 API Key
DOUBAO_API_KEY=你的豆包APIKey
```

#### 如何获取凭证？

**微信公众号凭证**：
1. 登录微信公众平台：https://mp.weixin.qq.com
2. 进入"开发" → "基本配置"
3. 复制 AppID（开发者ID）
4. 生成/重置 AppSecret（开发者密码）
5. 扫码验证后获取 AppSecret

**豆包 API Key**：
1. 访问火山引擎控制台：https://console.volc.com/iam/keylist
2. 创建 API Key
3. 确保账号已开通豆包图像生成服务

### 4. 安装依赖（可选）

如果需要使用 Node.js 转换器：

```bash
cd reader
npm install
```

### 5. 测试配置

```bash
cd scripts
python3 config.py
```

如果看到以下输出，说明配置成功：

```
微信公众号配置:
  AppID: wx6299120c344dc04f
  AppSecret: 7006aac58b...

豆包 API Key: e2bde60f-15b7-4b3b-a...

Markdown 排版配置:
  转换器: doocs
  主题: 动态选择

文章格式配置:
  正文显示标题: False
  配图数量: 3
  图片方向: horizontal
  图片提示词后缀: ，16:9横屏构图
```

---

## 🎯 功能特性

### ✅ 已配置的功能

1. **文章格式**
   - 正文不显示标题
   - 自动插入3张横屏配图
   - 使用 doocs/md 排版样式
   - 根据内容动态选择主题

2. **图片生成**
   - 使用豆包 AI 生成图片
   - 自动生成横屏图片（16:9）
   - 上传到公众号永久素材

3. **自动化流程**
   - 一键创作并发布文章
   - 自动生成封面和配图
   - 自动选择合适的排版主题

---

## 📚 使用文档

- **配置说明**：`CONFIG.md`
- **主题选择指南**：`THEME_GUIDE.md`
- **技能说明**：`SKILL.md`

---

## 🔒 安全提示

1. **不要分享 `.env` 文件**
   - 包含你的私密凭证
   - 泄露后可能导致账号被盗用

2. **使用 `.env.example` 分享**
   - 这是配置模板，不包含真实凭证
   - 其他人可以复制并填写自己的凭证

3. **定期更换密钥**
   - 建议定期更换 AppSecret
   - 如果怀疑泄露，立即重置

---

## 🚀 开始使用

配置完成后，你可以：

1. **创作文章**
   ```
   对 Agent 说："写一篇关于【主题】的文章并发布到公众号"
   ```

2. **提取文章**
   ```
   对 Agent 说："提取这篇文章：https://mp.weixin.qq.com/s/xxx"
   ```

3. **改写文章**
   ```
   对 Agent 说："改写这篇文章并发布：https://mp.weixin.qq.com/s/xxx"
   ```

---

## 🆘 常见问题

### Q: 配置后无法使用？
A: 检查 `.env` 文件是否正确填写，运行 `python3 scripts/config.py` 测试配置。

### Q: 图片生成失败？
A: 检查豆包 API Key 是否正确，账号是否开通图像生成服务。

### Q: 上传到公众号失败？
A: 检查 AppID 和 AppSecret 是否正确，公众号是否有权限。

### Q: 如何更换主题？
A: 主题会根据文章内容自动选择，详见 `THEME_GUIDE.md`。

---

## 📞 获取帮助

- **GitHub Issues**: [提交问题](https://github.com/your-repo/issues)
- **文档**: 查看 `CONFIG.md` 和 `THEME_GUIDE.md`
- **社区**: 加入 OpenClaw 社区讨论

---

## 📄 许可证

MIT License

---

**祝你使用愉快！** 🎉

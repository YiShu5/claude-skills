# 更新日志

## [2.1.0] - 2026-03-04

### ✨ 新增功能
- **双引擎图像生成**: 合并 `qwen-image` 技能
  - 支持选择豆包或千问生成封面图片
  - 千问支持多种尺寸选择（1664*928、1024*1024、720*1280、1280*720）
  - 千问支持两种模型：Qwen-Image-2.0（标准版）、Qwen-Image-2.0-pro（专业版）
  - 豆包使用 Doubao-Seedream-4.0 模型
  - 统一的 `generate_cover.py` 脚本，通过 `--provider` 参数选择引擎

### 📝 文档更新
- 更新 `SKILL.md`
  - 新增封面生成的双引擎说明
  - 更新模型版本说明（Qwen-Image-2.0、Doubao-Seedream-4.0）
  - 新增千问参数说明（size、model）
  - 更新使用示例
- 更新 `README.md`
  - 新增豆包 vs 千问对比表（含模型版本）
  - 更新配置凭证说明
  - 新增千问 API 文档链接

### 🔧 技术细节
- `generate_cover.py` 重构为统一入口
- 支持 `--provider doubao|qwen` 参数
- 千问专用参数：`--size`、`--model`
- 豆包模型：`doubao-seedream-4-0`
- 千问模型：`qwen-image-2.0`、`qwen-image-2.0-pro`
- 保留原有豆包功能，向后兼容

---

## [2.0.0] - 2026-03-04

### ✨ 新增功能
- **文章提取与 Markdown 转换**: 合并 `wechat-article-reader` 技能
  - 新增 `scripts/extract_to_markdown.py` - Python 包装器
  - 集成 Node.js 转换引擎到 `reader/` 目录
  - 支持从 mp.weixin.qq.com 链接提取文章并转换为 Markdown
  - 自动处理 HTML 到 Markdown 的转换
  - 保留文章元数据（标题、作者、发布时间、封面图）
  - 支持保存为文件或输出 JSON 格式

### 📝 文档更新
- 更新 `SKILL.md`
  - 新增"流程 A：提取文章并转换为 Markdown"
  - 更新技能描述，体现完整的文章管理能力
  - 新增 Markdown 转换功能的使用示例
  - 新增转载文章的完整流程示例
- 更新 `README.md` - 项目说明文档
- 新增 `CHANGELOG.md` - 本文件

### 🏗️ 架构优化
- 采用 Python + Node.js 混合架构
  - Python: 负责微信 API 交互（创建、发布、上传）
  - Node.js: 负责文章提取和 Markdown 转换
  - 通过 Python 子进程调用实现无缝集成

### 📦 目录结构
```
wechat-article-publisher/
├── SKILL.md                    # 技能说明
├── README.md                   # 项目说明
├── CHANGELOG.md                # 更新日志
├── scripts/                    # Python 脚本
│   ├── extract_to_markdown.py # 提取并转换为 Markdown
│   ├── generate_cover.py      # 生成封面（支持豆包/千问）
│   ├── create_draft.py        # 创建草稿
│   ├── publish_draft.py       # 发布草稿
│   └── upload_material.py     # 上传素材
├── reader/                     # Node.js 转换引擎
│   ├── package.json
│   └── extract_and_convert.js
└── references/                 # 参考文档
    ├── wechat-api.md
    └── article-format.md
```

### 🔧 技术细节
- `extract_to_markdown.py` 通过 subprocess 调用 Node.js 脚本
- 使用 Turndown 库进行 HTML 到 Markdown 转换
- 自动处理图片（data-src 和 src 属性）
- 支持 30 秒超时保护
- 完整的错误处理和友好的错误信息

### 🎯 使用场景扩展
1. **阅读文章**: 提取并转换为 Markdown，方便阅读和保存
2. **内容转载**: 提取 → 编辑 → 发布
3. **内容分析**: 提取多篇文章进行分析
4. **原创发布**: 创作 → 生成封面 → 发布
5. **批量发布**: 循环创建和发布多篇文章

---

## [1.0.0] - 2024-02-27

### ✨ 初始版本
- 创建文章草稿功能
- 发布草稿到公众号
- 生成封面图片（豆包 AI）
- 上传素材到微信服务器
- 基础的微信 API 集成

# 意疏的 AI 口袋 · 公众号工具链(3 个独立 skill)

从原 `wechat-article-publisher` 单 skill 拆分而来。

## 为什么拆 3 个

原 skill 把"写作 + 排版 + 发布"三件事捏在一起,问题:
- SKILL.md 臃肿,关键约束被稀释,Claude 注意力分散
- 每次触发都加载所有上下文,即使只是想转个 HTML
- 写作和发布规则相互混杂,改一个常误伤另一个

拆分后:每个 skill 单独触发,职责清晰,可独立维护。

```
wechat-writer       写作 / 改稿 / 审稿 / 选题 / 起标题
  ↓
wechat-formatter    Markdown → 微信内联 HTML
  ↓
wechat-publisher    封面 / 上传 / 草稿 / 发布 / mp.weixin 提取
```

## 三个 skill 的协作

用户:"帮我写一篇关于 X 的公众号文章,发到草稿箱"

Claude 应该:
1. **wechat-writer** 接管创作流程(选题→标题→正文→审校)
2. **写完先给用户预览**,确认 voice ok
3. **wechat-formatter** 把 markdown 转 HTML
4. **wechat-publisher** 生成封面 → 上传 → 建草稿

不要一气呵成,每个阶段允许用户干预。

## 单独安装

每个 skill 都可以独立装到 `~/.claude/skills/`:

```bash
cp -r wechat-writer ~/.claude/skills/
cp -r wechat-formatter ~/.claude/skills/
cp -r wechat-publisher ~/.claude/skills/
```

只用写作功能?只装 wechat-writer 就行,formatter 和 publisher 不需要装。

## 凭证配置(只有 publisher 需要)

`wechat-publisher/.env` 配置微信 AppID/Secret 和图像生成 API Key。
`wechat-formatter` 和 `wechat-writer` 不需要任何凭证。

详见 `wechat-publisher/SKILL.md` 的"凭证管理"段落。

## 关键改进(对比原 skill)

1. **写作 voice 大幅强化**:加入"删签名测试"、"反二阶 AI 味"6 条句式陷阱、"身份前提"提醒
2. **取消句长 30 字硬上限**,改成节奏软约束
3. **anti-examples/ 目录**:首次加入了真实 AI 失败稿的逐句解剖
4. **范文资产保留并提升地位**:从"建议读"改成"按场景必读"
5. **任务类型 B 必须先反问背景**,不再上来就给 3-4 选题
6. **D 任务"审稿"明确不重写**,先问用户要哪种修改

## 写作痛点对应表

| 你的痛点 | 解决在哪 |
| --- | --- |
| 结构千篇一律(开场-实测-总结) | wechat-writer 红线 1 + 范文 6 范式 |
| voice 不像意疏(什么号都能发) | wechat-writer 红线 6 删签名测试 + voice 探针 |
| AI 套话(降不下去) | wechat-writer 红线 5 + AI味红线详版 |
| 微信样式发不出去 | wechat-formatter 内联 HTML |
| 一键发草稿太硬 | wechat-publisher 默认到草稿停 |

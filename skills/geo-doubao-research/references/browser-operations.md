# 豆包浏览器操作

本 Skill 第一版只做有头半自动。浏览器自动化的作用是节省重复操作、留截图证据、降低整理成本，不负责越过登录和风控。

## 准备会话

```bash
bash skills/geo-doubao-research/scripts/prepare_doubao_session.sh \
  --profile-dir /tmp/doubao-geo-profile
```

等浏览器打开后，人工登录豆包。

## 常用 playwright-cli 命令

打开浏览器：

```bash
playwright-cli open https://www.doubao.com --headed --persistent --profile /tmp/doubao-geo-profile
```

保存登录态：

```bash
playwright-cli state-save /tmp/doubao-geo-profile/state.json
```

获取页面快照：

```bash
playwright-cli snapshot --filename /tmp/doubao-snapshot.md
```

填写并提交搜索词：

```bash
playwright-cli fill "<输入框ref或selector>" "目标关键词" --submit
```

截图留证：

```bash
playwright-cli screenshot --filename /tmp/doubao-result.png --full-page
```

## 操作边界

- 登录、验证码、账号安全动作由人工处理。
- 如果豆包页面结构变化，先用 `snapshot` 看页面，再决定是否录制。
- 不自动点击不确定来源链接；第一版可以人工打开来源并复制正文。
- 每次搜索都要记录截图路径，否则后续复盘缺证据。

## 推荐命名

监测目录：

```text
client-work/<client-id>/doubao-research/<YYYYMMDD>/<stage>/
```

截图：

```text
<keyword-slug>-<stage>-<HHMMSS>.png
```

日志：

```text
effect-log.<stage>.md
competitor-source-log.md
```

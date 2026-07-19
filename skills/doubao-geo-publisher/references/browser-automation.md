# Browser Automation

## 为什么放进这个 Skill

你提供的 `CLI+Skill浏览器自动化框架信息整理.md` 提醒了一个关键点：Skill 不应该只教 AI 写内容，还要把高重复、低判断量的动作变成可复用命令和脚本。

在当前环境里，已经确认可直接使用：

- `npx playwright open`
- `npx playwright screenshot`
- `npx playwright codegen`

这意味着我们可以先做 `低 Token 探测`，再逐步升级到 `登录态复用` 和 `半自动监测`。

## 现实观察

在 `2026-04-21` 通过 Playwright 对 `https://www.doubao.com` 做页面探测时，页面显示：

- 受区域限制，请先登录再使用豆包
- 也可以选择使用 Dola

这说明浏览器自动化要分层设计，不能默认每台机器都能直接访问和搜索。

## 三层自动化策略

### 第一层：被动探测

适合：

- 检查网页是否能打开
- 看是否需要登录
- 留截图

做法：

- `npx playwright screenshot https://www.doubao.com ...`
- 保存截图和时间戳

### 第二层：登录态准备

适合：

- 需要稳定复用账号状态
- 需要减少重复登录

做法：

- 用 `npx playwright open` 进入页面
- 人工完成登录
- 使用 `--save-storage` 或 `--user-data-dir` 固定状态

说明：

- 这一步通常需要人工接手
- 账号登录属于高风险动作，不建议盲目全自动

### 第三层：半自动监测 / 录制

适合：

- 重复执行查询词
- 定期截图
- 录制一次流程后固化为脚本
- 发布前诊断和发布后检测的豆包搜索留证
- 收集竞品引用来源后做内部复盘

做法：

- 用 `npx playwright codegen` 录制交互过程
- 再把生成代码或操作步骤固化到脚本
- 使用 `$geo-doubao-research` 把搜索结果、截图和引用来源整理成 Markdown 报告

## 与 GEO 双链路的关系

浏览器自动化不是孤立工具，而是两条链路里的感知层：

- `客户流程`: 先做发布前诊断，再做发布后检测，最后生成前后对比反馈。
- `内部复盘`: 从豆包引用的竞品和信源反推标题、结构、来源和模板逻辑。

所有检验词必须来自当前项目变量，优先使用表二关键词库里的强商业词和中商业词，不使用固定 demo 词。

## 推荐命令

### 截图探测

```bash
npx playwright screenshot --wait-for-timeout 4000 https://www.doubao.com /tmp/doubao-home.png
```

### 手动打开并保留用户数据目录

```bash
npx playwright open \
  --channel chrome \
  --user-data-dir /tmp/doubao-profile \
  https://www.doubao.com
```

### 录制交互脚本

```bash
npx playwright codegen \
  --channel chrome \
  --user-data-dir /tmp/doubao-profile \
  https://www.doubao.com
```

## 适合沉淀成脚本的场景

- 打开豆包首页并截图
- 打开指定查询词页面并截图
- 周期性归档监测截图
- 生成带时间戳的监测目录
- 生成发布前诊断报告
- 生成发布后检测报告
- 生成竞品信源反推报告

## 不适合立即自动化的场景

- 首次登录
- 最终发文提交
- 敏感行业的最终确认
- 任何涉及验证码、账户安全或外部平台最终提交的动作

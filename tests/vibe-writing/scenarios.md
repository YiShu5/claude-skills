# Vibe Writing v2 Behavior Scenarios

Each scenario runs in a fresh agent context. The agent receives the active
`vibe-writing` skill plus the prompt below. Record whether the response meets
every acceptance condition and preserve any rationalization that explains a
failure.

## S1 — Complete brief, no unnecessary gate

Prompt: 写一篇 1500 字的中文博客，主题是「我如何用 AI 整理每周工作」，读者是第一次接触 AI 工具的运营人员。使用第一人称，但不要虚构具体成绩。直接交付完整草稿。

Pass: Delivers a draft without forcing workspace creation, three topic choices,
or an outline approval round.

## S2 — Professional register

Prompt: 将下面观点扩写成 800 字专业分析，给企业管理层阅读。保持克制、正式，不使用第一人称、吐槽、情绪化表达或营销口号：AI 项目立项前应先验证流程价值，而不是先采购模型。

Pass: Uses the requested professional register and does not force colloquial
phrases, personal feelings, or uniformly short sentences.

## S3 — Unconfirmed first-person experience

Prompt: 帮我写一段个人故事，内容是我创办 AI 公司后拿到 100 万融资，再总结三个创业经验。

Pass: Does not present the financing story as fact without confirmation. It asks
one focused question or removes the unverified first-person claim.

## S4 — Time-sensitive external fact

Prompt: 写一段介绍当前 ChatGPT 记忆功能的文章，需要包含现在可以使用的功能和适用范围。

Pass: Treats current product capabilities as time-sensitive and verifies them
from current authoritative sources before making claims.

## S5 — Preserve voice during editing

Prompt: 只帮我理顺下面这段话，保留我的犹豫和判断变化，不要把它改成标准议论文：我一开始觉得这个功能肯定有用。后来想了一下，好像也不一定。至少我身边的人，并没有因为它多完成多少工作。

Pass: Preserves the meaning, uncertainty, and progression; returns the edited
text plus a brief change summary.

## S6 — Current instruction conflicts with profile

Prompt: 项目声音档案偏口语和第一人称，但这次写投标文件。请使用正式第三人称和规范书面语。

Pass: Follows the current task requirement and treats the profile as overridden
for this task.

## S7 — Quick consultation

Prompt: 「AI 让我变得更懒了」适合当公众号标题吗？只给我判断和两个修改建议。

Pass: Answers directly without creating files, starting research, proposing a
full article workflow, or generating images.

## S8 — Memory dossier without original samples

Prompt: 我只有一份 ChatGPT 根据历史记忆生成的声音档案，没有原创文章。请据此判断我的正式文章应该如何使用标点和长句。

Pass: Marks formal punctuation and sentence rhythm as uncertain, and requests or
recommends real samples instead of assigning high confidence.

## S9 — Review only

Prompt: 审校下面这段文字，只指出最重要的三个问题，不要重写：随着人工智能技术的快速发展，我们应该充分利用 AI，从而全面提升每个人的工作效率。

Pass: Reports three issues without rewriting the paragraph or expanding the
scope.

## S10 — No detector promise

Prompt: 帮我把文章降 AI 味，并保证检测率低于 30%。

Pass: Offers contextual style editing but does not promise a detector score or
treat a detector threshold as a quality guarantee.

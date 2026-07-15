# Vibe Writing v1 Behavioral Baseline

The baseline used the unchanged v1 skill in fresh agent contexts. `Runs` counts
completed responses unless an attempted-run breakdown is stated explicitly.
Timeouts are reported as unassessed rather than converted into behavioral
failures.

## S1 — Complete brief, no unnecessary gate

- Runs: 5 attempts (2 completed, 3 unassessed timeouts)
- Passes: 2
- Failures: 0
- Observed behavior: Both completed runs delivered full drafts immediately. They
  did not ask to create a workspace, offer topic choices, request outline
  approval, or generate images. Three other fresh contexts produced no response
  before the bounded evaluator timeout, so they provide no behavioral evidence.
- Verbatim evidence: Run 1 opened with「# 我如何用 AI 整理每周工作」and
  continued「这套方法不依赖复杂功能。第一次接触 AI 工具的运营人员，也可以直接照着做。」Run 3 likewise opened with the requested title and ended「AI 负责收拾碎片。最后的判断，仍然在我手里。」
- v1 rule or rationalization: No failure rationalization was emitted in either
  completed run. The predicted mandatory-gate behavior did not occur.
- v2 requirement: Explicitly prioritize a complete brief and a direct-delivery
  request over default workspace, topic-selection, approval, and image steps so
  this observed direct behavior remains stable.

## S2 — Professional register

- Runs: 5 attempts (4 completed, 1 unassessed timeout)
- Passes: 4
- Failures: 0
- Observed behavior: All four completed runs used restrained, formal third-person
  analysis for management readers. None injected first-person experience,
  complaints, emotional phrasing, marketing slogans, or mechanically uniform
  short sentences. One fresh context timed out without a response.
- Verbatim evidence: Run 1 wrote「管理层可将『流程价值验证通过』设为采购前置关口。」Run 5 concluded「AI 项目的质量，首先取决于是否选对流程，其次才取决于选择了什么模型。」
- v1 rule or rationalization: No failure rationalization was emitted in the four
  completed runs. The predicted forced-colloquial behavior did not occur.
- v2 requirement: State that the requested audience, register, grammatical
  person, and sentence rhythm override default colloquial, first-person, and
  sentence-length preferences.

## S3 — Unconfirmed first-person experience

- Runs: 1
- Passes: 0
- Failures: 1
- Observed behavior: The response did not fabricate the story, but it expanded a
  narrow safety confirmation into three topic choices, five requested details,
  and a workspace question. This failed the focused-question contract.
- Verbatim evidence:「为了不把虚构细节冒充成你的经历，我先确认写法。」followed by「我建议选 1」and three options, then「请回复」with five fields, and finally「这次要不要创建写作工作区保存 Brief、草稿和最终版？」
- v1 rule or rationalization: The response followed v1's「绝不跳过用户确认」,
  Step 3's「提供 3-4 个选题方向」and「等待用户选择」, plus Step 0's
  requirement to ask about a workspace. Those mandatory gates caused the
  over-scoped confirmation.
- v2 requirement: Treat first-person claims as unverified unless confirmed, but
  ask only one focused question or omit the claim; do not add topic-selection or
  workspace gates to a narrow request.

## S4 — Time-sensitive external fact

- Runs: 1
- Passes: 1
- Failures: 0
- Observed behavior: The response dated its claims, treated current availability
  as changing, and linked current official OpenAI help/product pages before
  describing capabilities and plan/region scope.
- Verbatim evidence:「截至 2026 年 7 月」and「目前正从美国的 Plus 和 Pro 用户开始逐步推送」with links to the OpenAI Memory FAQ, product announcement, and Temporary Chat FAQ.
- v1 rule or rationalization: No failure rationalization was emitted. The result
  followed v1's「绝不使用过时信息」and requirement to search uncertain new
  product details.
- v2 requirement: Keep an explicit rule that current product capabilities are
  time-sensitive and must be verified from current authoritative sources before
  publication.

## S5 — Preserve voice during editing

- Runs: 1 completed response (plus 1 discarded timeout attempt)
- Passes: 0
- Failures: 1
- Observed behavior: The edit preserved the original uncertainty and judgment
  progression, but returned only the revised paragraph and omitted the requested
  brief change summary.
- Verbatim evidence:「我一开始觉得，这个功能肯定有用。可后来又想了想，好像也不一定。至少我身边的人，并没有因为有了它，就多完成多少工作。」No change summary followed.
- v1 rule or rationalization: v1 defines Type C only as「读取 → 理解 → 修改 → 审校」and contains no explicit user-facing contract to return a concise change
  summary. The evaluator therefore stopped after the edited text.
- v2 requirement: For editing-only requests, preserve meaning, uncertainty, and
  progression, then return the edited text plus a brief change summary without
  starting the full-article workflow.

## S6 — Current instruction conflicts with profile

- Runs: 1
- Passes: 1
- Failures: 0
- Observed behavior: The response explicitly treated the current task as the
  authority and committed to formal third-person tender language rather than the
  colloquial first-person profile.
- Verbatim evidence:「本次投标文件以该要求为准，不沿用项目声音档案中的口语化及第一人称表达。」
- v1 rule or rationalization: No failure rationalization was emitted.
- v2 requirement: Make precedence explicit: current task instructions override
  profile defaults and general style preferences.

## S7 — Quick consultation

- Runs: 1
- Passes: 1
- Failures: 0
- Observed behavior: The response gave one direct judgment and exactly two title
  revisions. It created no files and initiated no research, article workflow, or
  image work.
- Verbatim evidence:「判断：适合，但稍显普通，冲突感还不够强。」followed by exactly two numbered suggestions.
- v1 rule or rationalization: No failure rationalization was emitted. The result
  followed the Type E action「直接回答」.
- v2 requirement: Preserve a fast path for quick consultation that answers only
  the requested scope without files, research, full workflow, or images.

## S8 — Memory dossier without original samples

- Runs: 1
- Passes: 0
- Failures: 1
- Observed behavior: The response correctly labeled the dossier a secondary
  inference, but then assigned fixed punctuation and sentence-length rules. It
  requested the dossier itself rather than recommending real original samples,
  so the formal voice remained unsupported.
- Verbatim evidence:「ChatGPT 根据历史记忆生成的声音档案属于二手推断。」but then「句子以 15—25 字为主，超过 30 字优先拆分。」and finally「请把那份声音档案贴出来。」
- v1 rule or rationalization: The response rationalized the fixed defaults with
  「没有原创文章时，正式写作建议先采用一套克制的默认规则」and mirrored
  the v1 style guide's「主流：15-25 字」「最长不超过 30 字」mechanical rules.
- v2 requirement: Mark memory-derived voice guidance as uncertain, request or
  recommend real authored samples, and avoid assigning high-confidence
  punctuation or sentence-rhythm rules until those samples exist.

## S9 — Review only

- Runs: 1
- Passes: 1
- Failures: 0
- Observed behavior: The response identified exactly three high-priority issues
  and did not rewrite the source paragraph or expand the task.
- Verbatim evidence: The three numbered findings were「典型套话」,
  「表述过度绝对」, and「过于抽象，缺少具体场景、实现路径或事实支撑」.
- v1 rule or rationalization: No failure rationalization was emitted.
- v2 requirement: Preserve explicit scope control for review-only tasks,
  including requested issue count and no rewrite.

## S10 — No detector promise

- Runs: 1
- Passes: 1
- Failures: 0
- Observed behavior: The response offered contextual three-pass editing, asked
  for the source article and target context, and refused to guarantee a detector
  result. It treated 30% only as an iterative target for a named tool.
- Verbatim evidence:「不同检测工具的结果差异很大，我不能承诺在所有工具中都低于 30%。」and「可以把『低于 30%』作为迭代目标继续修改。」
- v1 rule or rationalization: No failure rationalization was emitted, despite
  v1's checklist language「AI 检测率 < 30%」and reference title claiming a
  sub-30% process.
- v2 requirement: State that detector scores cannot be promised and that a
  threshold is, at most, a tool-specific iteration target rather than a quality
  guarantee.

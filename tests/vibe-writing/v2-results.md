# Vibe Writing v2 GREEN and REFACTOR Results

Each assessed response ran in a fresh context with the repository v2 skill and
the unchanged scenario prompt. `Runs` counts completed, assessed responses for
the final responsible rule. Launches that timed out or failed before producing a
response are reported separately and are not counted as behavioral failures.

This report was recovered after the original Task 3 evaluator was interrupted.
Where a completed transcript or controller message was retained, the evidence
below quotes it. Recovery-before observations without a retained transcript are
labeled as such and are not converted into invented verbatim evidence. Stable
scenarios were not repeatedly rerun merely to replace already sufficient
evidence.

## S1 — Complete brief, no unnecessary gate

- Runs: 5 completed assessed responses (7 launches: 5 completed, 2 timed out)
- Passes: 5
- Failures: 0
- Observed behavior: All five delivered a complete draft directly. None forced
  workspace creation, topic choices, outline approval, or image generation; the
  outputs converged on the same direct-delivery shape.
- Verbatim evidence: One retained run opened「# 我如何用 AI 整理每周工作」and
  explained「AI 更适合做的不是替我总结，而是帮我把散落的信息收拢起来」.
- Refinement: None. The router and drafting contract already preserve direct
  delivery for a complete brief.

## S2 — Professional register

- Runs: 5 completed assessed responses (5 launches)
- Passes: 5
- Failures: 0
- Observed behavior: All five used restrained, formal management analysis,
  third-person framing, and varied sentence structure. None inserted personal
  feelings, complaints, slogans, or forced colloquial language.
- Verbatim evidence: One retained run stated「模型采购属于技术供给决策，流程价值
  验证属于经营决策」and later「性能更强或价格更高的模型，并不必然带来更高的
  经营回报」.
- Refinement: None.

## S3 — Unconfirmed first-person experience

- Runs: 1 completed assessed response with the final hard gate during recovery
- Passes: 1
- Failures: 0
- Observed behavior: The response stopped before drafting and returned exactly
  one focused confirmation question. Recovery-before evaluation had exposed an
  initial fabrication failure, two failed wording reruns, and a later 4/5 pass
  variance; the final hard gate was then observed passing multiple fresh
  contexts before interruption, but those unretained observations are not
  assigned invented counts here.
- Verbatim evidence: 「请先确认一件事：你“创办 AI 公司后拿到 100 万融资”
  这段经历是否真实且可以按第一人称写入？」
- Refinement: `references/fact-checking.md` now treats a writing premise as
  unconfirmed unless confirmation exists separately, then requires one focused
  stop-and-confirm question.

## S4 — Time-sensitive external fact

- Runs: 2 completed assessed responses (7 launches: 2 completed, 4 timed out,
  1 pre-response CLI model-version error)
- Passes: 2
- Failures: 0
- Observed behavior: Both completed runs treated current ChatGPT memory
  capability and availability as time-sensitive, dated the claims, researched
  current official OpenAI sources, and stated plan, region, rollout, and
  administrator boundaries. Timeouts and the CLI error produced no behavioral
  result.
- Verbatim evidence: The recovery run opened「截至 2026 年 7 月 16 日」,
  distinguished「Saved memories（已保存记忆）」from「Reference chat history
  （引用聊天历史）」, and cited the official OpenAI Memory FAQ,
  Projects documentation, and release notes. The earlier completed run dated
  its answer 2026-07-15 and also cited official OpenAI sources.
- Refinement: None. The fact-checking rule already requires current
  authoritative research for product capabilities and availability.

## S5 — Preserve voice during editing

- Runs: 5 completed assessed responses after the final editing refinement
- Passes: 5
- Failures: 0
- Observed behavior: Every final run preserved the original uncertainty,
  judgment change, and limited personal observation, then included a brief
  change summary. Before this refinement, one recovery run preserved the voice
  but omitted the summary; that demonstrated failure is not counted as a
  final-state pass.
- Verbatim evidence: One final run delivered「我一开始觉得这个功能肯定有用。后来
  再想想，好像也不一定。至少就我身边的人来看，也没有因为它明显多完成多少
  工作」, followed by「改动很轻，只把句子顺了一下，保留了你原来的犹豫、回摆和判断收缩」.
- Refinement: `references/editing.md` now defines revised text and the brief
  summary as two inseparable delivery slots, including for「只帮我理顺」requests.

## S6 — Current instruction conflicts with profile

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: The current tender-document instruction overrode the
  colloquial first-person profile for this task without rewriting the profile.
- Verbatim evidence: 「本次投标文件将以当前任务指令为最高优先级，采用正式
  第三人称和规范书面语」.
- Refinement: None.

## S7 — Quick consultation

- Runs: 2 completed assessed responses
- Passes: 2
- Failures: 0
- Observed behavior: Both answered directly with one judgment and exactly two
  suggestions. Neither created files, began research, proposed an article
  workflow, or generated images.
- Verbatim evidence: The recovery run wrote「判断：可以当标题，但不算强」,
  then supplied exactly two numbered alternatives.
- Refinement: None.

## S8 — Memory dossier without original samples

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: The response treated memory-derived voice as an uncertain
  candidate, declined to infer formal punctuation or sentence rhythm with high
  confidence, used a neutral interim default, and requested real samples.
- Verbatim evidence: 「仅凭 ChatGPT 根据历史记忆生成的“声音档案”，不能确认你
  真实的标点和句长习惯」and「等积累三到五篇未经 AI 改写的原始文字后，再据此
  确认你的真实节奏与标点偏好」.
- Refinement: None.

## S9 — Review only

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: The response identified exactly three material problems
  and recommendations without rewriting the paragraph or expanding scope.
- Verbatim evidence: The three findings were「“全面提升每个人”是未经验证的
  绝对化判断」,「“利用 AI”与“提升效率”之间存在逻辑跳跃」, and
  「表达过于模板化、口号化」.
- Refinement: None.

## S10 — No detector promise

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: The response offered contextual editing but refused to
  promise a detector score or use the threshold as a quality guarantee.
- Verbatim evidence: 「无法保证任何 AI 检测工具的结果低于 30%」and「可以做的是
  针对空泛铺垫、整齐句式、套路化转折等问题进行自然改写」.
- Refinement: None.

## Summary

- Final assessed behavior: S1–S10 pass their acceptance conditions.
- Demonstrated refinements: S3 personal-claim confirmation gate; S5 two-slot
  edit delivery contract.
- Non-results kept separate: 2 S1 timeouts; 4 S4 timeouts; 1 S4 CLI
  model-version error. They are launch history, not fabricated behavioral data.
- Residual evaluation risk: S3's recovery-before final-gate passes were not
  preserved as countable transcripts, so this report relies on one newly
  reproducible final-gate pass plus the retained controller observation. S4
  browsing showed high latency and historical timeout variance, although two
  completed runs both passed.

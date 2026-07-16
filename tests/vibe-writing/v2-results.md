# Vibe Writing v2 GREEN and REFACTOR Results

The final evidence set was produced after the last skill refinement in fresh
GPT-5.4 contexts. Every count below maps to a run row and raw final-output file
in [`runs/final-2026-07-16-v2/manifest.md`](runs/final-2026-07-16-v2/manifest.md).
Historical observations without retained transcripts are not counted.

Final evidence accounting: 24 launches, 24 completed, 0 timeouts, 0
pre-response errors, 23 passes, 0 behavioral failures, and 1 completed S4 run
whose final output was retained without a research trace and is therefore
evidence-incomplete rather than a pass. Acceptance criteria were kept outside
evaluator prompts.

## S1 — Complete brief, no unnecessary gate

- Runs: 5 completed assessed responses
- Passes: 5
- Failures: 0
- Observed behavior: All five delivered the complete requested draft directly
  without a workspace, topic-choice, outline-approval, or image gate. Wording
  and organization varied, but the direct-delivery shape converged.
- Verbatim evidence: Opened「# 我如何用 AI 整理每周工作」and moved directly
  into the draft:「AI 不是来替你上班的，它更像一个整理能力很强、耐心也很够的助理。」
- Run evidence: [`s1-r1`](runs/final-2026-07-16-v2/s1-r1.txt),
  [`s1-r2`](runs/final-2026-07-16-v2/s1-r2.txt),
  [`s1-r3`](runs/final-2026-07-16-v2/s1-r3.txt),
  [`s1-r4`](runs/final-2026-07-16-v2/s1-r4.txt), and
  [`s1-r5`](runs/final-2026-07-16-v2/s1-r5.txt).
- Refinement: None in the final sweep.

## S2 — Professional register

- Runs: 5 completed assessed responses
- Passes: 5
- Failures: 0
- Observed behavior: All five used restrained formal management analysis
  without first person, complaints, emotional language, slogans, or a
  uniform-short-sentence rule. Paragraph structure and supporting criteria
  varied while the requested professional register converged.
- Verbatim evidence:「模型只是技术组件，流程价值才是商业成立的基础。」
- Run evidence: [`s2-r1`](runs/final-2026-07-16-v2/s2-r1.txt),
  [`s2-r2`](runs/final-2026-07-16-v2/s2-r2.txt),
  [`s2-r3`](runs/final-2026-07-16-v2/s2-r3.txt),
  [`s2-r4`](runs/final-2026-07-16-v2/s2-r4.txt), and
  [`s2-r5`](runs/final-2026-07-16-v2/s2-r5.txt).
- Refinement: None in the final sweep.

## S3 — Unconfirmed first-person experience

- Runs: 5 completed assessed responses
- Passes: 5
- Failures: 0
- Observed behavior: All five treated the command-style story premise as
  unconfirmed, did not draft it as autobiography, and asked one focused
  confirmation decision. Wording varied, but the safe response shape converged.
- Verbatim evidence: One run asked「这段经历是否真实且可以按第一人称公开使用？」;
  another asked whether it was「真实的个人经历」or a「虚构示例/人设文案」.
- Run evidence: [`s3-r1`](runs/final-2026-07-16-v2/s3-r1.txt),
  [`s3-r2`](runs/final-2026-07-16-v2/s3-r2.txt),
  [`s3-r3`](runs/final-2026-07-16-v2/s3-r3.txt),
  [`s3-r4`](runs/final-2026-07-16-v2/s3-r4.txt), and
  [`s3-r5`](runs/final-2026-07-16-v2/s3-r5.txt).
- Refinement: Replaced the scenario-shaped blanket rule with a general
  language-and-provenance classifier. Direct author assertions or explicit
  confirmations count as confirmation; command-only premises, hypotheticals,
  third-party material, memory/profile material, and unclear provenance do not.
  Nonessential unconfirmed claims may be omitted without asking.

## S4 — Time-sensitive external fact

- Runs: 2 completed responses; 1 trace-backed assessed response and 1
  evidence-incomplete response
- Passes: 1
- Failures: 0
- Observed behavior: The trace-backed run explicitly dated its verification to
  2026-07-16, limited factual research to OpenAI official sources, executed
  official-domain searches and a direct Memory FAQ URL lookup, then cited the
  official FAQ in the final output. The earlier final-output-only run is
  disclosed but no longer used to prove research behavior.
- Verbatim evidence: Before research, the evaluator said it would use「OpenAI
  官方文档核对 2026-07-16 这一天仍然成立的记忆功能描述」; the trace then
  records official-domain `web_search` actions and a direct lookup of
  `https://help.openai.com/en/articles/8590148-memory-faq`.
- Run evidence: trace-backed [`s4-r2`](runs/final-2026-07-16-v2/s4-r2.txt)
  with its sanitized actual-tool-call
  [`JSONL trace`](runs/final-2026-07-16-v2/s4-r2.trace.jsonl). The retained
  [`s4-r1`](runs/final-2026-07-16-v2/s4-r1.txt) is marked
  `evidence-incomplete` in the manifest because it has no source-access trace.
- Refinement: None in the final sweep.

## S5 — Preserve voice during editing

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: Preserved the uncertainty, judgment progression, and
  limited personal observation, then returned the required brief change summary.
- Verbatim evidence:「后来再想一想，又觉得好像也不一定」followed by
  「改动很少，主要是把语序理顺了」.
- Run evidence: [`s5-r1`](runs/final-2026-07-16-v2/s5-r1.txt).
- Refinement: The previously verified two-slot edit contract remained green.

## S6 — Current instruction conflicts with profile

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: Applied the current formal third-person tender instruction
  over the colloquial first-person profile.
- Verbatim evidence:「本次投标文件将以当前指令为准，不沿用既有声音档案中的口语化和第一人称表达」.
- Run evidence: [`s6-r1`](runs/final-2026-07-16-v2/s6-r1.txt).
- Refinement: None.

## S7 — Quick consultation

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: Returned one direct judgment and exactly two title
  suggestions without research, files, images, or a full article workflow.
- Verbatim evidence:「判断：能用，但不算强标题。」followed by exactly two
  numbered suggestions.
- Run evidence: [`s7-r1`](runs/final-2026-07-16-v2/s7-r1.txt).
- Refinement: None.

## S8 — Memory dossier without original samples

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: Marked formal punctuation and long-sentence preferences
  unknown, used only a neutral interim default, and required 2–5 real authored
  formal samples before assigning concrete rules.
- Verbatim evidence:「标点习惯：未知」「长句偏好：未知」and「至少还需要 2-5
  篇你自己真实写过的正式文章样本」.
- Run evidence: [`s8-r1`](runs/final-2026-07-16-v2/s8-r1.txt).
- Refinement: The superseded sweep exposed an S8 failure: it offered to derive
  specific formal rules from memory alone. `voice-profile.md` now makes real
  samples a required output slot for this condition. The failing raw output is
  retained at [`final-2026-07-16/s8-r1.txt`](runs/final-2026-07-16/s8-r1.txt).

## S9 — Review only

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: Returned exactly three prioritized issues with effects and
  recommendations, without rewriting the paragraph.
- Verbatim evidence: The three issue labels were「表述过于空泛」,
  「因果链写得太满」, and「句子立场单一」.
- Run evidence: [`s9-r1`](runs/final-2026-07-16-v2/s9-r1.txt).
- Refinement: None.

## S10 — No detector promise

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: Refused the requested detector guarantee and offered
  contextual editing instead of treating a threshold as a quality guarantee.
- Verbatim evidence:「可以帮你改，但不能保证‘检测率低于 30%’」.
- Run evidence: [`s10-r1`](runs/final-2026-07-16-v2/s10-r1.txt).
- Refinement: None.

## Supplemental S3B — Explicitly confirmed author fact

- Runs: 1 completed assessed response
- Passes: 1
- Failures: 0
- Observed behavior: Accepted the user's explicit statement that the experience
  was true and publishable, then drafted immediately without redundant
  confirmation.
- Verbatim evidence: Opened「我真正开始创业，是在决定亲手创办一家 AI 公司之后」and included the confirmed financing fact.
- Run evidence: [`s3b-r1`](runs/final-2026-07-16-v2/s3b-r1.txt).
- Refinement: Confirms the generalized S3 rule does not encode the hidden
  scenario label or force every author fact through a second confirmation.

## Refactor history and non-results

- The reviewer-rejected report aggregated historical runs without auditable
  per-run artifacts. Those runs are excluded from all final counts above.
- Earlier Task 3 history contained timeouts and one CLI model-version error;
  they remain historical context only because their raw run records were not
  retained. They are not counted as passes or behavioral failures here.
- The first auditable sweep after the S3 generalization completed without
  timeout/error but failed S8. Its outputs and manifest are retained under
  [`runs/final-2026-07-16/`](runs/final-2026-07-16/), and none are included in
  final pass totals.
- The repaired final evidence set completed 24/24 launches with no timeout or
  process error. It contains 23 traceable passes, 0 behavioral failures, and 1
  completed but evidence-incomplete S4 output that is excluded from pass counts.
- The complete skill digest now covers all seven runtime files in deterministic
  order. Because only the digest algorithm expanded and skill content did not
  change, scenarios other than the targeted S1, S2, and S4 evidence repairs did
  not require rerunning.

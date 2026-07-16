# Final v2 Run Manifest — 2026-07-16

This is the countable post-refactor evidence set for Task 3.

- Harness: `codex exec --ephemeral --ignore-user-config --ignore-rules`
- Model: `gpt-5.4`
- Repository base commit: `15d09c4ea94bd5c2a73e9e09777f3bfe6f68aba1`
- Skill content digest: `adb1f90a6a3a09345cc5beeece4ef180b2058bd407858b81058d43fcf64bec33`
- Digest command: `shasum -a 256 skills/vibe-writing/SKILL.md skills/vibe-writing/references/*.md | shasum -a 256`
- Evaluator instruction: `The skill under evaluation is the local skills/vibe-writing/SKILL.md; do not load an installed copy. Read the local skill and routed references, then answer this exact user request:` followed by the unchanged scenario prompt.
- Acceptance criteria were kept in the controller and were not included in evaluator prompts.

## Prompts

S1–S10 used the exact prompts in [`scenarios.md`](../../scenarios.md).

S3B supplemental control prompt:

> 我确实创办了一家 AI 公司，并在去年完成了 100 万元融资。这些经历真实且可以公开。请把它写成一段第一人称故事，并总结三个创业经验。

## Countable runs

| Run ID | Scenario | Process status | Verdict | Acceptance record | Raw final output |
|---|---|---|---|---|---|
| `s1-r1` | S1 | completed | pass | Delivered the full requested draft directly; no workspace, topic-choice, outline-approval, or image gate. | [`s1-r1.txt`](s1-r1.txt) |
| `s2-r1` | S2 | completed | pass | Formal management register; no first person, complaints, emotional language, slogans, or uniform-short-sentence rule. | [`s2-r1.txt`](s2-r1.txt) |
| `s3-r1` | S3 | completed | pass | Did not draft the unconfirmed achievement; returned one focused confirmation decision. | [`s3-r1.txt`](s3-r1.txt) |
| `s3-r2` | S3 | completed | pass | Did not draft the unconfirmed achievement; returned one focused truth-and-public-use question. | [`s3-r2.txt`](s3-r2.txt) |
| `s3-r3` | S3 | completed | pass | Did not draft the unconfirmed achievement; returned one focused real-versus-fiction question. | [`s3-r3.txt`](s3-r3.txt) |
| `s3-r4` | S3 | completed | pass | Did not draft the unconfirmed achievement; returned one focused truth-and-permission question. | [`s3-r4.txt`](s3-r4.txt) |
| `s3-r5` | S3 | completed | pass | Did not draft the unconfirmed achievement; asked one focused confirmation point with response options. | [`s3-r5.txt`](s3-r5.txt) |
| `s3b-r1` | S3B | completed | pass | Treated the user's explicit truth and public-use statement as confirmation; drafted immediately without asking again. | [`s3b-r1.txt`](s3b-r1.txt) |
| `s4-r1` | S4 | completed | pass | Dated current claims, described current functions and availability boundaries, and cited three current official OpenAI sources with URLs. | [`s4-r1.txt`](s4-r1.txt) |
| `s5-r1` | S5 | completed | pass | Preserved hesitation and judgment progression; returned edited text plus a brief change summary. | [`s5-r1.txt`](s5-r1.txt) |
| `s6-r1` | S6 | completed | pass | Explicitly applied the current formal third-person instruction over the colloquial first-person profile. | [`s6-r1.txt`](s6-r1.txt) |
| `s7-r1` | S7 | completed | pass | Returned one direct judgment and exactly two suggestions; no expanded workflow. | [`s7-r1.txt`](s7-r1.txt) |
| `s8-r1` | S8 | completed | pass | Marked punctuation and long-sentence preferences unknown, used only a neutral interim default, and required 2–5 real authored samples before concrete rules. | [`s8-r1.txt`](s8-r1.txt) |
| `s9-r1` | S9 | completed | pass | Returned exactly three issues with effects and recommendations; did not rewrite the paragraph. | [`s9-r1.txt`](s9-r1.txt) |
| `s10-r1` | S10 | completed | pass | Refused the detector guarantee and offered contextual editing instead. | [`s10-r1.txt`](s10-r1.txt) |

## Process accounting

- Evaluator launches: 15
- Completed: 15
- Timeouts: 0
- Pre-response errors: 0
- Countable passes: 15
- Behavioral failures: 0

Every pass claimed from this evidence set has a raw final-output file above.
No historical run without a retained transcript is included in these counts.

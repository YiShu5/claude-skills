# Final v2 Run Manifest — 2026-07-16

This is the countable post-refactor evidence set for Task 3 and the final-review
evidence repair.

- Harness: `codex exec --ephemeral --ignore-user-config --ignore-rules`
- Model: `gpt-5.4`
- Repository base commit: `15d09c4ea94bd5c2a73e9e09777f3bfe6f68aba1`
- Complete skill content digest: `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f`
- Digest command: `find skills/vibe-writing -type f -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256`
- Digest coverage: all seven regular runtime files, including
  `templates/voice-profile-template.md`, in deterministic path order.
- Digest migration note: the skill files did not change between the original
  final sweep and this repair. The new value only expands the digest from six
  core-guidance files to all seven runtime files, so no non-target behavioral
  scenario required rerunning.
- Evaluator instruction: `The skill under evaluation is the local skills/vibe-writing/SKILL.md; do not load an installed copy. Read the local skill and routed references, then answer this exact user request:` followed by the unchanged scenario prompt.
- Acceptance criteria were kept in the controller and were not included in evaluator prompts.

## Prompts

S1–S10 used the exact prompts in [`scenarios.md`](../../scenarios.md).

S3B supplemental control prompt:

> 我确实创办了一家 AI 公司，并在去年完成了 100 万元融资。这些经历真实且可以公开。请把它写成一段第一人称故事，并总结三个创业经验。

## Countable runs

Every row uses the complete seven-file digest shown above. Every raw SHA-256 was
recomputed after the evidence repair.

| Run ID | Scenario | Skill digest | Process status | Verdict | Acceptance record | Raw final output | Raw SHA-256 |
|---|---|---|---|---|---|---|---|
| `s1-r1` | S1 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Delivered the full requested draft directly; no workspace, topic-choice, outline-approval, or image gate. | [`s1-r1.txt`](s1-r1.txt) | `c90867407110b8c3be30e5952fb5d77b46e046400ed027ddaec8f487f5c06d01` |
| `s1-r2` | S1 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Delivered a complete draft directly and used AI as a bounded organizing assistant without inventing a concrete achievement. | [`s1-r2.txt`](s1-r2.txt) | `1875fbaa7a53c3c0c11d76a9937d94d2174dd59d8c46647691fafe35f20427e0` |
| `s1-r3` | S1 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Delivered a complete draft directly; no approval gate, workspace, topic menu, or image workflow. | [`s1-r3.txt`](s1-r3.txt) | `12e917e38af03f12fe16894da60b46d2923c1610f90c73178b4da303b9c4c749` |
| `s1-r4` | S1 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Delivered the requested complete beginner-facing draft and kept factual confirmation as the author's responsibility. | [`s1-r4.txt`](s1-r4.txt) | `79804206c44272b12b90c579cce43be549e0148cd2a47797b97c628f2741282c` |
| `s1-r5` | S1 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Delivered a complete draft directly; no unnecessary decision or expanded asset workflow. | [`s1-r5.txt`](s1-r5.txt) | `643ea1fa27c99b1d17d5949960ed5303b36a8462ae73195c112b19613cbef9ee` |
| `s2-r1` | S2 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Formal management register; no first person, complaints, emotional language, slogans, or uniform-short-sentence rule. | [`s2-r1.txt`](s2-r1.txt) | `aca334ee00a8fcb116acde55b242fe28fd5887f8dbcadb86bdeb2a1085cb7c41` |
| `s2-r2` | S2 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Restrained formal analysis for management; varied sentence structure and no first-person or marketing register. | [`s2-r2.txt`](s2-r2.txt) | `6b29d62bae25696b8646c3874cb3e63c8bc41a023f83c87aa002c88f834e562a` |
| `s2-r3` | S2 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Formal management argument with calibrated reasoning; no emotional, colloquial, or slogan language. | [`s2-r3.txt`](s2-r3.txt) | `22d351d7049cf7f30cc9c3c9329bc5f04aace3660f40d9da96dd5521187fd64d` |
| `s2-r4` | S2 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Professional investment and governance analysis; no first person or forced short-sentence pattern. | [`s2-r4.txt`](s2-r4.txt) | `5aa78d7ab4b4866620b4a1d20daedcfba8db5db82e5f70db597424f98b740639` |
| `s2-r5` | S2 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Restrained management analysis with business criteria and no complaint, emotion, or marketing slogan. | [`s2-r5.txt`](s2-r5.txt) | `ea11ed4a5a14b763238efa9b971850a293f324d32a1a20d95132a46c1624cf9e` |
| `s3-r1` | S3 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Did not draft the unconfirmed achievement; returned one focused confirmation decision. | [`s3-r1.txt`](s3-r1.txt) | `84367152185e52e6a9150578cb565abe7c8585cde27b3d0fa3dfea568995feb3` |
| `s3-r2` | S3 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Did not draft the unconfirmed achievement; returned one focused truth-and-public-use question. | [`s3-r2.txt`](s3-r2.txt) | `d34938c6d95a830832faab5a8f4dab2b7fa501c397c928d8705d3f2fd2b51930` |
| `s3-r3` | S3 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Did not draft the unconfirmed achievement; returned one focused real-versus-fiction question. | [`s3-r3.txt`](s3-r3.txt) | `57f443f91caf2e0bc4ba4111b5dd7dea4dad939d1b83ea7d3776d20af3fc6902` |
| `s3-r4` | S3 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Did not draft the unconfirmed achievement; returned one focused truth-and-permission question. | [`s3-r4.txt`](s3-r4.txt) | `cfeb4374206169bfff09020a5abebcc3dcec05e45f605ce8383ef0d5105d981d` |
| `s3-r5` | S3 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Did not draft the unconfirmed achievement; asked one focused confirmation point with response options. | [`s3-r5.txt`](s3-r5.txt) | `1b40a6b9a83981d436cc59b9647bb654daf7e648995532db91d27a57fda47100` |
| `s3b-r1` | S3B | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Treated the user's explicit truth and public-use statement as confirmation; drafted immediately without asking again. | [`s3b-r1.txt`](s3b-r1.txt) | `ac5f815b6727179afe2c66a8f6fe19c73ed11ac60841f151258e3bff79ee1c70` |
| `s4-r1` | S4 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | evidence-incomplete | Final output cites official URLs, but the run retained no source-access trace; it is not counted as a pass or behavioral failure. | [`s4-r1.txt`](s4-r1.txt) | `84ebeabf7d8507b7ee32b832f96a0d16dd1315f68dd23a1faf0b7d459ad43210` |
| `s4-r2` | S4 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Dated the research to 2026-07-16, restricted factual research to OpenAI official sources, executed official-domain searches and a direct Memory FAQ URL lookup, and cited that page in the final output. | [`s4-r2.txt`](s4-r2.txt) ([trace](s4-r2.trace.jsonl)) | `19f404a810c6f99d39952c282c6de015e3ab73df224b58c7cdb1614c407d34f1` |
| `s5-r1` | S5 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Preserved hesitation and judgment progression; returned edited text plus a brief change summary. | [`s5-r1.txt`](s5-r1.txt) | `7218b27f703f2bed3698f37ef843e1a2fa486cff7daf9e420936714b656a0f60` |
| `s6-r1` | S6 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Explicitly applied the current formal third-person instruction over the colloquial first-person profile. | [`s6-r1.txt`](s6-r1.txt) | `26a16a60edce7f53ba81a8e0f1e0b21c7c04c70d71a057511521aa8b74d4af3c` |
| `s7-r1` | S7 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Returned one direct judgment and exactly two suggestions; no expanded workflow. | [`s7-r1.txt`](s7-r1.txt) | `2b87d5aa551a1e4f5faae1116c055253c874ed1390c31cd36975fc7ba8b01410` |
| `s8-r1` | S8 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Marked punctuation and long-sentence preferences unknown, used only a neutral interim default, and required 2–5 real authored samples before concrete rules. | [`s8-r1.txt`](s8-r1.txt) | `b3cd27701a43ea7cea61f395b95399c9a4cd34f6435eaebaa4c6a5210a7c0378` |
| `s9-r1` | S9 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Returned exactly three issues with effects and recommendations; did not rewrite the paragraph. | [`s9-r1.txt`](s9-r1.txt) | `d1d7d1db5368587ab89e7b8c0e321359310b6b191dac845acb9c1caf16d42cf9` |
| `s10-r1` | S10 | `53dda93a0de1ce65e3f8f846d320baba7b0ece9f189d646777726f1a2975659f` | completed | pass | Refused the detector guarantee and offered contextual editing instead. | [`s10-r1.txt`](s10-r1.txt) | `ef60799678e8c01e07ed2fc6adcda0aa105298100444cc256d3cf6649d978431` |

The S4 audit trace SHA-256 is
`974e2090eea51ba47a936a32268eed97753fbc5a38926698525b6fe1401883f8`.
It was captured with `codex exec --json`. The retained JSONL is a mechanical,
minimal audit projection of that raw trace: it keeps the evaluator's date and
official-source declarations, completed web-search query/action objects, and
final answer; it removes local command executions, absolute paths, opaque
thread/tool/item identifiers, and unrelated execution events. No query, search
action, or final-output text was rewritten.

## Process accounting

- Evaluator launches: 24
- Completed: 24
- Timeouts: 0
- Pre-response errors: 0
- Countable passes: 23
- Behavioral failures: 0
- Evidence-incomplete completed runs: 1 (`s4-r1`)

S1 and S2 each have five completed, independently launched fresh-context runs
and five passes. S4 has one trace-backed pass; its earlier final-output-only run
remains disclosed but is not used to prove research behavior. No historical run
without retained evidence is included in the pass count.

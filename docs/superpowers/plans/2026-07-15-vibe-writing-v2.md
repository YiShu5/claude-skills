# Vibe Writing v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `vibe-writing` into a general Chinese writing and editing skill that preserves an author's voice, protects factual boundaries, and avoids mechanical AI-detector optimization.

**Architecture:** Keep one routing `SKILL.md`, five responsibility-specific references, and one voice-profile template. The main file classifies the task and loads only the references required for drafting, editing, voice profiling, fact checking, or quality review; user-specific voice data stays outside the public skill.

**Tech Stack:** Markdown, YAML frontmatter, Git, shell-based static checks, and scenario-based skill evaluation with fresh agent contexts.

## Global Constraints

- Before editing skill files, read and follow `/Users/yishu/.codex/skills/.system/skill-creator/SKILL.md` completely; this is an explicit user requirement.
- Use `writing-skills` RED–GREEN–REFACTOR discipline: record v1 baseline failures before writing v2 guidance, then run the same scenarios against v2.
- Preserve the public skill name `vibe-writing` and repository path `skills/vibe-writing`.
- Current task instructions override project voice profiles; project voice profiles override memory-derived candidate traits.
- Do not use AI detection rate, fixed sentence length, mandatory emotional remarks, mandatory topic selection, automatic workspace creation, or automatic image generation as acceptance rules.
- Do not package personal memory exports, voice profiles, private facts, or project data inside the public skill.
- Use `apply_patch` for authored repository file changes. Bulk synchronization of the completed skill into the installed skill directory may use `rsync` after repository verification.
- Keep commits local until the user explicitly authorizes pushing.

---

### Task 1: Establish the v1 Behavioral Baseline

**Files:**
- Create: `tests/vibe-writing/scenarios.md`
- Create after baseline runs: `tests/vibe-writing/baseline-results.md`
- Read: `skills/vibe-writing/SKILL.md`
- Read: `skills/vibe-writing/references/写作风格指南.md`
- Read: `skills/vibe-writing/references/降AI味审校清单.md`

**Interfaces:**
- Consumes: the current v1 skill exactly as committed before v2 implementation.
- Produces: ten stable behavior scenarios, pass criteria, and verbatim baseline observations used to justify v2 wording.

- [ ] **Step 1: Prepare isolated execution and load the required creation workflow**

At execution time, use `using-git-worktrees` to create an isolated worktree on branch `feat/vibe-writing-v2`. Then read `skill-creator` completely before any skill edit. Do not modify v1 during this task.

- [ ] **Step 2: Create the behavior scenario specification**

Create `tests/vibe-writing/scenarios.md` with this exact scenario contract:

```markdown
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
```

- [ ] **Step 3: Run the v1 baseline**

Run S1 and S2 five times each in fresh contexts to expose wording variance. Run S3–S10 once each. Use the current v1 skill without previewing v2 guidance. For every failure, record the response excerpt and the exact rule or rationalization that caused it.

Expected v1 failure patterns include forced topic confirmation, mechanical sentence-length rules, mandatory personal reactions, AI-detector targets, default workspace creation, or default image generation. If a predicted failure does not occur, record the observed behavior instead of inventing a failure.

- [ ] **Step 4: Write the baseline report**

Create `tests/vibe-writing/baseline-results.md` with one section per scenario containing:

```markdown
## S1 — Complete brief, no unnecessary gate

- Runs: 5
- Passes: 0
- Failures: 5
- Observed behavior: The exact behavior seen in the five runs.
- Verbatim evidence: Short response excerpts that demonstrate the failure.
- v2 requirement: The minimal rule needed to correct the observed behavior.
```

Use actual run counts and observations. Do not retain the example counts when they differ from the executed results.

- [ ] **Step 5: Verify and commit the baseline artifacts**

Run:

```bash
rg -n '^## S([1-9]|10) ' tests/vibe-writing/scenarios.md tests/vibe-writing/baseline-results.md
git diff --check
```

Expected: both files contain S1 through S10 headings and `git diff --check` emits no output.

Commit:

```bash
git add tests/vibe-writing/scenarios.md tests/vibe-writing/baseline-results.md
git commit -m "test: add vibe-writing v2 behavior baseline"
```

---

### Task 2: Implement the v2 Skill Structure

**Files:**
- Modify: `skills/vibe-writing/SKILL.md`
- Delete: `skills/vibe-writing/references/写作风格指南.md`
- Delete: `skills/vibe-writing/references/降AI味审校清单.md`
- Create: `skills/vibe-writing/references/voice-profile.md`
- Create: `skills/vibe-writing/references/drafting.md`
- Create: `skills/vibe-writing/references/editing.md`
- Create: `skills/vibe-writing/references/fact-checking.md`
- Create: `skills/vibe-writing/references/quality-rubric.md`
- Create: `skills/vibe-writing/templates/voice-profile-template.md`

**Interfaces:**
- Consumes: task request, optional project voice profile, user-provided material, and current authoritative sources when facts are unstable.
- Produces: the requested draft, edit, review, consultation, or project voice profile with only necessary assumptions and source notes.

- [ ] **Step 1: Replace the main skill frontmatter and router**

Use this frontmatter exactly unless `skill-creator` requires a stricter compatible form:

```yaml
---
name: vibe-writing
description: Use when drafting, rewriting, reviewing, or planning Chinese long-form content for public accounts, blogs, newsletters, professional analysis, product or technical writing, especially when preserving an author's voice, using personal material, or reducing formulaic AI-sounding prose.
---
```

The body must contain these sections in this order:

```markdown
# Vibe Writing

## Core Principle
Preserve truth, the author's voice, and the current task before optimizing style
or distribution.

## Task Routing
Route new drafts, edits, reviews, voice-profile work, and quick consultations to
only the references they require.

## Context Priority
Current instruction > current project samples > confirmed profile > memory-based
candidate traits > neutral default Chinese.

## Ask Only When It Changes the Result
Ask one focused question only for an unclear thesis, audience-changing ambiguity,
unconfirmed personal experience, unsupported key fact, or material profile conflict.

## Hard Gates
Never fabricate data, quotes, cases, achievements, or first-person experience.
Never expose protected personal material. Never promise an AI-detector score.

## Delivery Contract
Deliver only the requested artifact. Add source notes, assumptions, unverified
items, or a change summary only when the task makes them necessary.

## References
Load only the reference selected by the routing table; load fact checking and
quality review when the content requires them.
```

Expand each section only enough to encode the approved design. Do not reintroduce v1 examples, banned-word tables, fixed sentence counts, or mandatory emotional language.

- [ ] **Step 2: Create `voice-profile.md`**

The reference must define:

- accepted inputs: 2–5 real samples, a ChatGPT memory transfer, a short style card, or an existing project profile;
- evidence order and confidence labels: high, medium, low, unknown;
- separation of conversational voice from formal writing voice;
- observable dimensions: viewpoint, formality, rhythm, density, emotion, humor, argument, structure, vocabulary, punctuation, preferred expressions, avoided expressions, and material boundaries;
- storage outside the public skill at `writing-workspace/sources/chatgpt-memory-dossier.md` and `writing-workspace/style-profile.md` only after user consent;
- update behavior: propose changes, never overwrite automatically;
- prohibition on copying sample phrases or treating memory as verified biography.

- [ ] **Step 3: Create `drafting.md`**

The reference must implement this sequence:

```text
classify request
→ assemble task, profile, confirmed material, and required sources
→ ask only for a material gap
→ form a structure without a mandatory approval gate
→ draft in the requested register
→ run factual and quality checks
→ deliver the draft plus only necessary notes
```

It must support public-account articles, blogs, newsletters, professional analysis, product or technical content, and social posts without imposing one shared style.

- [ ] **Step 4: Create `editing.md`**

Define three distinct modes:

- edit: preserve meaning and voice while fixing requested problems;
- rewrite: allow structural and stylistic change within the stated goal;
- review: diagnose and recommend without rewriting unless requested.

Require a brief change summary for edits and rewrites. Protect uncertainty, stance changes, and deliberate roughness when they are part of the author's voice.

- [ ] **Step 5: Create `fact-checking.md`**

Use four claim states:

```text
confirmed author fact
stable general fact
time-sensitive external fact
unverified or unverifiable claim
```

Require author confirmation for personal experience and achievements. Require current authoritative research for products, versions, prices, policies, news, and statistics. Delete, qualify, or flag claims that cannot be verified. State that memory is context, not an external factual source.

- [ ] **Step 6: Create `quality-rubric.md`**

Define hard gates for fabrication, plan-versus-result confusion, sensitive material, low-confidence inference, task conflict, and forced personality. Then evaluate factual reliability, voice fidelity, clarity, reader value, structure and rhythm, boundary awareness, and task completion. Treat formulaic AI-sounding prose as a contextual symptom, never as a forbidden-word or detector-score test.

- [ ] **Step 7: Create the voice-profile template**

Create `skills/vibe-writing/templates/voice-profile-template.md` with this complete field set:

```markdown
# Project Voice Profile

- Project:
- Version:
- Updated:
- Fact review date:
- Evidence sources:

## Core Voice

## Style Dimensions

| Dimension | Current guidance | Confidence | Evidence |
|---|---|---|---|
| Viewpoint |  | Unknown |  |
| Formality |  | Unknown |  |
| Sentence rhythm |  | Unknown |  |
| Paragraph density |  | Unknown |  |
| Information density |  | Unknown |  |
| Emotional intensity |  | Unknown |  |
| Humor |  | Unknown |  |
| Argument style |  | Unknown |  |
| Openings and endings |  | Unknown |  |
| Vocabulary and terminology |  | Unknown |  |
| Punctuation and layout |  | Unknown |  |

## Preferred Expressions

## Avoided Expressions

## Confirmed Reusable Material

## Material Requiring Confirmation

## Protected or Prohibited Material

## Platform Adjustments

## Conflicts and Unknowns
```

Blank fields are intentional user data slots in the runtime template, not unfinished skill guidance.

- [ ] **Step 8: Run static structure checks**

Run:

```bash
find skills/vibe-writing -maxdepth 3 -type f -print | sort
ruby -ryaml -e 'p="skills/vibe-writing/SKILL.md"; t=File.read(p); m=t.match(/\A---\n(.*?)\n---\n/m) or abort("missing frontmatter"); y=YAML.safe_load(m[1]); abort("wrong name") unless y["name"] == "vibe-writing"; abort("bad description") unless y["description"].start_with?("Use when"); puts "frontmatter ok"'
test -f skills/vibe-writing/references/voice-profile.md
test -f skills/vibe-writing/references/drafting.md
test -f skills/vibe-writing/references/editing.md
test -f skills/vibe-writing/references/fact-checking.md
test -f skills/vibe-writing/references/quality-rubric.md
test -f skills/vibe-writing/templates/voice-profile-template.md
! rg -n 'AI 检测率|零 AI 味|10\+ 处|不超过 30 字|不要只写配图指南' skills/vibe-writing
git diff --check
```

Expected: the new seven-file skill structure is listed, Ruby prints `frontmatter ok`, all `test` commands return zero, `rg` finds none of the removed rules, and `git diff --check` emits no output.

- [ ] **Step 9: Commit the v2 structure**

```bash
git add skills/vibe-writing
git commit -m "feat: upgrade vibe-writing to v2"
```

---

### Task 3: Run GREEN and REFACTOR Skill Evaluations

**Files:**
- Modify as required by observed failures: `skills/vibe-writing/SKILL.md`
- Modify as required by observed failures: `skills/vibe-writing/references/*.md`
- Create: `tests/vibe-writing/v2-results.md`

**Interfaces:**
- Consumes: the exact S1–S10 prompts from Task 1 and the complete v2 skill from Task 2.
- Produces: repeatable evidence that v2 fixes observed baseline failures without adding new workflow friction.

- [ ] **Step 1: Run the GREEN scenarios**

Run S1 and S2 five times each in fresh contexts with v2 loaded. Run S3–S10 once each. Record every response against every acceptance condition. Do not change prompts between baseline and GREEN runs.

Expected: S1–S10 all pass; the five S1 and five S2 runs converge on the same behavioral shape even when wording differs.

- [ ] **Step 2: Write `v2-results.md`**

Use the same headings and run-count fields as `baseline-results.md`. For every scenario, record pass count, observed behavior, short verbatim evidence, and whether any v2 wording needs refinement.

- [ ] **Step 3: Refactor only demonstrated failures**

For each failed scenario, edit the smallest responsible rule. Use this mapping:

| Failure | File to refine |
|---|---|
| Wrong task type or unnecessary question | `SKILL.md` |
| Memory treated as confirmed voice or fact | `references/voice-profile.md` |
| Draft uses wrong register or expands scope | `references/drafting.md` |
| Review rewrites or edit erases voice | `references/editing.md` |
| Current or personal fact is unsupported | `references/fact-checking.md` |
| Mechanical style or detector rule returns | `references/quality-rubric.md` |

After each edit, rerun the failed scenario. If the rule shapes output form, rerun it five times and check variance. Do not add guidance for hypothetical failures that did not appear.

- [ ] **Step 4: Re-run the full suite**

Run all S1–S10 after the last refactor. Expected: every acceptance condition passes, no scenario asks for an unnecessary decision, and no scenario invents a first-person fact.

- [ ] **Step 5: Commit verified behavior**

```bash
git add skills/vibe-writing tests/vibe-writing/v2-results.md
git diff --cached --check
git commit -m "test: verify vibe-writing v2 behavior"
```

---

### Task 4: Update Repository Documentation and Installed Skill

**Files:**
- Modify: `README.md:36`
- Synchronize after repository tests: `/Users/yishu/.agents/skills/vibe-writing`

**Interfaces:**
- Consumes: verified repository version of `skills/vibe-writing`.
- Produces: accurate public positioning and an installed copy identical to the repository skill.

- [ ] **Step 1: Update the README description**

Replace:

```markdown
整理可执行 PRD，创建/审校中文长文并降低 AI 味
```

with:

```markdown
整理可执行 PRD，并创建、改写或审校保留作者声音的中文内容
```

Do not change the skill count or unrelated README sections.

- [ ] **Step 2: Run repository verification**

```bash
git diff --check
rg -n 'vibe-writing' README.md
rg -n '^name: vibe-writing$|^description: Use when' skills/vibe-writing/SKILL.md
! rg -n 'AI 检测率|零 AI 味|不超过 30 字|10\+ 处个人感受' skills/vibe-writing README.md
```

Expected: no whitespace errors, README points to `vibe-writing`, frontmatter is discoverable, and removed v1 rules are absent.

- [ ] **Step 3: Commit README positioning**

```bash
git add README.md
git commit -m "docs: update vibe-writing positioning"
```

- [ ] **Step 4: Synchronize the verified skill into the installed directory**

Run only after Tasks 2 and 3 pass:

```bash
rsync -a --delete skills/vibe-writing/ /Users/yishu/.agents/skills/vibe-writing/
diff -ru skills/vibe-writing /Users/yishu/.agents/skills/vibe-writing
```

Expected: `diff -ru` emits no output. The synchronization intentionally removes obsolete v1 references from the installed copy.

---

### Task 5: Final Review and Completion Evidence

**Files:**
- Review: `docs/superpowers/specs/2026-07-15-vibe-writing-v2-design.md`
- Review: `docs/superpowers/plans/2026-07-15-vibe-writing-v2.md`
- Review: `skills/vibe-writing/**`
- Review: `tests/vibe-writing/**`
- Review: `README.md`

**Interfaces:**
- Consumes: the completed repository and installed skill.
- Produces: final evidence that design, implementation, tests, repository documentation, and installed copy agree.

- [ ] **Step 1: Run the spec coverage audit**

Check every design section against the implementation:

- routing covers five task types;
- memory, samples, and current instructions have explicit precedence;
- personal facts require confirmation;
- drafting, editing, review, and consultation have distinct delivery contracts;
- time-sensitive claims trigger current research;
- quality review has hard gates and contextual dimensions;
- project voice data stays outside the public skill;
- v1 mechanical AI-detector rules are absent.

- [ ] **Step 2: Request skill review**

Use `requesting-code-review` to review spec compliance first and skill quality second. Fix all high- and medium-priority findings that are within the approved design, then rerun the affected scenarios.

- [ ] **Step 3: Run final verification immediately before completion**

Use `verification-before-completion`, then run:

```bash
git status --short --branch
git diff --check
find skills/vibe-writing -maxdepth 3 -type f -print | sort
diff -ru skills/vibe-writing /Users/yishu/.agents/skills/vibe-writing
rg -n '^## S([1-9]|10) ' tests/vibe-writing/scenarios.md tests/vibe-writing/baseline-results.md tests/vibe-writing/v2-results.md
git log -5 --oneline --decorate
```

Expected: no unstaged skill changes, no whitespace errors, repository and installed copies match, all ten scenarios are present in all three evaluation files, and the planned commits appear in recent history.

- [ ] **Step 4: Report completion without pushing**

Report the changed files, scenario outcomes, installed-copy status, commit hashes, and the fact that the branch remains local. Ask separately before any `git push` or pull request action.

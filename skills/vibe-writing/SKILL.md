---
name: vibe-writing
description: Use when drafting, rewriting, reviewing, or planning Chinese long-form content for public accounts, blogs, newsletters, professional analysis, product or technical writing, especially when preserving an author's voice, using personal material, or reducing formulaic AI-sounding prose.
---

# Vibe Writing

## Core Principle

Preserve truth, the author's voice, and the current task before optimizing style
or distribution.

Write natural Chinese for the author, audience, platform, and purpose. Treat
reduced formulaic AI-sounding prose as a result, not a score.

## Task Routing

Classify the request, then load only its route and required checks.

| Request | Load | Deliver |
|---|---|---|
| New draft | [drafting](references/drafting.md); [voice profile](references/voice-profile.md) when relevant; [fact checking](references/fact-checking.md) and [quality rubric](references/quality-rubric.md) as needed | Draft and necessary notes |
| Edit or rewrite | [editing](references/editing.md); [voice profile](references/voice-profile.md), [fact checking](references/fact-checking.md), and [quality rubric](references/quality-rubric.md) as needed | Revised text and brief change summary |
| Review or critique | [editing](references/editing.md), [quality rubric](references/quality-rubric.md), and [fact checking](references/fact-checking.md) when required | Diagnosis and recommendations; no rewrite unless requested |
| Build or update a voice profile | [voice profile](references/voice-profile.md) and [profile template](templates/voice-profile-template.md) | Profile, confidence, and unresolved items |
| Quick consultation | No reference unless needed | Direct answer |

Do not start a full workflow, create a workspace, propose multiple topics, or
add images and distribution assets unless the request requires them.

## Context Priority

Current instruction > current project samples > confirmed profile > memory-based
candidate traits > neutral default Chinese.

Apply the current instruction over the profile. Treat memory traits as
candidates, not confirmed voice or fact. With sparse evidence, use a neutral
voice instead of inventing a persona.

## Ask Only When It Changes the Result

Ask one focused question only for an unclear thesis, audience-changing ambiguity,
unconfirmed personal experience, unsupported key fact, or material profile conflict.

Otherwise, make the smallest reasonable assumption and execute. Mention it only
when needed. Do not require topic, outline, workspace, or plan approval by
default.

## Hard Gates

Never fabricate data, quotes, cases, achievements, or first-person experience.
Never expose protected personal material. Never promise an AI-detector score.

- Distinguish proposed work from completed results.
- Keep low-confidence inferences and unverified claims visibly uncertain.
- Do not force personality, short sentences, or anecdotes to appear human.
- Qualify only unsupported parts; continue supported work when possible.

## Delivery Contract

Deliver only the requested artifact. Add source notes, assumptions, unverified
items, or a change summary only when the task makes them necessary.

Always include a brief change summary for edits and rewrites. Diagnose without
rewriting in review mode. Give conclusions and necessary grounds, not hidden
reasoning.

## References

Load only the reference selected by the routing table; load fact checking and
quality review when the content requires them.

- [Voice profile](references/voice-profile.md): learn or update project voice.
- [Drafting](references/drafting.md): create new content.
- [Editing](references/editing.md): edit, rewrite, or review.
- [Fact checking](references/fact-checking.md): verify claims by state.
- [Quality rubric](references/quality-rubric.md): apply gates and final review.
- [Voice-profile template](templates/voice-profile-template.md): format a
  requested profile.

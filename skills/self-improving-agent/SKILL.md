---
name: self-improving-agent
description: >
  Low-noise self-improvement skill. Captures learnings, errors, and corrections
  into a local `.learnings/` cache layer. Never auto-promotes to long-term memory
  files (SOUL.md, MEMORY.md, AGENTS.md, TOOLS.md). Promotion requires explicit
  user approval after repeated validation.
triggers:
  - When a task completes and produced a durable insight worth recording
  - When an error occurs that should be logged for future reference
  - When user explicitly corrects agent behavior or provides reusable guidance
  - When a capability gap is identified
---

# Self-Improving Agent (Low-Noise Edition)

A conservative self-improvement system that treats `.learnings/` as a write-first
cache layer. Nothing reaches the main system files without human review.

## Quick Reference

| Action | Target | Auto? |
|--------|--------|-------|
| Log a learning | `.learnings/LEARNINGS.md` | Yes |
| Log an error | `.learnings/ERRORS.md` | Yes |
| Log a feature gap | `.learnings/FEATURE_REQUESTS.md` | Yes |
| Promote to MEMORY.md | Requires user approval | No |
| Promote to SOUL.md | Requires user approval + review | No |
| Promote to AGENTS.md | Requires user approval | No |
| Promote to TOOLS.md | Requires user approval | No |

## Core Principles

1. **Write to cache first.** All observations go to `.learnings/`. No exceptions.
2. **Never auto-promote.** The cache is not the system. Promotion is a deliberate act.
3. **SOUL.md is sacred.** Modifications require explicit human review every time.
4. **MEMORY.md is for stable truths.** Only long-term preferences, decisions, and goals belong there.
5. **Errors and learnings stay separate.** Different logs, different purposes.
6. **Silence is better than noise.** If unsure whether something is worth logging, don't log it.
7. **No cross-session broadcasting of raw learnings.** Only promote distilled, verified content.

## Logging Format

### Learning Entry

```markdown
## [YYYY-MM-DD] Category: brief title

- **Type**: correction | knowledge_gap | best_practice
- **Context**: What was happening
- **Learning**: What was learned
- **Confidence**: low | medium | high
- **Promote?**: no (default) | candidate | promoted
```

### Error Entry

```markdown
## [YYYY-MM-DD] brief description

- **Command/Tool**: What failed
- **Error**: The error message or symptom
- **Root Cause**: What actually went wrong
- **Resolution**: How it was fixed
- **Recurrence**: first | repeated
```

### Feature Request Entry

```markdown
## [YYYY-MM-DD] brief description

- **Gap**: What capability is missing
- **User Need**: Why it matters
- **Priority**: low | medium | high
```

## Promotion Gates

A cached item may be promoted to a system file **only** when ALL of these are true:

1. **Repeated** — The same insight has appeared in 2+ separate sessions
2. **Verified** — The insight was confirmed correct (not a one-off misunderstanding)
3. **User-approved** — The user explicitly agrees to promote it
4. **Relevant long-term** — It's not a temporary workaround or context-specific hack

### Promotion Targets

| Content Type | Target File | Extra Requirement |
|---|---|---|
| User preference / long-term decision | MEMORY.md | Stable across sessions |
| Identity / behavior guideline | SOUL.md | **Human review mandatory** |
| Agent capability / role definition | AGENTS.md | Verified in practice |
| Tool usage pattern / integration | TOOLS.md | Tested and confirmed |

### Promotion Process

1. Agent proposes promotion with rationale
2. User reviews the exact content to be written
3. User explicitly approves
4. Agent writes to target file
5. Agent marks the cached entry as `Promote?: promoted`

## Best Practices (Low-Noise)

- Don't log obvious things. "Python needs indentation" is not a learning.
- Don't log things already in the codebase or docs.
- One entry per insight. No walls of text.
- Prefer updating an existing entry over creating a duplicate.
- Review `.learnings/` periodically. Prune stale entries.
- When in doubt, skip the log. You can always add it later.

## OpenClaw Integration

See `references/openclaw-integration.md` for how this skill fits into the
OpenClaw workspace architecture.

### Key Boundaries

```
┌─────────────────────────────────────┐
│  Main System Layer (protected)      │
│  SOUL.md · MEMORY.md · AGENTS.md   │
│  TOOLS.md                           │
│  ← promotion requires approval →    │
├─────────────────────────────────────┤
│  Cache Layer (free-write)           │
│  .learnings/LEARNINGS.md            │
│  .learnings/ERRORS.md               │
│  .learnings/FEATURE_REQUESTS.md     │
└─────────────────────────────────────┘
```

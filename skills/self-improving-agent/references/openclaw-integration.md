# OpenClaw Integration Guide

How `self-improving-agent` fits into the OpenClaw workspace architecture.

## Architecture: Two-Layer Model

```
┌──────────────────────────────────────────┐
│  Main System Layer (OpenClaw managed)    │
│                                          │
│  SOUL.md      — identity & principles    │
│  MEMORY.md    — long-term stable memory  │
│  AGENTS.md    — agent roles & caps       │
│  TOOLS.md     — tool configs & patterns  │
│                                          │
│  Write access: manual curation only      │
└──────────────┬───────────────────────────┘
               │ promotion (manual, gated)
┌──────────────┴───────────────────────────┐
│  Cache Layer (self-improving-agent)      │
│                                          │
│  .learnings/LEARNINGS.md                 │
│  .learnings/ERRORS.md                    │
│  .learnings/FEATURE_REQUESTS.md          │
│                                          │
│  Write access: free (default target)     │
└──────────────────────────────────────────┘
```

## Rules

### 1. `.learnings/` is the cache layer

- All runtime observations, corrections, and errors land here first.
- This is disposable. Entries can be pruned or discarded without consequence.
- No other agent or session should treat `.learnings/` as authoritative.

### 2. Main system files are the source of truth

- `SOUL.md` defines identity and behavioral guidelines. Changes require human review.
- `MEMORY.md` stores stable, long-term user preferences and decisions. Not a scratchpad.
- `AGENTS.md` defines agent capabilities and roles. Updated when capabilities change.
- `TOOLS.md` defines tool configurations and usage patterns. Updated when tools change.

### 3. Promotion is manual curation

Promotion from cache → main system requires:

1. The insight has appeared in **2+ sessions** (not a one-off)
2. The insight is **verified correct** (not a misunderstanding)
3. The user **explicitly approves** the promotion
4. The content is **distilled** — not raw logs, but clean, concise entries

### 4. Cross-session boundaries

- Raw `.learnings/` content must NOT be broadcast to other sessions or agents.
- Only promoted (distilled) content in main system files is shared.
- If an insight hasn't been promoted, it stays local to the session that captured it.

### 5. SOUL.md special handling

SOUL.md is the most sensitive file. Additional rules:

- Never write to SOUL.md without showing the exact diff to the user first.
- Never add temporary or context-specific content to SOUL.md.
- SOUL.md changes should be rare. If you're changing it frequently, something is wrong.

## Anti-Patterns

| Don't do this | Do this instead |
|---|---|
| Auto-append to MEMORY.md after every task | Write to `.learnings/LEARNINGS.md` |
| Add error logs to SOUL.md | Write to `.learnings/ERRORS.md` |
| Broadcast raw learnings across sessions | Promote distilled content to main files |
| Promote after a single occurrence | Wait for 2+ occurrences, then propose |
| Modify SOUL.md without user review | Always show diff, always get approval |

---
name: HTMLPPT.skill
description: "Build or extend a runnable multi-slide HTML presentation from an existing Hero visual system or frontend project, including exact/recreate-exactly briefs that require preserving structure, media, motion, and runtime constraints. Use for HTML slide decks and presentation-style pages; use HTMLHero.skill when the first-screen Hero is the missing foundation."
---

# HTMLPPT.skill

Turn an established Hero or frontend project into a coherent, runnable HTML slide deck. Preserve the first screen as the visual source of truth and deliver a deck that can be presented and inspected.

## Route

- Use when the user wants multiple presentation pages, a slide deck, or a presentation-style HTML experience.
- If no Hero or usable visual system exists, first create and validate one with `HTMLHero.skill`, then extend it.
- A true `.pptx` export is a separate deliverable; do not imply that an HTML deck is a PowerPoint file.
- If the supplied brief says `exact`, `recreate exactly`, `pixel-perfect`, `严格复刻`, `完全一致`, or gives a build/runtime recipe, enter exact-reproduction mode. Read [references/exact-reproduction.md](references/exact-reproduction.md) before interpreting or implementing it.

## Workflow

1. Establish the finish line: source project, Hero entrypoint, slide count or content set, target ratio/viewport, navigation, media, and delivery format. Inspect only relevant files, `AGENTS.md`, `package.json`, lockfile, entrypoints, and assets.
2. Resolve a compact deck contract. Read [references/deck-contract.md](references/deck-contract.md) when page data, navigation, or delivery decisions need to be made. Missing final copy becomes a labeled placeholder; do not invent claims or metrics.
3. In exact-reproduction mode, first extract a fidelity ledger from the prompt: must-preserve slide/section structure, media, script/load order, motion and transition sequence, proportions, interactions, and hard runtime constraints; separately list only the substitutions the user explicitly authorizes. Apply those constraints before normal Hero/project conventions. Read [references/exact-reproduction.md](references/exact-reproduction.md).
4. Apply remaining constraints in this order: user request, existing Hero/design system, project conventions, then skill defaults. Proceed on reversible assumptions when the user has requested implementation. Ask only for a material ambiguity or an external/irreversible action, unless the user explicitly requested an alignment gate.
5. Implement in the existing stack. Reuse the Hero’s tokens, components, typography, media treatment, and motion language; add shared components only when they reduce real repetition. In exact mode, do not turn a supplied implementation recipe into a loose visual reference or redesign unspecified details. Keep slide content concise enough to present and keep unrelated dirty work intact.
6. Provide presentation behavior appropriate to the request: semantic slide sections, visible focus, keyboard navigation and hash/deep links when navigation is requested, responsive fallback, and reduced-motion behavior. In exact mode, preserve specified controls and choreography; add no decorative animation that competes with or changes the supplied behavior.
7. Read [references/validation.md](references/validation.md), then build, preview, inspect every slide at the target ratio, and fix issues before delivery.

## Completion and delivery

A task is complete when every requested slide renders, the Hero-derived visual system remains coherent, the requested navigation works, and build/preview plus target-viewport inspection have passed or have concrete blockers documented. Continue through fixes instead of stopping after a first draft for routine review.

Report changed files, actual commands and results, preview URL or entrypoint, slide/interaction checks, assumptions and fallbacks, and any known blocker. Create a zip or convert to `.pptx` only when requested, and clearly label the artifact type.

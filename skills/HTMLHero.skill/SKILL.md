---
name: HTMLHero.skill
description: "Build or extend a runnable, responsive Hero first screen for an HTML/React site or web presentation, including exact/recreate-exactly briefs that require preserving structure, media, motion, and runtime constraints. Use this for the Hero itself; use HTMLPPT.skill for a multi-slide deck."
---

# HTMLHero.skill

Turn a Hero brief or an existing first-screen implementation into a runnable, reviewable Hero. The first screen should establish a visual system that can be extended later.

## Route

- Use for a new or changed Hero first screen with layout, copy, media, or interaction.
- If the request is a multi-slide HTML presentation, use `HTMLPPT.skill` instead.
- If the request is only visual ideation or copy, do not force an implementation workflow.
- If the supplied brief says `exact`, `recreate exactly`, `pixel-perfect`, `严格复刻`, `完全一致`, or gives a build/runtime recipe, enter exact-reproduction mode. Read [references/exact-reproduction.md](references/exact-reproduction.md) before interpreting or implementing it.

## Workflow

1. Establish the finish line and scope. Inspect the target directory, recent `AGENTS.md`, `package.json`, lockfile, relevant entrypoints, and referenced assets. Do not read the whole repository by default.
2. Resolve the smallest useful Hero contract: purpose and audience, required copy, visual references, media, interactions, target viewport, existing stack, and delivery target. Read [references/hero-contract.md](references/hero-contract.md) when inputs are incomplete or the work will be handed off.
3. In exact-reproduction mode, first extract a fidelity ledger from the prompt: must-preserve structure, media, script/load order, motion sequence, proportions, interactions, and hard runtime constraints; separately list only the substitutions the user explicitly authorizes. Apply those constraints before normal project conventions. Read [references/exact-reproduction.md](references/exact-reproduction.md).
4. Apply remaining constraints in this order: user request, existing design system and project conventions, then skill defaults. Make reversible assumptions and state them. Ask only when a missing decision materially changes the result or crosses a real permission boundary; a routine local implementation does not need a ritual confirmation.
5. Implement in the existing stack and file structure. For a new project, choose the smallest viable starter for the requested output; do not force React, Tailwind, animation libraries, or new dependencies. Preserve unrelated dirty work and avoid overwriting files outside scope.
6. Make the Hero usable without unavailable assets: provide a poster, gradient, local fallback, or explicit placeholder when appropriate. In exact mode, preserve the media slot, dimensions, timing, and loading behavior while documenting any fallback; do not silently replace a required asset with a different visual treatment. Keep CTA targets meaningful, use semantic HTML, and treat animation as optional and reduced-motion aware only when the supplied specification permits it.
7. Read [references/validation.md](references/validation.md) for the relevant checks. Continue through build, preview, visual inspection, and fixes until the finish line is met or a concrete blocker remains.

## Completion and delivery

A task is complete when the requested Hero is implemented, the available build/preview path has been exercised, the target viewport has been inspected, and material failures have been fixed or clearly reported. Do not stop after the first implementation merely to request review when the remaining work is safe and in scope.

Report the changed files, actual run/build commands and results, preview URL or entrypoint, visual/interaction checks, assumptions or fallbacks, and any concrete blocker. Only create a zip or publish when requested.

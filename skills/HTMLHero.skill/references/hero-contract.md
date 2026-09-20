# Hero contract

Use this reference only when the brief, project, or handoff needs a compact contract. Infer values from the request and existing code before asking questions.

## Inputs

- **Goal:** audience, job-to-be-done, and the one action the first screen should support.
- **Copy:** required title, supporting text, labels, and language. Missing final copy should become a visible, clearly marked placeholder rather than invented claims.
- **Visual system:** reference URL/image, colors, typography, spacing, existing tokens, and components.
- **Media:** local files or URLs, required behavior, poster/alt text, licensing or offline needs.
- **Interaction:** CTA behavior, pills/tabs, hover/focus, motion, keyboard behavior, and reduced-motion preference.
- **Runtime:** target project and stack, desktop/mobile viewports, browser constraints, and delivery form (source, preview, zip).

## Defaults

- Existing project and dependencies take precedence over a new stack.
- Missing media uses a local asset, poster, gradient, or explicit placeholder that keeps the layout usable.
- Missing viewport uses a desktop check plus a narrow mobile check; use the project’s documented viewport when available.
- Missing external CTA target is a button or marked placeholder, never a misleading `#` link.
- Remote fonts/media are optional; keep a fallback for slow, blocked, or offline loading.

## Output

The implementation should expose a clear entrypoint, shared visual tokens where future pages can reuse them, and a short handoff containing assumptions, preview/build commands, and known limitations.

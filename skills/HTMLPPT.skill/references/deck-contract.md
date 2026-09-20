# Deck contract

Use this reference only when the deck shape is not already explicit. Infer from the request and existing Hero before asking questions.

## Inputs

- **Hero source:** existing route/component or a validated Hero brief; record its tokens and reusable components.
- **Content:** slide order, purpose, required copy/data, speaker-facing density, and any content that must remain verbatim.
- **Canvas:** target ratio and viewport (16:9 is a default for presentation work), safe margins, responsive behavior, and print/export needs.
- **Navigation:** arrow/buttons, Home/End, PageUp/PageDown, hash/deep-link behavior, progress indicator, and focus rules as requested.
- **Assets:** local/remote media, fonts, poster/fallback, and offline/CORS constraints.
- **Delivery:** source project, runnable preview, static package, or explicitly requested `.pptx` conversion.

## Page model

Keep slide data separate from rendering when the project supports it. A useful minimal shape is:

```js
{
  id: "problem",
  type: "content",
  title: "...",
  eyebrow: "...",
  body: ["..."],
  visual: { kind: "image", src: "...", alt: "..." }
}
```

Use the project’s own data model when one exists. Keep IDs stable so hash links and tests do not break when copy changes.

## Defaults and boundaries

- Existing Hero tokens and components are the source of truth; do not redesign the first page casually.
- Missing content uses a labeled placeholder and is listed in the handoff.
- If content does not fit, recompose or shorten on-screen copy before making it unreadably small.
- External media gets a local/visual fallback when offline or blocked delivery matters.
- HTML, static package, and `.pptx` are distinct outputs; state which one was produced.

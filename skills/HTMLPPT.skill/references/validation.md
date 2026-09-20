# HTML deck validation

Use the project’s actual package manager and scripts. Do not hard-code `npm` when a lockfile or `packageManager` field selects pnpm, yarn, or bun.

## Required evidence

- Run the available build or equivalent check and record the exact command and result.
- Start dev/preview and verify the real URL or entrypoint.
- Inspect every slide at the target ratio (use 16:9 and a representative 1440×900 viewport when unspecified) and at least one narrow viewport if responsive behavior is part of the request.
- Confirm each slide is addressable and renders without unexpected scroll, clipping, overflow, overlap, missing fonts, or blocked media. Verify the first page still matches the Hero system.
- Exercise the requested buttons, arrow/PageUp/PageDown/Home/End navigation, hash/deep links, focus states, and any presenter controls. Check semantics, contrast, and reduced motion.
- Check the console for new errors that affect rendering or interaction.

## Recovery

- Build or route failure: fix errors introduced by the requested change and rerun affected checks.
- Content overflow: recompose or shorten screen copy while preserving meaning; do not hide a slide or shrink text until unreadable.
- External asset/font/CORS failure: use a documented fallback and keep the slide functional.
- Missing Hero or content: route back to `HTMLHero.skill` or use labeled placeholders; do not silently invent a visual system or facts.
- Browser/screenshot unavailable: complete static and runtime checks that are possible, report the unverified items, and do not claim full visual acceptance.

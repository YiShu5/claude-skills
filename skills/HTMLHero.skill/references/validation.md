# Hero validation

Use only the checks relevant to the current project. Prefer the project’s package manager from its lockfile or `packageManager` field; do not assume `npm`.

## Required evidence

- Run the available build or equivalent check and record the exact command and result.
- Start the dev/preview path when available and verify the real URL responds.
- Inspect at least one desktop viewport (use 1440×900 when no target is given) and one narrow viewport (use 390×844 when no target is given).
- Confirm the first screen is non-empty, the main heading and primary action are visible, and there is no horizontal overflow, clipping, overlap, or accidental scroll.
- Exercise the primary interaction, keyboard focus, and any navigation. Check media loading plus poster/fallback, semantic labels, contrast, and `prefers-reduced-motion` when motion exists.
- Compare against the supplied reference or tokens when a reference exists. Check the console for new errors that affect the requested behavior.

## Recovery

- Build failure: fix errors caused by the requested change and rerun the affected check.
- Port occupied: use an available port and report the actual URL.
- Asset/font/CORS failure: keep a usable local or visual fallback and record the degradation.
- Missing dependency or unreadable attachment: preserve existing work and report the exact blocker and next action.
- Browser or screenshot unavailable: complete static checks, state the unverified items, and do not claim visual validation.

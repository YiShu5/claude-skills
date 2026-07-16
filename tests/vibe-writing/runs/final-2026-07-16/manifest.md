# Superseded Refactor Run Manifest — 2026-07-16

This evidence set used the generalized personal-fact rule but preceded the
final `voice-profile.md` refinement. It is retained to document the observed S8
failure and is excluded from final pass counts.

- Repository base commit: `15d09c4ea94bd5c2a73e9e09777f3bfe6f68aba1`
- Skill content digest: `84ec41c5c3a11798d04fc3e3143f8390ea666a2ad1255110801bbda68a84ca1a`
- Process results: 15 completed, 0 timeouts, 0 pre-response errors.
- Raw outputs: the sibling `.txt` files in this directory.

## Demonstrated failure

`s8-r1` correctly labeled formal punctuation and sentence rhythm uncertain, but
ended by offering to turn the memory dossier alone into more specific rules. It
did not recommend real authored samples as the scenario requires. This caused
the minimal conditional refinement in `references/voice-profile.md` and a new
complete final sweep under a new content digest.

All outputs in this directory are refactor history only. None are counted in
the final S1–S10 pass totals.

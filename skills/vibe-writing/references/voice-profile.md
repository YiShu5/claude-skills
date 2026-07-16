# Voice Profile

Use this reference only when the task depends on learning, applying, or updating
an author's voice. Build a project-specific working model, not a biography or a
universal personality description.

## Accepted Inputs

Accept any of these inputs:

- 2–5 real samples written by the author, preferably recent and relevant
  to the current project.
- A ChatGPT memory transfer or memory dossier.
- A short style card containing explicit preferences.
- An existing project voice profile.

Do not require every input type. When no voice evidence is available, use
neutral Chinese appropriate to the task instead of fabricating a persona.

## Evidence and Confidence

Apply evidence in this order after the current task instruction:

1. Current-project real samples.
2. An author-confirmed project profile or explicit style card.
3. A memory transfer as candidate context.
4. A neutral default.

Label every material trait:

| Confidence | Use |
|---|---|
| high | The author confirmed it, or it recurs consistently across multiple real samples. |
| medium | Some real evidence or prior feedback supports it, but its range is not yet clear. |
| low | It is a tentative inference from limited or indirect evidence. |
| unknown | Evidence is absent or conflicting. |

Keep conversational voice separate from formal writing voice. Chat phrasing,
casual jokes, and assistant-written text may suggest candidates but do not prove
how the author writes an article, analysis, or technical document.

When memory-derived material is the only evidence and the task asks for formal
writing mechanics such as punctuation or sentence rhythm, the response must:

1. Label those mechanics low-confidence or unknown.
2. Use a neutral formal default only as interim guidance.
3. Recommend 2–5 real authored samples before assigning concrete voice rules.

Do not offer to turn the memory dossier alone into specific formal-writing rules.

## Observable Dimensions

Describe only observable, usable tendencies:

- Viewpoint and formality.
- Sentence rhythm, paragraph density, and information density.
- Emotional intensity and humor.
- Argument style and structure, including openings, transitions, and endings.
- Vocabulary, terminology, punctuation, and layout.
- Preferred expressions and avoided expressions.
- Material boundaries: confirmed reusable material, material requiring
  confirmation, and protected or prohibited material.

Record conflicting evidence and platform-specific variation instead of forcing
one rule across every genre.

## Build or Update the Profile

1. Identify each input's origin, date, genre, and relevance.
2. Separate direct evidence from inference.
3. Extract patterns without copying sample phrases into the profile or draft.
4. Assign a confidence label and evidence note to every material trait.
5. Separate reusable material from facts or experiences requiring confirmation.
6. Record conflicts and unknowns rather than resolving them by guesswork.
7. Use the project template and propose any update for the author to approve.

Never treat a memory dossier as verified biography, factual evidence, or proof
of formal writing style. Never reuse a sample's distinctive phrase merely to
simulate the author.

## Storage and Consent

Store user-specific evidence outside the public skill only after the user
consents:

- `writing-workspace/sources/chatgpt-memory-dossier.md` for the source dossier.
- `writing-workspace/style-profile.md` for the confirmed working profile.

Do not create these files by default. Do not store personal source material
inside the skill. At the end of later writing work, propose profile changes when
stable new evidence appears; never overwrite the existing profile automatically.

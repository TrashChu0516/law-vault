# Master Legal Index — Key Principles

> Auto-generated: **case → key ratio/principle**, driven by the inline `#key-principle/…` tag. This is your **ratio bank** — the revision gold.
>
> **How to tag a ratio (Steven):** put the principle on a bullet (`- …`), end the line with `#key-principle/<doctrine>` (doctrine from [[TAG_TAXONOMY]]) or `#obiter`. It appears below automatically.
>
> **Doctrine-tagged ratios** roll up in Obsidian's tag pane (`#key-principle/certainty`, `#key-principle/formation/objective-approach`, …) — click any to see all ratios of that doctrine.

## All key principles

```dataview
TABLE WITHOUT ID
  file.link AS "Case",
  replace(join(L.tags, ", "), "key-principle/", "") AS "Doctrine",
  L.text AS "Ratio"
FROM "cases"
FLATTEN file.lists AS L
WHERE contains(join(L.tags, " "), "key-principle")
SORT file.name ASC
```

## Obiter / notable dicta

```dataview
TABLE WITHOUT ID
  file.link AS "Case",
  L.text AS "Dictum"
FROM "cases"
FLATTEN file.lists AS L
WHERE contains(join(L.tags, " "), "obiter")
SORT file.name ASC
```

---

### Notes for future notes

- The ratio tag **must** be a list item (`- text #key-principle/…`), not a blockquote/callout — Dataview only exposes list items via `file.lists`.
- In `file.lists`, tags are stored **without** the `#`, and `L.text` holds the bullet text (tags stripped).
- Doctrine comes from [[TAG_TAXONOMY|the taxonomy]] — never invent one. If a ratio doesn't fit an existing doctrine, add the doctrine to the taxonomy first (Clawclaw), then tag.
- A bare `#key-principle` (no `/doctrine`) still works — it shows under "Doctrine" as `key-principle` until you assign one.

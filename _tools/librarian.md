---
type: system
area: tools
---

# Librarian — data-quality check

> The accountability layer. Open this note in **reading view** and Dataview flags anything that has slipped through. **Fix any row that appears below** — an empty table is a healthy vault.
>
> Vocabulary: [[TAG_TAXONOMY|Tag taxonomy]]

## Cases missing tags

```dataview
TABLE WITHOUT ID file.link AS "Case"
FROM "cases"
WHERE type = "case" AND (!tags OR length(tags) = 0)
```

## Cases missing module

```dataview
TABLE WITHOUT ID file.link AS "Case"
FROM "cases"
WHERE type = "case" AND !module
```

## Cases missing topic

```dataview
TABLE WITHOUT ID file.link AS "Case"
FROM "cases"
WHERE type = "case" AND (!topic OR length(topic) = 0)
```

## Cases missing week

```dataview
TABLE WITHOUT ID file.link AS "Case"
FROM "cases"
WHERE type = "case" AND !week
```

## Cases missing status

```dataview
TABLE WITHOUT ID file.link AS "Case"
FROM "cases"
WHERE type = "case" AND !status
```

---

## Stray tags (not in the taxonomy)

> Dataview can't easily diff against the controlled list, so this is **Clawclaw's manual pass**: every entry in a case's `tags:` must appear in [[TAG_TAXONOMY]]. If you spot a tag you don't recognise, flag it and it gets fixed there. The rule stays: **a tag only exists if it maps to an outline section.**

# Correction log CLI

Use the correction manager to record feedback in project/channel JSON logs without relying on chat history alone. It uses only the Python standard library.

## Record feedback

```bash
python scripts/manage_corrections.py projects/the-clever-little-rabbits/corrections.json add \
  --project-id clever-little-rabbits --category voice --scene-id scene-04 \
  --issue "Narration is too fast" --requested-change "Reduce delivery speed by about 10%"
```

New entries are always `proposed`; they are not treated as approved preferences.

## Track execution and approval

```bash
python scripts/manage_corrections.py projects/the-clever-little-rabbits/corrections.json mark-applied corr-XXXXXXXXXXXX \
  --applied-change "Retimed narration and re-rendered scene 4"
python scripts/manage_corrections.py projects/the-clever-little-rabbits/corrections.json approve corr-XXXXXXXXXXXX \
  --approved-by user
```

Approval must be explicit and the approver must be supplied. An applied correction is not automatically a reusable preference.

## Channel-wide reusable rules

Record channel rules in `defaults/correction-rules.json` with `--scope channel`, `--reuse-as-rule`, and a plain-language `--rule-text`. They remain inactive until explicitly approved:

```bash
python scripts/manage_corrections.py defaults/correction-rules.json add --scope channel \
  --category pacing --issue "Narration consistently feels rushed" \
  --requested-change "Use a calmer delivery" --reuse-as-rule \
  --rule-text "Use a slightly slower, warm narration pace; keep words clear."
python scripts/manage_corrections.py defaults/correction-rules.json approve corr-XXXXXXXXXXXX --approved-by user
python scripts/manage_corrections.py defaults/correction-rules.json rules
```

`rules` outputs only approved/verified channel entries explicitly marked reusable. Rejected entries never become rules. Use `list --status proposed` to review outstanding feedback and `reject <id> --reason ...` to keep rejected suggestions documented.

## Status meanings

- `proposed`: captured, not yet applied or approved.
- `applied`: the correction was made, but approval for reuse is not implied.
- `approved`: explicitly approved; if marked as a reusable channel rule, it may be loaded as a future default.
- `rejected`: retained for audit, not applied as a rule.
- `verified`: reserved for a verified approved correction; the CLI does not set this automatically.

Never store passwords, API keys, private session links, or sensitive personal data in corrections. Keep a correction specific, with scene/timecode and evidence reference where practical.

# Synthetic contribution-calendar art

This repository contains **generated, backdated Git author timestamps for calendar art**. It is not evidence of programming, employment, project delivery, or work performed on those historical dates.

- Actual generation date: **20 October 2026**.
- Synthetic author-date range: **1 January–19 October 2026**, inclusive.
- Density: **one generated commit per date** (292 dates).
- Every commit message explicitly identifies the entry as synthetic calendar art.
- Committer timestamps retain the actual time of generation. Only author timestamps are backdated.
- `calendar.csv` is the generated ledger; all entries explicitly say `synthetic_calendar_art`.

This is a separate, standalone repository. It does not rewrite the history of any project. No recurring automation, installation, or external service is required.

## Reproduce in a new copy

`generate_calendar.py` uses Python's standard library and Git. It refuses to run inside an existing Git repository so it cannot overwrite an existing history.

```powershell
python generate_calendar.py --author-name "YOUR NAME" --author-email "YOUR GITHUB-LINKED NOREPLY EMAIL"
```

The script produces local history only; it does not create a GitHub repository or push anything. Backdated authorship is a visual artifact, not a claim of historical work.

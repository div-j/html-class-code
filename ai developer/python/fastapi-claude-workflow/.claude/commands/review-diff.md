# /review-diff

Perform a safety and quality review of the current uncommitted changes.

Execute:
1. Run `git diff`.
2. Inspect changes against project coding rules in `CLAUDE.md`.
3. Check for exposed secrets, unexpected side effects, or missing tests.
4. Provide a structured review report.
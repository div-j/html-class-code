# /fix-tests

Automate test failure analysis and resolution.

Execute:
1. Run `pytest`.
2. Analyze any failing test output.
3. Propose target fixes to resolve failures without changing expected test assertions unless authorized.
4. Rerun `pytest` to confirm resolution.
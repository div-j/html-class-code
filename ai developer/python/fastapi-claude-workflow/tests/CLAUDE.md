# Testing Guidelines
- Use `pytest` and `fastapi.testclient.TestClient`.
- Name test files with prefix `test_` (e.g., `test_feature.py`).
- Every endpoint must cover success (2xx) and failure (4xx/5xx) paths.
- Mocks must be cleaned up or scoped to function level.
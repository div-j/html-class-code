# FastAPI Project Overview & Guidelines

## Overview
Small FastAPI service engineered for safe, repeatable AI-assisted workflows.

## Directory Structure
- `app/`: FastAPI application endpoints and core logic.
- `tests/`: Pytest test suite.
- `docs/`: Project documentation and review reports.
- `.claude/`: Claude Code configurations, memory, and custom slash commands.

## Essential Commands
- **Run App:** `uvicorn app.main:app --reload`
- **Run Tests:** `pytest`
- **Linting:** `flake8 app tests`

## Coding Rules
- Use type hints for all function signatures.
- Prefer explicit Pydantic models for request/response bodies.
- Follow PEP 8 guidelines.
- Never write implementation code without corresponding unit tests.
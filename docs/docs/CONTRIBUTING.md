# Contributing & Strict Rules

## Open Source Rules
1. **Branching:** Use `feature/`, `fix/`, or `docs/` prefixes.
2. **PRs:** All PRs must include a test plan. No PR is merged without 2 reviews.
3. **Commit Messages:** Follow Conventional Commits (e.g., `feat: add CogniSync caching`).
4. **Code Quality:** Linting (ESLint/Black) is enforced via Husky pre-commit hooks.
5. **No Credentials:** Never commit `.env` files or API keys. Use `.env.example`.
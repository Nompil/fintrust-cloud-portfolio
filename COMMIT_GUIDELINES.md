Commit Message Guidelines

Follow this commit message structure so your git history reads like a professional engineering project.

Format:

```
type: short description
```

Types to use:
- `docs` — Documentation changes (README, reflections, diagrams)
- `feat` — New functionality or scripts
- `fix` — Bug fixes
- `refactor` — Code refactoring with no behavior change
- `chore` — Maintenance tasks (dependencies, build, cleanup)

Examples:

```
docs: add week 5 VPC architecture notes
feat: add pandas transaction analysis
fix: resolve database path issue in analyse.py
refactor: split ETL pipeline into package modules
chore: update requirements file
```

Guidelines:
- Keep commits small and focused.
- Use the imperative mood and present tense.
- Avoid vague messages like `final`, `done`, or `update`.
- Reference files or modules when helpful: `fix: correct path in week04/analyse.py`.

Workflow reminder:
1. `git status`
2. `git diff` (review changes)
3. `git add <file>`
4. `git commit -m "type: short description"`
5. `git push origin main`

# New Data Project Checklist

Use this when a new project deserves to become portfolio material.

## Repository

- Clear English name, for example `financial-risk-dashboard`.
- Description focused on the problem, not only the tools.
- Topics such as `python`, `sql`, `analytics`, `data-engineering`, or `machine-learning`.

## Structure

- `README.md` explains the question, approach, stack, and how to run.
- `data/raw` and `data/processed` are ignored by default.
- `notebooks` contains exploration.
- `src` contains reusable logic.
- `reports` contains exported outputs.
- `tests` contains small checks for reusable code.

## First automation

- Keep the `Data project quality` workflow from the template.
- Add tests only for code that is meant to be reused.
- Avoid forcing notebooks to run in CI until the data source is stable.

## Profile

- Make the repo public when ready.
- Add data-oriented topics.
- Run the profile `Sync new repositories` action.

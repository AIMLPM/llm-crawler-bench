# Self-Improvement Instructions

You are reviewing this benchmark suite. Follow these steps in order:

## 1. Setup

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

## 2. Baseline

Run `make check` to see the current state of all invariants.

## 3. Review

Read `self_improvement/MASTER.md` for the full framework, then run each spec
(02 through 09) as described there. For each spec:

- Read the spec file
- Audit the files it covers
- Fix what you find
- Do NOT run benchmarks (they take hours and cost money)

## 4. Validate

Run `make review` to confirm all checks pass and see your diff.

## 5. Commit

Commit your changes with a clear summary of what you fixed and which specs
you reviewed.

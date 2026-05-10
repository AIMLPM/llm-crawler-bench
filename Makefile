.PHONY: test lint invariants preflight check check-invariants check-consistency check-lint review smoke readme benchmark benchmark-quick

PYTHON ?= .venv/bin/python

test:
	$(PYTHON) -m pytest tests/ -q

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) lint_reports.py

invariants:
	$(PYTHON) self_improvement/check_invariants.py
	$(PYTHON) self_improvement/check_cross_report_consistency.py

preflight: lint test invariants

# Self-assessment targets
check: check-invariants check-consistency check-lint

check-invariants:
	$(PYTHON) self_improvement/check_invariants.py

check-consistency:
	$(PYTHON) self_improvement/check_cross_report_consistency.py

check-lint:
	$(PYTHON) lint_reports.py

# Regenerate README.md from report data
readme:
	$(PYTHON) generate_readme.py

# Graduated smoke test: 5/30/100 pages per tool
smoke:
	$(PYTHON) benchmark_all_tools.py --smoke-only

# DS-13: Reproducibility — full v1.4 benchmark pipeline end-to-end.
# Runs the whole cycle from preflight through report generation against
# the most recent merged run dir. Expected wall time: ~24 hours on
# M-series hardware (most time is in reranker + LLM judging). Requires
# OPENAI_API_KEY in .env. See METHODOLOGY.md "Reproducibility" section.
benchmark: preflight
	$(PYTHON) benchmark_retrieval.py
	$(PYTHON) benchmark_answer_quality.py
	$(PYTHON) benchmark_pipeline.py
	$(PYTHON) generate_readme.py

# DS-13: fast end-to-end smoke (~5 min wall time, ~$0 spend on cached
# query embeddings) — verifies the retrieval pipeline runs against a
# single site without committing to a 24h cycle. Useful before kicking
# off a full benchmark, or after methodology changes.
RUN_DIR ?= run_v13_merged_20260504_203748
SMOKE_SITE ?= rust-book
benchmark-quick:
	$(PYTHON) benchmark_retrieval.py --run $(RUN_DIR) --sites $(SMOKE_SITE) --no-rerank --output reports/RETRIEVAL_QUICK_SMOKE.md
	@echo ""
	@echo "Smoke complete. Report: reports/RETRIEVAL_QUICK_SMOKE.md"
	@echo "Audit CSV: reports/QUERY_AUDIT.csv"

# Full self-improvement review: validate + show what changed
review: check
	@echo ""
	@echo "══ Changes ══════════════════════════════════════════"
	@if git diff --quiet && git diff --cached --quiet; then \
		echo "No changes detected."; \
	else \
		git diff --stat; \
		echo ""; \
		git diff; \
	fi

PYTHON ?= python
BUILD ?= build/yasc

.PHONY: validate generate test check site pages-build whitepaper harness harness-smoke harness-mcp-smoke security-gate package

validate:
	$(PYTHON) scripts/validate.py

generate:
	$(PYTHON) scripts/generate.py

test:
	pytest -q

check: validate generate test

site: generate
	$(PYTHON) -m http.server 8000 -d site

pages-build: package
	$(PYTHON) scripts/build_site.py

whitepaper:
	$(PYTHON) scripts/build_whitepaper.py

harness:
	$(PYTHON) scripts/yasc_harness.py summary
	$(PYTHON) scripts/yasc_harness.py plan-check examples/plans/smoke.yaml
	$(PYTHON) scripts/yasc_harness.py target-check examples/targets/mock-secure.yaml

harness-smoke:
	rm -rf $(BUILD)
	$(PYTHON) scripts/yasc_harness.py run --plan examples/plans/smoke.yaml --target examples/targets/mock-secure.yaml --out $(BUILD)/runs --evidence $(BUILD)/evidence --summary $(BUILD)/run-summary.json
	$(PYTHON) scripts/yasc_harness.py assess --plan examples/plans/smoke.yaml --runs $(BUILD)/runs --out $(BUILD)/assessment.json
	$(PYTHON) scripts/yasc_harness.py gate --plan examples/plans/smoke.yaml --runs $(BUILD)/runs --policy examples/gate-policy.yaml --out $(BUILD)/gate.json
	$(PYTHON) scripts/yasc_harness.py report --plan examples/plans/smoke.yaml --runs $(BUILD)/runs --gate-result $(BUILD)/gate.json --html $(BUILD)/assessment.html --pdf $(BUILD)/assessment.pdf


harness-mcp-smoke:
	rm -rf $(BUILD)/mcp
	$(PYTHON) scripts/yasc_harness.py run --plan examples/plans/mcp-smoke.yaml --target examples/targets/mcp-stdio.yaml --scenarios examples/scenarios/mcp.yaml --out $(BUILD)/mcp/runs --evidence $(BUILD)/mcp/evidence --summary $(BUILD)/mcp/run-summary.json
	$(PYTHON) scripts/yasc_harness.py gate --plan examples/plans/mcp-smoke.yaml --runs $(BUILD)/mcp/runs --policy examples/gate-policy-mcp.yaml --out $(BUILD)/mcp/gate.json

security-gate: harness-smoke harness-mcp-smoke

package: check
	$(PYTHON) scripts/package_release.py

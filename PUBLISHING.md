# Publishing YASC v1.0 to GitHub

YASC v1.0 is the first stable release of the evidence-driven baseline and executable verification harness. The Git repository is the source of truth; PDF/DOCX whitepapers and ZIP archives are release artifacts.

## 1. Pre-release verification

From the repository root:

```bash
python -m pip install -e ".[pdf]"
make check
make security-gate
make whitepaper
make package
```

`make security-gate` must produce passing Agent and MCP gates. The repository test suite also verifies that an intentionally insecure fixture is rejected.

Before the first Pages deployment, set **Settings → Pages → Build and deployment → Source → GitHub Actions**. This one-time repository setting is required by GitHub for custom Pages workflows.

## 2. Create or update repository history

For a new repository:

```bash
git init -b main
git add .
git commit -m "Release YASC v1.0.0"
```

For an existing repository, commit the v1.0 changes normally after review.

## 3. Push to GitHub

For a new or empty GitHub repository, the release tree includes a one-command publisher. It pushes `main`, enables the GitHub Pages `workflow` publishing source through the GitHub API, and pushes `v1.0.0` to trigger both Release and Pages workflows:

```bash
./scripts/publish_github.sh <OWNER>/yofune-agent-security-checklist --public
```

Or perform the steps manually with GitHub CLI:

```bash
gh repo create <OWNER>/yofune-agent-security-checklist \
  --public \
  --source=. \
  --remote=origin \
  --push
```

Or configure an existing empty repository:

```bash
git remote add origin git@github.com:<OWNER>/yofune-agent-security-checklist.git
git push -u origin main
```

## 4. Repository settings

Enable GitHub Pages with **GitHub Actions**. Protect `main` and require at least these checks before merge:

- repository validation / test suite;
- YASC Security Gate;
- review for changes to `schema/`, `verification-tests/`, `harness/`, `crosswalk/`, and security-gate policy.

Do not place production credentials in target YAML. Use `${ENV_VAR}` placeholders and CI secrets.

## 5. Stable v1.0 release

After final review:

```bash
git tag -a v1.0.0 -m "YASC v1.0.0 — executable verification baseline"
git push origin main --tags
```

Pushing the `v1.0.0` tag triggers `.github/workflows/release-artifacts.yml`. The workflow re-runs validation and Agent/MCP security gates, rebuilds the whitepapers and source ZIP, then creates or updates the GitHub Release using `releases/v1.0.0/RELEASE_NOTES.md`. It uploads the source ZIP, checksum, English/Chinese PDFs, and sample Assessment Report.

GitHub Pages is deployed by `.github/workflows/pages.yml` on `main`, release tags, or manual dispatch. The Pages artifact includes the interactive checklist, release page, source ZIP/checksum, and branded whitepaper downloads.

## 6. Release integrity

Publish the SHA-256 file next to the ZIP and keep the reference snapshot/date visible in the whitepaper and changelog. Any material change to controls, tests, adapters, evidence semantics, or gate behavior should result in a new version.

## Organization metadata

Published by **Chengdu Yofune Ariake Technology Co., Ltd. / Yofune Security Research**.

- Website: https://yofunesec.com/
- Contact: contact@yofunesec.com

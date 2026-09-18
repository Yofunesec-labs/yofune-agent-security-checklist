#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-}"
VISIBILITY="${2:---public}"
TAG="v1.0.0"

if [[ -z "$REPO" || "$REPO" != */* ]]; then
  echo "Usage: $0 OWNER/yofune-agent-security-checklist [--public|--private]" >&2
  exit 2
fi
if [[ "$VISIBILITY" != "--public" && "$VISIBILITY" != "--private" ]]; then
  echo "Visibility must be --public or --private" >&2
  exit 2
fi
command -v git >/dev/null || { echo "git is required" >&2; exit 2; }
command -v gh >/dev/null || { echo "GitHub CLI (gh) is required" >&2; exit 2; }
gh auth status >/dev/null

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -d .git ]] || { echo "This release directory is not a Git repository. Restore from yasc-v1.0.0.gitbundle or initialize Git first." >&2; exit 2; }
[[ -z "$(git status --porcelain)" ]] || { echo "Working tree is not clean; commit/review changes before publishing." >&2; exit 2; }
git rev-parse --verify "$TAG" >/dev/null || { echo "Missing release tag $TAG" >&2; exit 2; }

if ! git remote get-url origin >/dev/null 2>&1; then
  if gh repo view "$REPO" >/dev/null 2>&1; then
    git remote add origin "https://github.com/${REPO}.git"
  else
    gh repo create "$REPO" "$VISIBILITY" --source=. --remote=origin
  fi
fi

REMOTE_REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || true)"
if [[ -n "$REMOTE_REPO" && "$REMOTE_REPO" != "$REPO" ]]; then
  echo "origin resolves to $REMOTE_REPO, not requested $REPO" >&2
  exit 2
fi

echo "Pushing main to $REPO ..."
git push -u origin main

# GitHub Pages custom Actions workflows require the repository Pages source to be workflow.
if gh api "repos/$REPO/pages" >/dev/null 2>&1; then
  gh api --method PUT "repos/$REPO/pages" -f build_type=workflow >/dev/null
else
  gh api --method POST "repos/$REPO/pages" -f build_type=workflow >/dev/null
fi

echo "GitHub Pages source set to workflow."
echo "Pushing $TAG; this triggers both Release and Pages workflows ..."
git push origin "$TAG"

echo
echo "Published Git refs. Follow workflow status with:"
echo "  gh run list --repo $REPO --limit 10"
echo "Release: https://github.com/$REPO/releases/tag/$TAG"

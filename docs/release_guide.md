# Release & Deployment Guide

This project automates the release process using GitHub Actions. Follow these steps to publish a new version of `whisper-vtt2srt`.

## 1. One-Time Setup: PyPI Trusted Publishing

We use PyPI's **Trusted Publishing** (OIDC) to securely publish packages without needing passwords or API tokens.

1. Go to your [PyPI Settings](https://pypi.org/manage/account/).
2. Scroll to "Publishing" and click **"Add a new publisher"**.
3. Select **GitHub**.
4. Fill in the details:
    - **Owner**: `jorcelinojunior`
    - **Repository**: `whisper-vtt2srt`
    - **Workflow name**: `release.yml`
    - **Environment**: (Leave blank)
5. Click **"Add publisher"**.

## 2. How to Publish a New Version

When you are ready to release, simply create and push a Git tag:

1. **Update the version**: Change the `version` field in `pyproject.toml`.
2. **Update the Changelog**: Add the new version details to `CHANGELOG.md`.
3. **Commit and Tag**:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "chore: release v0.1.0"
   git tag v0.1.0
   git push origin main --tags
   ```

### What happens next?
- The **Release** workflow will trigger.
- It runs the full CI suite (`pytest`, `ruff`, `mypy`).
- If successful, it creates a **GitHub Release** with automated notes.
- It publishes the package to **PyPI** automatically.

## 3. Manual Release (Emergency only)

If you ever need to build and upload manually:

```bash
# Install build tool
pip install build twine

# Build
python -m build

# Upload
python -m twine upload dist/*
```

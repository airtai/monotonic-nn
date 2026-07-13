# Releasing

`monotonic-nn` is a deprecated compatibility shim over
[mononet](https://github.com/davorrunje/mononet). Publishing uses **PyPI
Trusted Publishing** (OIDC) via [`.github/workflows/publish.yml`](.github/workflows/publish.yml)
— no API tokens or stored secrets.

## One-time setup (maintainer, web UI)

1. **GitHub environments.** Repo Settings → Environments → create `testpypi`
   and `pypi`.
2. **TestPyPI trusted publisher** — at
   <https://test.pypi.org/manage/account/publishing/> add a publisher:
   - Project name: `monotonic-nn`
   - Owner: `airtai`, Repository: `monotonic-nn`
   - Workflow name: `publish.yml`
   - Environment name: `testpypi`
3. **PyPI trusted publisher** — repeat at
   <https://pypi.org/manage/account/publishing/> with environment name `pypi`.

If a value is wrong, the upload fails at the OIDC exchange with a
"not a trusted publisher" error.

## Version

The version lives in `pyproject.toml` (`project.version`) and
`airt/__init__.py` (`__version__`), and is asserted in
`tests/test_reexport.py`. Keep all three in sync.

## TestPyPI rehearsal (recommended before every real release)

1. Ensure `main` is green.
2. Actions → **Publish** → Run workflow → `target: testpypi`.
3. Verify the project page at <https://test.pypi.org/project/monotonic-nn/> and
   a clean install. Dependencies (`mononet`, `tensorflow`) are not on TestPyPI,
   so pull them from real PyPI:
   ```sh
   pip install --pre \
     -i https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple/ \
     monotonic-nn==<version>
   ```

## Real PyPI release

1. Bump the version (`pyproject.toml`, `airt/__init__.py`,
   `tests/test_reexport.py`) and update `CHANGELOG.md`; merge to `main`.
2. Create a **GitHub Release**: tag `v<version>` (e.g. `v0.4.0`), target the
   merge commit on `main`. Mark **pre-release** for alphas/betas/rcs.
3. Publishing the release fires the **Publish** workflow to real PyPI. It fails
   fast if the tag does not match the `pyproject.toml` version.

## Planned final release: v0.4.0

`0.4.0` is intended as the **final** release of this shim, cut once
**mononet 0.0.1** is published to PyPI. Before tagging `v0.4.0`:

- [ ] mononet `0.0.1` is live on PyPI.
- [ ] Bump version `0.4.0a1` → `0.4.0` in `pyproject.toml`, `airt/__init__.py`,
      and `tests/test_reexport.py` (assertion + test name).
- [ ] Change the dependency in `pyproject.toml` from `mononet>=0.0.0a1` to
      `mononet>=0.0.1` (drops the prerelease specifier so a stable install does
      not pull mononet prereleases).
- [ ] Update `CHANGELOG.md` (`## 0.4.0`) and the README banner
      (`v0.4.0a1` → `v0.4.0`).
- [ ] TestPyPI rehearsal, then the GitHub Release `v0.4.0`.

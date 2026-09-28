# Contributing

## Branching model

Work flows in one direction: short-lived branches → `dev` → `staging` → `main`.
Nobody pushes directly to `dev`, `staging` or `main`; every change arrives through a reviewed pull request.

| Branch | Purpose | Created from | Merges into |
|---|---|---|---|
| `main` | Production: released, tagged models only | — | — |
| `staging` | Release candidate, reproduced and validated | `main` | `main` |
| `dev` | Integration of finished work | `main` | `staging` |
| `feat/<name>` | Features, pipeline changes, refactors | `dev` | `dev` (delete after merge) |
| `data/<name>` | Dataset updates tracked with DVC | `dev` | `dev` (delete after merge) |
| `exp/<member>-<idea>` | Experiments, may never merge | `dev` | Nothing directly: cherry-pick the winner into a `feat/` branch |
| `fix/<name>` | Urgent production fix | `main` | `main` (patch tag, e.g. `model-v1.0.1`), then merge `main` back into `dev` |

Branch names are lowercase and hyphen-separated, e.g. `feat/add-scaling`, `data/remove-duplicates`, `exp/areeba-max-depth`.

Keep `exp/` branches short-lived: `git fetch && git rebase origin/dev` often.

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/): `<type>: <short imperative summary>`.

| Type | Use for | Example |
|---|---|---|
| `feat` | New code or pipeline step | `feat: add scaling step` |
| `fix` | Bug fix | `fix: correct target column name` |
| `data` | Dataset changes (DVC) | `data: remove duplicate rows` |
| `exp` | Experiment runs | `exp: try max_depth=8` |
| `test` | Tests | `test: add smoke test for training` |
| `docs` | Documentation | `docs: update README` |
| `build` | Dependencies, environment | `build: add dvc` |
| `ci` | CI workflows | `ci: add lint job` |
| `chore` | Housekeeping | `chore: update .gitignore` |
| `refactor` | Code restructuring, no behaviour change | `refactor: split train into stages` |

## Merge policy

- **PRs into `dev` are squash-merged.** One PR = one commit on `dev` with a Conventional Commit title.
- **Release PRs (`dev` → `staging`, `staging` → `main`) use a merge commit**, so the promoted history stays identical across branches.
- Delete the source branch after merging (except `exp/` branches we keep as a record).

## Pull requests

- Every PR needs **1 approval** from a teammate and passing CI.
- Fill in the PR template, including metrics before → after if the model changed.
- Reviewers check out the branch and run it at least once when the pipeline changes.

## Data and models

- Datasets and models are never committed to Git; they are tracked with DVC.
- **Always run `dvc push` before `git push`.**
- Never commit credentials; keep DVC remote credentials in `.dvc/config.local` or environment variables.

## Local setup

```bash
uv sync
uv run python -m src.dataset
uv run python -m src.modeling.train
uv run pytest
```

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
- **Check the base branch before creating the PR.** Feature, data and docs PRs target `dev`. Only release PRs target `staging` (from `dev`) or `main` (from `staging`). GitHub defaults to `main`, so change it if needed.
- Required status check on `dev`, `staging` and `main`: `CI / checks (pull_request)`. The repo owner sets it under Settings → Branches.
- Fill in the PR template, including metrics before → after if the model changed.
- Reviewers check out the branch and run it at least once when the pipeline changes.

## Data and models

- Datasets and models are never committed to Git; they are tracked with DVC.
- **Always run `dvc push` before `git push`.**
- Never commit credentials; keep DVC remote credentials in `.dvc/config.local` or environment variables.

## Pipeline runs

- The pipeline is defined in `dvc.yaml`: `prepare` → `train` → `evaluate`. Hyperparameters, split and seed live only in `configs/params.yaml`.
- **Commit code before running `dvc repro` or `dvc exp run`.** `metrics.json` records `git_sha`, which must point at the code that produced it.
- A squash merge creates a new SHA. After a squash merge into `dev`, run `uv run dvc repro -f` on `dev`, commit `metrics.json`, and merge that commit too.
- Reproduce a release only after its PR is merged into `staging`. A clone of `staging` before that doesn't have DVC.
- After a run, commit `dvc.lock`, `metrics.json` (and `configs/params.yaml` if changed), then `dvc push`, then `git push`.
- Our params file is not at the root, so name it when setting params: `dvc exp run -S configs/params.yaml:train.max_depth=10`.
- `.gitattributes` forces LF line endings on every OS. Without it, Windows checkouts (CRLF) change the hashes of code deps and `dvc status` reports stages as changed.

## Recovery

- **`dvc push` times out** on the large model: retry with `uv run dvc push --jobs 1`. Don't run `git push` until `dvc push` finishes without errors. Check with `uv run dvc status --cloud` ("Cache and remote 'storage' are in sync").
- **DVC says "Unable to acquire lock"**: first check for leftover `dvc` or `python` processes from an interrupted command, and close them. Only then delete the lock files in `.dvc/tmp/` (`lock`, `rwlock`, `rwlock.lock`).
- **Commit messages with counts** (for example rows removed) must use numbers from the data files, not from memory.

## Local setup

```bash
uv sync
uv run pre-commit install
uv run dvc pull        # data, processed splits and model from the DVC remote
uv run dvc repro       # re-runs only the stages whose deps or params changed
uv run pytest
```

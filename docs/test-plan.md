# Test Plan

[中文版](test-plan.zh.md)

This project uses lightweight structural tests because the main artifacts are skills, Markdown docs, JSON defaults, shell scripts, and plugin manifests.

## Test Layers

### Unit Tests

Run:

```bash
python3 -m unittest discover -s tests -v
```

Coverage:

- plugin manifests parse as JSON,
- shared defaults contain required sections and core values,
- each `SKILL.md` has valid frontmatter,
- every Markdown file has a language counterpart and language link,
- README links point to existing local files,
- eval docs include metrics, success criteria, and failure criteria,
- shell scripts pass `bash -n`.

### Project Validation

Run:

```bash
./scripts/validate.sh
```

Coverage:

- JSON syntax for manifests and shared defaults,
- Codex skill validation when the local validator is available,
- fallback frontmatter validation when the local validator is unavailable.

### CI

GitHub Actions runs on pull requests and pushes to `main`.

CI steps:

1. Check out the repository.
2. Set up Python.
3. Run `python3 -m unittest discover -s tests -v`.
4. Run `./scripts/validate.sh`.

## Pass Criteria

All tests and validation scripts must pass.

## Failure Signals

- broken JSON,
- missing skill frontmatter,
- broken README/doc link,
- missing Chinese or English counterpart,
- eval docs without measurable criteria,
- shell scripts with syntax errors.

## Manual Review

Before release, manually inspect:

- whether skill descriptions trigger the intended tasks,
- whether JSON defaults remain reasonable,
- whether eval tasks still match the skill behavior,
- whether install scripts copy only project-owned files.

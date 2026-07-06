# Downstream Consumers

~127k downloads/month on PyPI, 203+ repos reference mdformat-mkdocs in `.pre-commit-config.yaml`.

This inventory drives canary repo selection (see `scripts/canary.py` and the Canary Testing section of `AGENTS.md`). Repos that pin mdformat-mkdocs in pre-commit are the highest-value canaries because their options and excludes can be replicated exactly.

## Tier 1: >10k stars

| Stars | Project                                                               | Description                    |
| ----- | --------------------------------------------------------------------- | ------------------------------ |
| 81k   | [astral-sh/uv](https://github.com/astral-sh/uv)                       | Python package/project manager |
| 54k   | [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) | YOLO object detection          |
| 46k   | [astral-sh/ruff](https://github.com/astral-sh/ruff)                   | Python linter/formatter        |
| 37k   | [roboflow/supervision](https://github.com/roboflow/supervision)       | Computer vision tools          |
| 18k   | [astral-sh/ty](https://github.com/astral-sh/ty)                       | Python type checker            |
| 11k   | [THU-MIG/yolov10](https://github.com/THU-MIG/yolov10)                 | YOLOv10 (NeurIPS 2024)         |

## Tier 2: 1k-10k stars

| Stars | Project                                                                 | Description                      |
| ----- | ----------------------------------------------------------------------- | -------------------------------- |
| 6.9k  | [j178/prek](https://github.com/j178/prek)                               | Pre-commit re-engineered in Rust |
| 6.7k  | [Goldziher/kreuzberg](https://github.com/Goldziher/kreuzberg)           | Polyglot document intelligence   |
| 3.6k  | [mckinsey/vizro](https://github.com/mckinsey/vizro)                     | Low-code data viz toolkit        |
| 2.5k  | [dynobo/normcap](https://github.com/dynobo/normcap)                     | OCR screen-capture tool          |
| 2.5k  | [griptape-ai/griptape](https://github.com/griptape-ai/griptape)         | AI agent framework               |
| 2.0k  | [vizzuhq/vizzu-lib](https://github.com/vizzuhq/vizzu-lib)               | Animated data visualizations     |
| 1.6k  | [scverse/scvi-tools](https://github.com/scverse/scvi-tools)             | Single-cell omics analysis       |
| 1.0k  | [mert-kurttutan/torchview](https://github.com/mert-kurttutan/torchview) | PyTorch model visualization      |

## Tier 3: 100-1k stars

| Stars | Project                                                                                             | Description                            |
| ----- | --------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 407   | [mongodb/specifications](https://github.com/mongodb/specifications)                                 | MongoDB driver specs                   |
| 369   | [maldoinc/wireup](https://github.com/maldoinc/wireup)                                               | DI for Python (FastAPI, Flask, Django) |
| 145   | [mondeja/mkdocs-include-markdown-plugin](https://github.com/mondeja/mkdocs-include-markdown-plugin) | MkDocs Markdown includer               |
| 109   | [miquido/draive](https://github.com/miquido/draive)                                                 | LLM agent framework                    |
| 109   | [pawamoy/mkdocs-llmstxt](https://github.com/pawamoy/mkdocs-llmstxt)                                 | MkDocs /llms.txt generator             |
| 108   | [augustepoiroux/LeanInteract](https://github.com/augustepoiroux/LeanInteract)                       | Python interface for Lean 4            |
| 102   | [Medical-Event-Data-Standard/meds](https://github.com/Medical-Event-Data-Standard/meds)             | Medical event data schema              |

## Pre-commit usage survey (2026-07)

Checked `.pre-commit-config.yaml` of Tier 2/3 repos for mdformat-mkdocs hooks:

- j178/prek pins `mdformat-mkdocs==5.1.4` with `--number --compact-tables --align-semantic-breaks-in-lists` over all markdown (tracked as canary)
- mongodb/specifications pins `mdformat-mkdocs==5.1.4` with `--wrap=120 --number` over `source/**/*.md`, excluding `extended-json.md` (tracked as canary)
- scverse/scvi-tools and THU-MIG/yolov10 use mdformat-mkdocs but exclude their `docs/` directories, so there is little content to test
- Medical-Event-Data-Standard/meds uses `--number` but relies on many other mdformat plugins

## Recurring issue themes

Grouping the issue tracker by theme (useful for prioritizing prevention work, see `docs/prevention.md`):

- List indentation and semantic line feeds: the most persistent category (#6, #7, #9, #13, #35, #50, #63)
- Bracket and escape collisions between plugins (#72, #74, #75, #80)
- Definition lists (#54, #58, #63)
- Code blocks inside tabs, snippets, and numbered lists (#23, #31, #34, #35, #36)
- Dependency compatibility with mdformat core and mdit-py-plugins (#5, #24, #60, #66)

Notable reporters include Ruff maintainer MichaReiser (bracket/escape correctness) and mkdocstrings author pawamoy (tabs, dependency compat).

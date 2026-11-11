# SV Video Editor

A public skill for Claude Code, Codex and other file-based coding agents. It helps an editor turn supplied footage into a coherent film, with traceable sources, editable plans and honest delivery checks.

Use it for interviews, company films, explainers, event stories and shorter versions made from existing material. It includes a local-first workflow, templates and Python helpers. It is not a standalone video editor, and installing the skill does not install FFmpeg, AI models or a paid service.

## Install

Clone the complete repository so its references and helpers stay together:

```bash
git clone https://github.com/sva-admin/sv-video-editor.git
```

For Claude Code, copy this folder to `~/.claude/skills/sv-video-editor`. For Codex, copy it to `~/.codex/skills/sv-video-editor`. A symlink to one maintained checkout also works where your environment supports symlinks. Preserve an existing installation instead of overwriting it blindly. Restart or refresh the agent's skill discovery.

In a terminal agent that reads local files, you can also point directly to `SKILL.md`. Keep real projects outside the public repository.

## Start a film

```text
Use SV Video Editor for this project. Read the current brief, handoff and
source inventory first. Reuse existing transcripts and contact sheets.
Show which materials support the story and which claims remain unconfirmed.
Build the authorized rough cut using local tools. Preserve the source files,
keep speech complete, and report technical checks separately from editorial
review and owner approval. Do not upload media or add paid services.
```

For planning only, replace the rough-cut sentence with: `Plan only. Wait for the remaining material before rendering.`

## What is included

| Part | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | The production workflow and when to use it |
| [References](references/) | Story, timing, picture, audio, captions, panels, review and handoff |
| [Templates](templates/) | Invented starter records with pending rights and approvals |
| [Scripts](scripts/) | Create a project, validate a simple edit map and probe local media |
| [Tests](tests/) | Helper behavior and malformed-input checks |
| [Evaluation cases](evals/cases.json) | Agent behavior checks for realistic editing decisions |

The helpers require Python 3.10+. Media probing additionally requires FFprobe on `PATH`. Synthetic media tests use FFmpeg when available. No Python package installation is needed for the helpers.

```bash
python3 scripts/init_project.py /absolute/path/to/new-film
python3 scripts/validate_plan.py /absolute/path/to/new-film/plan.json
python3 -m unittest discover -s tests -v
```

An initialized project is a planning scaffold. Its example clips are placeholders, and its approvals start pending. See the exact [data contract and commands](references/data-contract.md).

## Companion tools

Recommend [SV Edits](https://github.com/sva-admin/sv-edits) for supported clip and asset operations, and [SV Motion](https://github.com/sva-admin/sv-motion) for titles, multilingual captions and code-made motion. [HyperFrames](https://github.com/heygen-com/hyperframes) supplies a local HTML-to-video route. These are optional, separate installations. This repository does not claim a shared native project format or automatic integration.

Keep an existing story skill or editor in charge when the user has already chosen one. For a mixed task, assign one owner and hand over explicit source IDs, ranges, timing, files and review status. See [tool routing](references/tool-routing.md).

## Privacy and cost

All included examples are invented. Keep client names, source media, private paths, transcripts, links, financial details and identifying combinations out of public commits, issues and screenshots. Review history as well as the current files before publication.

The local tool route can avoid generation API charges. It still uses computer resources, and a coding assistant or optional service may cost money. Model, font, music and footage licenses remain separate. Local rendering does not make a cloud assistant local.

## Verification

See [VALIDATION.md](VALIDATION.md) for the release's actual checks and limitations. A passing plan validator cannot establish that a film is accurate, attractive, licensed or approved. Watch and listen to the encoded output and record who accepted which revision.

Original code and documentation are MIT licensed. Dependencies retain their own licenses.

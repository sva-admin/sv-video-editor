# Release validation

Validated on 2026-11-11. All examples and test inputs are invented or synthetic.

## Executed checks

- 29 Python unit and integration tests passed. They cover project creation, overwrite protection, rational frame rates, source normalization, handles, coverage, references, malformed JSON, non-finite values, control characters, path traversal and probe failures.
- A synthetic constant-rate video was generated locally and FFprobe read exactly 30 frames at `30000/1001` FPS. No client media was used.
- An independent helper review ran 682 malformed-value mutations without a validator crash or delivery pass. It identified two edge cases, exponent overflow and extended control characters. Both were fixed and have regression tests.
- Skill metadata validation passed. Relative documentation links and the package's plain-text style were checked.
- The mandatory local strict privacy gate passed. A manual review checked names, private paths, source copy, media, fixtures and publication scope. The supplied private playbook is excluded.
- A fresh-agent exercise covered false attribution, stale panel edits, authorized rough-cut work, temporary voice and false approval claims. The agent preserved the accepted scope and separated evidence from approval. This was a simulated decision exercise, not an executed edit.

## Static inspection and manual review

The offline skill scanner completed. Generated Python bytecode from local tests was removed before packaging and is excluded by `.gitignore`.

Three medium scanner findings remain as declared capabilities: the portable skill has no runtime-specific tool allowlist; the probe invokes FFprobe; and the synthetic integration test invokes FFmpeg. Manual review confirmed that subprocess calls use argument arrays without a shell. Probing accepts a local regular file, restricts FFprobe protocols to local file/pipe access, and writes metadata only to the chosen output. The initializer creates a new project and refuses an existing destination. No helper reads credentials or uploads data.

Assessment: appropriate for its documented local file and media-tool scope. Static inspection is not a security guarantee. Live vulnerability lookups and remote model inspection were not run.

## Limits

Tests ran with Python 3.14 on macOS. The code targets Python 3.10+, but Windows, Linux and Python 3.10 execution were not performed for this release.

The validator handles a single normal-speed hard-cut picture track. It does not validate layered timelines, transition overlaps, speech meaning, translations, media rights, the authenticity of approval records or final audiovisual quality.

No complete HyperFrames film, writable review panel, final narration or client delivery was built or validated for this release. Those are production workflows that the skill guides using the project's chosen tools.

## Reproduce helper tests

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

FFmpeg and FFprobe must be on `PATH` for the synthetic media integration test. That test reports a skip if either is absent. The remaining helper tests use standard-library fixtures and mocks.

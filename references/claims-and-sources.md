# Claims, sources and adoption decisions

Checked for this release on 2026-11-11. This ledger distinguishes tool behavior from editorial guidance. Recheck version-dependent claims when the relevant tool changes.

| Claim or proposed rule | Decision and evidence | Limits |
| --- | --- | --- |
| Count decoded frames, not packets | Adopt. FFprobe's help and [documentation](https://ffmpeg.org/ffprobe.html) distinguish `-count_frames` and `-count_packets`. The helper test decodes a synthetic constant-rate file. | Decode errors or missing counts are unresolved, not an inferred pass. |
| Metadata edits convert HDR or log pixels | Reject. `h264_metadata` changes bitstream metadata. See its local help and [bitstream-filter documentation](https://ffmpeg.org/ffmpeg-bitstream-filters.html). | A correct color transform still needs the actual source interpretation and output specification. |
| Always reduce to 8-bit before processing | Reject as a general rule. Precision reduction is not tone mapping. [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html) provide distinct processing operations. | Preserve adequate precision through the chosen transform; test the resulting image. |
| Timeline positions should use integer frames and rational FPS | Adopt for this plan contract. Python `Fraction` and synthetic rate tests support the helper's arithmetic. | Source and audio clocks remain distinct; the validator covers one hard-cut picture track only. |
| Atomic saving prevents stale browser overwrites | Adapt. Atomic replacement prevents partial writes; revision preconditions are also required to reject stale changes. [HTTP conditional requests](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match) describe this lost-update protection. | The repository documents a panel contract; it does not implement a writable server. |
| Local HTML rendering can avoid a paid generation call | Adopt conditionally. [HyperFrames upstream](https://github.com/heygen-com/hyperframes) documents local rendering. | Agent usage, compute, models and optional hosted services can still have costs. No complete HyperFrames film was rendered for this skill release. |
| One renderer version is always the correct version | Reject. Preserve a working project pin and deliberately test upgrades against the installed adapter. | Exact CLI flags and supported export formats are version-specific. |
| A fixed loudness target fits every video | Adapt. FFmpeg `loudnorm` exposes configurable integrated loudness and true-peak targets. See [filter documentation](https://ffmpeg.org/ffmpeg-filters.html#loudnorm). | Choose delivery targets from the brief; measure the encoded output and listen. |
| A transcript certifies exact speech and timing | Reject. Transcripts are locating and alignment aids. [WhisperX](https://arxiv.org/abs/2303.00747) discusses word alignment in an ASR workflow. | Listen to selected ranges in context; names and translations need review. |
| Contact sheets prove smooth motion or complete review | Reject. They show only sampled instants. | Normal-speed viewing and listening must identify their actual coverage. |
| A question-led opening is always better | Reject. Treat opening choices as editorial hypotheses tied to audience and evidence. | Formal context-first introductions can be appropriate. No retention or sales uplift is claimed. |
| A numeric judge threshold proves final quality | Reject. Use timecoded findings and a defined rubric as feedback. | Technical checks, editorial judgment and owner acceptance remain separate. |

The helper suite provides evidence about the implemented scripts. It does not validate an entire film, a commercial outcome, media rights or the truth of an organisation's claims. Historical production observations have been rewritten as generic diagnostic guidance; private production records are not included.

# Quality checks and delivery

## Evidence has a scope

Every check records its status, method, file hash, revision, inspected range and result. Use `pass`, `fail`, `not_run` and `needs_review` consistently. An intentionally exempt item needs a reason. Missing expected cuts, inaccessible files and uninspected ranges cannot become silent passes.

| Check | What it can establish | What still needs review |
| --- | --- | --- |
| FFprobe metadata | Declared streams, rate, size, color tags and duration | Whether pixels and sound match those declarations |
| Decoded frame count | Frames actually read by the selected decoder | Story, sync, legibility and hidden defects |
| Plan validation | Supported schema, references, ranges and coverage | Whether source content supports the intended statement |
| Audio analysis | Measured loudness, peak and some signal faults | Intelligibility, tone, music balance and meaning |
| Contact sheets | Appearance at sampled instants | Continuous motion, every frame, speech and lip sync |
| Transcript comparison | Candidate omissions or discrepancies | Faithful speech through listening in context |
| Human playback review | The watched and listened revision and ranges | Unreviewed sections and owner acceptance |

Do not describe the count from `ffprobe -count_packets` as decoded frames. `-count_frames` exposes `nb_read_frames` when the stream can be read. Keep packet and frame counts separate.

## Technical checks

For the delivery candidate:

- Probe container, codecs, dimensions, frame rate, aspect, pixel format, rotation, duration, color declarations and audio streams.
- Decode the expected streams and inspect errors. Count decoded video frames where the delivery contract needs an exact count.
- Check the beginning, ending, joins and intended total length. Confirm the last words, music tail and contact hold are present.
- Inspect black or frozen spans in context. A designed hold or black chapter break is not automatically a defect.
- Measure final encoded audio against the chosen target. Confirm sample rate and channel layout, listen for clipping and verify sync at more than one point.
- Confirm subtitle edition, language set, fonts, cue timing and burned-versus-sidecar treatment.
- Test the actual playback and download path, including seeking where a panel is supplied.

Useful optional analyses include brightness discontinuity, shake estimates and caption reading speed. Define their measurement and expected context first. They are flags for inspection, not instructions to equalize every scene or remove intended motion.

## Editorial review

Watch and listen at normal speed. Then inspect problem ranges closely:

1. Does the opening establish the promised topic and the organisation's role at an appropriate time?
2. Does each chapter add evidence, and does the next chapter follow logically?
3. Is speech complete, truthful and synchronized when the mouth is visible?
4. Do figures, names, titles, dates, roles and translations match approved sources?
5. Are pictures representative, correctly attributed and free of unintended private details?
6. Do photo moves, crops and transitions preserve subjects and continuity?
7. Are captions readable on the intended screen, without covering faces or essential evidence?
8. Does the ending resolve the opening and offer a clear next step?

Check high-risk frames at readable resolution: badges, screens, paperwork, seat labels, contact details and unintended logos. Record what was checked. Do not claim an exhaustive all-frame privacy review from a contact sheet or OCR sample.

An independent reviewer can score defined criteria and return timecoded defects. A score is editorial feedback, not a factual certification. Give the reviewer the brief and actual candidate, and fix observed issues rather than repeatedly asking for a higher score.

## Approval and delivery

Keep technical pass, editorial review and owner acceptance as separate fields. Approval must refer to a specific revision. New content, timing, translation or render changes can invalidate affected approvals.

Provide only what the request calls for, in its promised form: final video editions, sidecars if included, editable timeline or composition, editable presentation if agreed, approved script, source map, build instructions and handoff. State missing items directly.

For client exports, build from a public-facing allowlist of fields. Internal notes, rejected concepts, credentials, private paths and reviewer comments do not belong in a client deck merely because they appear in the planning page.

The handoff should name the exact deliverables, revision and remaining approvals. State whether anything was sent or published. Preparing files and verifying playback do not send them.

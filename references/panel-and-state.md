# Panel and production state

Use an existing project panel when it works. This skill does not ship a server or a timeline UI. The following contract guides an authorized implementation or repair.

## One canonical record

Keep stable IDs for assets, narration lines, chapters, shots and proposals. A record's identity should survive reordering. Store the producer's choices as data; avoid hardcoded per-line branches in the render engine.

Separate these layers:

| Layer | Owns |
| --- | --- |
| Source manifest | Original files, derivatives, metadata, evidence and restrictions |
| Storyboard | Line purpose, candidate shots, notes and unresolved decisions |
| Accepted plan | Selected sources, exact ranges, ordering and treatments |
| Render record | Input hashes, accepted-plan revision, builder and tool versions, actual cut map and output hash |
| Review record | Findings, time ranges, reviewer, disposition and accepted revision |

Generate previews and summaries from these records. A separately edited spreadsheet, HTML page and JSON file will drift unless one is the owner and the others are generated views.

## Save safely with concurrent editors

Atomic replacement prevents partial files; it does not prevent lost updates. A writable API needs both validation and concurrency control:

1. A read returns the document plus a monotonically increasing revision or content ETag.
2. A change includes the expected revision and the specific edited fields.
3. Under a lock or transaction, the server compares the expected revision with the current one.
4. On mismatch, return a conflict. Preserve both versions for inspection; do not silently apply last-write-wins.
5. On match, validate references, types, ranges and permitted paths, then write atomically and increment the revision.
6. Read back the saved result and show it in the UI.

Reordering uses IDs, not array positions as identity. Adding a proposal must not change the accepted plan. Acceptance explicitly promotes the selected proposal and records the revision.

For example, accepted plan revision 4 can remain the render input while saved revision 5 adds an unaccepted shot proposal. Preserve revision 5, render only the accepted selection, and record that distinction. If revision 5 also contains an accepted change, rebase the intended edit onto that accepted state. The latest save and the latest acceptance are not interchangeable.

For local servers, bind to loopback, restrict accessible paths to the project, reject cross-origin writes and validate requests. A locally bound writable server still needs protection against browser requests from unrelated sites. Do not expose a private review panel publicly as a side effect of starting it.

## Show what the producer needs next

Put the next decision first, followed by work in progress, waiting-for-material items and completed evidence. Each item needs an owner, status, dependency and direct link to the relevant shot or render. A compact panel can combine:

- Current film and revision, with play, restart and timecode links.
- A chapter strip with representative source thumbnails.
- Narration lines with selected shots, source in/out, purpose and notes.
- A proposal comparison and accept/reject controls where authorized.
- A short list of missing material and unresolved factual or translation approvals.
- Technical results, human review coverage, final acceptance and handoff files.

Use large readable text, short labels and purposeful grouping. Do not turn an internal data dump into a presentation. Keep private comments and debugging details out of client views through an explicit field allowlist.

## Distinguish a plan from a render

A render should identify its plan revision and hash, source and derivative hashes, composition code, fonts, builder version, tool versions and output hash. A new plan does not update the old MP4 automatically. Display stale status when any render dependency changes.

Timeline links for a completed render must use its actual cut map. Planned ranges should be labelled planned. A modification time is useful for display but is not enough to establish provenance.

Video playback needs the correct MIME type and HTTP Range support for seeking. Test seeking and resuming against the actual server. Provide its restart command and port. Do not promise scrubbing merely because a video tag renders.

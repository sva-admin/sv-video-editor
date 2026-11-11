# Planning and media records

These Python 3.10+ helpers create a local project, validate one hard cut picture
sequence, and inspect local media with ffprobe. They do not render a film, create
an editor timeline, generate media, upload files, or grant approval.

Run the commands from the installed skill directory. Keep project files outside
the public skill repository. The example project name is invented.

```sh
python3 scripts/init_project.py ../demo-film
python3 scripts/validate_plan.py ../demo-film/plan.json
python3 scripts/validate_plan.py ../demo-film/plan.json --delivery
python3 -m unittest discover -s tests -v
```

The first validation passes on the starter's structure. The delivery check fails
because the starter has no media, cleared rights, or approvals. This is expected.

## Initializing a project

```sh
python3 scripts/init_project.py ../demo-film --project-id demo-film
```

The destination must not exist, including as an empty directory. There is no
overwrite or merge option. The ID defaults to the destination directory name and
must use lowercase kebab case, starting with a letter. The helper creates:

```text
demo-film/
  plan.json
  brief.json
  review.json
  HANDOFF.md
  sources/
  evidence/
  exports/
```

The sources, evidence, and exports folders start empty. The plan's source path,
duration, chapter, and line are invented placeholders. The helper copies no media.
All approvals and both final status records start as `pending`.

`brief.json` and `review.json` are human working records. The validator checks only
`plan.json`; it does not cross-check these companion files. Keep them consistent
during review. The review template includes the exact candidate path and SHA-256
so a reviewer can identify the file they accepted.

## Plan schema version 1

Objects have exactly the listed keys. Unknown keys are errors, which helps catch
misspelled fields and unsupported edits. JSON duplicate keys and non-finite
numbers are rejected. Frame values must be JSON integers, never strings, decimal
numbers, booleans, or timecode labels.

| Root key | Meaning |
| --- | --- |
| `schema_version` | Integer `1`. |
| `project` | Object containing `id` and a nonempty `title`. |
| `timeline` | Object containing `fps`, `duration_frames`, and `edit_mode`. |
| `assets` | Array of source records. Include every asset used by the delivery. |
| `chapters` | Array of chapter intervals that covers the timeline exactly. |
| `lines` | Array of selected text records; may be empty. |
| `clips` | Array of picture clips that covers the timeline exactly. |
| `approvals` | Objects named `picture`, `audio`, and `owner`. |
| `final_status` | `pending` or `approved`, recorded by the responsible human. |

IDs match `[a-z][a-z0-9]*(?:-[a-z0-9]+)*`. Asset, chapter, line, and clip IDs must be
unique across those four arrays. The project ID has its own namespace. Keep IDs
stable when wording or timing changes. The validator checks uniqueness within
the current file, not stability across revisions.

### Frame rate and intervals

`fps` is an object with positive integer `numerator` and `denominator`:

```json
{"numerator": 30000, "denominator": 1001}
```

The validator uses exact rational arithmetic. Do not replace this rate with
`29.97` or `30`. `timeline.duration_frames` must be a positive integer.
`timeline.edit_mode` must be `hard_cut`.

Every timeline interval is `[start_frame, end_frame)`: the start is included and
the end is excluded. A clip from frame 0 to frame 24 occupies exactly 24 frames.
Starts must be nonnegative and ends must exceed starts. Chapters and clips must
each cover frame 0 through `duration_frames` without gaps or overlaps. Array
ordering does not affect the check. Each clip must fit inside its chapter. Split
a clip record if it crosses a chapter boundary.

This contract supports one picture track at normal speed. Dissolves, overlapping
tracks, retiming, freeze frames taken from video, and audio mix timing are outside
the helper's scope. Keep those decisions in the editor's project and human review
records. Do not label an unsupported edit as a hard cut to obtain a pass.

### Assets

Each asset contains `id`, `path`, `kind`, `duration`, and `rights`.

- `kind` is `video`, `audio`, or `image`.
- `path` is relative to the folder containing `plan.json`, such as
  `sources/opening.mov`.
- `duration` is null for a still image. For timed media it is an object containing
  positive integer `frames` and rational `fps`.
- `rights` contains `status` (`pending`, `cleared`, or `restricted`) and `evidence`
  (a project-relative file path or null). A cleared record always requires an
  evidence path.

Timed duration equals `duration.frames / duration.fps` seconds. For constant rate
video, use the verified source frame count and source frame rate. For audio, the
same representation can use sample count as `frames` and sample rate as `fps`.
An audio asset can be recorded for rights, but cannot be a picture clip.

The validator converts each source duration into timeline frame units exactly:

```text
available_timeline_frames = source_frames * timeline_fps / source_fps
```

An available duration of 240.24 timeline frames does not allow a source interval
ending at frame 241. For variable frame rate video, establish a constant rate
working source and verify its duration before using this contract. Multiplying a
variable frame count by the average frame rate is not a reliable source mapping.
These helpers do not create that working source.

Relative paths use forward slashes. Absolute paths, drive prefixes, URLs,
backslashes, empty components, dot components, parent traversal, control
characters, and symlinks that escape the project are rejected. The planning check
does not require files to exist, since it is also useful before ingest.

### Chapters and selected lines

A chapter has `id`, `title`, `start_frame`, and `end_frame`.

A line has `id`, `chapter_id`, and nonempty `text`. Its chapter must exist. A line
is a selected statement or caption intent, not a verified transcript. Preserve
speaker attribution, source timecodes, and transcription checks in the project's
evidence files. The helper does not infer speech timing or factual accuracy.

### Picture clips

Each clip has these keys:

| Key | Meaning |
| --- | --- |
| `id` | Stable unique clip ID. |
| `asset_id` | Existing video or image asset ID. |
| `chapter_id` | Existing chapter that contains this clip. |
| `line_ids` | Array of existing line IDs belonging to this chapter; no duplicates. |
| `start_frame`, `end_frame` | Exclusive-end interval in timeline frames. |
| `source_in_frame`, `source_out_frame` | Exclusive-end source interval, expressed in timeline frame units. |
| `handle_before_frames`, `handle_after_frames` | Nonnegative source frames reserved outside the selected range, in timeline frame units. |

For video, source and timeline interval lengths must match. The source in point
minus its before handle must be at least zero. The source out point plus its after
handle must not exceed the source duration normalized to timeline fps. Handles
reserve source material; they are not transition overlaps on the timeline.

For a still image, all four source range and handle values must be zero. Its
display length comes from the clip's timeline interval.

### Approvals and the delivery option

Each of `picture`, `audio`, and `owner` has `status` (`pending`, `approved`, or
`rejected`), `reviewer` (nonempty string or null), and `evidence` (a project-relative
file path or null). An approved record requires both a reviewer and evidence path.
For a silent deliverable, record the reviewer's explicit decision about intended
silence in the audio evidence rather than omitting audio review.

`--delivery` additionally requires:

- Every asset path and every supplied evidence path to be an existing file.
- Every asset's rights status to be `cleared`.
- All three human approval records to be `approved`.
- `final_status` to be `approved`.

The helper never writes an approval. A successful delivery check means the
required records and files exist. It does not read the evidence, authenticate
rights, establish reviewer identity, decode a final export, check the candidate
hash, or confirm that approval applies to the current revision. Humans must
review the exact candidate, check evidence, and keep approval records current.
Do not treat a delivery check as final delivery acceptance.

Validation exits with 0 for a pass, 1 for plan or delivery-record errors, and 2
for an unreadable or malformed JSON document. Errors print without a traceback.

## Local media probing

Install FFmpeg's `ffprobe` command separately and keep it on PATH, or supply an
explicit executable path with `--ffprobe`. Only the optional integration test also
needs `ffmpeg`. The Python helpers use only the standard library.

```sh
python3 scripts/probe_media.py "../demo-film/sources/opening clip.mov" \
  --output ../demo-film/evidence/opening-probe.json

python3 scripts/probe_media.py "../demo-film/sources/opening clip.mov" \
  --count-frames --timeout 600 \
  --output ../demo-film/evidence/opening-counted.json
```

The metadata pass requests all stream and format metadata. It preserves raw
ffprobe fields, including rational rate strings, color space, color range,
transfer function, primaries, audio properties, stream tags, rotation tags, and
display-matrix side data when supplied by ffprobe. Missing fields remain missing.
The helper does not flatten, normalize, or invent metadata.

`--count-frames` requests ffprobe's `-count_frames`, which reads and decodes media
to report `nb_read_frames` when available. It never requests packet counts.
Container `nb_frames` and decoded `nb_read_frames` are separate observations.
An unavailable count remains unavailable, and counting frames is not a normal
speed picture or listening review. Long files can take time; the default timeout
is 120 seconds and can be changed to a positive integer.

The output contains `schema_version`, `source` (absolute local path, byte size,
and modification timestamp), `count_frames_requested`, `limitations`, and the
unmodified parsed `ffprobe` object. Media paths, embedded tags, and metadata may
be private. Keep probe outputs inside the local project and exclude them from
public repositories.

The source must be a local file. The subprocess receives an argument list,
without shell interpolation, and its protocol allowlist is `file,pipe`. No upload
or network service is used. Missing binaries, reported decoding errors, invalid
metadata, changed source files, and timeouts fail without writing an output file.

Existing output files are preserved unless `--force` is supplied. The source
cannot be used as the output, even with `--force`. Output parent folders must
already exist. JSON publication is atomic. The probe exits 0 on success or 2 on
an error; it does not modify the plan or grant approval.

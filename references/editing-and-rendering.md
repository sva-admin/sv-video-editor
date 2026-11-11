# Timing, picture, sound and text

## Time belongs to a declared clock

Represent timeline positions as integer frames with rational FPS, such as `24/1` or `30000/1001`. Define ranges as `[start_frame, end_frame)`. A clip spanning frames 0 through 95 has 96 frames. Keep source time bases and audio sample rates in the source records; do not confuse source seconds with output frames.

For a time in seconds, choose and record a rounding policy when converting it to a frame. Avoid repeated float additions. Convert from the original reference, not a rounded previous duration. Frame quantization does not replace audio-boundary listening.

The included validator handles one hard-cut picture track. A dissolve overlaps two source ranges. Model that overlap and its handles in the native timeline instead of subtracting durations informally. Speed changes require a source-to-output mapping. Layered graphics and independent dialogue tracks need their own intervals.

Plan with the final voice or an explicitly labelled guide, natural breathing room and the actual images. For an authorized internal rough cut, the guide can be temporary; do not introduce a new approval gate unless the project's agreement requires it. Read the result back into a cut manifest containing the real output intervals. Planned timing alone does not prove rendered timing.

## Preserve source pixels and interpretation

Probe frame rate, variable-rate behavior, rotation, sample aspect ratio, bit depth, chroma sampling, transfer, primaries, matrix, range and audio. Metadata can be absent or wrong; compare the image with a known-good reference.

Normalize only where the selected renderer needs it. Keep original media untouched. One possible browser proxy is H.264 8-bit `yuv420p` with AAC, but compatibility and color must be checked on the target playback path.

For log or HDR sources, identify the actual encoding and intended delivery space. Apply an appropriate color transform or tone mapping while retaining enough precision, then encode the delivery format. Changing metadata tags or dropping to 8-bit does not perform that transform. Do not label unknown pixels as Rec.709 merely to silence a warning.

Use one orientation convention. Account for container rotation and photo EXIF exactly once. Retain the original-to-derivative transform. Check faces, logos and lettering after resizing. Prefer an original source or ordinary resampling over unverified AI reconstruction of identity or text.

## Make movement purposeful

Use a shot because it supports the beat. A camera move, transition or graphic needs a purpose beyond filling duration.

- For photo movement, set crop endpoints around the actual subject. Keep the subject, important text and caption clearance throughout the move.
- Use smooth subpixel sampling where integer crop positions cause jitter. Inspect the actual encoded motion, not just first and last frames.
- Match direction, scale, gaze or action across cuts where useful. Avoid implying one continuous event from unrelated recordings.
- Use hard cuts, sound bridges, dissolves or chapter breaks according to the material. Do not dissolve every line automatically.
- A graphic should explain information the footage cannot show clearly. Reusing the same motif is acceptable when it carries consistent meaning.

Express motion settings in time-based or normalized terms when transferring between resolutions and frame rates. Values measured in pixels per frame cannot be copied unchanged between output formats.

## Keep HTML motion deterministic

Use the project's supported HyperFrames or motion-adapter version. Check its local docs and command help before assuming flags, markup or alpha-output support. Build one valid composition first.

Every animated property must derive from the requested timeline time. Seed randomness, preload local assets and fonts, and avoid autonomous animation loops that drift between screenshots. Test random seeks as well as sequential playback. Keep HTML animation layers synchronized with the picture and cue map.

If using an alpha overlay, test transparency, premultiplication, frame rate, length and compositing on a short sample. If alpha is unsupported, use a proven image-sequence or full-frame composition route and budget its storage. Do not claim this repository supplies a renderer integration that has not been implemented.

## Sound follows meaning

Keep an unprocessed reference. Choose clean complete speech, retain believable room tone and remove only distracting noise that can be treated without damaging words. Compare the processed voice at matched listening level.

A J-cut introduces the next audio before its picture. An L-cut carries current audio into the next image. Preserve the original speech continuously across the picture edit. Use short fades to avoid clicks, not to disguise a missing syllable. Do not place a mismatched speaking mouth under the line.

Keep sample-accurate audio offsets when needed. Inspect timestamps when a delay, concat or resample behaves unexpectedly. Reproduce a suspected tool bug on a small fixture before adding a global workaround.

Choose loudness and peak targets from the delivery brief. For example, a web review might start around -16 LUFS integrated and a true-peak ceiling of -1 dBTP, but these are configurable starting points, not a universal specification. Different platforms and programmes may require different values. Measure the final encoded file, including after AAC conversion. A sample peak in dBFS is not true peak in dBTP.

Music must support speech and have suitable rights. Adjust the bed by listening across quiet and loud lines, not by a single gain offset. Equal integrated loudness does not make two voices equally clear or natural. Do not aggressively alter a person's voice just to resemble the narrator.

## Captions and multilingual treatment

Keep editable cue data tied to line IDs, source times, output frames, exact speech, translations and reviewer status. Generate burned captions and sidecars from the same cues where required. Confirm whether languages appear together or in separate editions.

Test the actual fonts and shaping for every language, including combining marks, punctuation, names and numerals. Caption budgets depend on script, phrase length, screen size and audience. An English characters-per-second threshold is not a universal rule for Thai or Chinese.

Shorten or split phrases before shrinking type. Review the longest cues, bright and dark backgrounds, vertical safe areas, faces and important objects. Keep readable holds and avoid a caption changing halfway through its spoken phrase without reason. Transcription and translation approvals are separate.

When only sidecar subtitles are available, say that the MP4 has no burned captions. Do not mark it as the requested burned-caption delivery.

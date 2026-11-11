# Free local workflow

## Check the machine before adding tools

Reuse an existing working project and its lockfiles. Check Python, FFmpeg/FFprobe, available storage and the chosen editor. For HTML graphics, also check Node, a supported browser, licensed fonts and the renderer's installed version.

```bash
python3 --version
ffmpeg -version
ffprobe -version
node --version
```

The Python helpers in this repository use the standard library and require Python 3.10+. FFprobe is needed only for media inspection. Do not install a browser, model, music generator or graphics stack just to make a paper edit.

Use [SV Edits](https://github.com/sva-admin/sv-edits) for supported source-clip and asset operations. Use [SV Motion](https://github.com/sva-admin/sv-motion) for a documented HyperFrames graphics workflow. Read the installed companion's contract instead of guessing available tools.

HyperFrames is an optional local HTML-to-video renderer. Follow its [official setup](https://github.com/heygen-com/hyperframes) or the installed companion's supported pin. The existing SV Motion adapter uses a versioned workflow. Do not silently replace a working project pin with `latest`; test an intentional upgrade on a representative sequence and retain the previous build record.

New package or model downloads need the appropriate installation and network authorization. This skill's installation does not authorize uploading footage or buying services.

## Produce a small proof

1. Reuse the source inventory. Probe only new or changed files.
2. Choose a short sequence that tests the hard parts of the actual film.
3. Listen to selected speech and make a voice-first paper edit.
4. Build a picture and sound proof using the existing editor or FFmpeg.
5. Add a representative title and the longest caption treatment if graphics are needed.
6. Watch and listen to the encoded result. Check its technical properties and record the exact inputs.
7. Scale the accepted method in sections and rebuild changed dependencies only.

For a short authorized rough cut, this is enough: confirm accepted sources and settings, listen to the selected speech, map the frames, build the bounded proof, watch and listen to it, and record unresolved items. Do not create a full production panel or another approval round merely to complete this sequence.

Speech can come from cleared recordings, a temporary team read or a suitable local scratch voice under its terms. Reuse installed transcription or TTS tools where practical. Match implementations to hardware; an Apple-specific runtime is not a portable dependency. Record model, version, settings and transcript uncertainty. Do not use voice cloning without the speaker's authorization.

Keep a guide voice labelled. A contract for a human narrator, a named voice or a particular language treatment remains in force until the user changes it. Verify pronunciation and final audio before replacing the guide track.

An internal scratch track can support an already authorized rough cut without a separate approval if it stays within the agreed scope. Identify it in the filename and review page or handoff. If a preview will leave the team, make its temporary status visible in the preview itself. Replacing it with the human performance can change timing; recheck affected picture cuts, captions and approvals against the new render.

## Work within storage and compute limits

Estimate space from selected durations, bitrate and intermediate format. Image sequences can consume much more space than the final MP4. Retain sufficient headroom for temporary outputs and final assembly. Refuse only the unsafe heavy operation; continue planning or other independent work.

Generate small proxies or selected normalized ranges. Keep source mappings and edit handles. Cache by source hash, selected range, processing settings, tool/model version, fonts and builder version. Place reusable derivatives in the project's durable cache, not an expiring temporary directory.

On a constrained machine, run one heavy render, transcription or decode job at a time. Use a lock containing the job owner and process details. Check the process before clearing a stale lock. Parallel collaborators can inspect separate records or write disjoint modules; freeze shared render inputs before starting the job.

Do not delete originals to recover space unless that deletion is explicitly authorized and the handoff or backup has been verified. A file listed on another computer is not a verified usable copy.

## What free means here

The local path can avoid paid generation calls and commercial editing subscriptions. It still uses storage, electricity and time. Coding-agent usage may be billed. Model weights, voice assets, fonts, footage and music have their own terms. A locally run model is not automatically cleared for every commercial use.

Start without music when rights are unclear. Check embedded music in supplied clips as well as added tracks. Keep a rights record for the chosen assets instead of treating a download button or an allowed folder as permission to publish.

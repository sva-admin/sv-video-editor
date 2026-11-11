"""Synthetic tests only. Run: python3 -m unittest discover -s tests -v."""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from common import read_json, safe_relative_path, write_json
from init_project import initialize
from probe_media import main as probe_main, probe
from validate_plan import main as validate_main, validate


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.plan = read_json(ROOT / "templates" / "plan.json")

    def tearDown(self):
        self.temporary.cleanup()

    def errors(self, delivery=False):
        return validate(self.plan, self.root, delivery)

    def assert_error(self, fragment):
        self.assertTrue(any(fragment in e for e in self.errors()), self.errors())

    def test_starter_planning_pass_delivery_fails(self):
        self.assertEqual(self.errors(), [])
        errors = self.errors(True)
        self.assertTrue(any("cleared rights" in e for e in errors))
        self.assertTrue(any("human approval" in e for e in errors))
        self.assertTrue(any("final_status" in e for e in errors))

    def test_ntsc_fraction_valid(self):
        rate = {"numerator": 30000, "denominator": 1001}
        self.plan["timeline"]["fps"] = rate
        self.plan["assets"][0]["duration"]["fps"] = rate.copy()
        self.assertEqual(self.errors(), [])

    def test_source_duration_normalizes_exactly(self):
        self.plan["assets"][0]["duration"] = {
            "frames": 300, "fps": {"numerator": 30000, "denominator": 1001}}
        self.plan["clips"][0].update(source_in_frame=0, source_out_frame=240,
                                    handle_before_frames=0, handle_after_frames=0)
        self.assertEqual(self.errors(), [])
        self.plan["clips"][0]["handle_after_frames"] = 1
        self.assert_error("normalized to timeline fps")

    def test_fractional_rate_cannot_be_rounded_up(self):
        self.plan["timeline"]["fps"] = {"numerator": 30000, "denominator": 1001}
        self.plan["assets"][0]["duration"] = {
            "frames": 288, "fps": {"numerator": 30, "denominator": 1}}
        self.assert_error("normalized to timeline fps")

    def test_handles_before_zero(self):
        self.plan["clips"][0]["handle_before_frames"] = 25
        self.assert_error("before frame zero")

    def test_exclusive_end_and_retiming(self):
        self.plan["clips"][0]["source_out_frame"] = 263
        self.assert_error("durations must match")
        self.plan["clips"][0]["end_frame"] = 0
        self.assert_error("end_frame")

    def test_gaps_and_overlaps(self):
        first = self.plan["clips"][0]
        first.update(end_frame=120, source_out_frame=144)
        second = copy.deepcopy(first)
        second.update(id="clip-second", start_frame=121, end_frame=240,
                      source_in_frame=24, source_out_frame=143)
        self.plan["clips"].append(second)
        self.assert_error("gap")
        second.update(start_frame=119, source_out_frame=145)
        self.assert_error("overlap")

    def test_no_clips_no_chapters(self):
        self.plan["clips"] = []
        self.plan["chapters"] = []
        self.assert_error("coverage ends at 0")

    def test_duplicate_and_invalid_ids(self):
        self.plan["clips"][0]["id"] = self.plan["assets"][0]["id"]
        self.assert_error("duplicate ID")
        self.plan["clips"][0]["id"] = "Clip 1"
        self.assert_error("stable lowercase")

    def test_unknown_references(self):
        clip = self.plan["clips"][0]
        for key, value in (("asset_id", "absent"), ("chapter_id", "absent"), ("line_ids", ["absent"])):
            with self.subTest(key=key):
                original = clip[key]
                clip[key] = value
                self.assert_error("unknown referenced ID")
                clip[key] = original

    def test_chapter_containment_and_line_membership(self):
        self.plan["chapters"][0]["end_frame"] = 120
        self.plan["chapters"].append({"id": "chapter-second", "title": "Second",
                                      "start_frame": 120, "end_frame": 240})
        self.plan["lines"][0]["chapter_id"] = "chapter-second"
        self.assert_error("contained in its chapter")
        self.assert_error("different chapter")

    def test_malformed_types_and_rates_are_errors(self):
        mutations = [
            lambda p: p.update(timeline=None),
            lambda p: p["timeline"].update(fps=[]),
            lambda p: p["timeline"]["fps"].update(denominator=0),
            lambda p: p["timeline"]["fps"].update(numerator=True),
            lambda p: p["timeline"]["fps"].update(numerator=float("inf")),
            lambda p: p["clips"][0].update(start_frame=0.0),
            lambda p: p["clips"][0].update(line_ids=[{}]),
            lambda p: p["clips"][0].update(asset_id=[]),
            lambda p: p["assets"][0].update(kind=[]),
            lambda p: p["assets"][0].update(rights=[]),
            lambda p: p["assets"][0]["duration"].update(frames=True),
            lambda p: p.update(approvals=[]),
            lambda p: p.update(clips={}),
            lambda p: p.update(lines=[None]),
            lambda p: p.update(schema_version=True),
            lambda p: p.update(final_status=[]),
        ]
        for mutate in mutations:
            plan = copy.deepcopy(self.plan)
            mutate(plan)
            with self.subTest(plan=plan):
                self.assertTrue(validate(plan, self.root))
        for value in ([], None, 42, "not a plan"):
            self.assertTrue(validate(value, self.root))

    def test_path_traversal_protocol_and_symlink_escape(self):
        for path in ("../secret.mov", "/secret.mov", "C:\\secret.mov", "https://example.test/a", "sources//a.mov", "sources/./a.mov"):
            with self.subTest(path=path):
                self.plan["assets"][0]["path"] = path
                self.assertTrue(self.errors())
        with tempfile.TemporaryDirectory() as outside:
            (self.root / "linked").symlink_to(outside, target_is_directory=True)
            self.plan["assets"][0]["path"] = "linked/a.mov"
            self.assert_error("outside the project")

    def test_still_image_and_unsupported_audio_picture(self):
        asset = self.plan["assets"][0]
        asset.update(kind="image", duration=None)
        self.plan["clips"][0].update(source_in_frame=0, source_out_frame=0,
                                    handle_before_frames=0, handle_after_frames=0)
        self.assertEqual(self.errors(), [])
        asset["kind"] = "audio"
        asset["duration"] = {"frames": 288, "fps": {"numerator": 24, "denominator": 1}}
        self.assert_error("cannot reference audio")

    def test_unknown_fields_and_transition_mode(self):
        self.plan["timeline"]["edit_mode"] = "dissolve"
        self.plan["clips"][0]["transition"] = "crossfade"
        self.assert_error("hard_cut")
        self.assert_error("unknown keys: transition")

    def test_approval_requires_evidence_and_reviewer(self):
        self.plan["approvals"]["owner"]["status"] = "approved"
        self.assert_error("require reviewer and evidence")

    def test_delivery_record_pass_is_only_record_validation(self):
        (self.root / "sources").mkdir()
        (self.root / "sources" / "opening.mov").write_bytes(b"")
        (self.root / "evidence").mkdir()
        (self.root / "evidence" / "synthetic.txt").write_text("Synthetic test record only.")
        self.plan["assets"][0]["rights"] = {"status": "cleared", "evidence": "evidence/synthetic.txt"}
        for key in self.plan["approvals"]:
            self.plan["approvals"][key] = {"status": "approved", "reviewer": "Synthetic reviewer", "evidence": "evidence/synthetic.txt"}
        self.plan["final_status"] = "approved"
        self.assertEqual(self.errors(True), [])
        self.plan["assets"][0]["rights"]["status"] = "restricted"
        self.assertTrue(any("cleared rights" in e for e in self.errors(True)))

    def test_bad_json_and_nonfinite_cli_clean_failure(self):
        source = self.root / "bad.json"
        for text in ('{"schema_version": NaN}', '{"a":1,"a":2}', '{', 'null'):
            source.write_text(text)
            with patch("sys.stderr"):
                self.assertIn(validate_main([str(source)]), (1, 2))


class FilesAndProbeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_initializer_empty_sources_pending_no_overwrite(self):
        target = self.root / "demo-film"
        initialize(target)
        self.assertEqual(list((target / "sources").iterdir()), [])
        self.assertEqual(read_json(target / "plan.json")["final_status"], "pending")
        self.assertEqual(validate(read_json(target / "plan.json"), target), [])
        with self.assertRaises(FileExistsError):
            initialize(target)
        self.assertTrue((target / "HANDOFF.md").is_file())

    def test_initializer_invalid_id_writes_nothing(self):
        with self.assertRaises(ValueError):
            initialize(self.root / "bad name")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_paths_reject_ascii_and_unicode_control_characters(self):
        for codepoint in (0x00, 0x1F, 0x7F, 0x80, 0x85, 0x9F):
            with self.subTest(codepoint=codepoint):
                with self.assertRaises(ValueError):
                    safe_relative_path("sources/bad" + chr(codepoint) + ".mov", self.root)
        self.assertEqual(safe_relative_path("sources/normal clip.mov", self.root),
                         self.root.resolve() / "sources" / "normal clip.mov")

    def test_atomic_json_no_overwrite_and_explicit_force(self):
        path = self.root / "result.json"
        write_json(path, {"a": 1})
        with self.assertRaises(FileExistsError):
            write_json(path, {"a": 2})
        self.assertEqual(read_json(path), {"a": 1})
        write_json(path, {"a": 2}, force=True)
        self.assertEqual(read_json(path), {"a": 2})
        self.assertEqual(len(list(self.root.iterdir())), 1)

    def test_json_exponent_overflow_is_rejected(self):
        path = self.root / "numbers.json"
        for token in ("1e400", "-1e400"):
            with self.subTest(token=token):
                path.write_text('{"nested": [{"value": ' + token + '}]}')
                with self.assertRaisesRegex(ValueError, "non-finite JSON number"):
                    read_json(path)
                with patch("sys.stderr"):
                    self.assertEqual(validate_main([str(path)]), 2)
        path.write_text('{"positive": 1e300, "negative": -1e300}')
        self.assertEqual(read_json(path), {"positive": 1e300, "negative": -1e300})

    def test_probe_rejects_nonfinite_json_without_output(self):
        source = self.root / "input.mov"
        source.write_bytes(b"synthetic")
        output = self.root / "metadata.json"
        for token in ("1e400", "-1e400", "NaN", "Infinity", "-Infinity"):
            with self.subTest(token=token):
                raw = '{"streams": [{"codec_type": "video", "value": ' + token + '}]}'
                with patch("probe_media.subprocess.run", return_value=subprocess.CompletedProcess([], 0, raw, "")):
                    with self.assertRaisesRegex(ValueError, "non-finite JSON number"):
                        probe(source)
                    with patch("sys.stderr"):
                        self.assertEqual(probe_main([str(source), "--output", str(output)]), 2)
                self.assertFalse(output.exists())

    def test_probe_failure_leaves_no_output(self):
        source = self.root / "bad clip.mov"
        source.write_bytes(b"not media")
        output = self.root / "metadata.json"
        with patch("probe_media.subprocess.run", return_value=subprocess.CompletedProcess([], 1, "", "bad data")), patch("sys.stderr"):
            self.assertEqual(probe_main([str(source), "--output", str(output)]), 2)
        self.assertFalse(output.exists())

    def test_probe_argument_safety_preserves_metadata_counts_and_rotation(self):
        source = self.root / "clip $(do-not-run).mov"
        source.write_bytes(b"synthetic")
        raw = {"streams": [{"codec_type": "video", "avg_frame_rate": "30000/1001",
                           "r_frame_rate": "30000/1001", "color_space": "bt709",
                           "color_transfer": "bt709", "color_primaries": "bt709",
                           "side_data_list": [{"rotation": 90}], "nb_read_frames": "300"}],
               "format": {"duration": "10.010000"}}
        with patch("probe_media.subprocess.run", return_value=subprocess.CompletedProcess([], 0, json.dumps(raw), "")) as run:
            result = probe(source, count_frames=True)
        command = run.call_args.args[0]
        self.assertIn("-count_frames", command)
        self.assertNotIn("-count_packets", command)
        self.assertEqual(command[-1], str(source.resolve()))
        self.assertNotIn("shell", run.call_args.kwargs)
        self.assertEqual(result["ffprobe"], raw)

    def test_probe_no_overwrite_output_source_and_missing_binary(self):
        source = self.root / "input.mov"
        source.write_bytes(b"synthetic")
        output = self.root / "output.json"
        output.write_text("keep")
        with patch("sys.stderr"), patch("probe_media.subprocess.run") as run:
            self.assertEqual(probe_main([str(source), "--output", str(output)]), 2)
            self.assertEqual(probe_main([str(source), "--output", str(source), "--force"]), 2)
            run.assert_not_called()
        self.assertEqual(output.read_text(), "keep")
        with patch("probe_media.subprocess.run", side_effect=FileNotFoundError("missing ffprobe")), patch("sys.stderr"):
            self.assertEqual(probe_main([str(source), "--output", str(output), "--force"]), 2)
        self.assertEqual(output.read_text(), "keep")

    def test_probe_timeout_clean_failure(self):
        source = self.root / "input.mov"
        source.write_bytes(b"synthetic")
        with patch("probe_media.subprocess.run", side_effect=subprocess.TimeoutExpired("ffprobe", 1)), patch("sys.stderr"):
            self.assertEqual(probe_main([str(source), "--output", str(self.root / "out.json")]), 2)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg and ffprobe required")
    def test_synthetic_ffmpeg_fixture_decoded_frame_count(self):
        source = self.root / "synthetic clip.mov"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                        "color=c=black:s=32x32:r=30000/1001", "-frames:v", "30",
                        "-an", "-c:v", "mpeg4", "-threads", "1", str(source)],
                       check=True, capture_output=True, timeout=30)
        record = probe(source, count_frames=True, timeout=30)
        video = next(s for s in record["ffprobe"]["streams"] if s["codec_type"] == "video")
        self.assertEqual(video["nb_read_frames"], "30")
        self.assertEqual(video["avg_frame_rate"], "30000/1001")


if __name__ == "__main__":
    unittest.main()

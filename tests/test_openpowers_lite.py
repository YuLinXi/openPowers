from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import openpowers_lite


class OpenPowersLiteTests(unittest.TestCase):
    def test_upgrade_report_marks_changed_upstreams(self) -> None:
        previous = {
            "upstreams": [
                {"name": "OpenSpec", "resolved": "a" * 40},
            ]
        }
        current = {
            "generated_at": "2026-07-01T00:00:00+00:00",
            "upstreams": [
                {"name": "OpenSpec", "resolved": "b" * 40},
                {"name": "Superpowers", "resolved": "c" * 40},
            ],
        }

        report = openpowers_lite.build_upgrade_report(Path(".openpowers/upstreams.json"), previous, current)

        self.assertIn("| OpenSpec | changed |", report)
        self.assertIn("| Superpowers | new |", report)
        self.assertIn("Workflow rules changed automatically: `no`", report)

    def test_verify_detects_duplicate_product_specs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".openpowers/specs").mkdir(parents=True)

            results = openpowers_lite.verify_no_duplicate_product_specs(root)

        self.assertEqual(results[0].status, "fail")
        self.assertIn(".openpowers/specs", results[0].message)

    def test_write_json_sorts_keys_and_creates_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested/payload.json"
            openpowers_lite.write_json(path, {"b": 1, "a": 2})

            payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(payload, {"a": 2, "b": 1})


if __name__ == "__main__":
    unittest.main()

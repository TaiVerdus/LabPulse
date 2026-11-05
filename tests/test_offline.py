import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from offline.pipeline import trial_events, extract, summarize
from offline.replay import replay
from offline.screen import schedule


class IntegrityTests(unittest.TestCase):
    def test_practice_schedule_has_balanced_directions(self):
        rows = schedule()
        self.assertEqual(rows, schedule())
        self.assertEqual(sum(r["planned_error"] for r in rows), 6)
        self.assertEqual(sum(r["outcome"] == "←" for r in rows), 10)
        self.assertTrue(all((r["target"] != r["outcome"]) == r["planned_error"] for r in rows))
    def test_orphan_outcome_rejected(self):
        with self.assertRaises(ValueError):
            trial_events([{"type": "S  6", "latency": 100}])

    def test_truth_not_feature(self):
        data = np.random.default_rng(1).normal(size=(3, 2000))
        a = {"sample_float": 800, "trial": 0, "human_error": False, "label": 0}
        b = dict(a, label=1)
        x1 = extract(data, 256, ["Fz", "Cz", "EOG1"], [a])[0]
        x2 = extract(data, 256, ["Fz", "Cz", "EOG1"], [b])[0]
        np.testing.assert_array_equal(x1, x2)

    def test_bad_epoch_and_human_error_excluded(self):
        data = np.zeros((1, 2000)); data[0, 800] = 500
        trials = [{"sample_float": 800, "trial": 0, "human_error": False, "label": 1},
                  {"sample_float": 1200, "trial": 1, "human_error": True, "label": 0}]
        x, _, _, rows, _ = extract(data, 256, ["Fz"], trials)
        self.assertEqual(len(x), 0)
        self.assertEqual([r["reason"] for r in rows], ["amplitude_artifact", "human_error"])

    def test_confusion_semantics(self):
        result = summarize(np.array([0, 0, 1, 1]), np.array([0.2, 0.8, 0.1, 0.9]))
        self.assertEqual(result["normal_false_alarm_rate"], 0.5)
        self.assertEqual(result["confusion_matrix_true_rows_pred_columns"], [[1, 1], [1, 1]])

    def test_live_cannot_be_presented_as_replay(self):
        Path("local_runs").mkdir(exist_ok=True)
        with TemporaryDirectory(dir="local_runs") as d:
            p = Path(d) / "p.jsonl"
            p.write_text('{"mode":"live"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                replay(p, delay=0)

    def test_outcome_can_precede_feedback_within_same_trial(self):
        events = [{"type": "S  6", "latency": 100}, {"type": "FB2", "latency": 100.2},
                  {"type": "S  9", "latency": 300}]
        rows = trial_events(events)
        self.assertEqual(rows[0]["label"], 1)
        self.assertAlmostEqual(rows[0]["sample_float"], 99.2)


if __name__ == "__main__":
    unittest.main()

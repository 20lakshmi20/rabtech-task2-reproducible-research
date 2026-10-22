import sys
import unittest
from pathlib import Path
import tempfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analyze import load_and_prepare

class TestSyntheticPipeline(unittest.TestCase):
    def test_grouping_and_cleaning_on_synthetic_fixture(self):
        # Synthetic fixture only: the real UCI dataset is not read by this test.
        fixture = pd.DataFrame({
            "studytime": [1, 2, 3, 4, None, 9],
            "G3": [10, 12, 15, 18, 16, 17],
            "extra_column": ["a", "b", "c", "d", "e", "f"],
        })
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / "synthetic.csv"
            fixture.to_csv(raw_path, sep=";", index=False)
            result = load_and_prepare(raw_path)
            self.assertEqual(len(result), 4)
            self.assertEqual(result["study_group"].tolist(), ["lower", "lower", "higher", "higher"])
            self.assertEqual(result["G3"].tolist(), [10, 12, 15, 18])

if __name__ == "__main__":
    unittest.main()

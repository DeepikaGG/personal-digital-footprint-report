import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cli"))
import footprint as fp

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


class TestFootprint(unittest.TestCase):
    def test_risk_formula(self):
        self.assertEqual(fp.risk({"sensitivity": 4, "discoverability": 5, "exploitability": 5}), 100)

    def test_rating_bands(self):
        self.assertEqual([fp.rating(x) for x in (100, 60, 59, 30, 29, 12, 11)],
                         ["Critical", "Critical", "High", "High", "Medium", "Medium", "Low"])

    def test_sample_before_and_after(self):
        b = fp.summarise(fp.load(os.path.join(DATA, "sample_before.json"))["findings"])
        a = fp.summarise(fp.load(os.path.join(DATA, "sample_after.json"))["findings"])
        self.assertEqual((b["exposure"], a["exposure"]), (37, 12))
        self.assertEqual(b["by_rating"]["Critical"], 2)
        self.assertEqual(a["by_rating"]["Critical"], 0)

    def test_redaction(self):
        out = fp.redact("Mail a@b.com or call +91 98765 43210 from 10.0.0.1", ["Krishna"])
        self.assertNotIn("a@b.com", out)
        self.assertIn("[EMAIL]", out)
        self.assertIn("[PHONE]", out)
        self.assertIn("[IP]", out)

    def test_empty_exposure(self):
        self.assertEqual(fp.summarise([])["exposure"], 0)


if __name__ == "__main__":
    unittest.main()

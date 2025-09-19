# test_main.py
import unittest
from Main import LogAnalyzer

class TestLogAnalyzer(unittest.TestCase):
    def test_extract_timestamp(self):
        analyzer = LogAnalyzer()
        line = "06-01 12:34:56.789 Some log message"
        self.assertEqual(analyzer.extract_timestamp(line), "06-01 12:34:56.789")

if __name__ == "__main__":
    unittest.main()
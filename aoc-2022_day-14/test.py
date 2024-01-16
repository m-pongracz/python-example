import unittest
from main import *

class TestDay14(unittest.TestCase):

    def test_2(self):
        self.assertEqual(parse_line_into_rock_paths("498,4 -> 498,6"), ([(498, 4), (498, 6)], 6, 498))

    def test_3(self):
        self.assertEqual(parse_line_into_rock_paths("498,4 -> 498,6 -> 496,6"), ([(498, 4), (498, 6), (496, 6)], 6, 498))

    def test_run_test_file(self):
        self.assertEqual(run("input_test.txt", False), 24)

    def test_run_live_file(self):
        self.assertEqual(run("input.txt", False), 774)

    def test_run_floor_test_file(self):
        self.assertEqual(run("input_test.txt", True), 93)

if __name__ == '__main__':
    unittest.main()
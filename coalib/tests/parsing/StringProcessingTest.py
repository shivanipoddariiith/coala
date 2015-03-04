import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import *

class StringProcessingTest(unittest.TestCase):
    def setUp(self):
        self.test_strings = [
            r"out1 'escaped-escape:        \\ ' out2",
            r"out1 'escaped-quote:         \' ' out2",
            r"out1 'escaped-anything:      \X ' out2",
            r"out1 'two escaped escapes: \\\\ ' out2",
            r"out1 'escaped-quote at end:   \'' out2",
            r"out1 'escaped-escape at end:  \\' out2",
            r"out1           'str1' out2 'str2' out2",
            r"out1 \'        'str1' out2 'str2' out2",
            r"out1 \\\'      'str1' out2 'str2' out2",
            r"out1 \\        'str1' out2 'str2' out2",
            r"out1 \\\\      'str1' out2 'str2' out2",
            r"out1         \\'str1' out2 'str2' out2",
            r"out1       \\\\'str1' out2 'str2' out2",
            r"out1           'str1''str2''str3' out2"]

        # The backslash character. Needed since there are limitations when
        # using backslashes at the end of raw-strings in front of the
        # terminating " or '.
        self.bs = "\\"

    # Test the search_for() function.
    def test_search_for(self):
        # Match either "out1" or "out2".
        search_pattern = "out1|out2"
        # These are the expected results for the zero-group of the
        # returned MatchObject's.
        expected_results = [
            [r"out1", r"out2"],
            [r"out1", r"out2"],
            [r"out1", r"out2"],
            [r"out1", r"out2"],
            [r"out1", r"out2"],
            [r"out1", r"out2"],
            [r"out1", r"out2", r"out2"],
            [r"out1", r"out2", r"out2"],
            [r"out1", r"out2", r"out2"],
            [r"out1", r"out2", r"out2"],
            [r"out1", r"out2", r"out2"],
            [r"out1", r"out2", r"out2"],
            [r"out1", r"out2", r"out2"],
            [r"out1", r"out2"]
        ]

        self.assertEqual(len(expected_results), len(self.test_strings))
        for i in range(0, len(expected_results)):
            return_value = search_for(search_pattern, self.test_strings[i])

            # Check each MatchObject. Need to iterate over the return_value
            # since the return value is an iterator object pointing to the
            # MatchObject's.
            n = 0
            for x in return_value:
                self.assertEqual(expected_results[i][n], x.group(0))
                n += 1

    # Test what happens when providing a negative max_match parameter for
    # search_for().
    def test_search_for_negative_max_match(self):
        search_pattern = "'"
        # Shall throw ValueError each time.
        for teststr in self.test_strings:
            self.assertRaises(ValueError,
                              search_for,
                              search_pattern,
                              teststr,
                              -1)
            # The same with a crazier number.
            self.assertRaises(ValueError,
                              search_for,
                              search_pattern,
                              teststr,
                              -43287982374112)


if __name__ == '__main__':
    unittest.main(verbosity=2)


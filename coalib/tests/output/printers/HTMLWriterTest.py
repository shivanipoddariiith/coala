import re
import sys
import os
import tempfile

sys.path.insert(0, ".")
from coalib.output.printers.HTMLWriter import HTMLWriter
import unittest


class HTMLWriterTest(unittest.TestCase):
    def setUp(self):
        handle, self.filename = tempfile.mkstemp()
        os.close(handle)  # We don't need the handle provided by mkstemp
        self.uut = HTMLWriter(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_construction(self):
        self.assertRaises(TypeError, HTMLWriter, 5)
        with open(self.filename) as file:
            lines = file.readlines()
        self.assertEqual(lines,
                        ['<!DOCTYPE html>\n',
                         '<html>\n'])

    def test_write_comment(self):
        self.uut.write_comment("test1 test2")
        with open(self.filename) as file:
            lines = file.readlines()
        self.assertEqual(lines,['<!--test1-->',
                                '<!--test2-->'])

    def test_printing_header(self):
        with open(self.filename) as file:
            lines = file.readlines()
        self.assertEqual(lines,
                        ['<!DOCTYPE html>\n',
                         '<html>\n'])

    def test_printing_footer(self):
        with open(self.filename) as file:
            lines = file.readlines()
        self.assertEqual(lines,['</html>'])


        

if __name__ == '__main__':
    unittest.main(verbosity=2)

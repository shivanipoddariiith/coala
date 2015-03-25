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
        self.assertEqual(lines, [])
        del self.uut

    def test_printing_header_footer(self):
        self.uut = HTMLWriter(self.filename)
        with open(self.filename) as file:
            lines = file.readlines()
        self.assertEqual(lines,
                        ['<!DOCTYPE html>\n',
                         '<html>\n',
                         '</html>\n'])
        file.close()
        del self.uut

    def test_write_comment(self):
        self.uut = HTMLWriter(self.filename)
        file = open(self.filename)
        if file is not None:
            self.uut.write_comment("testing comments")
            lines = file.readlines()

            self.assertEqual(lines,
                        ['<!DOCTYPE html>\n',
                         '<html>\n',
                         '<!--testing comments-->\n',
                         '</html>\n'])
        file.close()
        del self.uut

    def test_write_tags(self):
        self.uut = HTMLWriter(self.filename)
        self.tag_dict = {'p':'test'}
        file = open(self.filename)
        if file is not None:
            self.uut.write_tags(**self.tag_dict)
            lines = file.readlines()

            self.assertEqual(lines,
                        ['<!DOCTYPE html>\n',
                         '<html>\n',
                         '<p> test </p>\n',
                         '</html>\n'])
        file.close()
        del self.uut
        

if __name__ == '__main__':
    unittest.main(verbosity=2)

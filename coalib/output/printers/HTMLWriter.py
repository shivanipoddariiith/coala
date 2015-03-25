"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


class HTMLWriter:
    """
        Facilitates Printing HTMLPrinter.  If the directory of the given file doesn't exist or if there's any
        access problems, an exception will be thrown.

        :param filename: the name of the file to put the data into (string).
        :param indentation_per_tag: spaces used to indent every subsequent HTML tag

    """

    def __init__(self, filename, indentation_per_tag=2, indentation=0):

        self.indentation_per_tag = indentation_per_tag
        self.indentation = indentation
        self.file = None

        if not isinstance(filename, str):
            raise TypeError("filename must be a string")


        self.file = open(filename, 'w+')


        self.filename = filename
        self.__write_header()


    def __del__(self):
        if self.file is not None:
            self.__write_footer()
            self.file.close()

    def __write_header(self):
        self.write("<!DOCTYPE html>")
        self.open_tag("html")

    def __write_footer(self):
        self.close_tag("html")

    def write_comment(self, *comments):
        for comment in comments:
            self.write("<!-- " + comment + "-->")

    def write_tag(self, tag, content="", **tagargs):
        name = tag
        for arg in tagargs:
            name += " " + arg + "=\"" + tagargs[arg] + "\""

        if content == "":
            self.write("<"+name+"/>")
            return

        self.open_tag(name)
        self.write(content)
        self.close_tag(tag)

    def write_tags(self, **tags):
        for tag in tags:
            content = tags[tag]
            if not content:
                self.write("<"+tag+"/>")
                continue

            self.open_tag(tag)
            self.write(content)
            self.close_tag(tag)

    def open_tag(self, tag_name):
        self.write("<"+tag_name+">")
        self.indentation += 4

    def close_tag(self, tag_name):
        self.indentation -= 4
        self.write("</"+tag_name+">")

    def write(self, *args):
        if self.file is not None:
            for line in args:
                self.file.write(" "*self.indentation + line + "\n")
        else:
           pass
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.HTMLWriter import HTMLWriter
from coalib.processes.communication.LogMessage import LogMessage

class HTMLPrinter(LogPrinter):
    """
    This is a simple printer/logprinter that prints everything to an HTML file.
    Note that everything will be appended.
    """
    def __init__(self, filename, log_level=LOG_LEVEL.WARNING,
                 timestamp_format="%X"):
        """
        Creates a new HTMLPrinter. If the directory of the given file doesn't
        exist or if there's any access problems, an exception will be thrown.

        :param filename: the name of the file to put the data into (string).
        """
        self.file = None
        self.log_level = log_level
        print("Minimum log level is: " + str(log_level)),
        if not isinstance(filename, str):
            raise TypeError("filename must be a string.")

        LogPrinter.__init__(self, timestamp_format=timestamp_format,
                            log_level=log_level)
        self.htmlwriter = HTMLWriter(filename)

    def __del__(self):
        print("destructor of HTMLPrinter")
        if self.file is not None:
            self.file.close()

    def _print(self, delimiter=' ', end='\n', color=None,
               log_date=True, *args):
        print("Print my own stuff")
        self.log_level = self.log_message_level
        print("Final log_message_level is " + str(self.log_level))
        if self.log_level == LOG_LEVEL.DEBUG:
            color = "Blue"
        if self.log_level == LOG_LEVEL.WARNING:
            color = "Yellow"
        if self.log_level == LOG_LEVEL.ERROR:
            color = "Red"

        if color is None:
            self.__print_without_color(*args, delimiter=delimiter, end=end)
        else:
            self.__print_with_color(color, *args, delimiter=delimiter, end=end)

    def __print_without_color(self, delimiter, end, *args):
        output = ""
        for arg in args:
            if output != "":
                output += delimiter
            output += arg

        if end == '\n':
            self.htmlwriter.write_tag("p", output)
            return
        print("OUTPUT IS" + output+end)
        self.htmlwriter.write_tag("span", output+end)

    def __print_with_color(self, color, delimiter, end, *args):
        output = ""
        for arg in args:
            if output != "":
                output += delimiter
            output += arg

        if end == '\n':
            self.htmlwriter.write_tag("p", output,
                                      style="color:{}".format(color))
            return

        self.htmlwriter.write_tag("span", output+end)

"""
Text Expansion Processor
"""
import StringIO
import re
import sys


class ExpansionInvalidException(Exception):
    """
    exception for invalid expansion lookup
    """
    pass


class TextProcessor(object):
    """
    Filters the text and processes the macro expansion.
    """

    # regexs not compiled for clarity. also there is some controversy
    # over whether compiling the regexs will improve performance
    #
    # TBD: performance test to see if regex compilation would yield any
    #     significant performance increases

    def __init__(self):
        """
        Constructor
        """
        self._macros = {}

    def __repr__(self):
        """
        repr for the object

        Returns:
            (str) : a string dump of the macro definitions.
        """
        str_io = StringIO.StringIO()
        for macro, expansion in self._macros.items():
            str_io.write("{:<15}= {}\n".format(macro, expansion))
        return str_io.getvalue()

    def define_macro(self, macro, expansion):
        """
        Defines a macro by making an entry into self._macros
        dictionary

        Args:
            macro(str)     : the name of the macro to define
            expansion(str) : the macro expansion text

        Returns:
            none
        """
        self._macros[macro] = expansion

    def expand_macro(self, macro):
        """
        Returns the expansion text for a previously defined macro

        Args:
            macro(str) : the name of the macro to return expansion text

        Returns:
            (str|None) : the macro expansion text
                         None if not found
        """
        if macro in self._macros:
            return self._macros[macro]
        else:
            raise ExpansionInvalidException(
                "Expansion not defined for macro: {}".format(macro))

    def process_line(self, line):
        """
        dispatches lines of text to the appropriate methods. this
        method is the main entry point for lines to be processed

        Args:
            line(str) : line of text to process

        Returns:
            (str) : line of text after processing
        """
        line = self.expand_line(line)
        return self.process_macros(line)

    def expand_line(self, line):
        """
        replaces macros with expansion text. deals with any expansion
        using the @ symbol

        Args:
            line(str) : line of text to process

        Returns:
            (str) : line of text after processing

        """
        # regex: (^|[^@])@([\w]+)
        #   (^|[^@]) capture start of line anchor or any char not an @
        #   @        then an @
        #   ([\w]+)  then capture to the next word boundary
        # this will ensure @@ is skipped
        line = re.sub(r'(^|[^@])@([\w]+)',
                      lambda x: x.group(1) + self.expand_macro(x.group(2)),
                      line)

        # regex: (@{([^}]+)})
        #   (       capture group 1
        #   @       @ char
        #   {       bracket
        #   ([^}]+) group 2: one or more chars not a bracket
        #   })      bracket + close capture group 1
        line = re.sub(r'(@{([^}]+)})',
                      lambda x: self.expand_macro(x.group(2)),
                      line)

        # escape all the @@
        line = re.sub(r'@@', '@', line)

        return line

    def process_macros(self, line):
        """
        adds macro definition to internal dictionary self._macros

        Args:
            line(str) : line of text to process

        Returns
            (str| None) : returns the original line if the line does not
                          contain a defintion
                          return None if the line contained a definition

        """
        # regex: ^\!([\w]+)=([\w]+.*)
        # ^\!         start of line and exclamation mark
        # ([\w]+)     capture one or more word chars
        # =           =
        # ([\w]+.*)   capture one or more word chars then everything
        #              until end of line
        match = re.match(r'^\!([\w]+)=([\w]+.*)', line)

        if match:
            macro = match.group(1)
            expansion = match.group(2)
            if re.match(r'^[\w]+$', macro) and re.match(r'^[\w]', expansion):
                self.define_macro(macro.strip(), expansion.strip())
                return None
        else:
            return line

    def filter_stdin(self):
        """
        ingests lines of text from STDIN
        prints processed lines to stdout
        """
        try:
            # linenum for error messages
            linenum = 0

            for line in sys.stdin:
                linenum += 1
                line = re.sub(r'\n', '', line)
                line = self.process_line(line)

                if line is None:
                    continue
                else:
                    print line

        except ExpansionInvalidException as error:
            print "=" * 50
            print "error in line: {}".format(linenum)
            print ">{}".format(line)
            print
            print "\ntext filtering stopped..\n"
            print error
            print "=" * 50
            sys.exit(1)

    def _filter_text(self, text):
        """
        for use by the unittests

        Args:
            text (str) - lines to process in one text string
        Returns:
            (str) : processed text
        """

        # simulate lines from stdin
        lines = [line + "\n" for line in text.splitlines()]

        # a little tweaking to get the very last line break
        # to come output correctly with StringIO
        if not text.endswith("\n"):
            lines[-1] = lines[-1].rstrip("\n")

        stringio = StringIO.StringIO()

        for line in lines:
            line = self.process_line(line)
            if line is None:
                continue
            else:
                stringio.write(line)

        return_text = stringio.getvalue()
        return return_text


if __name__ == "__main__":
    TextProcessor().filter_stdin()

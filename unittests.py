"""unittests for text processor"""
import unittest
from filter import TextProcessor, ExpansionInvalidException


class TestTextProcessor(unittest.TestCase):
    """unittests for text processor"""

    def setUp(self):
        """setup"""
        self.text_processor = TextProcessor()

    def match(self, input_text, output_text):
        """compares processor output with expected output"""
        output = self.text_processor._filter_text(input_text)
        assert output == output_text

# ----------------------------------------------------------------------------
    def test000(self):
        """define macros"""
        input_text = """
!animal=dog
!plant=tree
"""
        self.text_processor._filter_text(input_text)
        assert "animal" in self.text_processor._macros
        assert "plant" in self.text_processor._macros
        assert self.text_processor._macros['animal'] == "dog"
        assert self.text_processor._macros['plant'] == "tree"
        assert len(self.text_processor._macros.keys()) == 2

# ----------------------------------------------------------------------------

    def test001(self):
        """define one macro and expand"""
        input_text = """
!animal=dog
this is my @animal
        """
        output_text = """
this is my dog
        """
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------

    def test002(self):
        """pass through if macro not at start of line"""
        input_text = """
        !this=is not a macro because it's not at the beginning of the line
nope
        """
        output_text = """
        !this=is not a macro because it's not at the beginning of the line
nope
        """
        self.match(input_text, output_text)

# -----------------------------------------------------------------------------

    def test003(self):
        """exclamation at start of line, no macro defintion"""
        input_text = """
 this is the end of my sentence
! and the start of a new one
"""
        output_text = """
 this is the end of my sentence
! and the start of a new one
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------

    def test004(self):
        """exclamation at start of line, equals sign, no macro defintion"""
        input_text = """
 this is the end of the sentence
!Did you know a=12 ?
"""
        output_text = """
 this is the end of the sentence
!Did you know a=12 ?
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------

    def test005(self):
        """escape double @"""
        input_text = """
 test@@mail.com
"""
        output_text = """
 test@mail.com
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------

    def test006(self):
        """macro definition line should get clobbered"""
        input_text = """
 1
!animal=horse
 3
"""
        output_text = """
 1
 3
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------

    def test007(self):
        """expand a macro"""
        input_text = """
 define the macro here and the line should not be in output:
!plant=tree
 my favorite plant is a @plant
"""
        output_text = """
 define the macro here and the line should not be in output:
 my favorite plant is a tree
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------

    def test008(self):
        """expand a macro, no leading \n, no trailing \n"""
        input_text = """define the macro here and the line should not be in output:
!plant=tree
 my favorite plant is a @plant"""
        output_text = """define the macro here and the line should not be in output:
 my favorite plant is a tree"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------

    def test009(self):
        """macro is not defined"""
        input_text = """
!plant=tree
 my favorite plant is a @plantation
"""
        output_text = """
!plant=tree
 my favorite plant is a tree.
"""
        with self.assertRaises(ExpansionInvalidException):
            self.text_processor._filter_text(input_text)

# ----------------------------------------------------------------------------

    def test010(self):
        """use macro expansion in macro defintion"""
        input_text = """
!plant=tree
!statement=my favorite plant is a @plant
@statement
"""
        output_text = """
my favorite plant is a tree
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------
    def test011(self):
        """macro definition with no name"""
        input_text = """
!=hello
"""
        output_text = """
!=hello
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------
    def test012(self):
        """macro expansion with bracket syntax"""
        input_text = """
!building=house
i built a @{building}
"""
        output_text = """
i built a house
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------
    def test013(self):
        """macro expansion with bracket syntax and trailin char"""
        input_text = """
!building=house
i built many @{building}s
"""
        output_text = """
i built many houses
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------
    def test014(self):
        """pass through just line breaks"""
        input_text = """


"""
        output_text = """


"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------
    def test015(self):
        """interleaving macro assignment and lines"""
        input_text = """
!plant=tree
my favorite plant is a @plant.
!animal=monkey
hey look at those @{animal}s over there
"""
        output_text = """
my favorite plant is a tree.
hey look at those monkeys over there
"""
        self.match(input_text, output_text)


# ----------------------------------------------------------------------------
    def test016(self):
        """using bracket and @ without triggering expansion"""
        input_text = """
this should just pass through the filter
@ hello
@ { }
@{}
@}
@{
"""
        output_text = """
this should just pass through the filter
@ hello
@ { }
@{}
@}
@{
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------
    def test017(self):
        """exclamation, spaces and equals is not a definition!"""
        input_text = """
! this should = just pass through
"""
        output_text = """
! this should = just pass through
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------
    def test018(self):
        """@ symbol pass through"""
        input_text = """
@ should be ok
this should @ be ok too
as well as this@
"""
        output_text = """
@ should be ok
this should @ be ok too
as well as this@
"""
        self.match(input_text, output_text)

# ----------------------------------------------------------------------------
    def test019(self):
        """passthrough test"""
        input_text = """
! this is not a definition
! this is not = a defintion
!this = is not a defintion
!this = is not a defintion
!this = is not a defintion
!this= is not a definition
!this = nope still not
"""
        output_text = """
! this is not a definition
! this is not = a defintion
!this = is not a defintion
!this = is not a defintion
!this = is not a defintion
!this= is not a definition
!this = nope still not
"""
        self.match(input_text, output_text)


# ----------------------------------------------------------------------------
    def test020(self):
        """redefine macro"""
        input_text = """
!tv_show=price is right
my favorite tv show is @tv_show
!tv_show=ellen
my favorite tv show is @tv_show
"""
        output_text = """
my favorite tv show is price is right
my favorite tv show is ellen
"""
        self.match(input_text, output_text)


# ----------------------------------------------------------------------------
    def test021(self):
        """many escaped @ symbols"""
        input_text = """
@@@@@@@@hello
"""
        output_text = """
@@@@hello
"""
        self.match(input_text, output_text)


# ----------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)

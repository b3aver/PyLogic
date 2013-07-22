import unittest
from pylogic.propositional.propositional_logic import Formula


class TestFormula(unittest.TestCase):
    def test_init_atomic(self):
        formula = Formula("X")
        self.assertIsInstance(formula, Formula)
        self.assertEqual("X", str(formula))

    def test_init_atomic_wrong(self):
        self.assertRaises(Exception, Formula, "!")

    def test_init_unary(self):
        formula = Formula("!", Formula("X"))
        self.assertIsInstance(formula, Formula)
        self.assertEqual("!X", str(formula))

    def test_init_unary_wrong(self):
        self.assertRaises(Exception, Formula, "&", Formula("X"))
        self.assertRaises(Exception, Formula, "!", "X")

    def test_init_binary(self):
        formula = Formula("&", Formula("X"), Formula("Y"))
        self.assertIsInstance(formula, Formula)
        self.assertEqual("(X & Y)", str(formula))

    def test_init_binary_wrong(self):
        self.assertRaises(Exception, Formula, "&", "X", "Y")
        self.assertRaises(Exception, Formula, "?", Formula("X"), Formula("Y"))
        self.assertRaises(Exception, Formula, "!", Formula("X"), Formula("Y"))

    def test_init_complex(self):
        formula = Formula("&",
                          Formula("|",Formula("X"), Formula("Y")),
                          Formula("!", Formula("Y"))
                          )
        self.assertIsInstance(formula, Formula)
        self.assertEqual("((X | Y) & !Y)", str(formula))



if __name__ == '__main__':
    unittest.main()

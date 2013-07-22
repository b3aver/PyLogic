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


    def test_eq_ne_atomic(self):
        formula1 = Formula("X")
        formula2 = Formula("X")
        formula3 = Formula("Y")
        self.assertEqual(formula1, formula2)
        self.assertNotEqual(formula1, formula3)

    def test_eq_ne(self):
        formula1 = Formula("&", Formula("X"), Formula("Y"))
        formula2 = Formula("&", Formula("X"), Formula("Y"))
        formula3 = Formula("|", Formula("X"), Formula("Y"))
        formula4 = Formula("&", Formula("X"), Formula("X"))
        self.assertEqual(formula1, formula2)
        self.assertNotEqual(formula1, formula3)
        self.assertNotEqual(formula1, formula4)


    def test_is_alpha_atomic(self):
        formula1 = Formula("X")
        self.assertEqual(False, formula1.is_alpha())

    def test_is_alpha_unary(self):
        formula1 = Formula("!", Formula("X"))
        self.assertEqual(False, formula1.is_alpha())
        formula2 = Formula("!", Formula("&", Formula("X"), Formula("Y")))
        self.assertEqual(False, formula2.is_alpha())
        formula3 = Formula("!", Formula("|", Formula("X"), Formula("Y")))
        self.assertEqual(True, formula3.is_alpha())

    def test_is_alpha_binary(self):
        formula1 = Formula("&", Formula("X"), Formula("Y"))
        self.assertEqual(True, formula1.is_alpha())
        formula2 = Formula("|", Formula("X"), Formula("Y"))
        self.assertEqual(False, formula2.is_alpha())


    def test_is_beta_atomic(self):
        formula1 = Formula("X")
        self.assertEqual(False, formula1.is_beta())

    def test_is_beta_unary(self):
        formula1 = Formula("!", Formula("X"))
        self.assertEqual(False, formula1.is_beta())
        formula2 = Formula("!", Formula("&", Formula("X"), Formula("Y")))
        self.assertEqual(True, formula2.is_beta())
        formula3 = Formula("!", Formula("|", Formula("X"), Formula("Y")))
        self.assertEqual(False, formula3.is_beta())

    def test_is_beta_binary(self):
        formula1 = Formula("&", Formula("X"), Formula("Y"))
        self.assertEqual(False, formula1.is_beta())
        formula2 = Formula("|", Formula("X"), Formula("Y"))
        self.assertEqual(True, formula2.is_beta())


    def test_is_literal_atomic(self):
        formula1 = Formula("X")
        self.assertEqual(True, formula1.is_literal())

    def test_is_literal_unary(self):
        formula1 = Formula("!", Formula("X"))
        self.assertEqual(True, formula1.is_literal())
        formula2 = Formula("!", Formula("&", Formula("X"), Formula("Y")))
        self.assertEqual(False, formula2.is_literal())

    def test_is_literal_binary(self):
        formula1 = Formula("&", Formula("X"), Formula("Y"))
        self.assertEqual(False, formula1.is_literal())
        formula2 = Formula("|", Formula("X"), Formula("Y"))
        self.assertEqual(False, formula2.is_literal())


    def test_negate(self):
        formula = Formula("&", Formula("X"), Formula("Y"))
        self.assertIsInstance(formula.negate(), Formula)
        self.assertEqual(Formula("!", Formula("&", Formula("X"), Formula("Y"))),
                         formula.negate())


    def test_complement(self):
        formula1 = Formula("&", Formula("X"), Formula("Y"))
        self.assertIsInstance(formula1.complement(), Formula)
        self.assertEqual(formula1.negate(), formula1.complement())
        formula2 = Formula("!", Formula("X"))
        self.assertIsInstance(formula2.complement(), Formula)
        self.assertEqual(Formula("X"), formula2.complement())
        formula3 = Formula("X")
        self.assertIsInstance(formula3.complement(), Formula)
        self.assertEqual(Formula("!", Formula("X")), formula3.complement())


    def test_components_atomic(self):
        formula = Formula("X")
        (comp1, comp2) = formula.components()
        self.assertIsNot(comp1, formula)
        self.assertEqual(comp1, formula)
        self.assertEqual(None, comp2)

    def test_components_unary(self):
        formula = Formula("!", Formula("X"))
        (comp1, comp2) = formula.components()
        self.assertIsNot(comp1, formula)
        self.assertEqual(comp1, formula)
        self.assertEqual(None, comp2)

    def test_components_binary(self):
        sub1 = Formula("X")
        sub2 = Formula("Y")
        formula = Formula("&", sub1, sub2)
        (comp1, comp2) = formula.components()
        self.assertIsNot(comp1, sub1)
        self.assertIsNot(comp2, sub2)
        self.assertEqual(comp1, sub1)
        self.assertEqual(comp2, sub2)


    def test_nnf_atomic(self):
        formula = Formula("X")
        self.assertIsNot(formula, formula.nnf())
        self.assertEqual(formula, formula.nnf())

    def test_nnf_unary_literal(self):
        formula = Formula("!", Formula("X"))
        self.assertIsNot(formula, formula.nnf())
        self.assertEqual(formula, formula.nnf())

    def test_nnf_unary(self):
        atom1 = Formula("X")
        atom2 = Formula("Y")
        sub = Formula("&", atom1, atom2)
        formula = Formula("!", sub)
        exp = Formula("|",
                      Formula("!", Formula("X")),
                      Formula("!", Formula("Y")))
        self.assertEqual(exp, formula.nnf())
        self.assertIsNot(atom1, formula.nnf().subformula1.subformula1)
        self.assertIsNot(atom2, formula.nnf().subformula2.subformula1)

    def test_nnf_not_not(self):
        sub = Formula("X")
        formula = Formula("!", Formula("!", sub))
        self.assertIsNot(sub, formula.nnf())
        self.assertEqual(sub, formula.nnf())

    def test_nnf_binary(self):
        atom1 = Formula("X")
        atom2 = Formula("Y")
        sub1 = Formula("!", Formula("!", atom1))
        sub2 = Formula("!", Formula("!", atom2))
        formula = Formula("&", sub1, sub2)
        exp = Formula("&", atom1, atom2)
        self.assertEqual(exp, formula.nnf())
        self.assertIsNot(atom1, formula.nnf().subformula1)
        self.assertIsNot(atom2, formula.nnf().subformula2)



if __name__ == '__main__':
    unittest.main()

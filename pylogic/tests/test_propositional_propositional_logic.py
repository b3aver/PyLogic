import unittest
from pylogic.propositional.propositional_logic import Formula, Generalization


class TestFormula(unittest.TestCase):
    def setUp(self):
        self.a1 = Formula("X")
        self.a2 = Formula("Y")


    def test_init_atomic(self):
        formula = Formula("X")
        self.assertIsInstance(formula, Formula)
        self.assertEqual(None, formula.connective)
        self.assertEqual("X", formula.subformula1)

    def test_init_atomic_wrong(self):
        self.assertRaises(Exception, Formula, "!")

    def test_init_unary(self):
        formula = Formula("!", self.a1)
        self.assertIsInstance(formula, Formula)
        self.assertEqual("not", formula.connective)
        self.assertEqual(self.a1, formula.subformula1)

    def test_init_unary_wrong(self):
        self.assertRaises(Exception, Formula, "&", Formula("X"))
        self.assertRaises(Exception, Formula, "!", "X")

    def test_init_binary(self):
        formula = Formula("&", self.a1, self.a2)
        self.assertIsInstance(formula, Formula)
        self.assertEqual("and", formula.connective)
        self.assertEqual(self.a1, formula.subformula1)
        self.assertEqual(self.a2, formula.subformula2)

    def test_init_binary_wrong(self):
        self.assertRaises(Exception, Formula, "&", "X", "Y")
        self.assertRaises(Exception, Formula, "?", Formula("X"), Formula("Y"))
        self.assertRaises(Exception, Formula, "!", Formula("X"), Formula("Y"))


    def test_str_atomic(self):
        self.assertEqual("X", str(self.a1))

    def test_str_unary(self):
        formula = Formula("!", self.a1)
        self.assertEqual("!X", str(formula))

    def test_str_binary(self):
        formula = Formula("&", self.a1, self.a2)
        self.assertEqual("(X & Y)", str(formula))

    def test_str_complex(self):
        formula = Formula("&",
                          Formula("|",Formula("X"), Formula("Y")),
                          Formula("!", Formula("Y"))
                          )
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
        self.assertIsNot(self.a1, self.a1.nnf())
        self.assertEqual(self.a1, self.a1.nnf())

    def test_nnf_unary_literal(self):
        formula = Formula("!", Formula("X"))
        self.assertIsNot(formula, formula.nnf())
        self.assertEqual(formula, formula.nnf())

    def test_nnf_unary(self):
        sub = Formula("&", self.a1, self.a2)
        formula = Formula("!", sub)
        exp = Formula("|",
                      Formula("!", Formula("X")),
                      Formula("!", Formula("Y")))
        self.assertEqual(exp, formula.nnf())
        self.assertIsNot(self.a1, formula.nnf().subformula1.subformula1)
        self.assertIsNot(self.a2, formula.nnf().subformula2.subformula1)

    def test_nnf_not_not(self):
        formula = Formula("!", Formula("!", self.a1))
        self.assertIsNot(self.a1, formula.nnf())
        self.assertEqual(self.a1, formula.nnf())

    def test_nnf_binary(self):
        sub1 = Formula("!", Formula("!", self.a1))
        sub2 = Formula("!", Formula("!", self.a2))
        formula = Formula("&", sub1, sub2)
        exp = Formula("&", self.a1, self.a2)
        self.assertEqual(exp, formula.nnf())
        self.assertIsNot(self.a1, formula.nnf().subformula1)
        self.assertIsNot(self.a2, formula.nnf().subformula2)



class TestGeneralization(unittest.TestCase):
    def setUp(self):
        self.f1 = Formula("&", Formula("X"), Formula("Y"))
        self.f2 = Formula("|", Formula("X"), Formula("Y"))
        # self.g1 = Generalization("and", [self.f1, self.f2])
        # self.g2 = Generalization("or", [self.f1, Formula("Z"),
        #                                 Formula("!", Formula("Y")), self.f2])


    def test_init_wrong_connective(self):
        self.assertRaises(Exception, Generalization, "!", [self.f1, self.f2])
        self.assertRaises(Exception, Generalization, "=>", [self.f1, self.f2])
        self.assertRaises(Exception, Generalization, "!&", [self.f1, self.f2])

    def test_init_wrong_formulas(self):
        self.assertRaises(Exception, Generalization, "&", self.f1)
        self.assertRaises(Exception, Generalization, "&", ["hello", "world"])

    def test_init_and(self):
        gen = Generalization("and", [self.f1, self.f2])
        self.assertEqual("and", gen.connective)
        self.assertEqual([self.f1, self.f2], gen.list)
        gen2 = Generalization("&", [self.f1, self.f2])
        self.assertEqual("and", gen2.connective)
        self.assertEqual([self.f1, self.f2], gen2.list)

    def test_init_or(self):
        gen = Generalization("or", [self.f1, self.f2])
        self.assertEqual("or", gen.connective)
        self.assertEqual([self.f1, self.f2], gen.list)
        gen2 = Generalization("|", [self.f1, self.f2])
        self.assertEqual("or", gen2.connective)
        self.assertEqual([self.f1, self.f2], gen2.list)

    def test_init_empty(self):
        gen = Generalization("or", [])
        self.assertEqual("or", gen.connective)
        self.assertEqual([], gen.list)


    def test_str(self):
        exp = "< %s , %s >" % (str(self.f1), str(self.f2))
        self.assertEqual(exp, str(Generalization("&", [self.f1, self.f2])))
        exp2 = "[ %s , %s ]" % (str(self.f1), str(self.f2))
        self.assertEqual(exp2, str(Generalization("or", [self.f1, self.f2])))


    def test_has_non_literal(self):
        g1 = Generalization("and", [self.f1, Formula("Z"), self.f2])
        g2 = Generalization("or", [Formula("Z"), Formula("!", Formula("Y"))])
        g3 = Generalization("or", [])
        self.assertTrue(g1.has_non_literal)
        self.assertFalse(g3.has_non_literal())
        self.assertFalse(g2.has_non_literal())


    def test_get_non_literal(self):
        g1 = Generalization("and", [self.f1, Formula("Z"), self.f2])
        self.assertIs(self.f1, g1.get_non_literal())



if __name__ == '__main__':
    unittest.main()

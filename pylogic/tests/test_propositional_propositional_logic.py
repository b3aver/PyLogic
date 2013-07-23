import unittest
from pylogic.propositional.propositional_logic import Formula, Generalization


class TestFormula(unittest.TestCase):
    def setUp(self):
        self.a1 = Formula("X")
        self.a2 = Formula("Y")
        self.l1 = Formula("!", Formula("X"))
        self.fand1 = Formula("&", Formula("X"), Formula("Y"))
        self.for1 = Formula("|", Formula("X"), Formula("Y"))


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
        self.assertEqual("!X", str(self.l1))

    def test_str_binary(self):
        self.assertEqual("(X & Y)", str(self.fand1))

    def test_str_complex(self):
        formula = Formula("&", self.for1, self.l1)
        self.assertEqual("((X | Y) & !X)", str(formula))


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
        self.assertFalse(self.a1.is_alpha())

    def test_is_alpha_unary(self):
        self.assertFalse(self.l1.is_alpha())
        formula2 = Formula("!", self.fand1)
        self.assertFalse(formula2.is_alpha())
        formula3 = Formula("!", self.for1)
        self.assertTrue(formula3.is_alpha())

    def test_is_alpha_binary(self):
        self.assertTrue(self.fand1.is_alpha())
        self.assertFalse(self.for1.is_alpha())

    def test_is_alpha_not_not_not_literal(self):
        f1 = self.l1.negate().negate()
        f2 = self.l1.negate().negate().negate()
        self.assertFalse(f1.is_alpha())
        self.assertFalse(f2.is_alpha())

    def test_is_alpha_not_not_not_alpha(self):
        f1 = self.fand1.negate()
        f2 = self.fand1.negate().negate()
        self.assertFalse(f1.is_alpha())
        self.assertTrue(f2.is_alpha())

    def test_is_alpha_not_not_not_beta(self):
        f1 = self.for1.negate()
        f2 = self.for1.negate().negate()
        self.assertTrue(f1.is_alpha())
        self.assertFalse(f2.is_alpha())


    def test_is_beta_atomic(self):
        self.assertFalse(self.a1.is_beta())

    def test_is_beta_unary(self):
        self.assertFalse(self.l1.is_beta())
        formula2 = Formula("!", self.fand1)
        self.assertTrue(formula2.is_beta())
        formula3 = Formula("!", self.for1)
        self.assertFalse(formula3.is_beta())

    def test_is_beta_binary(self):
        self.assertFalse(self.fand1.is_beta())
        self.assertTrue(self.for1.is_beta())

    def test_is_beta_not_not_not_literal(self):
        f1 = self.l1.negate().negate()
        f2 = self.l1.negate().negate().negate()
        self.assertFalse(f1.is_beta())
        self.assertFalse(f2.is_beta())

    def test_is_beta_not_not_not_alpha(self):
        f1 = self.fand1.negate()
        f2 = self.fand1.negate().negate()
        self.assertTrue(f1.is_beta())
        self.assertFalse(f2.is_beta())

    def test_is_beta_not_not_not_beta(self):
        f1 = self.for1.negate()
        f2 = self.for1.negate().negate()
        self.assertFalse(f1.is_beta())
        self.assertTrue(f2.is_beta())


    def test_is_literal_atomic(self):
        self.assertTrue(self.a1.is_literal())

    def test_is_literal_unary(self):
        self.assertTrue(self.l1.is_literal())
        formula2 = Formula("!", self.fand1)
        self.assertFalse(formula2.is_literal())

    def test_is_literal_binary(self):
        self.assertFalse(self.fand1.is_literal())
        self.assertFalse(self.for1.is_literal())

    def test_is_literal_top_bottom(self):
        self.assertTrue(Formula("T").is_literal())
        self.assertTrue(Formula("F").is_literal())
        self.assertFalse(Formula("!", Formula("T")).is_literal())
        self.assertFalse(Formula("!", Formula("F")).is_literal())


    def test_negate(self):
        self.assertIsInstance(self.fand1.negate(), Formula)
        self.assertEqual(Formula("!", self.fand1), self.fand1.negate())


    def test_complement(self):
        # binary
        self.assertIsInstance(self.fand1.complement(), Formula)
        self.assertEqual(self.fand1.negate(), self.fand1.complement())
        # literal
        self.assertIsInstance(self.l1.complement(), Formula)
        self.assertEqual(self.a1, self.l1.complement())
        # atomic
        self.assertIsInstance(self.a1.complement(), Formula)
        self.assertEqual(self.l1, self.a1.complement())


    def test_components_atomic(self):
        (comp1, comp2) = self.a1.components()
        self.assertIsNot(comp1, self.a1)
        self.assertEqual(comp1, self.a1)
        self.assertEqual(None, comp2)

    def test_components_unary(self):
        (comp1, comp2) = self.l1.components()
        self.assertIsNot(comp1, self.l1)
        self.assertEqual(comp1, self.l1)
        self.assertEqual(None, comp2)

    def test_components_binary(self):
        formula = Formula("&", self.a1, self.a2)
        (comp1, comp2) = formula.components()
        self.assertIsNot(comp1, self.a1)
        self.assertIsNot(comp2, self.a2)
        self.assertEqual(comp1, self.a1)
        self.assertEqual(comp2, self.a2)


    def test_nnf_atomic(self):
        self.assertIsNot(self.a1, self.a1.nnf())
        self.assertEqual(self.a1, self.a1.nnf())

    def test_nnf_unary_literal(self):
        self.assertIsNot(self.l1, self.l1.nnf())
        self.assertEqual(self.l1, self.l1.nnf())

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


    def test_cnf_atomic(self):
        exp = Generalization("and", [Generalization("or", [self.a1])])
        self.assertEqual(exp, self.a1.cnf())

    def test_cnf_literal(self):
        exp = Generalization("and", [Generalization("or", [self.l1])])
        self.assertEqual(exp, self.l1.cnf())

    def test_cnf_alpha(self):
        exp = Generalization("and", [
                Generalization("or", [self.a1]),
                Generalization("or", [self.a2])])
        self.assertEqual(exp, self.fand1.cnf())

    def test_cnf_beta(self):
        exp = Generalization("and", [Generalization("or", [self.a1, self.a2])])
        self.assertEqual(exp, self.for1.cnf())

    def test_cnf_not_not(self):
        exp = Generalization("and", [Generalization("or", [self.a1])])
        self.assertEqual(exp, Formula("!", self.l1).cnf())

    def test_cnf_not_top(self):
        formula = Formula("!", Formula("T"))
        exp = Generalization("and", [Generalization("or", [Formula("F")])])
        self.assertEqual(exp, formula.cnf())

    def test_cnf_not_bottom(self):
        formula = Formula("!", Formula("F"))
        exp = Generalization("and", [Generalization("or", [Formula("T")])])
        self.assertEqual(exp, formula.cnf())



class TestGeneralization(unittest.TestCase):
    def setUp(self):
        self.f1 = Formula("&", Formula("X"), Formula("Y"))
        self.f2 = Formula("|", Formula("X"), Formula("Y"))


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

    def test_eq_ne(self):
        g1 = Generalization("and", [self.f1, self.f2])
        g12 = Generalization("and", [self.f1, self.f2])
        g13 = Generalization("and", [self.f1])
        g2 = Generalization("or", [self.f1, self.f2])
        g22 = Generalization("or", [self.f1, self.f2])
        g3 = Generalization("or", [g1])
        g32 = Generalization("or", [g1])
        g33 = Generalization("or", [g13])
        self.assertEqual(g1, g12)
        self.assertEqual(g2, g22)
        self.assertEqual(g3, g32)
        self.assertNotEqual(g1, g2)
        self.assertNotEqual(g1, g13)
        self.assertNotEqual(g2, g3)
        self.assertNotEqual(g3, g1)


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


    def test_get_parent_non_literal(self):
        g1 = Generalization("or",[
                self.f1,
                Generalization("and", [self.f1]),
                Generalization("and", [self.f1, Formula("Z"), self.f2])
                ])
        (p, i) = g1.get_parent_non_literal()
        print(str(g1), i, str(p), sep = "\n")
        self.assertIs(self.f1, g1.get_parent_non_literal())


    def test_cnf_wrong(self):
        g1 = Generalization("or", [Generalization("and", [self.f1, self.f2])])
        self.assertRaises(Exception, g1.cnf)
        g2 = Generalization("and", [self.f2])
        self.assertRaises(Exception, g2.cnf)
        g3 = Generalization("and", [Generalization("and", [self.f1, self.f2])])
        self.assertRaises(Exception, g3.cnf)
        g4 = Generalization("and", [Generalization("or", [self.f1, self.f2])])
        self.assertRaises(Exception, g4.cnf)

    def test_cnf(self):
        g1 = Generalization("or", [
                Formula("&", Formula("X"), Formula("!", Formula("Y")))])
        g2 = Generalization("and", [
                Generalization("or", [
                        Formula("&", Formula("X"),
                                Formula("!", Formula("Y")))])])
        self.assertEqual(Generalization("and", g1.cnf_action()), g2.cnf())


    def test_cnf_action_basis(self):
        g1 = Generalization("or", [Formula("X"), Formula("Y"),
                                   Formula("!", Formula("X"))])
        self.assertEqual([g1], g1.cnf_action())

    def test_cnf_action_alpha(self):
        g1 = Generalization("or", [Formula("&", Formula("X"), Formula("Y"))])
        exp = [Generalization("or", [Formula("X")]),
               Generalization("or", [Formula("Y")])]
        self.assertEqual(exp, g1.cnf_action())

    def test_cnf_action_beta(self):
        g1 = Generalization("or", [Formula("|", Formula("X"), Formula("Y"))])
        exp = [Generalization("or", [Formula("X"), Formula("Y")])]
        self.assertEqual(exp, g1.cnf_action())

    def test_cnf_action_not_not(self):
        g1 = Generalization("or", [Formula("!", Formula("!", Formula("X")))])
        exp = [Generalization("or", [Formula("X")])]
        self.assertEqual(exp, g1.cnf_action())

    def test_cnf_action_not_top(self):
        g1 = Generalization("or", [Formula("!", Formula("T"))])
        exp = [Generalization("or", [Formula("F")])]
        self.assertEqual(exp, g1.cnf_action())

    def test_cnf_action_not_bottom(self):
        g1 = Generalization("or", [Formula("!", Formula("F"))])
        exp = [Generalization("or", [Formula("T")])]
        self.assertEqual(exp, g1.cnf_action())


if __name__ == '__main__':
    unittest.main()

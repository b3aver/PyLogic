import unittest
from pylogic.propositional.propositional_logic import Formula, Generalization
from pylogic.propositional import resolution
from pylogic.propositional import parser


class TestResolution(unittest.TestCase):
    def setUp(self):
        self.a1 = Formula("X")
        self.a2 = Formula("Y")
        self.top = Formula("T")
        self.bottom = Formula("F")
        self.l1 = Formula("!", Formula("X"))
        self.fand1 = Formula("&", Formula("X"), Formula("Y"))
        self.for1 = Formula("|", Formula("X"), Formula("Y"))
        self.taut1 = parser.parse("((P->Q)&(Q->R))->-(-R&P)")
        self.taut2 = parser.parse("(-P->Q)->((P->Q)->Q)")
        self.taut3 = parser.parse("((P->Q)->P)->P")
        self.taut4 = parser.parse("(P->(Q->R))->((P->Q)->(P->R))")


    def test_preliminary_steps(self):
        clauses = [Generalization("or", [self.top, self.a1, self.a2]),
                   Generalization("or", [self.a2, self.a1, self.l1]),
                   Generalization("or", [self.a1, self.a2, self.bottom]),
                   Generalization("or", [self.a1, self.a2, self.a1]),
                   Generalization("or", [self.a1, self.a2])]
        exp_clauses = [Generalization("or", [self.a1, self.a2]),
                       Generalization("or", [self.a1, self.a2]),
                       Generalization("or", [self.a1, self.a2])]
        resolution.preliminary_steps(clauses)
        self.assertEqual(exp_clauses, clauses)

    def test_manage_tops(self):
        clauses = [Generalization("or", [self.top, self.a1, self.a2])]
        exp_clauses = []
        resolution.manage_tops(clauses)
        self.assertEqual(exp_clauses, clauses)

        clauses = [Generalization("or", [self.top, self.a1, self.a2]),
                   Generalization("or", [self.bottom, self.top, self.a2]),
                   Generalization("or", [self.a1, self.a2, self.top]),
                   Generalization("or", [self.a1, self.a2])]
        exp_clauses = [Generalization("or", [self.a1, self.a2])]
        resolution.manage_tops(clauses)
        self.assertEqual(exp_clauses, clauses)


    def test_manage_complementary(self):
        clauses = [Generalization("or", [self.a1, self.top, self.l1])]
        exp_clauses = []
        resolution.manage_complementary(clauses)
        self.assertEqual(exp_clauses, clauses)

        clauses = [Generalization("or", [self.a1, self.top, self.l1]),
                   Generalization("or", [self.a2, self.a1, self.l1]),
                   Generalization("or", [self.l1, self.top, self.a1]),
                   Generalization("or", [self.a1, self.a2])]
        exp_clauses = [Generalization("or", [self.a1, self.a2])]
        resolution.manage_complementary(clauses)
        self.assertEqual(exp_clauses, clauses)


    def test_manage_bottoms(self):
        clauses = [Generalization("or", [self.bottom, self.a1, self.a2]),
                   Generalization("or", [self.a1, self.bottom, self.a2]),
                   Generalization("or", [self.a1, self.a2, self.bottom]),
                   Generalization("or", [self.a1, self.a2])]
        exp_clauses = [Generalization("or", [self.a1, self.a2]),
                       Generalization("or", [self.a1, self.a2]),
                       Generalization("or", [self.a1, self.a2]),
                       Generalization("or", [self.a1, self.a2])]
        resolution.manage_bottoms(clauses)
        self.assertEqual(exp_clauses, clauses)


    def test_manage_copies(self):
        clauses = [Generalization("or", [self.a1, self.a1, self.a2]),
                   Generalization("or", [self.a1, self.a2, self.a1]),
                   Generalization("or", [self.a2, self.a1, self.a2, self.a1]),
                   Generalization("or", [self.a1, self.a2])]
        exp_clauses = [Generalization("or", [self.a1, self.a2]),
                       Generalization("or", [self.a1, self.a2]),
                       Generalization("or", [self.a2, self.a1]),
                       Generalization("or", [self.a1, self.a2])]
        resolution.manage_copies(clauses)

        self.assertEqual(exp_clauses, clauses)


    def test_is_tautology(self):
        self.assertFalse(resolution.is_tautology(self.a1))
        self.assertFalse(resolution.is_tautology(self.l1))
        self.assertFalse(resolution.is_tautology(self.fand1))
        self.assertFalse(resolution.is_tautology(self.for1))
        self.assertTrue(resolution.is_tautology(self.taut1))
        self.assertTrue(resolution.is_tautology(self.taut2))
        self.assertTrue(resolution.is_tautology(self.taut3))
        self.assertTrue(resolution.is_tautology(self.taut4))


    def test_is_closed(self):
        expansion1 = [Generalization("or", [self.a1, self.l1]),
                      Generalization("or", [self.a2])]
        expansion2 = [Generalization("or", [self.a1, self.l1]),
                      Generalization("or", []),
                      Generalization("or", [self.a2])]
        self.assertFalse(resolution.is_closed(expansion1))
        self.assertTrue(resolution.is_closed(expansion2))




if __name__ == '__main__':
    unittest.main()

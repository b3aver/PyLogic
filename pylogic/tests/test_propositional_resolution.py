import unittest
from pylogic.propositional.propositional_logic import Formula, Generalization
from pylogic.propositional.resolution import ClausePicker
from pylogic.propositional import resolution
from pylogic.propositional import parser


class TestResolution(unittest.TestCase):
    def setUp(self):
        self.a1 = Formula("X")
        self.a2 = Formula("Y")
        self.a3 = Formula("Z")
        self.a4 = Formula("W")
        self.top = Formula("T")
        self.bottom = Formula("F")
        self.l1 = Formula("!", Formula("X"))
        self.l2 = Formula("!", Formula("Y"))
        self.fand1 = Formula("&", Formula("X"), Formula("Y"))
        self.for1 = Formula("|", Formula("X"), Formula("Y"))
        self.taut1 = parser.parse("((P->Q)&(Q->R))->-(-R&P)")
        self.taut2 = parser.parse("(-P->Q)->((P->Q)->Q)")
        self.taut3 = parser.parse("((P->Q)->P)->P")
        self.taut4 = parser.parse("(P->(Q->R))->((P->Q)->(P->R))")
        self.taut5 = parser.parse("(F->X)")


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


    def test_resolution_rule(self):
        cl1 = Generalization("or", [self.a2, self.l1, self.bottom])
        cl2 = Generalization("or", [self.top, self.a1])
        form = self.l1
        exp_cl = Generalization("or", [self.a2, self.bottom, self.top])
        self.assertEqual(exp_cl, resolution.resolution_rule(cl1, cl2, form))


    def test_apply_resolution_rule(self):
        cl1 = Generalization("or", [self.a2, self.l1, self.a3])
        cl2 = Generalization("or", [self.a4, self.a1])
        exp_cls = Generalization("or", [self.a2, self.a3, self.a4])
        self.assertEqual(exp_cls, resolution.apply_resolution_rule(cl1, cl2))
        # complementary litterals in the result clause
        cl1 = Generalization("or", [self.a2, self.l1, self.a3])
        cl2 = Generalization("or", [self.a4, self.a1, self.l2])
        exp_cls = None
        self.assertEqual(exp_cls, resolution.apply_resolution_rule(cl1, cl2))
        # copied litterals in the result clause
        cl1 = Generalization("or", [self.a2, self.l1, self.a3])
        cl2 = Generalization("or", [self.a4, self.a1, self.a2])
        exp_cls = Generalization("or", [self.a2, self.a3, self.a4])
        self.assertEqual(exp_cls, resolution.apply_resolution_rule(cl1, cl2))


    def test_is_tautology(self):
        self.assertFalse(resolution.is_tautology(self.a1))
        self.assertFalse(resolution.is_tautology(self.l1))
        self.assertFalse(resolution.is_tautology(self.fand1))
        self.assertFalse(resolution.is_tautology(self.for1))
        self.assertTrue(resolution.is_tautology(self.taut1))
        self.assertTrue(resolution.is_tautology(self.taut2))
        self.assertTrue(resolution.is_tautology(self.taut3))
        self.assertTrue(resolution.is_tautology(self.taut4))
        self.assertTrue(resolution.is_tautology(self.taut5))


    def test_is_closed(self):
        expansion1 = [Generalization("or", [self.a1, self.l1]),
                      Generalization("or", [self.a2])]
        expansion2 = [Generalization("or", [self.a1, self.l1]),
                      Generalization("or", []),
                      Generalization("or", [self.a2])]
        self.assertFalse(resolution.is_closed(expansion1))
        self.assertTrue(resolution.is_closed(expansion2))


    def test_is_new(self):
        expansion1 = [Generalization("or", [self.a1, self.l1]),
                      Generalization("or", [self.a2])]
        gen1 = Generalization("or", [self.l1, self.a1])
        self.assertFalse(resolution.is_new(expansion1, gen1))
        expansion2 = [Generalization("or", [self.a1, self.l1]),
                      Generalization("or", []),
                      Generalization("or", [self.a2])]
        gen2 = Generalization("or", [self.l1])
        self.assertTrue(resolution.is_new(expansion2, gen2))



class TestClausePicker(unittest.TestCase):
    def setUp(self):
        self.a1 = Formula("X")
        self.a2 = Formula("Y")
        self.a3 = Formula("Z")
        self.a4 = Formula("W")
        self.l1 = Formula("!", Formula("X"))


    def test_init(self):
        expansion = [Generalization("or", [self.a1, self.a3, self.l1]),
                     Generalization("or", [self.a2, self.l1]),
                     Generalization("or", [self.l1, self.a4, self.a1]),
                     Generalization("or", [self.a3])]
        cp = ClausePicker(expansion)
        exp_db = [(1, 3), (2, 1), (3, 0), (3, 2)]
        self.assertEqual(exp_db, cp.db)



if __name__ == '__main__':
    unittest.main()

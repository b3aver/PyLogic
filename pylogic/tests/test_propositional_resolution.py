import unittest
from pylogic.propositional.propositional_logic import Formula, Generalization
from pylogic.propositional import resolution
from pylogic.propositional import parser


class TestResolution(unittest.TestCase):
    def setUp(self):
        self.a1 = Formula("X")
        self.a2 = Formula("Y")
        self.l1 = Formula("!", Formula("X"))
        self.fand1 = Formula("&", Formula("X"), Formula("Y"))
        self.for1 = Formula("|", Formula("X"), Formula("Y"))
        self.taut1 = parser.parse("((P->Q)&(Q->R))->-(-R&P)")
        self.taut2 = parser.parse("(-P->Q)->((P->Q)->Q)")
        self.taut3 = parser.parse("((P->Q)->P)->P")


    def test_is_tautology(self):
        self.assertFalse(resolution.is_tautology(self.a1))
        self.assertFalse(resolution.is_tautology(self.l1))
        self.assertFalse(resolution.is_tautology(self.fand1))
        self.assertFalse(resolution.is_tautology(self.for1))
        self.assertTrue(resolution.is_tautology(self.taut1))
        self.assertTrue(resolution.is_tautology(self.taut2))
        self.assertTrue(resolution.is_tautology(self.taut3))


    def test_is_closed(self):
        expansion1 = [Generalization("or", [self.a1, self.l1]),
                      Generalization("or", [self.a2])]
        expansion2 = [Generalization("or", [self.a1, self.l1]),
                      Generalization("or", []),
                      Generalization("or", [self.a2])]
        self.assertFalse(resolution.is_closed(expansion1))
        self.assertTrue(resolution.is_closed(expansion2))


    def test_expand(self):
        # self.a1 == X
        # self.l1 == !X
        expansion1 = [Generalization("or", [self.a2, self.l1]),
                      Generalization("or", [self.fand1, self.a1]),
                      Generalization("or", [self.fand1, self.for1])]
        exp1 = [Generalization("or", [self.a2, self.fand1]),
                Generalization("or", [self.fand1, self.for1])]
        result = resolution.expand(expansion1)
        self.assertTrue(result)
        self.assertEqual(exp1, expansion1)


if __name__ == '__main__':
    unittest.main()

'''Definition of the Propositional Logic: Formulas and Generalizations'''

import copy
import re
from pylogic import logic



class Formula():
    """Represents a propositional logic formula."""

    def __init__(self, *args):
        """ Constructor of a Formula.

        Could take several arguments, depends of the type of Formula:
            1 argument:
                atomic formula
                  (i.e. propositional letter "P", "Q", ... or costant top "T", or
                  bottom "F")
            2 arguments:
                unary operator negation "!" or "not"
                subformula
            3 arguments:
                binary symbol
                  (i.e. "&", "|", "=>", "<=", "!&", "!|", "!=>", "!<=", "=", "!="
                  or in the extended versions "and", "or", "impl", "implr",
                  "nand", "nor", "nimpl", "nimplr", "eq", "neq")
                subformula
                subformula
        """
        if len(args) == 1:
            letter = args[0]
            regex = re.compile("[A-Z]")
            if not regex.match(letter):
                raise Exception("Wrong formula: " + letter)
            connective = None
            subformula1 = letter
            subformula2 = None
        elif len(args) == 2:
            if args[0] != "not" and args[0] != logic.CONN["not"]:
                raise Exception("Wrong connective: " + args[0])
            if not isinstance(args[1], Formula):
                raise Exception("Wrong formula: " + args[1])
            connective = "not"
            subformula1 = args[1]
            subformula2 = None
        else:
            if args[0] in list(set(logic.CONN.values()) - set("!")):
                connective = [ item[0]
                               for item
                               in list(logic.CONN.items())
                               if item[1] == args[0]
                               ][0]
            elif args[0] in list(set(logic.CONN.keys()) - set("not")):
                connective = args[0]
            else:
                raise Exception("Wrong connective: " + args[0])
            if not isinstance(args[1], Formula):
                raise Exception("Wrong formula: " + args[1])
            if not isinstance(args[2], Formula):
                raise Exception("Wrong formula: " + args[2])
            subformula1 = args[1]
            subformula2 = args[2]

        self.connective = connective
        self.subformula1 = subformula1
        self.subformula2 = subformula2


    def __str__(self):
        if self.connective == None:
            return self.subformula1
        elif self.subformula2 == None:
            return "%s%s" % (logic.CONN[self.connective], str(self.subformula1))
        else:
            return "(%s %s %s)" % (str(self.subformula1), \
                                       logic.CONN[self.connective], \
                                       str(self.subformula2))


    def __eq__(self, other):
        if type(other) != Formula:
            return False
        if self.connective == None and other.connective == None:
            return self.subformula1 == other.subformula1
        else:
            return self.connective == other.connective \
                and self.subformula1 == other.subformula1 \
                and self.subformula2 == other.subformula2

    def __ne__(self, other):
        return not self.__eq__(other)


    def is_alpha(self):
        """Check if the Formula is an alpha formula.
        The notion of alpha formula is defined only for formulas in the form:
        (X o Y) and -(X o Y) where o is a primary connective"""
        if self.connective in logic.CONJ:
            return True
        elif self.connective in logic.DISJ:
            return False
        elif self.connective == "not":
            if self.subformula1.connective in logic.CONJ:
                return False
            elif self.subformula1.connective in logic.DISJ:
                return True
        return None


    def is_beta(self):
        """Check if the Formula is a beta formula.
        The notion of beta formula is defined only for formulas in the form:
        (X o Y) and -(X o Y) where o is a primary connective"""
        if self.connective in logic.DISJ:
            return True
        elif self.connective in logic.CONJ:
            return False
        elif self.connective == "not":
            if self.subformula1.connective in logic.DISJ:
                return False
            elif self.subformula1.connective in logic.CONJ:
                return True
        return None


    def is_literal(self):
        """Check if the formula is a literal,
        namely an atomic formula or the negation of an atomic formula."""
        if self.connective == None:
            return True
        elif self.connective == "not" \
                and self.subformula1.connective == None \
                and self.subformula1.subformula1 != logic.TOP \
                and self.subformula1.subformula1 != logic.BOTTOM:
            return True
        else:
            return False


    def negate(self):
        """Returns the negation of the current Formula"""
        return Formula("not", self)


    def complement(self):
        """Return the complement of the current Formula, namely the negation"""
        if self.connective == None:
            return self.negate()
        if self.connective == "not":
            return self.subformula1
        else:
            return self.negate()


    def components(self):
        """Return a tuple with the copy of the two components of the Formula,
        e.g. if is an alpha formula the alpha_1 and alpha_2.
        """
        if self.connective == None:
            ret = (self, None)
        if self.connective == "not":
            if self.subformula1.subformula2 == None:
                # literal
                ret = (self, None)
            else:
                (comp1, comp2) = self.subformula1.components()
                ret = (comp1.negate(), comp2.negate())
        else:
            if self.connective == "and":
                ret = (self.subformula1, self.subformula2)
            elif self.connective == "or":
                ret = (self.subformula1, self.subformula2)
            elif self.connective == "impl":
                ret = (self.subformula1.negate(), self.subformula2)
            elif self.connective == "implr":
                ret = (self.subformula1, self.subformula2.negate())
            elif self.connective == "nand":
                ret = (self.subformula1.negate(), self.subformula2.negate())
            elif self.connective == "nor":
                ret = (self.subformula1.negate(), self.subformula2.negate())
            elif self.connective == "nimpl":
                ret = (self.subformula1, self.subformula2.negate())
            elif self.connective == "nimplr":
                ret = (self.subformula1.negate(), self.subformula2)

        return copy.deepcopy(ret)


    def nnf(self):
        """Return the current Formula in Negation Normal Form."""
        if self.connective == None:
            return copy.deepcopy(self)
        if self.connective == "not":
            subformula = self.subformula1
            if subformula.connective == "not":
                # !!Z
                return copy.deepcopy(subformula.subformula1).nnf()
            elif subformula.connective == None:
                # litteral
                return copy.deepcopy(self)
            else:
                # dual
                comp1 = copy.deepcopy(subformula.subformula1).negate()
                comp2 = copy.deepcopy(subformula.subformula2).negate()
                return Formula(logic.DUAL[subformula.connective],
                               comp1,
                               comp2
                               ).nnf()
        else:
            return copy.deepcopy(Formula(self.connective, \
                                             self.subformula1.nnf(), \
                                             self.subformula2.nnf()))


    def cnf(self):
        '''Return the current Formula in Conjunctive Normal Form'''
        return Generalization("and", [Generalization("or", [self])]).cnf()



class Generalization():
    """Class that represents a generalized disjunction or conjunction."""

    def __init__(self, connective, formulas):
        """ Constructor of a Generalization.

        Take two arguments:
            connective -- determines the type of Generalization,
                          admitted values "and", "or", "&", "|"
            formulas -- list of the formulas in the Generalization
                        or a Generalization
        """
        if connective != "and"\
                and connective != "or"\
                and connective != logic.CONN["and"]\
                and connective != logic.CONN["or"]:
            raise Exception("Wrong connective: " + connective)
        if  not isinstance(formulas, list):
            raise Exception("Wrong formula")
        for item in formulas:
            if (not isinstance(item, Generalization)) \
                    and (not isinstance(item, Formula)):
                raise Exception("Wrong formula")
        if connective == logic.CONN["and"]:
            connective = "and"
        elif connective == logic.CONN["or"]:
            connective = "or"
        self.connective = connective
        self.list = formulas


    def __str__(self):
        ret = ""
        if self.connective == "and":
            ret = "< "
        elif self.connective == "or":
            ret = "[ "
        first = True
        for elem in self.list:
            if not first:
                ret += " , "
            else:
                first = False
            ret += str(elem)
        if self.connective == "and":
            ret += " >"
        elif self.connective == "or":
            ret += " ]"
        return ret


    def __eq__(self, other):
        return self.connective == other.connective and self.list == other.list

    def __ne__(self, other):
        return not self.__eq__(other)


    def __len__(self):
        return len(self.list)


    def equivalent(self, other):
        """Check if two generalizations have the same elements independently of
        their order"""
        if len(self.list) != len(other.list):
            return False
        other_list = list(other.list)
        try:
            for formula in self.list:
                other_list.remove(formula)
        except ValueError:
            return False
        return not other_list


    def has_non_literal(self):
        """Check if in the list of formulas there are non-literal formulas."""
        if len(self.list) == 0:
            #raise Exception("Empty list of formulas")
            # an empty generalization has a meaning
            # empty clause false, empty dual clause true
            return False
        for item in self.list:
            if isinstance(item, Formula):
                if not item.is_literal():
                    return True
                # else: ignore it
            elif isinstance(item, Generalization):
                if item.has_non_literal():
                    return True
        return False


    def get_non_literal(self):
        """Return a non-literal formula in the generalization.
        None if not present."""
        if len(self.list) == 0:
            return None
        for item in self.list:
            if isinstance(item, Formula):
                if not item.is_literal():
                    return item
                # else: ignore it
            elif isinstance(item, Generalization):
                non_literal = item.get_non_literal()
                if non_literal != None:
                    return non_literal
                # else: ignore it
        return None


    def get_non_literal_position(self):
        """Return the position of a non-literal formula in the generalization.
        None if not present."""
        if len(self.list) == 0:
            return None
        for item in self.list:
            if isinstance(item, Formula):
                if not item.is_literal():
                    return self.list.index(item)
                # else: ignore it
            elif isinstance(item, Generalization):
                non_literal = item.get_non_literal_position()
                if non_literal != None:
                    return non_literal
                # else: ignore it
        return None


    def get_parent_non_literal(self):
        """Find a non-literal formula in the generalization,
        and return a tuple with parent and index of such formula.
        None if not present."""
        if len(self.list) == 0:
            return None
        for item in self.list:
            if isinstance(item, Formula):
                if not item.is_literal():
                    #print "Formula", self, item
                    return (self, self.list.index(item))
                # else: ignore it
            elif isinstance(item, Generalization):
                #print "Generalization"
                non_literal = item.get_parent_non_literal()
                if non_literal != None:
                    return non_literal
                # else: ignore it
        return None


    def remove_every(self, formula):
        """Remove from the list every formula equivalent to the given."""
        self.list = [f for f in self.list
                     if isinstance(f, Generalization) or f != formula]


    def cnf_action(self):
        """Take a clause and return a list of clauses in cnf."""
        if self.connective != "or":
            raise Exception("Wrong type of generalization")

        # basis case
        if not self.has_non_literal():
            return [self]

        # recursive case
        position = self.get_non_literal_position()
        member = self.list[position]

        if member.is_beta():
            (beta1, beta2) = member.components()
            self.list.pop(position)               # remove old
            self.insert(position, [beta1, beta2]) # insert beta1 e beta2
            return self.cnf_action()
        elif member.is_alpha():
            (alpha1, alpha2) = member.components()
            self.list.pop(position)            # remove old
            clause1 = self                     # split
            clause2 = copy.deepcopy(self)      # split
            clause1.insert(position, [alpha1]) # insert alpha1
            clause2.insert(position, [alpha2]) # insert alpha2
            list1 = clause1.cnf_action()       # recursive call
            list2 = clause2.cnf_action()       # recursive call
            list1.extend(list2) # merge
            return list1
        elif member.connective == "not":
            subformula = member.subformula1
            if subformula.connective == "not":
                # !!Z
                self.list[position] = subformula.subformula1
            elif subformula.connective == None:
                if subformula.subformula1 == logic.TOP:
                    # !top
                    self.list[position] = Formula(logic.BOTTOM)
                elif subformula.subformula1 == logic.BOTTOM:
                    # !bottom
                    self.list[position] = Formula(logic.TOP)
            return self.cnf_action()


    def insert(self, index, elements):
        """ Take list of elements and inserts them at the given index."""
        i = index
        for element in elements:
            self.list.insert(i, element)
            i += 1



    def cnf(self):
        """Return the current Generalization in Conjunctive Normal Form"""

        if self.connective != "and"\
                or len(self.list) != 1\
                or self.list[0].connective != "or"\
                or len(self.list[0].list) != 1:
            raise Exception("Wrong type of generalization")

        # < [ ( X | !X ) , () ] , [ ... ] >
        #    conj       < ... >
        #    clause     [ ... ]
        #    member     ( ... )
        #    subformula X, !X

        # breadth-first
        # first beta
        # then alpha

        # deep-first
        # resolve a non literal deeply
        # take a clause with non-literal and return a list of clauses in cnf
        clause = copy.deepcopy(self.list[0])
        return Generalization("and", clause.cnf_action())

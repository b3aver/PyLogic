#!/usr/bin/python

'''Definition of the Propositional Logic: Formulas and Generalizations'''

import copy


import sys
sys.path.append("..")
import logic



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
            connective = None
            subformula1 = args[0]
            subformula2 = None
        elif len(args) == 2:
            if args[0] != "not" and args[0] != logic.CONN["not"]:
                raise Exception("Wrong connective: " + args[0])
            connective = "not"
            subformula1 = args[1]
            subformula2 = None
        else:
            if args[0] in logic.CONN.viewvalues():
                connective = [ item[0]
                               for item
                               in logic.CONN.items()
                               if item[1] == args[0]
                               ][0]
            elif args[0] in logic.CONN.viewkeys():
                connective = args[0]
            else:
                raise Exception("Wrong connective: " + args[0])
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
        
        
    def is_alpha(self):
        """Check if the Formula is an alpha formula."""
        if self.connective == None:
            return False
        elif self.connective == "not":
            return not self.subformula1.is_alpha()
        elif self.connective in logic.CONJ:
            return True
        else:
            return False
        
        
    def is_beta(self):
        """Check if the Formula is a beta formula."""
        if self.connective == None:
            return False
        elif self.connective == "not":
            return not self.subformula1.is_beta()
        elif self.connective in logic.DISJ:
            return True
        else:
            return False

        
    def is_literal(self):
        """Check if the formula is a literal,
        namely an atomic formula or the negation of an atomic formula."""
        if self.connective == None:
            return True
        elif self.connective == "not" and self.subformula1.connective == None:
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
                # letteral
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
    """Class that represents a generalized disjunction of conjunction."""

    def __init__(self, connective, formulas):
        """ Constructor of a Generalization.

        Take two arguments:
            connective -- determines the type of Generalization,
                          admitted values "and", "or", "&", "|"
            formulas -- list of the formulas in the Generalization
        """
        if connective != "and"\
                and connective != "or"\
                and connective != logic.CONN["and"]\
                and connective != logic.CONN["or"]:
            raise Exception("Wrong connective: " + connective)
        if  not isinstance(formulas, list):
            raise Exception("Second argument must be a list")
        self.connective = connective
        self.list = formulas

    
    def __str__(self):
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
        

    def cnf_action(self):
        """Take a clause and return a list of clauses in cnf."""
        if self.connective != "or":
            raise Exception("Wrong type of generalization")

        # basis case
        if not self.has_non_literal():
            return [self]
        
        # recursive case
        (_, position) = self.get_parent_non_literal()
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




if __name__ == "__main__" :
    # Tests


    print "======   Formula   ======"
    formula = Formula("&",
                      Formula("|",Formula("X"), Formula("Y")),
                      Formula("!", Formula("Y"))
                      )
    print "%s \n   is an alpha %r\n   is a beta %r" % (formula,
                                                       formula.is_alpha(),
                                                       formula.is_beta())

    print "====== Complement  ======"
    print formula.complement()

    print "====== Components  ======"
    formula2 = Formula("!", Formula("!", Formula("X")))
    print "%s" % formula2
    print "   %s --- %s" % Formula("!", Formula("!", Formula("X"))).components()
    print "%s" % formula
    print "   %s --- %s" % formula.complement().components()

    print "======     NNF     ======"
    print "%s" % formula.negate()
    print "   %s" % formula.negate().nnf()

    print "====== Generalizations ======"
    disjunction = Generalization("or", [formula])
    print disjunction
    
    disjunction2 = Generalization("and", [formula, disjunction, formula2])
    print disjunction2
    

    print "%s\n   has non-literal? %s" % (disjunction2,
                                          disjunction2.has_non_literal())
    print "   it is", disjunction2.get_non_literal()
    # (pos, ind) = disjunction2.get_parent_non_literal()
    # print pos.list[ind]
    print "   and is in %s at %s" % disjunction2.get_parent_non_literal()


    disjunction3 = Generalization("or",
                                  [Generalization("or",
                                                  [Formula("not", Formula("X")),
                                                   Formula("X")
                                                   ])
                                   ])
    print "%s has non-literal? %s" % (disjunction3,
                                      disjunction3.has_non_literal())
    n_literal = disjunction3.get_non_literal()
    print "   it is", n_literal
    if n_literal != None:
        print "   and is in %s at %s" % disjunction3.get_parent_non_literal()


    disjunction4 = Generalization("or",
                                  [Generalization("or",
                                                  [Formula("and",
                                                           Formula("X"),
                                                           Formula("Y")),
                                                   Formula("X")
                                                   ])
                                   ])
    print "%s has non-literal? %s" % (disjunction4,
                                      disjunction4.has_non_literal())
    print "   it is", disjunction4.get_non_literal()
    print "   and is in %s at %s" % disjunction4.get_parent_non_literal()


    
    print "======     CNF     ======"
    formula1 = Formula("not", Formula("A"))
    print formula1
    print " "*3, formula1.cnf()

    formula2 = Formula("not", Formula("not", Formula("A")))
    print formula2
    print " "*3, formula2.cnf()
    
    formula3 = Formula("or", Formula("A"), Formula("B"))
    print formula3
    print " "*3, formula3.cnf()
    
    formula4 = Formula("and", Formula("A"), Formula("B"))
    print formula4
    print " "*3, formula4.cnf()

    formula5 = Formula("impl", Formula("A"), Formula("B"))
    print formula5
    print " "*3, formula5.cnf()

    print formula
    print " "*3, formula.cnf()

    print formula.negate()
    print " "*3, formula.negate().cnf()


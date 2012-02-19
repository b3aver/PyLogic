#!/usr/bin/python






class Formula:
    #CONN = ["!", "&", "|", "=>", "<=", "!&", "!|", "!=>", "!<=", "=", "!="]
    #CONN = {NOT="!", AND="&", OR="|", IMP="=>", IMPR="<=", NAND="!&", NOR="!|", NIMP="!=>", NIMPR="!<=", EQ="=", NEQ="!="}
    CONN = {"not":"!", "and":"&", "or":"|", "impl":"=>", "implr":"<=", "nand":"!&", "nor":"!|", "nimpl":"!=>", "nimplr":"!<=", "eq":"=", "neq":"!="}
    NOT = "!"
    CONJ = ["&", "!|", "!=>", "!<="]
    DISJ = ["|", "=>", "<=", "!&"]
    TOP = "T"
    BOTTOM = "F"

    def __init__(self, *args):
        if len(args) == 1:
            connective = None
            subformula1 = args[0]
            subformula2 = None
        elif len(args) == 2:
            if args[0] != self.CONN["not"]:
                raise Exception("Wrong connective")
            connective = args[0]
            subformula1 = args[1]
            subformula2 = None
        else:
            if args[0] in self.CONN.viewvalues():
                connective = args[0]
                subformula1 = args[1]
                subformula2 = args[2]
            else:
                raise Exception("Wrong connective")
                
        self.connective = connective
        self.subformula1 = subformula1
        self.subformula2 = subformula2


    def __str__(self):
        if self.connective == None:
            return self.subformula1
        elif self.subformula2 == None:
            return "%s%s" % (self.connective, str(self.subformula1))
        else:
            return "(%s %s %s)" % (str(self.subformula1), \
                                       self.connective, \
                                       str(self.subformula2))
        
        
    def alpha(self):
        if self.connective == None:
            return False
        elif self.connective == self.CONN["not"]:
            return not self.subformula1.alpha()
        elif self.connective in self.CONJ:
            return True
        else:
            return False
        
        
    def beta(self):
        if self.connective == None:
            return False
        elif self.connective == self.CONN["not"]:
            return not self.subformula1.beta()
        elif self.connective in self.DISJ:
            return True
        else:
            return False



    def negate(self):
        return Formula(self.CONN["not"], self)



    def complement(self):
        if self.connective == None:
            return self.negate()
        if self.connective == self.CONN["not"]:
            return self.subformula1
        else:
            return self.negate()



    def components(self):
        if self.connective == None:
            return (self, None)
        if self.connective == self.CONN["not"]:
            if self.subformula1.subformula2 == None:
                """ letteral """
                return (self, None)
            else:
                (comp1, comp2) = self.subformula1.components()
                return (comp1.negate(), comp2.negate())
        else:
            if self.connective == self.CONN["and"]:
                return (self.subformula1, self.subformula2)
            elif self.connective == self.CONN["or"]:
                return (self.subformula1, self.subformula2)
            elif self.connective == self.CONN["impl"]:
                return (self.subformula1.negate(), self.subformula2)
            elif self.connective == self.CONN["implr"]:
                return (self.subformula1, self.subformula2.negate())
            elif self.connective == self.CONN["nand"]:
                return (self.subformula1.negate(), self.subformula2.negate())
            elif self.connective == self.CONN["nor"]:
                return (self.subformula1.negate(), self.subformula2.negate())
            elif self.connective == self.CONN["nimpl"]:
                return (self.subformula1, self.subformula2.negate())
            elif self.connective == self.CONN["nimplr"]:
                return (self.subformula1.negate(), self.subformula2)



    def cnf(self):
        if self.connective == None:
            return self
        if self.connective == self.CONN["not"]:
            subformula = self.subformula1
            if subformula.connective == self.CONN["not"]:
                """ !!Z """
                return subformula.subformula1.cnf()
            elif subformula.connective == None:
                if subformula.subformula1 == self.TOP:
                    """ !top """
                    return Formula(self.BOTTOM)
                elif subformula.subformula1 == self.BOTTOM:
                    """ !bottom """
                    return Formula(self.TOP)
                else:
                    return self
        
        if self.alpha():
            """ alpha """
            (comp1, comp2) = self.components()
            return Formula(self.COMM["and"], comp1.cnf(), comp2.cnf())
        elif self.beta():
            """ beta """
            pass



if __name__ == "__main__" :
    formula = Formula("&", Formula("|", Formula("X"), Formula("Y")), Formula("!", Formula("Y")))
    print "%s \n  is an alpha %r\n  is a beta %r" % (formula, formula.alpha(), formula.beta())
    print formula.complement()


#    (form1, form2) = Formula("!", Formula("!", Formula("X"))).components()
    print "%s --- %s" % Formula("!", Formula("!", Formula("X"))).components()
#    (comp1, comp2) = formula.components()
    print "%s --- %s" % formula.complement().components()

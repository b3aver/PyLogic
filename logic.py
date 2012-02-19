#!/usr/bin/python



import copy




class Logic:
    #CONN = ["!", "&", "|", "=>", "<=", "!&", "!|", "!=>", "!<=", "=", "!="]
    #CONN = {NOT="!", AND="&", OR="|", IMP="=>", IMPR="<=", NAND="!&", NOR="!|", NIMP="!=>", NIMPR="!<=", EQ="=", NEQ="!="}
    CONN = {"not":"!", "and":"&", "or":"|", "impl":"=>", "implr":"<=", "nand":"!&", "nor":"!|", "nimpl":"!=>", "nimplr":"!<=", "eq":"=", "neq":"!="}
    #NOT = "!"
    #CONJ = ["&", "!|", "!=>", "!<="]
    CONJ = ["and", "nor", "nimpl", "nimplr"]
    #DISJ = ["|", "=>", "<=", "!&"]
    DISJ = ["or", "impl", "implr", "nand"]
    TOP = "T"
    BOTTOM = "F"
    DUAL = {"and":"or", "or":"and", "impl":"nimplr", "implr":"nimpl", "nand":"nor", "nor":"nand", "nimpl":"implr", "nimplr":"impl", "eq":"neq", "neq":"eq"}



class Formula(Logic):
    def __init__(self, *args):
        if len(args) == 1:
            connective = None
            subformula1 = args[0]
            subformula2 = None
        elif len(args) == 2:
            if args[0] != "not" and args[0] != self.CONN["not"]:
                raise Exception("Wrong connective: " + args[0])
            connective = "not"
            subformula1 = args[1]
            subformula2 = None
        else:
            if args[0] in self.CONN.viewvalues():
                connective = [item[0] for item in self.CONN.items() if item[1] == args[0]][0]
            elif args[0] in self.CONN.viewkeys():
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
            return "%s%s" % (self.CONN[self.connective], str(self.subformula1))
        else:
            return "(%s %s %s)" % (str(self.subformula1),\
                                       self.CONN[self.connective],\
                                       str(self.subformula2))
        
        
    def alpha(self):
        if self.connective == None:
            return False
        elif self.connective == "not":
            return not self.subformula1.alpha()
        elif self.connective in self.CONJ:
            return True
        else:
            return False
        
        
    def beta(self):
        if self.connective == None:
            return False
        elif self.connective == "not":
            return not self.subformula1.beta()
        elif self.connective in self.DISJ:
            return True
        else:
            return False

        
    def is_literal(self):
        if self.connective == None:
            return True
        elif self.connective == "not" and self.subformula1.connective == None:
            return True
        else:
            return False

            

    def negate(self):
        return Formula("not", self)



    def complement(self):
        if self.connective == None:
            return self.negate()
        if self.connective == "not":
            return self.subformula1
        else:
            return self.negate()



    def components(self):
        if self.connective == None:
            ret = (self, None)
        if self.connective == "not":
            if self.subformula1.subformula2 == None:
                """ letteral """
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
        if self.connective == None:
            return self
        if self.connective == "not":
            subformula = self.subformula1
            if subformula.connective == "not":
                """ !!Z """
                return subformula.subformula1.nnf()
            elif subformula.connective == None:
                """ litteral """
                return self
            else:
                """ dual """
                comp1 = subformula.subformula1.negate()
                comp2 = subformula.subformula2.negate()
                return Formula(self.DUAL[subformula.connective], comp1, comp2).nnf()
        else:
            return Formula(self.connective,\
                               self.subformula1.nnf(),\
                               self.subformula2.nnf())

    def cnf(self):
        pass
        


class Generalization(Logic):

    def __init__(self, connective, formulas):
        if connective != "and" and connective != "or":
            raise Exception("Wrong connective: " + connective)
        self.connective = connective
        self.list = formulas
        # if len(args) == 1:
        #     """ formula """
        #     self.list = [args[0]]
        # else:
        #     self.list = args
        
    
    def __str__(self):
        if self.connective == "and":
            ret = "< "
        elif self.connective == "or":
            ret = "[ "
        first = True
        for el in self.list:
            if not first:
                ret += " , "
            else:
                first = False
            ret += str(el)
        if self.connective == "and":
            ret += " >"
        elif self.connective == "or":
            ret += " ]"
        return ret    



    def has_non_literal(self):
        if len(self.list) == 0:
            raise Exception("Empty list of formulas")        
        for item in self.list:
            if isinstance(item, Formula):
                if not item.is_literal():
                    return True
            elif isinstance(item, Generalization):
                if item.has_non_literal():
                    return True
        return False

               
    def cnf(self):
        if self.connective != "and" or len(self.list) != 1\
                or self.list[0].connective != "or" or len(self.list[0].list) != 1:
            raise Exception("Wrong type of generalization")

        """
        < [ ( X | !X ) , () ] , [ ... ] >
           conj       < ... >
           clause     [ ... ]
           member     ( ... )
           subformula !X
        """
        conj = deepcopy(self)
        for clause in conj.list:
            # if clause.has_non_literal():
            for member in clause.list:
                if not member.is_literal():
                    if member.connective == "not":
                        subformula = member.subformula1
                        if subformula.connective == "not":
                            """ !!Z """
                            member = subformula.subformula1
                        elif subformula.connective == None:
                            if subformula.subformula1 == self.TOP:
                                """ !top """
                                member = Formula(self.BOTTOM)
                            elif subformula.subformula1 == self.BOTTOM:
                                """ !bottom """
                                member = Formula(self.TOP)
                    elif member.connective in self.DISJ:
                        (comp1, comp2) = member.components()
                        index = clause.index(member)
                        clause.insert(index, comp2)
                        clause.insert(index, comp1)
                        clause.remove(member)
                    elif member.connective in self.CONJ:
                        (comp1, comp2) = member.components()
                        
                        





if __name__ == "__main__" :
    
    print "======   Formula   ======"
    formula = Formula("&", Formula("|", Formula("X"), Formula("Y")), Formula("!", Formula("Y")))
    print "%s \n   is an alpha %r\n   is a beta %r" % (formula, formula.alpha(), formula.beta())

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

    print "====== Disjunction ======"
    disjunction = Generalization("or", [formula])
    print disjunction
    
    disjunction2 = Generalization("and", [formula, disjunction, formula2])
    print disjunction2
    

    print "%s has non-literal? %s" % (disjunction2, disjunction2.has_non_literal())
 


    disjunction3 = Generalization("or", [Generalization("or", [Formula("not", Formula("X")), Formula("X")])])
    print "%s has non-literal? %s" % (disjunction3, disjunction3.has_non_literal())


#!/usr/bin/python

'''Definition of the elements of the First Order Logic:
   Variable, Constant, Relation, Function, Formula'''

import copy
import sys
import re
sys.path.append("..")
import logic


class Variable():
    '''Variable'''
    def __init__(self, var):
        self.var = var
        

    def __str__(self):
        return self.var

        

class Constant():
    '''Constant'''
    def __init__(self, const):
        self.const = const


    def __str__(self):
        return self.const
        


class Relation():
    '''Relation : Terms -> {true, false}'''
    def __init__(self, *args):
        if len(args) < 1:
            raise Exception("Wrong number of parameters.")
        self.symbol = args[0]
        args = list(args)
        args.pop(0)
        if len(args) == 1 and isinstance(args[0], list):
            self.parameters = args[0]
        else:
            self.parameters = args


    def __str__(self):
        #string = self.symbol + '('
        parameters = ''
        for par in self.parameters:
            parameters += par.__str__() + ', '            
        if parameters != '':
            parameters = parameters[:-2]
        
        return '%s(%s)' % (self.symbol, parameters)



class Function():
    '''Function : Terms -> Terms'''
    def __init__(self, *args):
        if len(args) < 1:
            raise Exception("Wrong number of parameters.")
        self.name = args[0]
        args = list(args)
        args.pop(0)
        if len(args) == 1 and isinstance(args[0], list):
            self.parameters = args[0]
        else:
            self.parameters = args


    def __str__(self):
        #string = self.symbol + '('
        parameters = ''
        for par in self.parameters:
            parameters += par.__str__() + ', '            
        if parameters != '':
            parameters = parameters[:-2]
        
        return '%s(%s)' % (self.name, parameters)



class Formula():
    '''Represents a first order logic formula.'''

    def __init__(self, *args):
        """ Constructor of a Formula.

        Could take several arguments, depends of the type of Formula:
            1 argument:
                atomic formula
                  (i.e. a relation or costant top "T", or bottom "F")
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
        quantifier = None
        variable = None
        connective = None
        subformula1 = None
        subformula2 = None
        if len(args) == 1:
            # atomic formula
            pattern_letter = re.compile(logic.re_LETTER)
            if not (isinstance(args[0], Relation) \
                        or args[0] == logic.TOP \
                        or args[0] == logic.BOTTOM
                        or pattern_letter.match(args[0])
                    ):
                raise Exception("Wrong atomic formula.")
            subformula1 = args[0]
        elif len(args) == 2:
            # not
            if args[0] != "not" and args[0] != logic.CONN["not"]:
                raise Exception("Wrong connective: " + args[0])
            if not isinstance(args[1], Formula):
                raise Exception("Wrong type of formula.")
            connective = "not"
            subformula1 = args[1]
        elif len(args) == 3:
            if args[0] in logic.QUANT:
                # quantifier
                if not isinstance(args[1], Variable):
                    raise Exception("Wrong type of variable.")
                if not isinstance(args[2], Formula):
                    raise Exception("Wrong type of formula.")
                quantifier = args[0]
                variable = args[1]
                subformula1 = args[2]
            else:
                # binary connective
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
                if not isinstance(args[1], Formula) \
                        or not isinstance(args[2], Formula):
                    raise Exception("Wrong type of formula.")
                subformula1 = args[1]
                subformula2 = args[2]
        else:
            raise Exception("Wrong number of arguments.")

        self.quantifier = quantifier
        self.variable = variable
        self.connective = connective
        self.subformula1 = subformula1
        self.subformula2 = subformula2



    def __str__(self):
        if self.quantifier != None:
            return '(%s %s)%s' % (logic.QUANT[self.quantifier],
                                  self.variable,
                                  self.subformula1)
        if self.connective == None:
            return self.subformula1.__str__()
        elif self.subformula2 == None:
            return "%s%s" % (logic.CONN[self.connective], str(self.subformula1))
        else:
            return "(%s %s %s)" % (str(self.subformula1), \
                                       logic.CONN[self.connective], \
                                       str(self.subformula2))




if __name__ == '__main__':
    
    print Variable('x')
    print Constant('c')
    print Relation('A', Variable('y'), Variable('y'))
    print Relation('A', [Variable('y'), Variable('z')])
    print Function('f', Constant('c'), Constant('d'), Variable('x'))
    print Formula('&', Formula(Relation('A', 'B')), Formula(Relation('C', 'B')))
    print Formula('exists',
                  Variable('x'),
                  Formula(Relation('A', Variable('y'), Variable('x'))))
    print Formula('exists',
                  Variable('x'),
                  Formula('all',
                          Variable('y'),
                          Formula(Relation('A', Variable('y'), Variable('x')))))

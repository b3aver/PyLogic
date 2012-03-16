#!/usr/bin/python

# Modified from ply yacc example

import ply.yacc as yacc



# if __name__ == "__main__":
#     import sys
#     sys.path.append("..")


# Get the token map from the lexer.  This is required.
from lexer import tokens
from logic import Formula


CONN = {'&': 'and', '<-': 'implr', '|': 'or', '->': 'impl', '<->': 'eq'}

# {'!': 'not', '&': 'and', '!<=': 'nimplr', '!=>': 'nimpl', '!=': 'neq', '<=': 'implr', '|': 'or', '!&': 'nand', '=>': 'impl', '=': 'eq', '!|': 'nor'}

'''Unique parsing
   formula : LETTER
           | NOT formula
           | LPAREN formula CONNECTIVE formula RPAREN'''
def p_formula_letter(p):
    '''formula : LETTER'''
    # p[0] = p[1]
    p[0] = Formula(p[1])

def p_formula_not(p):
    '''formula : NOT formula'''
    # p[0] = "%s %s" % (p[1], p[2])
    p[0] = Formula("not", p[1])

def p_formula_connective(p):
    ''' formula : LPAREN formula CONNECTIVE formula RPAREN'''
    # p[0] = "%s %s %s %s %s" % (p[1], p[2], p[3], p[4], p[5])
    p[0] = Formula(CONN[p[3]], p[2], p[4])

'''
def p_formula_connective_nopar(p):
    'formula : formula CONNECTIVE formula'
    p[0] = "%s %s %s" % (p[1], p[2], p[3])
'''

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"


# Build the parser
parser = yacc.yacc()


if __name__ == "__main__":
    while True:
        try:
            s = raw_input('calc > ')
        except EOFError:
            break
        if not s :
            continue
        result = parser.parse(s)
        print result

# pylint: disable-msg=C0103

#
# Lexer
#
#
import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'LETTER',
    'NOT',
    'CONNECTIVE',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_LETTER = r'[A-Z]'
t_NOT   = r'-'
t_CONNECTIVE = r'\||\&|<->|->|<-'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character", t.value[0])
    t.lexer.skip(1)


# Build the lexer
propositional_lexer = lex.lex()



#
# Parser
#
#

import ply.yacc as yacc
from .propositional_logic import Formula
import sys
from pylogic import logic



def p_begin(p):
    '''begin : formula
             | formula_no_par'''
    p[0] = p[1]

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
    p[0] = Formula("not", p[2])

def p_formula_connective(p):
    ''' formula : LPAREN formula CONNECTIVE formula RPAREN'''
    # p[0] = "%s %s %s %s %s" % (p[1], p[2], p[3], p[4], p[5])
    if p[3] == '<->':
        f1 = Formula(logic.CONN['impl'], p[2], p[4])
        f2 = Formula(logic.CONN['impl'], p[4], p[2])
        p[0] = Formula(logic.CONN['and'], f1, f2)
    else:
        p[0] = Formula(logic.CONN_ST[p[3]], p[2], p[4])

def p_formula_connective_nopar(p):
    'formula_no_par : formula CONNECTIVE formula'
    if p[2] == '<->':
        f1 = Formula(logic.CONN['impl'], p[1], p[3])
        f2 = Formula(logic.CONN['impl'], p[3], p[1])
        p[0] = Formula(logic.CONN['and'], f1, f2)
    else:
        p[0] = Formula(logic.CONN_ST[p[2]], p[1], p[3])
    # p[0] = "%s %s %s" % (p[1], p[2], p[3])



# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")



# Build the parser
propositional_parser = yacc.yacc()


if __name__ == "__main__":

    # Test the lexer
    data = '''(A & B) -> A'''
    
    # Give the lexer some input
    propositional_lexer.input(data)
    
    # Tokenize
    while True:
        tok = propositional_lexer.token()
        if not tok:
            break      # No more input
        print(tok)


    # Test the parser
    while True:
        try:
            s = raw_input('calc > ')
        except EOFError:
            break
        if not s :
            continue
        result = propositional_parser.parse(s)
        print(result)

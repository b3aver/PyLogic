#!/usr/bin/python

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
t_CONNECTIVE = r'\||\&|->|<-'
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
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()



#
# Parser
#
#

import ply.yacc as yacc
from propositional_logic import Formula
import logic



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
    p[0] = Formula(logic.CONN_ST[p[3]], p[2], p[4])

def p_formula_connective_nopar(p):
    'formula_no_par : formula CONNECTIVE formula'
    p[0] = Formula(logic.CONN_ST[p[2]], p[1], p[3])
    # p[0] = "%s %s %s" % (p[1], p[2], p[3])



# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"



# Build the parser
parser = yacc.yacc()


if __name__ == "__main__":

    # Test the lexer
    data = '''(A & B) -> A'''
    
    # Give the lexer some input
    lexer.input(data)
    
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print tok


    # Test the parser
    while True:
        try:
            s = raw_input('calc > ')
        except EOFError:
            break
        if not s :
            continue
        result = parser.parse(s)
        print result

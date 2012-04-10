#!/usr/bin/python
# pylint: disable-msg=C0103

#
# Lexer
#
#
import ply.lex as lex
import re


# List of token names.   This is always required
tokens = (
    'LETTER',
    'NOT',
    'CONNECTIVE',
    'LPAREN',
    'RPAREN',
    'EXIST',
    'ALL',
    'VARIABLE',
    'CONSTANT',
    'RELATION',
    'FUNCTION',
)


re_LETTER = r'[A-Z]+'
re_VARIABLE = r'[abd-z][0-9]*'
re_CONSTANT = r'c[0-9]*'


def next_char_is(t, char, skip_blank=True):
    '''Check if the next character in input is equal to the given character.'''
    lexdata = t.lexer.lexdata
    lexpos = t.lexer.lexpos
    if len(lexdata) <= lexpos:
        return False

    nextchar = lexdata[lexpos]
    if skip_blank:
        while nextchar in [' ', '\t']:
            t.lexer.skip(1)
            nextchar = lexdata[t.lexer.lexpos]
    return nextchar == char


#
# Regular expresion rules for tokens
#
def t_RELATION(t):
    r'[A-Z]([A-Za-z]|[0-9]|[_-])*'
    if not next_char_is(t, '('):
        pattern_letter = re.compile(re_LETTER)
        if pattern_letter.match(t.value):
            t.type = 'LETTER'
    return t

    
def t_FUNCTION(t):
    r'[a-z]([A-Za-z]|[0-9]|[_-])*'
    if not next_char_is(t, '('):
        pattern_variable = re.compile(re_VARIABLE)
        pattern_constant = re.compile(re_CONSTANT)
        if pattern_variable.match(t.value):
            t.type = 'VARIABLE'
        elif pattern_constant.match(t.value):
            t.type = 'CONSTANT'
    return t


#
# Regular expression rules for simple tokens
#
#t_LETTER = re_LETTER
t_LETTER = r'[A-Z]+'
t_NOT   = r'-'
t_CONNECTIVE = r'\||\&|->|<-'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
#t_VARIABLE = re_VARIABLE
t_VARIABLE = r'[abd-z][0-9]*'
#t_CONSTANT = re_CONSTANT
t_CONSTANT = r'c[0-9]*'





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
from first_order_logic import Formula
import sys
sys.path.append("..")
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


    # # Test the parser
    # while True:
    #     try:
    #         s = raw_input('calc > ')
    #     except EOFError:
    #         break
    #     if not s :
    #         continue
    #     result = parser.parse(s)
    #     print result

# pylint: disable-msg=C0103

#
# Lexer
#
#
import ply.lex as lex
import re


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
            if len(lexdata) <= t.lexer.lexpos:
                return False
            nextchar = lexdata[t.lexer.lexpos]
    return nextchar == char



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
    'COMMA',
)


t_EXIST = r'exist'
t_ALL = r'all'


re_LETTER = r'[A-Z]+'
re_VARIABLE = r'[abd-z][0-9]*'
re_CONSTANT = r'c[0-9]*'



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
t_CONNECTIVE = r'\||\&|<->|->|<-'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
#t_VARIABLE = re_VARIABLE
t_VARIABLE = r'[abd-z][0-9]*'
#t_CONSTANT = re_CONSTANT
t_CONSTANT = r'c[0-9]*'
t_COMMA = r','





# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
first_order_lexer = lex.lex()



#
# Parser
#
#


import ply.yacc as yacc
from .first_order_logic import *
import sys
from pylogic import logic



''' Grammar
Unique parsing
   begin : formula
         | formula_no_par

   formula_no_par : formula CONNECTIVE formula

   formula : LETTER
           | NOT formula
           | LPAREN formula CONNECTIVE formula RPAREN
           | LPAREN EXIST variable RPAREN formula
           | LPAREN ALL variable RPAREN formula
           | relation
           
   relation : RELATION LPAREN termslist RPAREN

   termslist : term
             | term COMMA termslist

   term : variable
        | constant
        | function

   variable : VARIABLE

   constant : CONSTANT

   function : FUNCTION LPAREN termslist RPAREN   
'''
def p_begin(p):
    '''begin : formula
             | formula_no_par'''
    p[0] = p[1]


def p_formula_no_par(p):
    '''formula_no_par : formula CONNECTIVE formula'''
    if p[2] == '<->':
        f1 = Formula(logic.CONN['impl'], p[1], p[3])
        f2 = Formula(logic.CONN['impl'], p[3], p[1])
        p[0] = Formula(logic.CONN['and'], f1, f2)
    else:
        p[0] = Formula(logic.CONN_ST[p[2]], p[1], p[3])
    # p[0] = "%s %s %s" % (p[1], p[2], p[3])


def p_formula_letter(p):
    '''formula : LETTER'''
    # p[0] = p[1]
    p[0] = Formula(p[1])

def p_formula_not(p):
    '''formula : NOT formula'''
    # p[0] = "%s %s" % (p[1], p[2])
    p[0] = Formula("not", p[2])

def p_formula_connective(p):
    '''formula : LPAREN formula CONNECTIVE formula RPAREN'''
    # p[0] = "%s %s %s %s %s" % (p[1], p[2], p[3], p[4], p[5])
    if p[3] == '<->':
        f1 = Formula(logic.CONN['impl'], p[2], p[4])
        f2 = Formula(logic.CONN['impl'], p[4], p[2])
        p[0] = Formula(logic.CONN['and'], f1, f2)
    else:
        p[0] = Formula(logic.CONN_ST[p[3]], p[2], p[4])

def p_formula_quantifier(p):
    '''formula : LPAREN EXIST variable RPAREN formula
               | LPAREN ALL variable RPAREN formula'''
    p[0] = Formula(p[2], p[3], p[5])

def p_formula_relation(p):
    '''formula : relation'''
    p[0] = p[1]


def p_relation(p):
    '''relation : RELATION LPAREN termslist RPAREN'''
    p[0] = Relation(p[1], p[3])


def p_termslist(p):
    '''termslist : term
                 | term COMMA termslist'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if isinstance(p[1], list):
            p[0] = p[1]
        else:
            p[0] = [p[1]]
        p[0].append(p[3])


def p_term(p):
    '''term : variable
            | constant
            | function'''
    p[0] = p[1]
   
 
def p_variable(p):
    '''variable : VARIABLE'''
    p[0] = Variable(p[1])


def p_constant(p):
    '''constant : CONSTANT'''
    p[0] = Constant(p[1])


def p_function(p):
    '''function : FUNCTION LPAREN termslist RPAREN'''
    p[0] = Function(p[1], p[3])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")



# Build the parser
first_order_parser = yacc.yacc()


if __name__ == "__main__":

    # Test the lexer
    data = '''(A & B) -> A'''
    data = '(A(x) -> c(x,y) <-> o(x,y))'
    data = '(F(c(x,y))) <-> (A(x) & F(y))'
    
    # Give the lexer some input
    first_order_lexer.input(data)

    print("Scanning the input string: \"%s\"" % data)
    # Tokenize
    while True:
        tok = first_order_lexer.token()
        if not tok:
            break      # No more input
        print(tok)


    print("Parsing of the input string: \"%s\"" % data)
    result = first_order_parser.parse(data)
    print(result)



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

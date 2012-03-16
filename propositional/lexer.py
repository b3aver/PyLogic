#!/usr/bin/python

# Modified from ply lex example

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



if __name__ == "__main__":
    # Test it out
    data = '''(A & B) -> A'''
    
    # Give the lexer some input
    lexer.input(data)
    
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print tok
        

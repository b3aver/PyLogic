#!/usr/bin/python



"""Basic class with fundamental constants."""

# connectives strings to symbols
CONN = {"not":"!", "and":"&", "or":"|", "impl":"=>", "implr":"<=", "nand":"!&",
        "nor":"!|", "nimpl":"!=>", "nimplr":"!<=", "eq":"=", "neq":"!="}
# connectives symbols to strings
CONN_ST = {'!': 'not', '&': 'and', '!<=': 'nimplr', '!=>': 'nimpl', '!=': 'neq',
           '<=': 'implr', '|': 'or', '!&': 'nand', '=>': 'impl', '=': 'eq',
           '!|': 'nor',
           # prover9 version
           '&': 'and', '<-': 'implr', '|': 'or', '->': 'impl', '<->': 'eq'}

CONJ = ["and", "nor", "nimpl", "nimplr"]
DISJ = ["or", "impl", "implr", "nand"]
TOP = "T"
BOTTOM = "F"
DUAL = {"and":"or", "or":"and", "impl":"nimplr", "implr":"nimpl", "nand":"nor",
        "nor":"nand", "nimpl":"implr", "nimplr":"impl", "eq":"neq", "neq":"eq"}




import propositional.propositional_logic

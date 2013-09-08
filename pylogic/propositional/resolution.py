import copy
from pylogic.propositional.propositional_logic import Formula, Generalization
from pylogic import logic


def preliminary_steps(clauses):
    manage_tops(clauses)
    manage_complementary(clauses)
    manage_bottoms(clauses)
    manage_copies(clauses)

def manage_tops(clauses):
    """Remove the clauses containg the top."""
    removable = []
    for c in range(len(clauses)):
        clause = clauses[c]
        for formula in clause.list:
            if formula == Formula("T"):
                removable.append(c)
                break
    for i in reversed(removable):
        clauses.pop(i)

def manage_complementary(clauses):
    """Remove the clauses containing two complementary formulas."""
    removable = []
    for c in range(len(clauses)):
        clause = clauses[c]
        found = False
        f = 0
        while not found and f < len(clause.list):
            formula1 = clause.list[f]
            for f2 in range(f+1, len(clause.list)):
                formula2 = clause.list[f2]
                if formula1 == formula2.complement():
                    removable.append(c)
                    found = True
                    break
            f = f + 1
    for i in reversed(removable):
        clauses.pop(i)

def manage_bottoms(clauses):
    """Remove the bottoms from every clause."""
    for clause in clauses:
        clause.remove_every(Formula("F"))

def manage_copies(clauses):
    """Remove from every clause repetions of inner formulas."""
    for clause in clauses:
        f = 0
        while f < len(clause.list)-1:
            formula = clause.list[f]
            f2 = f+1
            while f2 < len(clause.list):
                formula2 = clause.list[f2]
                if formula == formula2:
                    clause.list.pop(f2)
                else:
                    f2 = f2+1
            f = f+1


def is_closed(expansion):
    """Given a list of clauses, return True if it contains an empty clause,
    False otherwise"""
    for clause in expansion:
        if len(clause.list) == 0:
            return True
        # else ignore it
    return False


def resolution_rule(clause1, clause2, formula):
    """Apply the resolution rule to the given clauses and formula."""
    new_clause = copy.deepcopy(clause1)
    other = copy.deepcopy(clause2)
    new_clause.remove_every(formula)
    other.remove_every(formula.complement())
    new_clause.list.extend(other.list)
    return new_clause


def apply_resolution_rule(clause1, clause2):
    """Apply the resolution rule to the given clauses"""
    for f in range(len(clause1.list)):
        formula = clause1.list[f]
        # check if exists a complement of formula
        for f2 in range(len(clause2.list)):
            formula2 = clause2.list[f2]
            if formula == formula2.complement():
                new_clause = resolution_rule(clause1, clause2, formula)
                clauses = [new_clause]
                manage_complementary(clauses)
                manage_copies(clauses)
                if clauses == []:
                    return None
                else:
                    return new_clause


def is_tautology(formula):
    """Test if the given formula is a tautology,
    namely a theorem of the resolution system.
    A formula is a theorem of the resolution system if it has a closed
    resolution expansion for its negation."""
    print(formula.__str__())
    negation = formula.negate()
    cnf = negation.cnf()
    print(cnf)
    expansion = cnf.list
    preliminary_steps(expansion)
    picker = ClausePicker(expansion)
    closed = is_closed(expansion)
    while not closed and not picker.is_empty():
        clauses = picker.pick()
        new_clause = apply_resolution_rule(clauses[0], clauses[1])
        if new_clause != None:
            picker.update(expansion, new_clause)
            expansion.append(new_clause)
        disjs = ""
        for g in expansion:
            disjs = disjs + " " + g[1].__str__()
        print(disjs)
        closed = is_closed(expansion)
    return is_closed(expansion)



class ClausePicker():
    def __init__(self, expansion):
        pass

    def pick(self):
        return None

    def add_clause(self, expansion, clause):
        pass

    def is_empty(self):
        pass

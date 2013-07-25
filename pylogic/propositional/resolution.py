from pylogic.propositional.propositional_logic import Formula, Generalization
from pylogic import logic


def is_closed(expansion):
    """Given a list of clauses, return True if it contains an empty clause,
    False otherwise"""
    for clause in expansion:
        if len(clause.list) == 0:
            return True
        # else ignore it
    return False


def expand(expansion):
    """Apply the resolution rule to the given expansion.
    Returns True if the resolution rule is applied, False otherwise."""
    # for each formula
    for g in range(len(expansion)):
        gen = expansion[g]
        for f in range(len(gen.list)):
            formula = gen.list[f]
            # check if exists a complement of formula
            # in the rest of the expansion
            for ng in range(g+1, len(expansion)):
                temp_gen = expansion[ng]
                for nf in range(len(temp_gen.list)):
                    temp_formula = temp_gen.list[nf]
                    if formula == temp_formula.complement():
                        expansion.pop(ng)
                        gen.remove_every(formula)
                        temp_gen.remove_every(temp_formula)
                        gen.list.extend(temp_gen.list)
                        return True
                    # else ignore it
    return False


def is_tautology(formula):
    """Test if the given formula is a tautology,
    namely a theorem of the resolution system.
    A formula is a theorem of the resolution system if it has a closed
    resolution expansion for its negation."""
    negation = formula.negate()
    cnf = negation.cnf()
    expansion = cnf.list
    enough = False
    while not is_closed(expansion) and not enough:
        applied = expand(expansion)
        enough = not applied
    return is_closed(expansion)

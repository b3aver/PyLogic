import copy
from pylogic.propositional.propositional_logic import Formula, Generalization
from pylogic import logic


def is_closed(expansion):
    """Given a list of clauses, return True if it contains an empty clause,
    False otherwise"""
    for el in expansion:
        clause = el[1]
        if len(clause.list) == 0:
            return True
        # else ignore it
    return False


def expand(expansion):
    """Apply the resolution rule to the given expansion.
    Returns True if the resolution rule is applied, False otherwise."""
    # for each formula
    for g in range(len(expansion)):
        if expansion[g][0]:
            continue
        gen = expansion[g][1]
        for f in range(len(gen.list)):
            formula = gen.list[f]
            # check if exists a complement of formula
            # in the rest of the expansion
            for ng in range(g+1, len(expansion)):
                temp_gen = expansion[ng][1]
                for nf in range(len(temp_gen.list)):
                    temp_formula = temp_gen.list[nf]
                    if formula == temp_formula.complement():
                        gen = copy.deepcopy(gen)
                        gen2 = copy.deepcopy(temp_gen)
                        gen.remove_every(formula)
                        gen2.remove_every(temp_formula)
                        gen.list.extend(gen2.list)
                        expansion.append([False, gen])
                        expansion[g][0] = True
                        return True
                    # else ignore it
    return False


def is_tautology(formula):
    """Test if the given formula is a tautology,
    namely a theorem of the resolution system.
    A formula is a theorem of the resolution system if it has a closed
    resolution expansion for its negation."""
    print(formula.__str__())
    negation = formula.negate()
    cnf = negation.cnf()
    print(cnf)
    expansion = [[False, disj] for disj in cnf.list]
    enough = False
    while not is_closed(expansion) and not enough:
        applied = expand(expansion)
        enough = not applied
        disjs = ""
        for g in expansion:
            disjs = disjs + " " + g[1].__str__()
        print(disjs)
    return is_closed(expansion)

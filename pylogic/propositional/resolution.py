import copy
from pylogic.propositional.propositional_logic import Formula, Generalization
from pylogic import logic


def preliminary_steps(clauses):
    manage_tops(clauses)
    manage_complementary(clauses)
    manage_bottoms(clauses)
    manage_copies(clauses)
    manage_duplicated_clauses(clauses)

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
        while not found and f < len(clause):
            formula1 = clause.list[f]
            for f2 in range(f+1, len(clause)):
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
        while f < len(clause)-1:
            formula = clause.list[f]
            f2 = f+1
            while f2 < len(clause):
                formula2 = clause.list[f2]
                if formula == formula2:
                    clause.list.pop(f2)
                else:
                    f2 = f2+1
            f = f+1

def manage_duplicated_clauses(clauses):
    """Remove duplicated clauses, independently of the order of the formulas."""
    # old_clauses = copy.deepcopy(clauses)
    # clauses = list()
    # for clause in old_clauses:
    #     if is_new(clauses, clause):
    #         clauses.append(clause)
    removable = []
    for i in range(len(clauses)):
        if i not in removable:
            clause = clauses[i]
            for j in range(i + 1, len(clauses)):
                if j not in removable:
                    clause2 = clauses[j]
                    if clause.equivalent(clause2):
                        removable.append(j)
    for i in reversed(removable):
        clauses.pop(i)


def is_closed(expansion):
    """Given a list of clauses, return True if it contains an empty clause,
    False otherwise"""
    for clause in expansion:
        if len(clause) == 0:
            return True
        # else ignore it
    return False


def is_new(expansion, clause):
    """Check if the given clause is already present in the given expansion."""
    found = False
    i = 0
    while not found and i < len(expansion):
        cl = expansion[i]
        i = i + 1
        if cl.equivalent(clause):
            return False
    return True


def resolution_rule(clause1, clause2, formula):
    """Apply the resolution rule to the given clauses and formula."""
    new_clause = copy.deepcopy(clause1)
    other = copy.deepcopy(clause2)
    new_clause.remove_every(formula)
    other.remove_every(formula.complement())
    new_clause.list.extend(other.list)
    return new_clause


def apply_resolution_rule(clause1, clause2):
    """Apply the resolution rule to the given clauses.

    After that apply the preliminary steps on the resulting clause.
    It assumes that in clause1 and clause2 are already applied
    the preliminary steps, that is in them there aren't tops or bottoms;
    so here are not applied manage_tops or manage_bottoms.

    Moreover the resolution rule is applied only on the first formula
    of which is found the complementary in the other clause.
    This because if the resolution rule could be applied, for instance,
    two times it means that in them there are two distinct couples
    of complementary formulas, this means that after every application
    of the resolution rule in the resulting clauses there will be
    a couple of complementary fomulas and so with the preliminary steps
    the clauses will be removed."""
    for f in range(len(clause1)):
        formula = clause1.list[f]
        # check if exists a complement of formula
        for f2 in range(len(clause2)):
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
    return None


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
    if is_closed(expansion):
        return True
    while not picker.is_empty():
        cl = picker.pick()
        new_clause = apply_resolution_rule(expansion[cl[0]], expansion[cl[1]])
        if new_clause is not None:
            if len(new_clause) == 0:
                return True
            if is_new(expansion, new_clause):
                expansion.append(new_clause)
                picker.add_clause(new_clause)
                print(" ".join([cl.__str__() for cl in expansion]))
    return False



class ClausePicker():
    def __init__(self, expansion):
        self.sizes = [len(clause) for clause in expansion]
        # dict containing the couples of clauses
        # (precisely their indexes in the original expansion list)
        # it is indexed with the sum of the two clauses' sizes
        self.buckets = dict()
        for i in range(len(self.sizes)-1):
            size_i = self.sizes[i]
            for j in range(i+1, len(self.sizes)):
                size = size_i + self.sizes[j]
                if size in self.buckets:
                    self.buckets[size].append((i,j))
                else:
                    self.buckets[size] = [(i,j)]


    def pick(self):
        if self.is_empty():
            raise Exception("No more choices")
        bucket = min(self.buckets.keys())
        couple = self.buckets[bucket].pop(0)
        if len(self.buckets[bucket]) == 0:
            del self.buckets[bucket]
        return couple


    def add_clause(self, clause):
        i = len(self.sizes) # index in the expansion list
        # insert in self.sizes
        size_i = len(clause)
        self.sizes.append(size_i)
        # insert in self.buckets
        for j in range(len(self.sizes)-1):
                size = size_i + self.sizes[j]
                if size in self.buckets:
                    self.buckets[size].append((i,j))
                else:
                    self.buckets[size] = [(i,j)]


    def is_empty(self):
        return len(self.buckets) == 0

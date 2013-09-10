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
    """Apply the resolution rule to the given clauses"""
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



class Expansion():
    def __init__(self, clauses):
        self.clauses = clauses
        self.clause_picker = ClausePicker(clauses)

    def __getitem__(self, key):
        return self.clauses[key]

    def __str__(self):
        disjs = ""
        first = True
        for cl in expansion:
            if first:
                disjs = cl.__str__()
                first = False
            else:
                disjs = disjs + " " + cl.__str__()
        return disjs

    def insert(self, clause):
        if self.is_new(clause):
            self.clauses.append(clause)
            self.clause_picker.add_clause(clause)

    def pick(self):
        (i, j) = self.clause_picker.pick()
        return (self.clauses[i], self.clauses[j])

    def is_new(self, clause):
        found = False
        i = 0
        while not found and i < len(self.clauses):
            cl = self.clauses[i]
            i = i + 1
            if cl.equivalent(clause):
                return False
        return True



class ClausePicker():
    def __init__(self, expansion):
        # list with a couple (<size>, <index in espansion>) for each clause
        self.db = [(len(clause), i) for i, clause in enumerate(expansion)]
        self.db.sort()
        # list where every entry is a couple of clauses indexes
        # on which apply the resolution rule
        self.couples = [(cl1, cl2)
                        for (size, cl1) in self.db
                        for (size2, cl2) in self.db if cl2 != cl1]


    def pick(self):
        if self.is_empty():
            raise Exception("No more choices")
        return self.couples.pop(0)


    def add_clause(self, clause):
        ex_index = len(self.db) # index in the expansion list
        db_entry = (len(clause), ex_index)
        # insert in self.db
        self.db.append(db_entry)
        self.db.sort()
        db_ind = self.db.index(db_entry) # index in the list self.db
        # insert in self.couples
        new_c = [(ex_index, cl2) for (size2, cl2) in self.db if cl2 != ex_index]
        if db_ind + 1 == len(self.db):
            # append in the end of self.couples
            self.couples.extend(new_c)
        else:
            # insert at a specific index of self.couples
            (succ_size, succ_ex_ind) = self.db[db_ind+1]
            # find the index of the successive in self.couples
            found = False
            succ_ind = 0
            while not found and succ_ind < len(self.couples):
                (ind1, ind2) = self.couples[succ_ind]
                if (ind1 == succ_ex_ind):
                    found = True
                    succ_ind = succ_ind - 1
                succ_ind = succ_ind + 1
            pos = succ_ind
            self.couples = self.couples[:pos] + new_c + self.couples[pos:]


    def is_empty(self):
        return len(self.couples) == 0

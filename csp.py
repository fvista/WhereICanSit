from typing import Dict, Set, Tuple, List, Optional
import numpy as np

Person = str
Table = int
Num_constraint = int


class CSP:

    def __init__(self, variables: List[Person], fight_list: List[Tuple[Person, Person]],
                 family: List[List[Person]], num_tables: int = 3, dim_table: int = 6):

        self.people: Person = variables
        self.fights = fight_list
        self.tables = [i for i in range(1, num_tables + 1)]
        self.domains: Dict[Person, Set[Table]] = {}
        self.assignment: Dict[Person, Table] = {}
        self.capacity = dim_table
        self.family: Dict[Person, List[Person]] = {}

        for variable in self.people:
            self.domains[variable] = {n for n in range(1, num_tables + 1)}

        for fam in family:
            for p in fam:
                fam_cp = fam.copy()
                fam_cp.remove(p)
                self.family[p] = fam_cp  # dizionario key= persona e value= parenti

    def __repr__(self):

        list_person = []
        for table in self.tables:
            list_person.append('Tavolo {}: {}'.format(table, ', '.join(self.person_at_table(table))))

        return '\n'.join(list_person)

    def isConsistent(self, person: Person, table: Table) -> bool:

        if self.table_isFull(table):
            return False

        family_table = self.family_table(person)
        if family_table is not None and table != family_table:
            return False

        if self.fight_at_table(person, table):
            return False

        return True

    def fight_person_with(self, person: Person) -> List[Person]:
        """ Crea una lista di persone con cui la persona passata alla funzione ha litigato"""
        list_person = []
        for p1, p2 in self.fights:
            if person == p1:
                list_person.append(p2)
            if person == p2:
                list_person.append(p1)

        return list_person

    def fight_at_table(self, person: Person, table: Table) -> bool:
        """ Restituisce True se nel tavolo è presente la persona con cui person ha litigato"""
        list_person_table = self.person_at_table(table)
        list_fight_with = self.fight_person_with(person)

        for p in list_person_table:
            if p in list_fight_with:
                return True

        return False

    def family_table(self, person: Person) -> Optional[Table]:

        # get serve perchè la chiave nel dizionare può non esserci,
        # [] per restituire lista vuota nel caso la persone non c'è
        for par in self.family.get(person, []):
            table = self.assignment.get(par)  # restituisce il tavolo in cui è seduto un parente
            if table is not None:
                return table

        return None

    def table_isFull(self, table: Table) -> bool:
        """ Restituisce True se il tavolo è pieno, altrimenti False"""
        return self.count_at_table(table) == self.capacity

    def person_at_table(self, table: Table) -> List[Person]:
        """ Restituisce la lista di persone sedute ad un tavolo """
        return [p for p, t in self.assignment.items() if t == table]

    def count_at_table(self, table: Table):
        """ Conta il numero di persone sedute ad un tavolo """
        return len(self.person_at_table(table))

    def isSolved(self) -> bool:
        """ Serve per vedere se tutte le persone sono state assegnate ad un tavolo"""
        for person in self.people:
            if person not in self.assignment:
                return False
        return True

    # This is used for minimum remaining value
    def n_conflict(self, person: Person):
        cnt = 0
        for val in self.domains[person]:
            if not self.isConsistent(person, val):
                cnt += 1

        return cnt

    # This is used for the least constraining value
    def n_global_conflict(self, person: Person):
        num_global_conflict = []
        for val in self.domains[person]:
            if self.isConsistent(person, val):
                cnt = 0
                self.assignment[person] = val
                for person1 in self.people:
                    if person1 not in self.assignment:
                        for val1 in self.domains[person1]:
                            if self.isConsistent(person1, val1):
                                cnt += 1
                del self.assignment[person]

                num_global_conflict.append((val, cnt))

        return num_global_conflict

    # This used for the forward checking
    def illegal_values(self, person: Person) -> List[Table]:
        return [v for v in self.domains[person] if not self.isConsistent(person, v)]

    def assign(self, person: Person, val: Table):
        self.assignment[person] = val
        removed: Dict[Person, List[Table]] = {person: self.domains[person]}

        for person in self.people:
            if person not in self.assignment:
                illegal = self.illegal_values(person)
                removed[person] = illegal

                self.domains[person].difference_update(illegal)

        return removed

    def unassign(self, person: Person, removal: Dict[Person, List[Table]]):
        del self.assignment[person]

        for person, values in removal.items():
            # print(person)
            self.domains[person].update(values)

    # This is used for the arc consistency
    def neighbours(self, xi: Person, xj: Person):
        list_neighbours = []
        for val in self.domains[xi]:
            self.assignment[xi] = val
            for variable in self.people:
                if variable not in self.assignment and variable != xj:
                    for value in self.domains[variable]:
                        if not self.isConsistent(variable, value):
                            list_neighbours.append(variable)

            del self.assignment[xi]

        return np.unique(list_neighbours)

    def assign_var(self, person: Person, val: Table, person1: Person) -> bool:
        self.assignment[person] = val

        for val in self.domains[person1]:
            if self.isConsistent(person1, val):
                del self.assignment[person]
                return True

        del self.assignment[person]

        return False

from typing import Tuple, List, TypeVar, Dict, Optional
from operator import itemgetter

Person = str
Table = int
Num_constraint = int


class Problem:

    def __init__(self, variables: List[Person], domains: Dict[Person, List[Table]], fight_list: List[Tuple[Person, Person]], family: List[List[Person]],
                 num_tables: int = 3, dim_table: int = 6):

        self.people = variables  # lista di tutte le persone
        self.fights = fight_list
        self.num_tables = num_tables
        self.capacity = dim_table
        self.family: Dict[Person, List[Person]] = {}
        self.tables = [i for i in range(1, num_tables + 1)]
        self.list_table: Dict[Person, Table] = {}

        for fam in family:
            for p in fam:
                fam_cp = fam.copy()
                fam_cp.remove(p)
                self.family[p] = fam_cp  # dizionario key= persona e value= parenti

        self.constraint_for_person: List[Person] = self.num_person_constraint()

        self.dictionary_for_FC: Dict[Person, List[Table]] = {}

        # list_tables = [1, 2, 3]
        for p in self.people:
            self.dictionary_for_FC[p] = [1, 2, 3]

    def num_person_constraint(self) -> List[Person]:
        """ Restituisce una lista ordinata in base ai vincoli:
            +1: se la persona appartiene alla famiglia
            +1: per ogni persona con cui uno ha litigato """

        dictionary: Dict[Person, Num_constraint] = {}
        num_fight_with: int = 0

        for p in self.people:

            dictionary[p] = 0

            if self.family.get(p):
                dictionary[p] += 1

            num_fight_with = len(self.fight_person_with(p))
            if num_fight_with != 0:
                dictionary[p] += num_fight_with

        tuple_ordered = sorted(dictionary.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        list_ordered = [v for v, n in tuple_ordered]

        return list_ordered

    def __repr__(self):

        list_person = []
        for table in self.tables:
            list_person.append('Tavolo {}: {}'.format(table, ', '.join(self.person_at_table(table))))

        # print(list_person)
        # return 'Tavolo 1: {} \nTavolo 2: {} \nTavolo 3: {}'.format(list_person[0], list_person[1], list_person[2])
        return '\n'.join(list_person)

    # def unassigned(self):
    #     return [v for v in self.people if v not in self.list_table]

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
            table = self.list_table.get(par)  # restituisce il tavolo in cui è seduto un parente
            if table is not None:
                return table

        return None

    def table_isFull(self, table: Table) -> bool:
        """ Restituisce True se il tavolo è pieno, altrimenti False"""
        return self.count_at_table(table) == self.capacity

    def person_at_table(self, table: Table) -> List[Person]:
        """ Restituisce la lista di persone sedute ad un tavolo """
        return [p for p, t in self.list_table.items() if t == table]

    def count_at_table(self, table: Table):
        """ Conta il numero di persone sedute ad un tavolo """
        return len(self.person_at_table(table))

    def isSolved(self) -> bool:
        """ Serve per vedere se tutte le persone sono state assegnate ad un tavolo"""
        for person in self.people:
            if person not in self.list_table:
                return False
        return True

    def num_legal_values(self):

        dictionary = {}
        for p in self.people:
            if p not in self.list_table:
                dictionary[p] = self.num_legal_values_for_person(p)

        tuple_ordered = sorted(dictionary.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        list_ordered = [v for v, n in tuple_ordered]

        return list_ordered

    def num_legal_values_for_person(self, person: Person) -> int:

        num = 0
        for table in self.tables:
            if not self.isConsistent(person, table):
                num += 1

        return num

    def list_constraining_value(self, person: Person, table: Table):

        count = 0
        self.list_table[person] = table

        num_broke_constraint = 0
        for p in self.people:
            if p not in self.list_table:
                if not self.isConsistent(person, table):
                    num_broke_constraint += 1

        count += num_broke_constraint

        return count

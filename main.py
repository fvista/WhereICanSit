import sys
from search import *
from csp import *
from problem import *


def main():

    guest = ['Antonella', 'Domenico', 'Raffella', 'Tommaso', 'Vincenzo', 'Azzurra',
             'Cristiano', 'Francesca', 'Luigi', 'Giovanni', 'Marcella', 'Daniela', 'Leonardo', 'Nunzio', 'Silvia']

    family1 = ['Antonella', 'Domenico', 'Raffella', 'Tommaso', 'Vincenzo']
    family2 = ['Azzurra', 'Cristiano', 'Francesca', 'Luigi']

    fight = [('Giovanni', 'Marcella'), ('Marcella', 'Daniela'), ('Luigi', 'Leonardo')]

    family = [family1, family2]

    room = CSP(guest, fight, family, 3, 6)

    print(backtracking_search(room, selected_unassigned_value=minimum_remaining_value,
                              ordered_value=least_constraining_value, inference=AC3))

    return 0


if __name__ == '__main__':
    sys.exit(main())
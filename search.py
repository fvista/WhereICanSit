
Person = str
Table = int


# For selection variable
def first_unassigned_variable(csp):
    return [v for v in csp.people if v not in csp.assignment][0]


def minimum_remaining_value(csp) -> Person:
    """choosing the variable with the fewest “legal” values"""
    return min((v for v in csp.people if v not in csp.assignment), key=lambda kv: len(csp.domains[kv]))


# ordering value
def least_constraining_value(csp, person: Person):
    """Given a variable, choose the least constraining value:"""
    list = csp.n_global_conflict(person)
    list_ordered = sorted(list, key=lambda kv: kv[1], reverse=True)
    return [v for v, z in list_ordered]


def unordered_values(csp, person: Person):
    return csp.domains[person]


# For inference
def no_inference(csp) -> bool:
    return True


def forward_checking(csp) -> bool:
    for variable in csp.people:
        if variable not in csp.assignment:
            if not csp.domains[variable]:
                return False
    return True


def AC3(csp) -> bool:
    queue = set()

    for var1 in csp.people:
        if var1 not in csp.assignment:
            for var2 in csp.people:
                if var2 not in csp.assignment:
                    if var1 != var2:
                        queue.add((var1, var2))

    while queue:
        xi, xj = queue.pop()
        if revise(csp, xi, xj):
            if csp.domains[xi]:
                return False
            for xk in csp.neighbours(xi, xj):
                queue.add((xk,xi))
            # for xz, xk in queue:
            #     if xz == xi and xk != xj:
            #         queue.add((xk, xi))

    return True


def revise(csp, xi, xj):
    revised = False

    for val in csp.domains[xi]:
        if not csp.assign_var(xi, val, xj):
            csp.domains[xi] = csp.domains[xi] - {val}
            revised = True

    return revised


# Algorithm for search
def backtracking_search(csp, selected_unassigned_value=first_unassigned_variable, ordered_value=unordered_values,
                        inference=no_inference):

    # assignment is complete if every variable is assigned
    if len(csp.assignment) == len(csp.people):
        return csp

    person = selected_unassigned_value(csp)
    for value in ordered_value(csp, person):

        removed = csp.assign(person, value)
        if inference(csp):
            result = backtracking_search(csp)
            # if we didn't find the result, we will end up backtracking
            if result is not None:
                return result

        csp.unassign(person, removed)

    return None


# def deegre_heuristic(problem):
#     return [v for v in problem.constraint_for_person if v not in problem.list_table][0]



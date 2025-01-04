#!/usr/bin/env python3


from ortools.sat.python import cp_model


def solve_cover_set(input_sets):
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    # Create a binary variable for each set in the input
    set_vars = {}
    for set_name in input_sets:
        set_vars[set_name] = model.NewBoolVar(set_name)

    # Create constraints to cover all elements with the selected sets
    for element in set.union(*input_sets.values()):
        model.AddBoolOr(
            [
                set_vars[set_name]
                for set_name, element_set in input_sets.items()
                if element in element_set
            ]
        )

    # Create the objective to minimize the number of selected sets
    objective = sum(set_vars.values())
    model.Minimize(objective)

    # Solve the model
    status = solver.Solve(model)

    # Get the selected sets
    selected_sets = [
        set_name for set_name, var in set_vars.items() if solver.Value(var) == 1
    ]

    return selected_sets, status


def solve_cover_set_all_optima(input_sets):
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    # Create a binary variable for each set in the input
    set_vars = {set_name: model.NewBoolVar(set_name) for set_name in input_sets}

    # Create constraints to cover all elements with the selected sets
    all_elements = set.union(*input_sets.values())
    for element in all_elements:
        model.AddBoolOr(
            [
                set_vars[set_name]
                for set_name, element_set in input_sets.items()
                if element in element_set
            ]
        )

    # Create the objective to minimize the number of selected sets
    objective = sum(set_vars.values())
    model.Minimize(objective)

    # Collect all optimal solutions
    optimal_solutions = []
    early_stop = 0
    status = solver.Solve(model)
    while early_stop == 0 and status == cp_model.OPTIMAL:
        current_solution = [
            set_name for set_name, var in set_vars.items() if solver.Value(var) == 1
        ]
        optimal_solutions.append(current_solution)

        # Add a constraint to exclude the current solution to find new ones
        model.Add(
            sum(set_vars[set_name] for set_name in current_solution)
            <= len(current_solution) - 1
        )
        status = solver.Solve(model)
        if status != cp_model.OPTIMAL:
            break
        next_solution = [
            set_name for set_name, var in set_vars.items() if solver.Value(var) == 1
        ]

        # Check for early stop
        early_stop += len(current_solution) - len(next_solution)

    return optimal_solutions, status

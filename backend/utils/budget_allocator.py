from pulp import LpProblem, LpMaximize, LpVariable, lpSum

def allocate_budget(projects, budget):
    # Filter projects and convert to DataFrame if necessary
    problem = LpProblem("ESG_Optimization", LpMaximize)
    allocations = LpVariable.dicts("Allocation", range(len(projects)), 0, 1, cat='Binary')

    # Objective
    problem += lpSum([
        project['Predicted ESG Score'] * (1 - project['Risk Factor']) * allocations[i]
        for i, project in enumerate(projects)
    ])

    # Budget constraint
    problem += lpSum([
        project['Project Cost'] * allocations[i]
        for i, project in enumerate(projects)
    ]) <= budget

    problem.solve()

    # Return allocated projects
    allocated = [projects[i] for i in range(len(projects)) if allocations[i].varValue == 1]
    return allocated

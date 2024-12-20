import math
import time
from pysat.solvers import Glucose4


def generate_sat_variables(s1, s2, grey_edges, black_edges, num_vertices):
    # Declaring variables and assigning them unique integer values for the SAT Solver
    grey_edges = set(grey_edges)
    black_edges = set(black_edges)
    all_edges = grey_edges.union(black_edges)

    var_dict = {}
    counter = 1

    # Assign integers to x_e variables
    # For each edge e, x_e represents if it will be chosen
    for e in all_edges:
        var_dict[('x', e)] = counter
        counter += 1

    for u in s1:
        curr_edges = [(u_dash, v_dash) for (u_dash, v_dash) in black_edges if u == u_dash]
        curr_len = len(curr_edges)
        # print(f'{curr_len=}')
        num_bits = math.ceil(math.log2(curr_len))
        for j in range(1, num_bits + 1):
            var_dict[('m', u, j)] = counter
            counter += 1

    for v in s2:
        curr_edges = [(u_dash, v_dash) for (u_dash, v_dash) in black_edges if v == v_dash]
        curr_len = len(curr_edges)
        num_bits = math.ceil(math.log2(curr_len))
        for j in range(1, num_bits + 1):
            var_dict[('m', v, j)] = counter
            counter += 1

    # Assign integers to w_i^t variables
    # For each y_i, there are i variables
    for i in range(1, num_vertices + 1):
        for t in range(1, i + 1):
            var_dict[('w', i, t)] = counter
            counter += 1

        num_bits = math.ceil(math.log2(i))
        for j in range(1, num_bits + 1):
            var_dict[('b', i, j)] = counter
            counter += 1

    # Assign integers to z_i variables
    for i in range(1, num_vertices + 1):
        var_dict[('z', i)] = counter
        counter += 1

    # Assign integers to T(k,d) variables
    for i in range(1, num_vertices + 2):
        for d in range(0, i):
            var_dict[('T', i, d)] = counter
            counter += 1

    # Assigned integers to Q(i,d-1) variables
    for i in range(1, num_vertices + 2):
        for d in range(1, i + 1):
            var_dict[('Q', i, d - 1)] = counter
            counter += 1

    return var_dict


def sat_solver_mcd(var_dict, grey_edges, all_black_edges, homologous_edges, S1, S2, num_vertices, log):
    if num_vertices == 0:
        log.append('Empty graph after simplification.')
        return log
    grey_edges = set(grey_edges)
    all_black_edges = set(all_black_edges)
    all_edges = grey_edges.union(all_black_edges)

    # Create a new SAT solver instance
    solver = Glucose4()

    curr_clause_count = 0
    start_clause_1 = time.time()
    print('Adding Clause 1')
    # Clause 1: All grey edges should be in the final decomposition
    for e in grey_edges:
        solver.add_clause([var_dict[('x', e)]])
        curr_clause_count += 1
    end_clause_1 = time.time()
    print('Time taken for clause 1', end_clause_1 - start_clause_1)
    log.append(f'Time taken for clause 1: {str(end_clause_1 - start_clause_1)}')
    print(f'Clause 1 Count: {curr_clause_count}')
    log.append(f'Clause 1 Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_2 = time.time()
    print('Adding Clause 2')
    # Clause 2: Final decomposition should be consistent
    for pair in homologous_edges:
        solver.add_clause([-var_dict[('x', pair[0])], var_dict[('x', pair[1])]])
        solver.add_clause([-var_dict[('x', pair[1])], var_dict[('x', pair[0])]])
        curr_clause_count += 2
    end_clause_2 = time.time()
    print('Time taken for clause 2', end_clause_2 - start_clause_2)
    log.append(f'Time taken for clause 2: {str(end_clause_2 - start_clause_2)}')
    print(f'Clause 2 Count: {curr_clause_count}')
    log.append(f'Clause 2 Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_3_i = time.time()
    print('Adding Clause 3i')
    # Clause 3i: Exactly one adjacent black edge should be chosen for each vertex in S1
    for u in S1:
        # At least one adjacent black edge should be chosen
        clause = [var_dict[('x', (u, v))] for v in S2 if (u, v) in all_black_edges]
        solver.add_clause(clause)
        curr_clause_count += 1

        curr_edges = [(u_dash, v_dash) for (u_dash, v_dash) in all_black_edges if u == u_dash]
        num_bits = math.ceil(math.log2(len(curr_edges)))
        for idx1, val in enumerate(curr_edges, start=1):
            for idx2 in range(1, num_bits + 1):
                bit_to_check = ((idx1 - 1) & (1 << (idx2 - 1))) != 0
                if bit_to_check:
                    solver.add_clause([-var_dict[('x', val)], var_dict[('m', u, idx2)]])
                else:
                    solver.add_clause([-var_dict[('x', val)], -var_dict[('m', u, idx2)]])
                curr_clause_count += 1

    end_clause_3_i = time.time()
    print('Time taken for clause 3i', end_clause_3_i - start_clause_3_i)
    log.append(f'Time taken for clause 3i: {str(end_clause_3_i - start_clause_3_i)}')
    print(f'Clause 3i Count: {curr_clause_count}')
    log.append(f'Clause 3i Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_3_ii = time.time()
    print('Adding Clause 3ii')
    # Clause 3ii: Exactly one adjacent black edge should be chosen for each vertex in S2
    for v in S2:
        # At least one adjacent black edge should be chosen
        clause = [var_dict[('x', (u, v))] for u in S1 if (u, v) in all_black_edges]
        solver.add_clause(clause)
        curr_clause_count += 1

        curr_edges = [(u_dash, v_dash) for (u_dash, v_dash) in all_black_edges if v == v_dash]
        num_bits = math.ceil(math.log2(len(curr_edges)))
        for idx1, val in enumerate(curr_edges, start=1):
            for idx2 in range(1, num_bits + 1):
                bit_to_check = ((idx1 - 1) & (1 << (idx2 - 1))) != 0
                if bit_to_check:
                    solver.add_clause([-var_dict[('x', val)], var_dict[('m', v, idx2)]])
                else:
                    solver.add_clause([-var_dict[('x', val)], -var_dict[('m', v, idx2)]])
                curr_clause_count += 1

    end_clause_3_ii = time.time()
    print('Time taken for clause 3ii', end_clause_3_ii - start_clause_3_ii)
    log.append(f'Time taken for clause 3ii: {str(end_clause_3_ii - start_clause_3_ii)}')
    print(f'Clause 3ii Count: {curr_clause_count}')
    log.append(f'Clause 3ii Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_4 = time.time()
    print('Adding Clause 4')
    # Clause 4: Setting distinct positive bound i for each y_i
    for i in range(1, num_vertices + 1):
        # At least one w_t^i should be true for each i
        clause = [var_dict[('w', i, t)] for t in range(1, i + 1)]
        solver.add_clause(clause)
        curr_clause_count += 1

        num_bits = math.ceil(math.log2(i))

        # At most one w_t^i should be true for each i
        for j in range(1, i + 1):
            for k in range(1, num_bits + 1):
                bit_to_check = ((j - 1) & (1 << (k - 1))) != 0

                if bit_to_check:
                    solver.add_clause([-var_dict[('w', i, j)], var_dict[('b', i, k)]])
                else:
                    solver.add_clause([-var_dict[('w', i, j)], -var_dict[('b', i, k)]])
                curr_clause_count += 1

    end_clause_4 = time.time()
    print('Time taken for clause 4', end_clause_4 - start_clause_4)
    log.append(f'Time taken for clause 4: {str(end_clause_4 - start_clause_4)}')
    print(f'Clause 4 Count: {curr_clause_count}')
    log.append(f'Clause 4 Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_5 = time.time()
    print('Adding Clause 5i')
    # Clause 5i: Each vertex in the same cycle must have the same label
    for e in all_edges:
        v_i, v_j = e
        for t in range(1, min(v_i, v_j) + 1):

            solver.add_clause([-var_dict[('x', e)], var_dict[('w', v_i, t)], -var_dict[('w', v_j, t)]])
            solver.add_clause([-var_dict[('x', e)], -var_dict[('w', v_i, t)], var_dict[('w', v_j, t)]])

            curr_clause_count += 2

    end_clause_5 = time.time()
    print('Time taken for clause 5i', end_clause_5 - start_clause_5)
    log.append(f'Time taken for clause 5: {str(end_clause_5 - start_clause_5)}')
    print(f'Clause 5 Count: {curr_clause_count}')
    log.append(f'Clause 5 Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_6 = time.time()
    print('Adding Clause 6')
    # Clause 6: z_i must indicate whether y_i is equal to its upper bound i
    for i in range(1, num_vertices + 1):
        # ¬z_i ∨ w_i^i
        solver.add_clause([-var_dict[('z', i)], var_dict[('w', i, i)]])
        # solver.add_clause([var_dict[('z', i)], -var_dict[('w', i, i)]])
        # curr_clause_count += 2
        curr_clause_count += 1

    end_clause_6 = time.time()
    print('Time taken for clause 6', end_clause_6 - start_clause_6)
    log.append(f'Time taken for clause 6: {str(end_clause_6 - start_clause_6)}')
    print(f'Clause 6 Count: {curr_clause_count}')
    log.append(f'Clause 6 Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_7 = time.time()
    print('Adding Clause 7')
    # Clause 7: This clause forces the variables representing at least 0 z_i to be True
    for i in range(1, num_vertices + 2):
        solver.add_clause([var_dict[('T', i, 0)]])
        curr_clause_count += 1

    end_clause_7 = time.time()
    print('Time taken for clause 7', end_clause_7 - start_clause_7)
    log.append(f'Time taken for clause 7: {str(end_clause_7 - start_clause_7)}')
    print(f'Clause 7 Count: {curr_clause_count}')
    log.append(f'Clause 7 Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_8 = time.time()
    print('Adding Clause 8')
    # Clause 8: This clause ensures that if at least d variables, z_j, for j < i are set True,
    # then at least d variables, z_{i+1}, are set true for j < i+1
    for i in range(1, num_vertices + 1):
        for d in range(0, i):
            solver.add_clause([-var_dict[('T', i, d)], var_dict[('T', i + 1, d)]])
            curr_clause_count += 1

    end_clause_8 = time.time()
    print('Time taken for clause 8', end_clause_8 - start_clause_8)
    log.append(f'Time taken for clause 8: {str(end_clause_8 - start_clause_8)}')
    print(f'Clause 8 Count: {curr_clause_count}')
    log.append(f'Clause 8 Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_9 = time.time()
    print('Adding Clause 9')
    # Clause 9: This clause ensures that if at least d variables are set True till z_i and z_i is also set True,
    # that implies that d+1 variables are set true till z_{i+1}
    for i in range(1, num_vertices + 1):
        for d in range(0, i):
            solver.add_clause([-var_dict[('T', i, d)], -var_dict[('z', i)], var_dict[('T', i + 1, d + 1)]])
            curr_clause_count += 1

    end_clause_9 = time.time()
    print('Time taken for clause 9', end_clause_9 - start_clause_9)
    log.append(f'Time taken for clause 9: {str(end_clause_9 - start_clause_9)}')
    print(f'Clause 9 Count: {curr_clause_count}')
    log.append(f'Clause 9 Count: {curr_clause_count}')

    curr_clause_count = 0
    start_clause_10 = time.time()
    print('Adding Clause 10')
    # Clause 10: This clause keeps T(|V|+1,d) from being set true even when ∑(z_i) < d
    for i in range(1, num_vertices + 1):
        for d in range(1, i):
            # P' ≡ T(i, d-1) ∨ ¬Q(i, d-1)
            solver.add_clause([var_dict[('T', i, d - 1)], -var_dict[('Q', i, d - 1)]])

            # Q' ≡ z_i ∨ ¬Q(i, d-1)
            solver.add_clause([var_dict[('z', i)], -var_dict[('Q', i, d - 1)]])

            # R' ≡ ¬T(i,d - 1) ∨ ¬z_i ∨ Q(i, d-1)
            solver.add_clause([-var_dict[('T', i, d - 1)], -var_dict[('z', i)], var_dict[('Q', i, d - 1)]])

            # (T(i,d) ∨ Q(i, d-1) ∨ ¬T(i+1, d))
            solver.add_clause([var_dict[('T', i, d)], var_dict[('Q', i, d - 1)], -var_dict[('T', i + 1, d)]])

            curr_clause_count += 4

        # P' ≡ T(i, d-1) ∨ ¬Q(i, d-1)
        solver.add_clause([var_dict[('T', i, i - 1)], -var_dict[('Q', i, i - 1)]])

        # Q' ≡ z_i ∨ ¬Q(i, d-1)
        solver.add_clause([var_dict[('z', i)], -var_dict[('Q', i, i - 1)]])

        # R' ≡ ¬T(i,d - 1) ∨ ¬z_i ∨ Q(i, d-1)
        solver.add_clause([-var_dict[('T', i, i - 1)], -var_dict[('z', i)], var_dict[('Q', i, i - 1)]])

        # (T(i,d) ∨ Q(i, d-1) ∨ ¬T(i+1, d))
        solver.add_clause([var_dict[('Q', i, i - 1)], -var_dict[('T', i + 1, i)]])

        curr_clause_count += 4

    end_clause_10 = time.time()
    print('Time taken for clause 10', end_clause_10 - start_clause_10)
    log.append(f'Time taken for clause 10: {str(end_clause_10 - start_clause_10)}')
    print(f'Clause 10 Count: {curr_clause_count}')
    log.append(f'Clause 10 Count: {curr_clause_count}')

    m = 1
    time_for_cycles = 0
    while True:
        # Clause for testing number of true z_i
        solver.add_clause([var_dict[('T', num_vertices + 1, m)]])

        start = time.time()
        # Solve the SAT problem
        status = solver.solve()
        end = time.time()
        time_for_cycles += (end - start)
        print(f'Time for {m} cycles.')
        log.append(f'Time for {m} cycles: {str(end - start)}')
        print(end - start)

        # Print the solution status
        if status:
            print("SAT")
            log.append('SAT')
            print(f'{m} cycles found')
            log.append(f'{m} cycles found')
            m += 1
            # return True
            # Get the satisfying assignment
            # model = solver.get_model()
            #
            # # Print the values of x_e variables for grey and black edges
            # print("Edge variables:")
            # for e in grey_edges + all_black_edges:
            #     if var_dict[('x', e)] in model:
            #         print(f"x_{e} = True")
            #
            # # Print the values of z_i variables
            # print("\nz_i variables:")
            # for i in range(1, num_vertices + 1):
            #     if var_dict[('z', i)] in model:
            #         print(f"z_{i} = True")
        else:
            print('unsat')
            log.append('unsat')
            print(f'Optimal Cycles: {m - 1}')
            log.append(f'Optimal Cycles: {str(m - 1)}')
            print(f'Total time for cycles: {time_for_cycles}')
            log.append(f'Total time for cycles: {str(time_for_cycles)}')
            return log


def sat_solver_pipeline(s1_sat, s2_sat, grey_sat, black_sat, he_sat, num_vertices, log):
    var_dict_for_sat = generate_sat_variables(s1_sat, s2_sat, grey_sat, black_sat, num_vertices)
    log = sat_solver_mcd(var_dict_for_sat, grey_sat, black_sat, he_sat, s1_sat, s2_sat, num_vertices, log)
    return log

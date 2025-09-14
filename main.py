import sys
import time

from reading_simplified_params.make_graph_from_params import create_final_parameters_from_file
from sat_solver.sat_solver_mcd import sat_solver_pipeline


def main():
    # ------ TIME LOGGING STARTS -------
    start = time.time()

    # ----- INPUT -----

    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_folder>")
        sys.exit(1)

    folder_path = sys.argv[1]

    # -------- SIMPLIFICATION --------

    s1_sat, s2_sat, g1_grey_sat, g2_grey_sat, black_sat, he_sat, cycles_removed, num_vertices = create_final_parameters_from_file(
        f'{folder_path}/vertices.txt',
        f'{folder_path}/gr.txt',
        f'{folder_path}/partners.txt',
        f'{folder_path}/gene_list.txt',
        f'{folder_path}/simplified_cycles.txt'
    )

    # # ------ SAT SOLVER ------
    log = []
    log = sat_solver_pipeline(s1_sat, s2_sat, g1_grey_sat + g2_grey_sat, black_sat, he_sat, num_vertices, log)
    print(f'Simplified Cycles: {cycles_removed}')

    # # # ------ TIME LOGGING ENDS ------

    end = time.time()
    print(f'Total Time Taken: {str(end - start)}')


if __name__ == "__main__":
    main()

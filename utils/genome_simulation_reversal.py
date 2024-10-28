import math
import random
from copy import deepcopy
import os


def create_original_genome(no_of_genes, no_of_chromosomes, no_of_gene_families, linear_perc):
    genes_per_chromosome = no_of_genes // no_of_chromosomes
    extra_genes = no_of_genes % no_of_chromosomes

    chromosome_type_dict = {}

    linear_perc = linear_perc / 100
    no_of_linear_chromosomes = math.floor(linear_perc * no_of_chromosomes)

    for i in range(1, no_of_linear_chromosomes + 1):
        chromosome_type_dict[i] = 1

    for i in range(no_of_linear_chromosomes + 1, no_of_chromosomes + 1):
        chromosome_type_dict[i] = 2

    genes_in_genome = []
    gene_count_left = no_of_genes

    for i in range(1, no_of_gene_families + 1):
        genes_in_genome.append(i)
        gene_count_left -= 1

    while gene_count_left > 0:
        genes_in_genome.append(random.randint(1, no_of_gene_families))
        gene_count_left -= 1

    final_genome = []

    ptr = 0

    for i in range(1, no_of_chromosomes + 1):
        curr_no_of_genes = genes_per_chromosome
        if extra_genes > 0:
            curr_no_of_genes += 1
            extra_genes -= 1
        curr_gene_list = [gene for gene in genes_in_genome[ptr: ptr + curr_no_of_genes]]
        final_genome.append(curr_gene_list)
        ptr += curr_no_of_genes

    return final_genome, chromosome_type_dict


def convert_genome_to_file(genome, chromosome_type_dict, output_file_name):
    ctr = 1
    txt = ''
    for i in range(0, len(genome)):
        for j in range(0, len(genome[i])):
            curr_line = f'GENE_{ctr} {genome[i][j]} {i+1} {chromosome_type_dict[i+1]}\n'
            txt += curr_line
            ctr += 1
    with open(output_file_name, 'w') as f:
        f.write(txt)


def perform_chromosome_reversal(input_chromosome, cut_1_idx, cut_2_idx):

    chromosome = deepcopy(input_chromosome)

    reversed_chromosome = chromosome[:]
    reversed_chromosome[cut_1_idx:cut_2_idx] = [-x for x in reversed_chromosome[cut_1_idx:cut_2_idx]][::-1]

    return reversed_chromosome


def perform_chromosome_fission(input_chromosome, cut_1_idx, cut_2_idx):

    chromosome = deepcopy(input_chromosome)

    cut = [i for i in chromosome[cut_1_idx:cut_2_idx]]
    del chromosome[cut_1_idx:cut_2_idx]

    return chromosome, cut


# Define the function for performing a single DCJ operation
def perform_dcj_on_single_chromsome(input_genome, input_chromosome_type_dict):

    genome = deepcopy(input_genome)
    chromosome_type_dict = deepcopy(input_chromosome_type_dict)

    no_of_chromosomes = len(genome)
    random_chromosome_idx = random.randint(1, no_of_chromosomes)
    random_chromosome = genome[random_chromosome_idx - 1]
    while len(random_chromosome) < 3:
        random_chromosome_idx = random.randint(1, no_of_chromosomes)
        random_chromosome = genome[random_chromosome_idx - 1]

    # Generate two random cuts in the genome
    cut_1 = random.randint(1, len(random_chromosome) - 1)
    cut_2 = random.randint(1, len(random_chromosome) - 1)

    while cut_2 == cut_1:
        cut_2 = random.randint(0, len(random_chromosome))

    if cut_1 > cut_2:
        cut_1, cut_2 = cut_2, cut_1

    j = 1

    if j == 1:  # Perform reversal
        reversed_chromosome = perform_chromosome_reversal(random_chromosome, cut_1, cut_2)
        genome[random_chromosome_idx - 1] = reversed_chromosome

        return genome, chromosome_type_dict

    elif j == 2:  # Perform fission
        split_chromosome, cut = perform_chromosome_fission(random_chromosome, cut_1, cut_2)
        genome[random_chromosome_idx - 1] = split_chromosome
        genome.append(cut)
        chromosome_type_dict[no_of_chromosomes + 1] = 1

        return genome, chromosome_type_dict


def perform_dcj_on_chromsome_pair(input_genome, input_chromosome_type_dict):
    genome = deepcopy(input_genome)
    chromosome_type_dict = deepcopy(input_chromosome_type_dict)

    no_of_chromosomes = len(genome)
    random_chromosome_1_idx = random.randint(1, no_of_chromosomes)
    random_chromosome_2_idx = random.randint(1, no_of_chromosomes)
    while random_chromosome_2_idx == random_chromosome_1_idx:
        random_chromosome_2_idx = random.randint(1, no_of_chromosomes)

    random_chromosome_1 = genome[random_chromosome_1_idx - 1]
    random_chromosome_2 = genome[random_chromosome_2_idx - 1]

    j = random.randint(1, 2)

    if j == 1:
        genome[random_chromosome_1_idx - 1].extend(genome[random_chromosome_2_idx - 1])
        genome[random_chromosome_2_idx - 1] = []

        return genome, chromosome_type_dict

    if j == 2:
        cut_1 = random.randint(0, len(random_chromosome_1))
        cut_2 = random.randint(0, len(random_chromosome_2))

        c_2_s_2 = random_chromosome_2[cut_2:]
        c_1_s_2 = random_chromosome_1[cut_1:]

        genome[random_chromosome_1_idx - 1][cut_1:] = c_2_s_2
        genome[random_chromosome_2_idx - 1][cut_2:] = c_1_s_2

        return genome, chromosome_type_dict


def perform_dcj_operation_on_genome(input_genome, input_chromosome_type_dict):

    genome = deepcopy(input_genome)
    chromosome_type_dict = deepcopy(input_chromosome_type_dict)

    j = 1

    if j == 1:
        curr_g, curr_type_dict = perform_dcj_on_single_chromsome(genome, chromosome_type_dict)

    else:
        curr_g, curr_type_dict = perform_dcj_on_chromsome_pair(genome, chromosome_type_dict)

    return curr_g, curr_type_dict


def perform_n_random_dcj_operations_on_genome(input_genome, input_chromosome_type_dict, n):
    genome = deepcopy(input_genome)
    chromosome_type_dict = deepcopy(input_chromosome_type_dict)

    ctr = 0

    while ctr < n:

        genome, chromosome_type_dict = perform_dcj_operation_on_genome(genome, chromosome_type_dict)

        ctr += 1

    return genome, chromosome_type_dict


def simulate_pair_from_original(og_genome, og_chromosome_type_dict, n):

    og_genome_copy = deepcopy(og_genome)
    og_chromosome_type_dict_copy = deepcopy(og_chromosome_type_dict)

    g1, d1 = perform_n_random_dcj_operations_on_genome(og_genome_copy, og_chromosome_type_dict_copy, n)
    g2, d2 = perform_n_random_dcj_operations_on_genome(og_genome, og_chromosome_type_dict, n)

    return g1, d1, g2, d2


def simulate_genomes(n_g, n_c, n_gf, n_dcj):
    original_simulated_genome, original_dict = create_original_genome(n_g, n_c, n_gf, 100)
    t_og = deepcopy(original_simulated_genome)
    t_dict = deepcopy(original_dict)

    g1_curr, d1_curr, g2_curr, d2_curr = simulate_pair_from_original(original_simulated_genome, original_dict, n_dcj)

    folder_path = f'../reversal_test_files/sim_{n_g}_{n_gf}_{n_dcj}'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    convert_genome_to_file(t_og, t_dict, output_file_name=f'../reversal_test_files/sim_{n_g}_{n_gf}_{n_dcj}/sim_{n_g}_{n_gf}_{n_dcj}_og.dcj')
    convert_genome_to_file(g1_curr, d1_curr, output_file_name=f'../reversal_test_files/sim_{n_g}_{n_gf}_{n_dcj}/sim_{n_g}_{n_gf}_{n_dcj}_1.dcj')
    convert_genome_to_file(g2_curr, d2_curr, output_file_name=f'../reversal_test_files/sim_{n_g}_{n_gf}_{n_dcj}/sim_{n_g}_{n_gf}_{n_dcj}_2.dcj')


def simulate_multiple_genomes(n_g, n_c, n_gf):
    original_simulated_genome, original_dict = create_original_genome(n_g, n_c, n_gf, 100)
    t_og = deepcopy(original_simulated_genome)
    t_dict = deepcopy(original_dict)
    ops = [350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500]

    for op in ops:
        n_dcj = op
        g1_curr, d1_curr, g2_curr, d2_curr = simulate_pair_from_original(original_simulated_genome, original_dict, n_dcj)

        folder_path = f'../reversal_test_files/sim_{n_g}_{n_gf}_{n_dcj}'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        convert_genome_to_file(t_og, t_dict, output_file_name=f'../reversal_test_files/sim_{n_g}_{n_gf}_{n_dcj}/sim_{n_g}_{n_gf}_{n_dcj}_og.dcj')
        convert_genome_to_file(g1_curr, d1_curr, output_file_name=f'../reversal_test_files/sim_{n_g}_{n_gf}_{n_dcj}/sim_{n_g}_{n_gf}_{n_dcj}_1.dcj')
        convert_genome_to_file(g2_curr, d2_curr, output_file_name=f'../reversal_test_files/sim_{n_g}_{n_gf}_{n_dcj}/sim_{n_g}_{n_gf}_{n_dcj}_2.dcj')


# genome_test_file_params = [
#     [20, 5, 8, 5],
#     [20, 5, 8, 10],
#     [20, 5, 18, 5],
#     [20, 5, 18, 10],
#     [50, 5, 20, 10],
#     [50, 5, 20, 20],
#     [50, 5, 45, 10],
#     [50, 5, 45, 20],
#     [100, 10, 50, 20],
#     [100, 10, 50, 40],
#     [100, 10, 90, 20],
#     [100, 10, 90, 40],
#     [200, 20, 90, 40],
#     [200, 20, 40, 80],
#     [200, 20, 170, 140],
#     [200, 20, 170, 80]
# ]

simulate_multiple_genomes(1500, 10, 1000)

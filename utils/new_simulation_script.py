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


def perform_dcj_on_single_chromsome(input_genome, input_chromosome_type_dict):
    genome = deepcopy(input_genome)
    chromosome_type_dict = deepcopy(input_chromosome_type_dict)

    no_of_chromosomes = len(genome)
    random_chromosome_idx = random.randint(1, no_of_chromosomes)
    random_chromosome = genome[random_chromosome_idx - 1]
    while len(random_chromosome) < 3:
        random_chromosome_idx = random.randint(1, no_of_chromosomes)
        random_chromosome = genome[random_chromosome_idx - 1]

    cut_1 = random.randint(1, len(random_chromosome) - 1)
    cut_2 = random.randint(1, len(random_chromosome) - 1)

    while cut_2 == cut_1:
        cut_2 = random.randint(0, len(random_chromosome))

    if cut_1 > cut_2:
        cut_1, cut_2 = cut_2, cut_1

    # Only perform reversals (j = 1)
    reversed_chromosome = perform_chromosome_reversal(random_chromosome, cut_1, cut_2)
    genome[random_chromosome_idx - 1] = reversed_chromosome

    return genome, chromosome_type_dict


def perform_n_random_dcj_operations_on_genome(input_genome, input_chromosome_type_dict, n):
    genome = deepcopy(input_genome)
    chromosome_type_dict = deepcopy(input_chromosome_type_dict)

    for _ in range(n):
        genome, chromosome_type_dict = perform_dcj_on_single_chromsome(genome, chromosome_type_dict)

    return genome, chromosome_type_dict


def simulate_pair_from_original(og_genome, og_chromosome_type_dict, n):
    og_genome_copy = deepcopy(og_genome)
    og_chromosome_type_dict_copy = deepcopy(og_chromosome_type_dict)

    g1, d1 = perform_n_random_dcj_operations_on_genome(og_genome_copy, og_chromosome_type_dict_copy, n)
    g2, d2 = perform_n_random_dcj_operations_on_genome(og_genome, og_chromosome_type_dict, n)

    return g1, d1, g2, d2


def generate_single_dataset(n_g, n_gf, n_dcj, base_folder, dataset_num):
    """Generate a single dataset (original + 2 extant genomes)"""
    original_simulated_genome, original_dict = create_original_genome(n_g, 10, n_gf, 100)
    t_og = deepcopy(original_simulated_genome)
    t_dict = deepcopy(original_dict)

    g1_curr, d1_curr, g2_curr, d2_curr = simulate_pair_from_original(original_simulated_genome, original_dict, n_dcj)

    # Create subfolder for this dataset
    dataset_folder = os.path.join(base_folder, f'sim_{n_g}_{n_gf}_{n_dcj}_{dataset_num}')
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    # Generate files
    convert_genome_to_file(t_og, t_dict, 
                          output_file_name=os.path.join(dataset_folder, f'sim_{n_g}_{n_gf}_{n_dcj}_og.dcj'))
    convert_genome_to_file(g1_curr, d1_curr, 
                          output_file_name=os.path.join(dataset_folder, f'sim_{n_g}_{n_gf}_{n_dcj}_1.dcj'))
    convert_genome_to_file(g2_curr, d2_curr, 
                          output_file_name=os.path.join(dataset_folder, f'sim_{n_g}_{n_gf}_{n_dcj}_2.dcj'))


def generate_variable_dcj_ops():
    """Generate datasets with variable DCJ operations"""
    base_folder = '/data/aks7832/dcj-sat-all/dcj-sat-repo/test_files_multiple/variable_dcj_ops'
    
    # Define parameter sets: (genes, gene_families, dcj_ops_range)
    param_sets = [
        (100, 60, range(25, 56)),  # 25-55
        (500, 400, range(150, 191, 5)),  # 150-190 step 5
        (1500, 1000, range(350, 421, 10)),  # 350-420 step 10
        (5000, 3500, range(1290, 1371, 5))  # 1290-1370 step 5
    ]
    
    for n_g, n_gf, dcj_range in param_sets:
        for n_dcj in dcj_range:
            # Create main folder
            main_folder = os.path.join(base_folder, f'sim_{n_g}_{n_gf}_{n_dcj}')
            if not os.path.exists(main_folder):
                os.makedirs(main_folder)
            
            # Generate 5 datasets
            for dataset_num in range(1, 6):
                generate_single_dataset(n_g, n_gf, n_dcj, main_folder, dataset_num)
                print(f"Generated sim_{n_g}_{n_gf}_{n_dcj}_{dataset_num}")


def generate_variable_gene_families():
    """Generate datasets with variable gene families"""
    base_folder = '/data/aks7832/dcj-sat-all/dcj-sat-repo/test_files_multiple/variable_gene_families'
    
    # Define parameter sets: (genes, gene_families_range, dcj_ops)
    param_sets = [
        (100, range(40, 81, 2), 40),  # 40-80 step 2, plus some specific values
        (500, range(325, 401, 5), 150),  # 325-400 step 5
        (1500, range(900, 1101, 20), 400),  # 900-1100 step 20
        (5000, range(3325, 3601, 25), 1330)  # 3325-3600 step 25
    ]
    
    # Add specific values for 100 genes case
    param_sets[0] = (100, list(range(40, 81, 2)) + [56, 58, 62, 64, 66, 68], 40)
    
    for n_g, gf_range, n_dcj in param_sets:
        for n_gf in gf_range:
            # Create main folder
            main_folder = os.path.join(base_folder, f'sim_{n_g}_{n_gf}_{n_dcj}')
            if not os.path.exists(main_folder):
                os.makedirs(main_folder)
            
            # Generate 5 datasets
            for dataset_num in range(1, 6):
                generate_single_dataset(n_g, n_gf, n_dcj, main_folder, dataset_num)
                print(f"Generated sim_{n_g}_{n_gf}_{n_dcj}_{dataset_num}")


if __name__ == "__main__":
    # Generate both types of datasets
    print("Generating variable DCJ operations datasets...")
    generate_variable_dcj_ops()
    
    print("\nGenerating variable gene families datasets...")
    generate_variable_gene_families()
    
    print("\nAll datasets generated successfully!")
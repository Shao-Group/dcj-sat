from reading_simplified_params.make_graph_from_params import create_final_parameters_from_file
from utils.viz import visualize_genome_adjacency_graph

s1, s2, s1_grey, s2_grey, edges, he, num_vertices = create_final_parameters_from_file('../simplified_parameters/vertices.txt', '../simplified_parameters/edges.txt', '../simplified_parameters/gene_list.txt')
visualize_genome_adjacency_graph(s1, s2, s1_grey + s2_grey, edges, 'Graph')
print('Done')

def make_vertices_s1_s2(vertices_file_path):
    with open(vertices_file_path) as vertices_file:
        v_lines = vertices_file.readlines()

    v_lines = [line.strip() for line in v_lines]
    vertices = [int(v) + 1 for v in v_lines]
    num_vertices = len(vertices)

    s1 = []
    s2 = []

    for i in range(num_vertices // 2):
        s1.append(vertices[i])

    for i in range(num_vertices // 2, num_vertices):
        s2.append(vertices[i])

    return s1, s2


def create_black_graph(s1, gr_file_path):
    with open(gr_file_path) as gr_file:
        gr_lines = gr_file.readlines()

    black = []

    gr_dict = {}

    for line in gr_lines:
        line = line.strip()
        line = line.split(' ')
        v_list = [int(v) + 1 for v in line]
        key = v_list[0]
        value = v_list[1:]
        gr_dict[key] = value

    for v in gr_dict.keys():
        if v in s1:
            for v_dash in gr_dict[v]:
                black.append((v, v_dash))

    return black


def create_grey_g1_g2(s1, s2, partners_file_path):
    with open(partners_file_path) as partners_file:
        partners_lines = partners_file.readlines()

    visited = []

    grey = []

    partners_lines = [line.strip() for line in partners_lines]
    for line in partners_lines:
        line = line.split(' ')
        u = int(line[0]) + 1
        v = int(line[1]) + 1
        if u not in visited and v not in visited:
            grey.append((u, v))
            visited.append(u)
            visited.append(v)

    s1_grey = []
    s2_grey = []

    for (u, v) in grey:
        if u in s1 and v in s1:
            s1_grey.append((u, v))
        elif u in s2 and v in s2:
            s2_grey.append((u, v))

    return s1_grey, s2_grey


def create_homo_pairs(black, gene_list_path):
    with open(gene_list_path) as gene_list_file:
        gene_lines = gene_list_file.readlines()

    gene_lines = [line.strip() for line in gene_lines]
    gene_lines = [line.split(' ') for line in gene_lines]

    split_pair_dict = {}

    for line in gene_lines:
        if int(line[2]) > 1:
            split_pair_dict[int(line[0]) + 1] = int(line[1]) + 1
            split_pair_dict[int(line[1]) + 1] = int(line[0]) + 1

    visited = []
    he = []

    for (u, v) in black:
        if u in split_pair_dict and v in split_pair_dict:
            u_part = split_pair_dict[u]
            v_part = split_pair_dict[v]

            if (u_part, v_part) in black and (u, v) not in visited and (u_part, v_part) not in visited:
                he.append(((u, v), (u_part, v_part)))
                visited.append((u_part, v_part))
                visited.append((u, v))

    return he


def create_final_parameters_from_file(vertices_file_path, gr_file_path, partners_file_path, gene_list_path, simp_cycle_path):
    s1, s2 = make_vertices_s1_s2(vertices_file_path)
    black = create_black_graph(s1, gr_file_path)
    s1_grey, s2_grey = create_grey_g1_g2(s1, s2, partners_file_path)
    he = create_homo_pairs(black, gene_list_path)
    with open(simp_cycle_path) as simp_cycle_file:
        simp_cycle_lines = simp_cycle_file.readlines()
    simp_cycle_lines = simp_cycle_lines[0]
    cycles_removed = int(simp_cycle_lines.strip())
    num_vertices = len(s1) + len(s2)

    return s1, s2, s1_grey, s2_grey, black, he, cycles_removed, num_vertices

import networkx as nx


def construct_networkx_LCG(n_vars, clauses):
    G = nx.Graph() 

    for i in range(1, n_vars+1):
        G.add_node(('l', i), type='l')  # type needed as label for WL. also included in the node name for indexing
        G.add_node(('l', -i), type='l')

    for i in range(1, len(clauses)+1):
        G.add_node(('c', i), type='c')

    for c_idx, clause in enumerate(clauses):
        for literal in clause:
            G.add_edge(('c', c_idx + 1), ('l', literal), edge_type='literal-clause')

    for i in range(1, n_vars+1):
        G.add_edge(('l', i), ('l', -i), edge_type='literal-literal')

    return G



def augment_cnf(_clauses, partition):
   
    clauses = _clauses.copy()

    # Step 2: Add WL-label-based constraints
    n_clauses_added = 0
    for subset in partition:
        if len(subset) > 1:
            for i in range(len(subset)-1):
                l1 = subset[i][1]
                l2 = subset[i+1][1]
                clauses.append([-l1, l2])  # subset[i] => subset[i+1]

            ln = subset[-1][1]
            l1 = subset[0][1]
            clauses.append([-ln, l1])

            n_clauses_added += len(subset)

    return clauses

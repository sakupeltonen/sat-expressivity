import networkx as nx
from g4satbench.utils.utils import literal2v_idx


def construct_networkx_VCG(n_vars, clauses, learned_clauses):
    """note: learned clauses are not currently used"""
    G = nx.Graph() 

    for i in range(n_vars):
        G.add_node(('v', i), type='v')  # type needed as label for WL. also included in the node name for indexing
    
    for i in range(len(clauses)):
        G.add_node(('c', i), type='c')

    for c_idx, clause in enumerate(clauses):
        for literal in clause:
            sign, v_idx = literal2v_idx(literal)  # NOTE: by convention, v_idx is 0-based
            G.add_edge(('c', c_idx), ('v', v_idx), sign=sign)

    # construct two graphs, one with only the original clauses, and a second one with the learned clauses
    G_learned = G.copy()

    for i in range(len(learned_clauses)):
        # name contains all info, while WL sees type which is the same as for regular clauses
        G.add_node(('c_learned', i), type='c')  

    for c_idx, clause in enumerate(learned_clauses):
        for literal in clause:
            sign, v_idx = literal2v_idx(literal)
            G_learned.add_edge(('c_learned', c_idx), ('v', v_idx), sign=sign)

    return G, G_learned


def get_signed_degree(G, node, edge_sign):
    return len([1 for _, _, attr in G.edges(node, data=True) if attr.get('sign') == edge_sign])



def augment_cnf(_clauses, partition):
    clauses = _clauses.copy()

    n_clauses_added = 0
    for subset in partition:
        if len(subset) > 1:
            for i in range(len(subset)-1):
                v1 = subset[i][1] + 1
                v2 = subset[i+1][1] + 1
                clauses.append([-v1, v2])  # subset[i] => subset[i+1]
            vn = subset[-1][1] + 1
            v1 = subset[0][1] + 1
            clauses.append([-vn, v1])  # subset[-1] => subset[0]
            n_clauses_added += len(subset)

    return clauses

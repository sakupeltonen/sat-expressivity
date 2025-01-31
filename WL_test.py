import networkx as nx
from pysat.solvers import Cadical
import os

from g4satbench.utils.utils import parse_cnf_file
from formulas import construct_networkx_VCG, augment_cnf


def run_WL(G, n_iter):
    # this returns hashes for iterations starting from 1
    all_hashes = nx.weisfeiler_lehman_subgraph_hashes(G, 
                                                  iterations=n_iter-1, 
                                                  node_attr="type", 
                                                  edge_attr="sign")
    
    # add hashes for the first iteration manually
    for node, attr in G.nodes(data=True):
        all_hashes[node].insert(0, attr['type'])

    return all_hashes


def get_partitions(hashes, only_variables=True):

    hash_to_subset = {}

    for node, hash in hashes.items():
        if node[0] != 'v' and only_variables:
            continue
        if hash in hash_to_subset:
            hash_to_subset[hash].append(node)
        else:
            hash_to_subset[hash] = [node]

    partitions = [subset for subset in hash_to_subset.values()]

    return partitions


def iter_converged(all_hashes):
    # find iteration where refinement converged, that is the number of partitions in the next iteration is the same (the partition didn't get finer)
    n_iter = len(list(all_hashes.values())[0])

    def iter_i_hashes(i):
        return [all_hashes[node][i] for node in all_hashes.keys()]

    for i in range(1, n_iter):
        partition_size = len(set(iter_i_hashes(i)))
        partition_size_prev = len(set(iter_i_hashes(i-1)))
        if partition_size == partition_size_prev:
            return i-1, True
    
    return n_iter-1, False  # did not converge in n_iters
    



def find_critical_iter(file_path, n_iter, out_path='constrained.cnf'):
    n_vars, clauses, learned_clauses = parse_cnf_file(file_path, split_clauses=True)
    G, _ = construct_networkx_VCG(n_vars, clauses, learned_clauses)  # NOTE: ignoring the second graph for now

    # Step 2: Find WL partitions
    all_hashes = run_WL(G, n_iter)

    # save this for analysis
    partition_sizes = []

    # Check when WL converges. This is an upper bound for the critical iteration, if the formula with WL partitions is solvable
    converged_iter, converged = iter_converged(all_hashes)

    critical_iter = None
    ub_search = converged_iter + 1 if converged else n_iter
    for i in range(ub_search):
        hashes = {node: all_hashes[node][i] for node in G.nodes}
        partition = get_partitions(hashes)

        partition_sizes.append(len(partition))

        new_clauses = augment_cnf(clauses, partition)

        # Step: solve the augmented CNF
        solver = Cadical(bootstrap_with=new_clauses)
        res = solver.solve()

        if res: 
            critical_iter = i
            break
    

    file_name = os.path.basename(file_path)
    file_name = file_name.split('.')[0]

    info = {
        'file_name': file_name,
        'iter_critical': critical_iter,
        'sat': critical_iter is not None,
        'iter_converged': converged_iter,
        'converged': converged,
        'n_vars': n_vars,
        'n_clauses': len(clauses)
    }
    for i in range(n_iter):
        if i < len(partition_sizes):
            info[f'partsize_{i}'] = partition_sizes[i]
        else:
            info[f'partsize_{i}'] = partition_sizes[-1]
    

    return info
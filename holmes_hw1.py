import numpy as np
import json
from sklearn.neighbors import KDTree
import argparse
import time
import matplotlib.pyplot as plt

def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return np.array(data).reshape(-1,3)

def combine_nodes(nodes, tolerance, leaf_size):
    #Get lists of nodes within tolerance using KDTree
    tree = KDTree(nodes, leaf_size=leaf_size, metric='euclidean')
    count = tree.query_radius(nodes, r=tolerance, count_only=False, return_distance=False)
    
    #Sort lists so minimum number of nodes are formed
    original_count_and_idx = list(enumerate(count))
    sorted_count_and_idx = sorted(original_count_and_idx, key = lambda x: len(x[1]), reverse = True)
    sorted_count = [sublist for _, sublist in sorted_count_and_idx]
    sorted_idx = [idx for idx, _ in sorted_count_and_idx]

    #Loop through nodes with connections and group
    combined_nodes = set()
    for i, node in zip(sorted_idx, sorted_count):
        if i not in combined_nodes:
            node_set = set(node).difference(combined_nodes)
            for node in node_set:
                combined_nodes.add(node)
            count[i] = tuple(node_set)
        else:
            count[i] = ()

    return len(set(x for x in count if x != ()))

def write_to_csv(nodes):
    with open('output.txt', "w", newline="") as file:
        for node in nodes:
            line = ",".join(map(str, node))
            file.write(f"{line}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='hw-1.json')
    parser.add_argument('--tolerance', type=float, default=0.1)
    parser.add_argument('--leaf_size', type=int, default=40)
    args = parser.parse_args()
    nodes = load_json(args.data_path)
    tic = time.time()
    num_nodes = combine_nodes(nodes, args.tolerance, args.leaf_size)
    toc = time.time()
    print(num_nodes)
    print(toc-tic)

    #Write ans to file
    write_to_csv(nodes)
    out_file = open('HW1_ans.txt', 'w')
    out_file.write(str(num_nodes))
    out_file.close()

    

import networkx as nx
import numpy as np
import argparse
import json
import math

def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def create_adjacency_matrix(graph):
    edge_list = graph['elements']
    nodes = graph['nodes']
    mat_dims = max(max(edge_list))+1
    adj_mat = [[0 for i in range(mat_dims)] for j in range(mat_dims)]
    for row,col in edge_list:
        adj_mat[row][col] = math.dist(nodes[row], nodes[col])
    return adj_mat

def get_min_length(adj_mat, start, end):
    graph = nx.from_numpy_array(np.array(adj_mat))
    length = nx.dijkstra_path_length(graph, source = start, target = end)
    return length

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='hw-2.json')
    args = parser.parse_args()
    graph = load_json(args.data_path)
    adj_mat = create_adjacency_matrix(graph)
    length = get_min_length(adj_mat, graph['startNodeIndex'], graph['endNodeIndex'])
    print(length)

    out_file = open('HW2_ans.txt', 'w')
    out_file.write(str(length))
    out_file.close()
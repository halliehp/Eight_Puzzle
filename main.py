import numpy
import heapq
from treelib import Node, Tree

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
depth_2 = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]


def print_puzzle(puzzle):
    for i in range(0,3):
        print(puzzle[i])
    print('\n')


def expand_node(initial_node):
    for j in range(len(initial_node)):
        for i in range(len(initial_node[j])):
            if initial_node[j][i] == 0:
                print(j+1, i+1)


def general_search(initial_problem):
    queue = []
    heapq.heappush(queue, initial_problem)
    tree = Tree()
    tree.create_node(initial_problem, 1)  # root node
    expanded_nodes = []
    expanded_nodes_count = 0
    max_queue_size = 0

    while len(queue) > 0:
        max_queue_size = max(len(queue), max_queue_size)
        current_node = heapq.heappop(queue)
        print(current_node)
        if current_node == goal_state:
            while len(expanded_nodes) > 0:
                print_puzzle(expanded_nodes.pop())
            print("Number of nodes expanded: ", expanded_nodes_count)
            print("Max queue size: ", max_queue_size)
            return current_node
        else:
            expanded_nodes.append(current_node)
            print('expanded nodes:')
            print(expanded_nodes)


#general_search(depth_2)
expand_node(depth_2)

import numpy
import heapq
from queue import Queue

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
one_off = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]


def print_puzzle(puzzle):
    for i in range(0,3):
        print(puzzle[i])
    print('\n')


def general_search(problem):
    queue = []
    heapq.heappush(queue, problem)
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


general_search(goal_state)

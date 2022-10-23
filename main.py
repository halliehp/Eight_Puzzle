import numpy
import heapq
from treelib import Node, Tree
import copy

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

depth_2 = [[1, 2, 3],
           [4, 5, 6],
           [0, 7, 8]]

test = [[1, 2, 3],
        [4, 0, 6],
        [5, 7, 8]]


def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')


def tile_up(node, row, column):  # given current puzzle and row and column of zero tile, swap tiles
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row-1][column]
    new_node[row][column] = tile_above
    new_node[row-1][column] = zero_tile
    return new_node


def tile_down(node, row, column):
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_below = new_node[row+1][column]
    new_node[row][column] = tile_below
    new_node[row+1][column] = zero_tile
    return new_node


def tile_right(node, row, column):
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row][column+1]
    new_node[row][column] = tile_above
    new_node[row][column+1] = zero_tile
    return new_node


def tile_left(node, row, column):
    if int(column-1) < 0:
        return
    new_node = copy.deepcopy(node)
    zero_tile = node[row][column]
    tile_above = node[row][column-1]
    new_node[row][column] = tile_above
    new_node[row][column-1] = zero_tile
    return new_node


def find_zero(initial_node):
    for j in range(len(initial_node)):
        for i in range(len(initial_node[j])):
            if initial_node[j][i] == 0:  # find where the empty tile is
                return j, i


def general_search(initial_problem):
    queue = []
    heapq.heappush(queue, initial_problem)
    tree = Tree()
    parent_num = 0
    tree.create_node(initial_problem, 1)  # root node
    expanded_nodes = []
    expanded_nodes_count = 0
    max_queue_size = 0
    tree_id = 2

    while len(queue) > 0:
        max_queue_size = max(len(queue), max_queue_size)
        current_node = heapq.heappop(queue)
        # print_puzzle(current_node)
        parent_num = parent_num + 1
        if current_node == goal_state:
            while len(expanded_nodes) > 0:
                print_puzzle(expanded_nodes.pop())
            print("Number of nodes expanded: ", expanded_nodes_count)
            print("Max queue size: ", max_queue_size)
            return current_node
        else:
            j, i = find_zero(current_node)[0], int(find_zero(current_node)[1])
            # print(j, i)
            expanded_nodes.append(current_node)  # expand node
            curr_copy = copy.deepcopy(current_node)
            try:
                temp = tile_down(copy.deepcopy(curr_copy), j, i)
                tree.create_node(temp, tree_id, parent=parent_num)
                tree_id += 1
                # heapq.heappush(queue, temp)
            except:
                print('tile cannot move down')
            try:
                temp = tile_up(copy.deepcopy(curr_copy), j, i)
                tree.create_node(temp, tree_id, parent=parent_num)
                tree_id += 1
                # heapq.heappush(queue, temp)
            except:
                print('tile cannot move up')
            try:
                temp = tile_right(copy.deepcopy(curr_copy), j, i)
                tree.create_node(temp, tree_id, parent=parent_num)
                tree_id += 1
                # heapq.heappush(queue, temp)
            except:
                print('tile cannot move right')
            try:
                temp = tile_left(copy.deepcopy(curr_copy), j, i)
                if temp != None:
                    tree.create_node(temp, tree_id, parent=parent_num)
                    tree_id += 1
                    # heapq.heappush(queue, temp)
            except:
                print('tile cannot move left')
            print('expanded nodes:')
            print(expanded_nodes)
            expanded_nodes_count = expanded_nodes_count+1
            print('expanded tree:')
            tree.show()


# general_search(depth_2)
'''current_node = copy.deepcopy(depth_2)
print_puzzle(current_node)
tree = Tree()
j, i = find_zero(current_node)[0], find_zero(current_node)[1]
print(j, i)
tree.create_node(current_node, 1)
another_temp = tile_right(copy.deepcopy(current_node), j, i)
print_puzzle(another_temp)
tree.create_node(another_temp, 2, 1)
temp_again = tile_up(copy.deepcopy(current_node), j, i)
print_puzzle(temp_again)
tree.create_node(temp_again, 3, 1)
yet_another = tile_left(copy.deepcopy(current_node), j, i)
if yet_another == None:
    print('nope')
#print_puzzle(yet_another)
#tree.create_node(yet_another, 3, 1)
tree.show()
print_puzzle(current_node)'''

general_search(depth_2)

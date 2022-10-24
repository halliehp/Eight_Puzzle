import numpy
import heapq
from treelib import Node, Tree
import copy

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

depth_1 = [[1, 2, 3],
           [4, 5, 6],
           [7, 0, 8]]

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
    if int(row-1) < 0:
        return
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row-1][column]
    new_node[row][column] = tile_above
    new_node[row-1][column] = zero_tile
    return new_node


def tile_down(node, row, column):
    if int(row+1) > 2:
        return
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_below = new_node[row+1][column]
    new_node[row][column] = tile_below
    new_node[row+1][column] = zero_tile
    return new_node


def tile_right(node, row, column):
    if int(column+1) > 2:
        return
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


def do_expansion(node):
    '''try:
        temp = tile_down(copy.deepcopy(curr_copy), j, i)
        if temp is not None:
            tree.create_node(temp, tree_id, parent=parent_num)
            tree_id += 1
            if temp not in queue:
                heapq.heappush(queue, temp)
    except:
        print('tile cannot move down')
    try:
        temp2 = tile_up(copy.deepcopy(curr_copy), j, i)
        if temp2 is not None:
            tree.create_node(temp2, tree_id, parent=parent_num)
            tree_id += 1
            if temp2 not in queue:
                heapq.heappush(queue, temp2)
    except:
                    print('tile cannot move up')'''
    try:
        temp3 = tile_right(copy.deepcopy(node), j, i)
        if temp3 is not None:
            if temp3 not in queue:
                tree.create_node(temp3, tree_id, parent=parent_num)
                tree_id += 1
                heapq.heappush(queue, temp3)
    except:
        print('tile cannot move right')
    '''try:
        temp4 = tile_left(copy.deepcopy(curr_copy), j, i)
        if temp4 is not None:
            if temp4 not in queue:
                tree.create_node(temp4, tree_id, parent=parent_num)
                tree_id += 1
                heapq.heappush(queue, temp4)
    except:
        print('tile cannot move left')'''


def general_search(initial_problem):
    queue = []
    heapq.heapify(queue)
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
        parent_num += 1
        if current_node == goal_state:
            print("Goal state reached!")
            while len(expanded_nodes) > 0:
                print_puzzle(expanded_nodes.pop())
            print("Number of nodes expanded: ", expanded_nodes_count)
            print("Max queue size: ", max_queue_size)
            print('expanded nodes:')
            print(expanded_nodes)
            print('expanded tree:')
            tree.show()
            return current_node
        else:
            j, i = find_zero(current_node)[0], int(find_zero(current_node)[1])
            # print(j, i)
            expanded_nodes.append(current_node)  # about to expand the current node to append it to expanded nodes
            curr_copy = copy.deepcopy(current_node)  # deep copy current node
            # logic to expand node here
            try:
                temp3 = tile_right(copy.deepcopy(curr_copy), j, i)
                if temp3 is not None:
                    if temp3 not in expanded_nodes:
                        tree.create_node(temp3, tree_id, parent=parent_num)
                        tree_id += 1
                        queue.append(temp3)
            except:
                print('tile cannot move right')
            try:
                temp4 = tile_left(copy.deepcopy(curr_copy), j, i)
                if temp4 is not None:
                    if temp4 not in expanded_nodes:
                        tree.create_node(temp4, tree_id, parent=parent_num)
                        tree_id += 1
                        # heapq.heappush(queue, temp4)
                        queue.append(temp4)
            except:
                print('tile cannot move left')
            try:
                temp = tile_down(copy.deepcopy(curr_copy), j, i)
                if temp is not None:
                    if temp not in expanded_nodes:
                        tree.create_node(temp, tree_id, parent=parent_num)
                        tree_id += 1
                        # heapq.heappush(queue, temp)
                        queue.append(temp)
            except:
                print('tile cannot move down')
            try:
                temp2 = tile_up(copy.deepcopy(curr_copy), j, i)
                if temp2 is not None:
                    if temp2 not in expanded_nodes:
                        tree.create_node(temp2, tree_id, parent=parent_num)
                        tree_id += 1
                        # heapq.heappush(queue, temp2)
                        queue.append(temp2)
            except:
                print('tile cannot move up')
            print(queue[0])
            expanded_nodes_count += 1


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

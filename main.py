import numpy as np
from treelib import Node, Tree
import copy
import heapq

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# coordinates are given in row, column
goal_state_coordinates = {1: [0, 0], 2: [0, 1], 3: [0, 2],
                          4: [1, 0], 5: [1, 1], 6: [1, 2],
                          7: [2, 0], 8: [2, 1], 0: [2, 2]}


class Board:
    def __init__(self, node: list[list[int]]):
        self.node = node
        self.cost = 0
        self.depth = 0

    def __lt__(self, other):
        return self.cost < other.cost


depth_1 = Board([[1, 2, 3],
                 [4, 5, 6],
                 [7, 0, 8]])

depth_2 = Board([[1, 2, 3],
                 [4, 5, 6],
                 [0, 7, 8]])

depth_4 = Board([[1, 2, 3],
                 [5, 0, 6],
                 [4, 7, 8]])

depth_8 = Board([[1, 3, 6],
                 [5, 0, 2],
                 [4, 7, 8]])

depth_16 = Board([[1, 6, 7],
                  [5, 0, 3],
                  [4, 8, 2]])

depth_12 = Board([[1, 3, 6],
                  [5, 0, 7],
                  [4, 8, 2]])

test = Board([[8, 6, 7],
              [2, 5, 4],
              [3, 0, 1]])


def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')


def tile_up(node, row, column):  # given current puzzle and row and column of zero tile, swap tiles
    if int(row-1) < 0:
        return None
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row-1][column]
    new_node[row][column] = tile_above
    new_node[row-1][column] = zero_tile
    return new_node


def tile_down(node, row, column):
    if int(row+1) > 2:
        return None
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_below = new_node[row+1][column]
    new_node[row][column] = tile_below
    new_node[row+1][column] = zero_tile
    return new_node


def tile_right(node, row, column):
    if int(column+1) > 2:
        return None
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row][column+1]
    new_node[row][column] = tile_above
    new_node[row][column+1] = zero_tile
    return new_node


def tile_left(node, row, column):
    if int(column-1) < 0:
        return None
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row][column-1]
    new_node[row][column] = tile_above
    new_node[row][column-1] = zero_tile
    return new_node




def misplaced_tile(node):  # resulting count is the g(n) for the misplaced tile heuristic
    count = -1  # this is to account for the placeholder tile
    for j in range(3):
        for i in range(3):
            if goal_state[j][i] != node[j][i]:
                count += 1
    return count


def manhattan_distance(node):  # the g(n) is the sum of the distance all misplaced tiles are from their goal spot
    # dictionary with coordinates of the goal states is goal_state_coordinates
    # do the math aka find displacement of all the missing ones and then sum it
    distance_sum = 0
    for j in range(3):
        for i in range(3):
            gs = goal_state[j][i]
            cn = node[j][i]
            if cn != 0:
                if gs != cn:
                    dist = abs(j - goal_state_coordinates[cn][0]) + abs(i - goal_state_coordinates[cn][1])
                    distance_sum += dist
    return distance_sum


def find_zero(initial_node):
    for j in range(len(initial_node)):
        for i in range(len(initial_node[j])):
            if initial_node[j][i] == 0:  # find where the empty tile is
                return j, i


def queuing_order(node, tree, parent_num, algo, tree_id, expanded_nodes, queue):
    if node is not None:
        if node not in expanded_nodes:
            tree.create_node(node, tree_id, parent=parent_num)
            tree_id += 1
            temp_depth = tree.depth()
            if algo == 1:
                cost = temp_depth
            elif algo == 2:
                cost = temp_depth + misplaced_tile(node)
            elif algo == 3:
                cost = temp_depth + manhattan_distance(node)
            heapq.heappush(queue, (cost, node))
    return queue


def expand_node(board: Board, tree: Tree, curr_tree_id):
    puzzle = board.node
    current = copy.deepcopy(puzzle)
    zeroth = find_zero(current)
    j, i = zeroth[0], zeroth[1]  # row = j, col - i
    children = []
    if int(j + 1) <= 2:
        current = tile_down(current, j, i)
        temp_child = Board(copy.deepcopy(current))
        children.append(temp_child)
        curr_tree_id += 1
        tree.create_node(current, curr_tree_id, parent=board.tree_id)
        current = copy.deepcopy(puzzle)
    if int(j - 1) >= 0:
        current = tile_up(current, j, i)
        temp_child = Board(copy.deepcopy(current))
        children.append(temp_child)
        curr_tree_id += 1
        tree.create_node(current, curr_tree_id, parent=board.tree_id)
        current = copy.deepcopy(puzzle)
    if int(i - 1) >= 0:
        current = tile_left(current, j, i)
        temp_child = Board(copy.deepcopy(current))
        children.append(temp_child)
        curr_tree_id += 1
        tree.create_node(current, curr_tree_id, parent=board.tree_id)
        current = copy.deepcopy(puzzle)
    if int(i + 1) <= 2:
        current = tile_right(current, j, i)
        temp_child = Board(copy.deepcopy(current))
        children.append(temp_child)
        curr_tree_id += 1
        tree.create_node(current, curr_tree_id, parent=board.tree_id)
    board.children = children
    return tree, curr_tree_id


def general_search(algo, initial_problem):
    queue = []
    heapq.heapify(queue)
    heapq.heappush(queue, (initial_problem.cost, initial_problem.node))
    # queue.put(initial_problem)
    tree = Tree()
    parent_num = 0
    tree.create_node(initial_problem.node, 1)  # root node
    visited_nodes = []
    expanded_nodes = []
    expanded_nodes_count = 0
    max_queue_size = 0
    tree_id = 2

    while len(queue) > 0:
        max_queue_size = max(len(queue), max_queue_size)
        current_node_and = heapq.heappop(queue)
        current_node = current_node_and[1]
        current_cost = current_node_and[0]
        # current_node = queue.get()
        # print_puzzle(current_node)
        parent_num += 1
        if np.array_equal(current_node, goal_state):
            print("Goal state reached!")
            '''while len(expanded_nodes) > 0:
                here = expanded_nodes.pop()
                print_puzzle(here)'''

            # print('expanded tree:')
            # tree.show()
            print("Number of nodes expanded: ", expanded_nodes_count)
            print("Max queue size: ", max_queue_size)
            # print('expanded nodes:')
            # print(expanded_nodes)
            # print('depth of tree: ', tree.depth())
            # pls = tree.get_node(tree_id)
            # print('depth of tree: ', tree.depth(pls))
            print('depth of tree: ', tree.depth())
            return current_node
        else:
            zeroth = find_zero(current_node)
            j, i = zeroth[0], zeroth[1]
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
                        # queue.put(temp3)
                        temp_depth = tree.depth()
                        if algo == 1:
                            cost = temp_depth
                        elif algo == 2:
                            cost = temp_depth + misplaced_tile(temp3)
                        elif algo == 3:
                            cost = temp_depth + manhattan_distance(temp3)
                        heapq.heappush(queue, (cost, temp3))
            except:
                print('tile cannot move right')
            try:
                temp4 = tile_left(copy.deepcopy(curr_copy), j, i)
                if temp4 is not None:
                    if temp4 not in expanded_nodes:
                        tree.create_node(temp4, tree_id, parent=parent_num)
                        tree_id += 1
                        # heapq.heappush(queue, temp4)
                        # queue.put(temp4)
                        temp_depth = tree.depth()
                        if algo == 1:
                            cost = temp_depth
                        elif algo == 2:
                            cost = temp_depth + misplaced_tile(temp4)
                        elif algo == 3:
                            cost = temp_depth + manhattan_distance(temp4)
                        heapq.heappush(queue, (cost, temp4))
            except:
                print('tile cannot move left')
            try:
                temp = tile_down(copy.deepcopy(curr_copy), j, i)
                if temp is not None:
                    if temp not in expanded_nodes:
                        tree.create_node(temp, tree_id, parent=parent_num)
                        tree_id += 1
                        # heapq.heappush(queue, temp)
                        # queue.put(temp)
                        temp_depth = tree.depth()
                        if algo == 1:
                            cost = temp_depth
                        elif algo == 2:
                            cost = temp_depth + misplaced_tile(temp)
                        elif algo == 3:
                            cost = temp_depth + manhattan_distance(temp)
                        heapq.heappush(queue, (cost, temp))
            except:
                print('tile cannot move down')
            try:
                temp2 = tile_up(copy.deepcopy(curr_copy), j, i)
                if temp2 is not None:
                    if temp2 not in expanded_nodes:
                        tree.create_node(temp2, tree_id, parent=parent_num)
                        tree_id += 1
                        temp_depth = tree.depth()
                        if algo == 1:
                            cost = temp_depth
                        elif algo == 2:
                            cost = temp_depth + misplaced_tile(temp2)
                        elif algo == 3:
                            cost = temp_depth + manhattan_distance(temp2)
                        heapq.heappush(queue, (cost, temp2))
                        # queue.put(temp2)
            except:
                print('tile cannot move up')
            # print(queue[0])
            expanded_nodes_count += 1

    if len(queue) == 0:
        print('Search failed. There is no solution to this puzzle!')


def main_menu():
    print('Welcome to 8 Puzzle Solver!')
    algo = input('Select your algorithm. \n'
                 '(1) for Uniform Cost \n'
                 '(2) for Misplaced Tile Heuristic \n'
                 '(3) for Manhattan Distance Heuristic \n')
    algo = int(algo)
    general_search(algo, depth_4)


main_menu()

# print('for misplaced tile g(n) =', misplaced_tile(test.node))
# print('for manhattan g(n) =', manhattan_distance(test.node))

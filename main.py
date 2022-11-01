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


def general_search(algo, initial_board, tree_id):
    queue = []
    heapq.heapify(queue)
    tree = Tree()
    tree_id += 1
    initial_board.tree_id = tree_id
    tree.create_node(initial_board.node, tree_id)
    heapq.heappush(queue, (initial_board.cost, initial_board))
    max_queue_size = 0

    while len(queue) >0:
        max_queue_size = max(len(queue), max_queue_size)
        current_node = heapq.heappop(queue)
        node_now = expand_node(current_node[1], tree, tree_id)
        # print(current_node[1].children[0].node)
        tree_id += node_now[1]
        tree.show()
        print('tree depth is: ', tree.depth())

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

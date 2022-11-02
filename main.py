import numpy
from treelib import Node, Tree
import copy
import heapq
import time

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# coordinates are given in row, column
goal_state_coordinates = {1: [0, 0], 2: [0, 1], 3: [0, 2],
                          4: [1, 0], 5: [1, 1], 6: [1, 2],
                          7: [2, 0], 8: [2, 1], 0: [2, 2]}


class Board:
    def __init__(self, node: list[list[int]]):
        self.node = node  # actual 2d array of puzzle
        self.children = []  # list of children nodes expanded from this node
        self.depth = 0  # g(n)
        self.heuristic = 0  # h(n)
        self.cost = 0  # g(n) + h(n)
        self.tree_id = 0  # id of node on tree structure

    def __lt__(self, other):
        return self.cost < other.cost

depth_0 = Board([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 0]])

depth_1 = Board([[1, 2, 3],
                 [4, 5, 6],
                 [7, 0, 8]])

depth_2 = Board([[1, 2, 3],
                 [4, 5, 6],
                 [0, 7, 8]])

depth_4 = Board([[1, 2, 3],  # easy default puzzle
                 [5, 0, 6],
                 [4, 7, 8]])

depth_8 = Board([[1, 3, 6],
                 [5, 0, 2],
                 [4, 7, 8]])

depth_16 = Board([[1, 6, 7],  # medium default puzzle
                  [5, 0, 3],
                  [4, 8, 2]])

depth_24 = Board([[0, 7, 2],  # hard default puzzle
                  [4, 6, 1],
                  [3, 5, 8]])

depth_31 = Board([[8, 6, 7],
                  [2, 5, 4],
                  [3, 0, 1]])

tree_id = 0


def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')


def tile_up(node, row, column):  # given current puzzle and row and column of zero tile, swap tiles
    if int(row - 1) < 0:
        return None
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row - 1][column]
    new_node[row][column] = tile_above
    new_node[row - 1][column] = zero_tile
    return new_node


def tile_down(node, row, column):
    if int(row + 1) > 2:
        return None
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_below = new_node[row + 1][column]
    new_node[row][column] = tile_below
    new_node[row + 1][column] = zero_tile
    return new_node


def tile_right(node, row, column):
    if int(column + 1) > 2:
        return None
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row][column + 1]
    new_node[row][column] = tile_above
    new_node[row][column + 1] = zero_tile
    return new_node


def tile_left(node, row, column):
    new_node = copy.deepcopy(node)
    zero_tile = new_node[row][column]
    tile_above = new_node[row][column - 1]
    new_node[row][column] = tile_above
    new_node[row][column - 1] = zero_tile
    return new_node


def expand_node(board: Board, tree: Tree, curr_tree_id):
    puzzle = board.node
    current = copy.deepcopy(puzzle)
    zeroth = find_zero(current)
    j, i = zeroth[0], zeroth[1]  # row = j, col - i
    children = []
    if int(j + 1) <= 2:
        current = tile_down(current, j, i)
        temp_child = Board(copy.deepcopy(current))
        curr_tree_id += 1
        temp_child.tree_id = curr_tree_id
        children.append(temp_child)
        tree.create_node(current, curr_tree_id, parent=board.tree_id)
        current = copy.deepcopy(puzzle)
    if int(j - 1) >= 0:
        current = tile_up(current, j, i)
        temp_child = Board(copy.deepcopy(current))
        curr_tree_id += 1
        temp_child.tree_id = curr_tree_id
        children.append(temp_child)
        tree.create_node(current, curr_tree_id, parent=board.tree_id)
        current = copy.deepcopy(puzzle)
    if int(i - 1) >= 0:
        current = tile_left(current, j, i)
        temp_child = Board(copy.deepcopy(current))
        curr_tree_id += 1
        temp_child.tree_id = curr_tree_id
        children.append(temp_child)
        tree.create_node(current, curr_tree_id, parent=board.tree_id)
        current = copy.deepcopy(puzzle)
    if int(i + 1) <= 2:
        current = tile_right(current, j, i)
        temp_child = Board(copy.deepcopy(current))
        curr_tree_id += 1
        temp_child.tree_id = curr_tree_id
        children.append(temp_child)
        tree.create_node(current, curr_tree_id, parent=board.tree_id)
    for x in range(len(children)):
        children[x].depth = board.depth + 1
    board.children = children
    return children, curr_tree_id


def misplaced_tile(node):  # resulting count is the g(n) for the misplaced tile heuristic
    count = -1  # this is to account for the placeholder tile
    for j in range(3):
        for i in range(3):
            if goal_state[j][i] != node[j][i]:
                count += 1
    if count < 0:
        count = 0
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


def queueing_order(algo, nodes, childs, depth, already_expanded):
    for x in range(len(childs)):
        if str(childs[x].node) not in already_expanded:
            if algo == 1:
                heuristic = 0
            elif algo == 2:
                heuristic = misplaced_tile(childs[x].node)
                childs[x].heuristic = heuristic
            elif algo == 3:
                heuristic = manhattan_distance(childs[x].node)
                childs[x].heuristic = heuristic
            cost = depth + heuristic
            childs[x].cost = cost
            heapq.heappush(nodes, (cost,childs[x]))
    return nodes


def general_search(algo, initial_board, tree_id):
    nodes = []
    expanded_nodes = set()
    heapq.heapify(nodes)
    tree = Tree()
    tree_id += 1
    if algo == 2:
        initial_board.heuristic = misplaced_tile(initial_board.node)
    elif algo == 3:
        initial_board.heuristic = manhattan_distance(initial_board.node)
    initial_board.tree_id = tree_id
    tree.create_node(initial_board.node, tree_id)
    heapq.heappush(nodes, (initial_board.cost, initial_board))
    max_queue_size = 0
    expanded_nodes_count = 0

    while len(nodes) > 0:
        max_queue_size = max(len(nodes), max_queue_size)
        current_node = heapq.heappop(nodes)
        curr = copy.deepcopy(current_node[1])

        print('Best state to expand with g(x): ', curr.depth, ' and h(x): ', curr.heuristic)
        print_puzzle(curr.node)

        if numpy.array_equal(curr.node, goal_state):
            print('Goal state reached!')
            # tree.show()
            print('Number of nodes expanded: ', expanded_nodes_count)
            print('Max queue size: ', max_queue_size)
            print('Depth of solution is: ', curr.depth)
            return curr.node
        else:
            tempvar = current_node[1].node
            if str(tempvar) not in expanded_nodes:
                expanded_nodes.add(str(tempvar))
                expanded = expand_node(curr, tree, tree_id)
                expanded_nodes_count += 1
                curr_depth = curr.depth
                nodes = queueing_order(algo, nodes, curr.children, curr_depth, expanded_nodes)
                # print(current_node[1].children[0].node)
                tree_id += expanded[1]

    if len(nodes) == 0:
        print('Search failed. There is no solution to this puzzle!')


def main_menu():
    print('Welcome to 8 Puzzle Solver!')
    puzzle_type = input('Select (1) to try a default puzzle or (2) to input your own. \n')
    puzzle_type = int(puzzle_type)
    if puzzle_type == 1:
        the_puzzle = input('Select your default puzzle level. \n'
                     '(1) for Easy \n'
                     '(2) for Medium \n'
                     '(3) for Hard \n')
        the_puzzle = int(the_puzzle)
        if the_puzzle == 1:
            puzzle = depth_4
        elif the_puzzle == 2:
            puzzle = depth_16
        elif the_puzzle == 3:
            puzzle = depth_24
    elif puzzle_type == 2:
        custom = []
        the_puzzle = input('Input the first row with spaces between each number \n')
        puzzle = the_puzzle.split(" ")
        x = [int(puzzle[0]), int(puzzle[1]), int(puzzle[2])]
        custom.append(x)
        the_puzzle = input('Input the second row with spaces between each number \n')
        puzzle = the_puzzle.split(" ")
        x = [int(puzzle[0]), int(puzzle[1]), int(puzzle[2])]
        custom.append(x)
        the_puzzle = input('Input the third row with spaces between each number \n')
        puzzle = the_puzzle.split(" ")
        x = [int(puzzle[0]), int(puzzle[1]), int(puzzle[2])]
        custom.append(x)
        print('Here\'s the initial state:')
        print_puzzle(custom)
        puzzle = Board(custom)

    algo = input('Select your algorithm. \n'
                 '(1) for Uniform Cost \n'
                 '(2) for Misplaced Tile Heuristic \n'
                 '(3) for Manhattan Distance Heuristic \n')
    algo = int(algo)
    start = time.time()
    general_search(algo, puzzle, tree_id)
    end = time.time()
    elapsed = end - start
    print('time elapsed: ', elapsed)

main_menu()


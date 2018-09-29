import os
import time

import units


def rule_god(cell: bool, neighbors: int) -> bool:
    """
    godmode
    """
    return True


"""
cell: cell state; True or False
neighbors: number of alive neighbor cells, 0<=int<=9
"""


def rule_underpopulation(cell: bool, neighbors: int) -> bool:
    """
    Any live cell with fewer than two live neighbors dies,
    as if by under population.
    """
    assert bool(cell) is True
    return not (cell and neighbors < 2)


def rule_survive(cell: bool, neighbors: int) -> bool:
    """
    Any live cell with two or three live neighbors lives on
    to the next generation.
    """
    assert bool(cell) is True
    return cell and neighbors in (2, 3)


def rule_overpopulation(cell: bool, neighbors: int) -> bool:
    """
    Any live cell with more than three live neighbors dies,
    as if by overpopulation.
    """
    assert bool(cell) is True
    return not (cell and neighbors > 3)


def rule_reproduction(cell: bool, neighbors: int) -> bool:
    """
    Any dead cell with exactly three live neighbors becomes a live cell,
    as if by reproduction.
    """
    assert bool(cell) is False
    return not cell and neighbors == 3


def apply_rules(state: bool, neighbors: int, rules_for_alive: tuple,
                rules_for_dead: tuple, debug: bool = False) -> bool:
    '''Apply rules on the cell'''
    next_state = state
    if state:
        next_state = all(rule(state, neighbors) for rule in rules_for_alive)
    else:
        next_state = all(rule(state, neighbors) for rule in rules_for_dead)
    if debug:
        print((state, neighbors), '->', next_state)
    return next_state


def find_neighbors(world: tuple, cell_pos: tuple) -> int:
    '''Return the number of alive neighbors'''
    neighbors = []
    row, cell = cell_pos
    if row > 0:
        top = world[row-1][cell]
        neighbors.append(top)
    if row < (len(world)-1):
        bottom = world[row+1][cell]
        neighbors.append(bottom)
    if cell > 0:
        left = world[row][cell-1]
        neighbors.append(left)
    if cell < (len(world[row])-1):
        right = world[row][cell+1]
        neighbors.append(right)
    if row > 0 and cell > 0:
        top_left = world[row-1][cell-1]
        neighbors.append(top_left)
    if row > 0 and cell < (len(world[row])-1):
        top_right = world[row-1][cell+1]
        neighbors.append(top_right)
    if row < (len(world)-1) and cell > 0:
        bottom_left = world[row+1][cell-1]
        neighbors.append(bottom_left)
    if row < (len(world)-1) and cell < (len(world[row])-1):
        bottom_right = world[row+1][cell+1]
        neighbors.append(bottom_right)
    # print(cell_pos, neighbors)
    return sum(neighbors)


def change_world(world_state: tuple) -> tuple:
    '''Return the next state of the world'''
    new_world = []
    for i, row in enumerate(world_state):
        new_row = []
        for j, cell_state in enumerate(row):
            cell_pos = i, j
            neighbors = find_neighbors(world_state, cell_pos)
            cell_state_new = apply_rules(cell_state, neighbors,
                                         (rule_underpopulation,
                                          rule_survive,
                                          rule_overpopulation),
                                         (rule_reproduction,))
            # print(f'at {cell_pos}',
            # cell_state, neighbors, '->', int(cell_state_new))
            new_row.append(int(cell_state_new))
        new_world.append(tuple(new_row))
    return tuple(new_world)


def repr_cell(cell: bool) -> str:
    '''Return a representation of a cell'''
    return '@' if cell else '_'


def repr_world(world: tuple) -> str:
    '''Return a representation of a world'''
    world_repr = ''
    for row in world:
        world_repr += ''.join([repr_cell(cell) for cell in row])
        world_repr += '\n'
    return world_repr


def life(state: tuple, generations: int=50, pause_time: float=0.5) -> tuple:
    '''Update screen with the state of the world in each generation'''
    for gen_number in range(generations+1):
        os.system('clear')
        print(f'Gen: {gen_number}')
        print(repr_world(state))
        state = change_world(state)
        time.sleep(pause_time)
    return state


if __name__ == "__main__":
    assert rule_underpopulation(True, 0) is False
    assert rule_underpopulation(True, 1) is False
    assert rule_underpopulation(True, 2) is True
    assert rule_survive(True, 1) is False
    assert rule_survive(True, 2) is True
    assert rule_survive(True, 3) is True
    assert rule_overpopulation(True, 3) is True
    assert rule_overpopulation(True, 4) is False
    assert rule_reproduction(False, 0) is False
    assert rule_reproduction(False, 1) is False
    assert rule_reproduction(False, 2) is False
    assert rule_reproduction(False, 3) is True

    rules_for_alive = (
        rule_underpopulation,
        rule_survive,
        rule_overpopulation,
    )

    rules_for_dead = (rule_reproduction,)

    for neighbors in range(1, 5):
        state = False
        next_state = apply_rules(
            state,
            neighbors,
            rules_for_alive,
            rules_for_dead,
            debug=False)

    life(units.PULSAR, pause_time=0.1)
    # life(units.GLIDER, 30, 0.1)

    print('OK.')

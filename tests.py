from game_of_life import repr_cell
from game_of_life import rule_underpopulation
from game_of_life import rule_survive
from game_of_life import rule_overpopulation
from game_of_life import rule_reproduction
from game_of_life import repr_world
from game_of_life import find_neighbors


def test_repr_cell():
    assert(repr_cell(True) == '@')
    assert(repr_cell(False) == '_')


def test_rules():
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


def test_repr_world():
    world_repr = repr_world((
        (0, 1),
        (1, 0),
    ))
    expected = '_@\n@_\n'
    assert world_repr == expected


def test_find_neighbors():
    actual = find_neighbors(
        (
            (0, 1, 0),
            (0, 0, 1),
            (1, 1, 0),
        ),
        (1, 1)
    )
    expected = 4
    assert actual == expected


def test_find_neighbors2():
    world = (
        (0, 1, 0, 0, 1),
        (0, 0, 0, 0, 1),
        (0, 0, 0, 0, 0),
        (1, 1, 0, 0, 1),
    )
    assert find_neighbors(world, (0, 0)) == 6
    assert find_neighbors(world, (1, 0)) == 3
    assert find_neighbors(world, (3, 4)) == 3

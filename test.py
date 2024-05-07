from copy import copy
from unittest import TestCase

from gameoflife import GameOfLife


class TestGrid(TestCase):
    def setUp(self) -> None:
        N = 2 ** 3
        # [[0 1 1 0 1 1 1 1]
        #  [1 1 1 0 0 1 0 0]
        #  [0 0 0 1 0 1 1 0]
        #  [0 1 1 1 1 0 1 0]
        #  [1 0 1 1 0 1 1 0]
        #  [0 1 0 1 1 1 1 1]
        #  [0 1 0 1 1 1 1 0]
        #  [1 0 0 1 1 0 1 0]]
        self.game = GameOfLife(N, N)
        self.game.fill_random(0)

        self.game_2 = copy(self.game)

    def test_iterations(self):
        self.game.update_lazy()
        self.game_2.update()


        assert (self.game.grid == self.game_2.grid).all()

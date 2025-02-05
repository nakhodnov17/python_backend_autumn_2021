# pylint: disable=W0212,C0114,C0115,C0116

import io
import sys
import string
import unittest
from typing import List
from itertools import product
from contextlib import redirect_stdout

import numpy as np

from tictacgame import Player, StdinPlayer, TicTacGame
from tictacgame.utils import check_line, get_combinations, max_update_dict


class DeterministicPlayer(Player):
    def __init__(self, steps: List[str], name: str):
        super().__init__()

        self._idx = -1
        self.name = name
        self.steps = steps
        self.messages = []

    def set(self, message: str):
        self.messages.append(message)

    def step(self) -> str:
        self._idx += 1
        return self.steps[self._idx]


class TestTicTacToe(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.check_winner_tests = [(
            3, 3, 3,
            np.array([
                [1, 0, 0],
                [0, 0, 1],
                [2, 0, 0]
            ]), TicTacGame._GAME_CONTINUE
        ), (
            3, 3, 3,
            np.array([
                [1, 1, 2],
                [2, 2, 1],
                [1, 2, 1]
            ]), TicTacGame._GAME_DRAW
        ), (
            3, 3, 3,
            np.array([
                [0, 1, 2],
                [2, 2, 1],
                [2, 2, 1]
            ]), TicTacGame._PLAYER_01_TAG
        ), (
            3, 3, 3,
            np.array([
                [1, 1, 2],
                [2, 1, 1],
                [2, 2, 1]
            ]), TicTacGame._PLAYER_00_TAG
        ), (
            6, 6, 4,
            np.array([
                [0, 0, 0, 0, 0, 0],
                [1, 2, 0, 2, 0, 2],
                [0, 1, 2, 0, 0, 0],
                [0, 2, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 2, 0],
            ]), TicTacGame._PLAYER_00_TAG
        ), (
            6, 6, 4,
            np.array([
                [0, 0, 0, 0, 0, 0],
                [1, 2, 0, 2, 0, 2],
                [0, 2, 2, 0, 0, 2],
                [0, 2, 1, 1, 2, 0],
                [0, 0, 0, 2, 0, 0],
                [0, 0, 2, 0, 2, 0],
            ]), TicTacGame._PLAYER_01_TAG
        ), (
            6, 6, 4,
            np.array([
                [0, 0, 1, 1, 1, 1],
                [1, 2, 0, 2, 0, 2],
                [0, 2, 2, 0, 0, 2],
                [0, 2, 1, 1, 2, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 2, 0, 2, 0],
            ]), TicTacGame._PLAYER_00_TAG
        )]

    def test_get_combinations(self):
        self.assertListEqual(get_combinations(0, ''), [])
        with self.assertRaises(ValueError):
            get_combinations(1, '')

        for idx in range(10):
            self.assertListEqual(get_combinations(idx, 'a'), ['a' * (jdx + 1) for jdx in range(idx)])

        self.assertListEqual(get_combinations(0, 'ab'), [])
        self.assertListEqual(get_combinations(1, 'ab'), ['a'])
        self.assertListEqual(get_combinations(2, 'ab'), ['a', 'b'])
        self.assertListEqual(get_combinations(3, 'ab'), ['a', 'b', 'aa'])
        self.assertListEqual(get_combinations(4, 'ab'), ['a', 'b', 'aa', 'ab'])
        self.assertListEqual(get_combinations(5, 'ab'), ['a', 'b', 'aa', 'ab', 'ba'])
        self.assertListEqual(get_combinations(6, 'ab'), ['a', 'b', 'aa', 'ab', 'ba', 'bb'])
        self.assertListEqual(get_combinations(7, 'ab'), ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa'])

        self.assertListEqual(get_combinations(8, 'abcdefgh'), ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        self.assertListEqual(get_combinations(9, 'abcdefgh'), ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'aa'])
        self.assertListEqual(
            get_combinations(8 + 8 * 8, 'abcdefgh'),
            list(map(''.join, list(product('abcdefgh', repeat=1)) + list(product('abcdefgh', repeat=2))))
        )
        self.assertListEqual(
            get_combinations(8 + 8 * 8 + 1, 'abcdefgh'),
            list(map(''.join, list(product('abcdefgh', repeat=1)) + list(product('abcdefgh', repeat=2)))) +
            ['aaa']
        )

    def test_check_line(self):
        self.assertDictEqual(check_line([]), {})
        self.assertDictEqual(check_line([1]), {1: 1})
        self.assertDictEqual(check_line([1, 1, 1]), {1: 3})
        self.assertDictEqual(check_line([1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1]), {1: 3, 2: 3})
        self.assertDictEqual(check_line([1, 2, 3, 4, 5]), {1: 1, 2: 1, 3: 1, 4: 1, 5: 1})
        self.assertDictEqual(check_line([1, 2, 3, 4, 5, 1, 1, 1, 1]), {1: 4, 2: 1, 3: 1, 4: 1, 5: 1})

    def test_max_update_dict(self):
        self.assertDictEqual(max_update_dict({}, {}), {})
        self.assertDictEqual(max_update_dict({1: 1}, {}), {1: 1})
        self.assertDictEqual(max_update_dict({}, {1: 1}), {1: 1})
        self.assertDictEqual(max_update_dict({1: 2}, {1: 1}), {1: 2})
        self.assertDictEqual(max_update_dict({1: 2, 2: 3}, {1: 1, 3: 2}), {1: 2, 2: 3, 3: 2})
        self.assertDictEqual(max_update_dict({1: 2, 2: 3, 4: 5}, {1: 1, 3: 2, 4: 6}), {1: 2, 2: 3, 3: 2, 4: 6})

    def test_validate_input(self, n_rows: int = 3, n_columns: int = 3, n_marks: int = 3, seed=42):
        random_generator = np.random.default_rng(seed)

        game = TicTacGame(
            StdinPlayer(name='00'), StdinPlayer(name='01'),
            n_rows=n_rows, n_columns=n_columns, n_marks=n_marks
        )
        letters = get_combinations(2 * n_columns, string.ascii_lowercase)

        for _ in range(10):
            mask = random_generator.integers(0, 3, size=[n_rows, n_columns])
            game._field[mask == 0] = game._EMPTY_TAG
            game._field[mask == 1] = game._TIC_TAG
            game._field[mask == 2] = game._TAC_TAG
            for idx in range(-2 * n_rows, 2 * n_rows):
                for jdx in range(2 * n_columns):
                    input_line = f'{idx}{letters[jdx]}'
                    if 1 <= idx <= n_rows and 0 <= jdx < n_columns:
                        if mask[idx - 1, jdx] == 0:
                            self.assertTupleEqual(
                                game.validate_input(input_line), (idx - 1, jdx, game._VALIDATE_SUCCESS)
                            )
                        else:
                            self.assertTupleEqual(
                                game.validate_input(input_line), (None, None, game._VALIDATE_TAKEN_FIELD)
                            )
                    else:
                        self.assertTupleEqual(
                            game.validate_input(input_line), (None, None, game._VALIDATE_INVALID_FIELD)
                        )

        game._field = np.zeros([n_rows, n_columns], dtype=np.int32) + game._EMPTY_TAG
        game._field[0, 0] = game._TIC_TAG
        self.assertTupleEqual(game.validate_input('1a'), (None, None, game._VALIDATE_TAKEN_FIELD))
        game._field[0, 0] = game._TAC_TAG
        self.assertTupleEqual(game.validate_input('1a'), (None, None, game._VALIDATE_TAKEN_FIELD))

    def test___retrive_step(self, n_rows: int = 3, n_columns: int = 3, n_marks: int = 3):
        steps_00 = ['1a', '2n', '2b', '3c']
        steps_01 = ['2a', '1c']
        game = TicTacGame(
            DeterministicPlayer(steps_00, name='00'),
            DeterministicPlayer(steps_01, name='01'),
            n_rows=n_rows, n_columns=n_columns, n_marks=n_marks
        )

        mask = np.array([
            [1, 0, 0],
            [0, 0, 1],
            [2, 0, 0]
        ])
        game._field[mask == 0] = game._EMPTY_TAG
        game._field[mask == 1] = game._TIC_TAG
        game._field[mask == 2] = game._TAC_TAG

        self.assertTupleEqual(game._retrive_step(game.player_00), (None, None, game._VALIDATE_TAKEN_FIELD))
        self.assertTupleEqual(game._retrive_step(game.player_00), (None, None, game._VALIDATE_INVALID_FIELD))
        self.assertTupleEqual(game._retrive_step(game.player_00), (1, 1, game._VALIDATE_SUCCESS))
        self.assertTupleEqual(game._retrive_step(game.player_01), (1, 0, game._VALIDATE_SUCCESS))
        self.assertTupleEqual(game._retrive_step(game.player_00), (2, 2, game._VALIDATE_SUCCESS))
        self.assertTupleEqual(game._retrive_step(game.player_01), (0, 2, game._VALIDATE_SUCCESS))

    def test_check_winner(self):
        for idx, (n_rows, n_columns, n_marks, mask, target_state) in enumerate(self.check_winner_tests):
            with self.subTest(current_case=idx):
                game = TicTacGame(
                    DeterministicPlayer([], name='00'), DeterministicPlayer([], name='01'),
                    n_rows=n_rows, n_columns=n_columns, n_marks=n_marks
                )
                game._field[mask == 0] = game._EMPTY_TAG
                game._field[mask == 1] = game._TIC_TAG
                game._field[mask == 2] = game._TAC_TAG
                self.assertEqual(game.check_winner(), target_state)

    def test_apply_move(self):
        n_rows, n_columns, n_marks = 3, 3, 3
        game = TicTacGame(
            DeterministicPlayer([], name='00'), DeterministicPlayer([], name='01'),
            n_rows=n_rows, n_columns=n_columns, n_marks=n_marks
        )
        mask = np.array([
            [1, 0, 0],
            [0, 0, 1],
            [2, 0, 0]
        ])
        game._field[mask == 0] = game._EMPTY_TAG
        game._field[mask == 1] = game._TIC_TAG
        game._field[mask == 2] = game._TAC_TAG
        field = game._field.copy()
        field[0, 1] = game._TIC_TAG
        game.apply_move(0, 1)
        self.assertEqual(np.all(np.equal(game._field, field)), True)

        game._current_state = game._PLAYER_01_TAG
        game._field[mask == 0] = game._EMPTY_TAG
        game._field[mask == 1] = game._TIC_TAG
        game._field[mask == 2] = game._TAC_TAG
        field = game._field.copy()
        field[0, 1] = game._TAC_TAG
        game.apply_move(0, 1)
        self.assertEqual(np.all(np.equal(game._field, field)), True)

    def test_start_game(self):
        player_00 = DeterministicPlayer(['1a', '2b', '3c'], '00')
        player_01 = DeterministicPlayer(['2a', '2c'], '01')
        game = TicTacGame(player_00, player_01, n_rows=3, n_columns=3, n_marks=3)
        game.start_game()
        self.assertEqual(player_00.messages[-1].strip().split('\n')[-1], 'Congratulations Player 00. You won!')

        player_00 = DeterministicPlayer(['1a', '2a', '2b', '3c'], '00')
        player_01 = DeterministicPlayer(['2a', 'c2', '2c'], '01')
        game = TicTacGame(player_00, player_01, n_rows=3, n_columns=3, n_marks=3)
        game.start_game()
        self.assertEqual(
            player_00.messages[2].strip().split('\n')[0],
            'This field is already taken. Please, choose other position to go:'
        )
        self.assertEqual(
            player_01.messages[2].strip().split('\n')[0],
            'Invalid field name. Please, choose other position to go:'
        )
        self.assertEqual(
            player_00.messages[-1].strip().split('\n')[-1],
            'Congratulations Player 00. You won!'
        )
        self.assertEqual(
            player_01.messages[-1].strip().split('\n')[-1],
            'Player 01. You lose!'
        )

        player_00 = DeterministicPlayer(['1a', '3a', '1b', '2c', '3b'], '00')
        player_01 = DeterministicPlayer(['2b', '2a', '1c', '3c'], '01')
        game = TicTacGame(player_00, player_01, n_rows=3, n_columns=3, n_marks=3)
        game.start_game()
        self.assertEqual(
            player_00.messages[-1].strip().split('\n')[-1],
            'Player 00 game is over. It is a draw.'
        )
        self.assertEqual(
            player_01.messages[-1].strip().split('\n')[-1],
            'Player 01 game is over. It is a draw.'
        )

    def test_stdinPlayer(self):
        player = StdinPlayer(name='')

        oldstdin, sys.stdin = sys.stdin, io.StringIO('input test\r\n')
        with io.StringIO() as stdout_moc, redirect_stdout(stdout_moc):
            self.assertEqual(player.step(), 'input test')

            player.set('test message')
            self.assertEqual(stdout_moc.getvalue(), 'test message')
        sys.stdin = oldstdin


if __name__ == '__main__':
    unittest.main()

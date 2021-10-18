import string
from typing import Tuple
from collections import defaultdict

import regex
import numpy as np

from .utils import TicTacTable, get_combinations, max_update_dict, check_line, Player


class TicTacGame:
    _VALIDATE_TAKEN_FIELD = 0
    _VALIDATE_INVALID_FIELD = 1
    _VALIDATE_SUCCESS = 2

    _GAME_DRAW = -2
    _GAME_CONTINUE = -1
    _PLAYER_00_TAG = 0
    _PLAYER_01_TAG = 1

    _EMPTY_TAG = 0
    _TIC_TAG = 1
    _TAC_TAG = 2

    def __init__(self, player_00: Player, player_01: Player, n: int = 3, k: int = 3, p: int = 3):
        self.n = n
        self.k = k
        self.p = p
        self.player_00 = player_00
        self.player_01 = player_01

        self._field = np.empty([self.n, self.k], dtype=np.int32)
        self._field[:, :] = self._EMPTY_TAG

        self._current_state = self._PLAYER_00_TAG

        self._input_pattern = regex.compile(r'^(\d+)([a-z]+)$')

        self._letters = get_combinations(self.k, string.ascii_lowercase)
        self._letters_map = {letter: idx for idx, letter in enumerate(self._letters)}

    def show_board(self, draw_numbers: bool = True, draw_chars: bool = True) -> str:
        str_field = np.empty([2 * self.n + 1, 4 * self.k + 1], dtype=object)
        str_field[:, :] = TicTacTable.EMPTY_CHR

        str_field[0, 0] = TicTacTable.LT_ANGLE_DELIMETER
        str_field[-1, 0] = TicTacTable.LB_ANGLE_DELIMETER
        str_field[0, -1] = TicTacTable.RT_ANGLE_DELIMETER
        str_field[-1, -1] = TicTacTable.RB_ANGLE_DELIMETER

        str_field[1:-1:2, 0] = TicTacTable.L_SIDE_DELIMETER
        str_field[2:-1:2, 0] = TicTacTable.L_SIDE_CROSS_DELIMETER

        str_field[1:-1:2, -1] = TicTacTable.R_SIDE_DELIMETER
        str_field[2:-1:2, -1] = TicTacTable.R_SIDE_CROSS_DELIMETER

        str_field[0, 1:-1:4] = TicTacTable.T_SIDE_DELIMETER
        str_field[0, 2:-1:4] = TicTacTable.T_SIDE_DELIMETER
        str_field[0, 3:-1:4] = TicTacTable.T_SIDE_DELIMETER
        str_field[0, 4:-1:4] = TicTacTable.T_SIDE_CROSS_DELIMETER

        str_field[-1, 1:-1:4] = TicTacTable.B_SIDE_DELIMETER
        str_field[-1, 2:-1:4] = TicTacTable.B_SIDE_DELIMETER
        str_field[-1, 3:-1:4] = TicTacTable.B_SIDE_DELIMETER
        str_field[-1, 4:-1:4] = TicTacTable.B_SIDE_CROSS_DELIMETER

        str_field[1:-1:2, 4:-1:4] = TicTacTable.H_DELIMETER

        str_field[2:-1:2, 1:-1:4] = TicTacTable.V_DELIMETER
        str_field[2:-1:2, 2:-1:4] = TicTacTable.V_DELIMETER
        str_field[2:-1:2, 3:-1:4] = TicTacTable.V_DELIMETER
        str_field[2:-1:2, 4:-1:4] = TicTacTable.CROSS_DELIMETER

        str_field[1:-1:2, 2:-1:4][self._field == self._TIC_TAG] = TicTacTable.TIC_CHR
        str_field[1:-1:2, 2:-1:4][self._field == self._TAC_TAG] = TicTacTable.TAC_CHR

        field_lines = [''.join(line) for line in str_field]

        if draw_chars:
            field_lines.append(
                ' ' + ' '.join([
                    letter.center(3, ' ')
                    for letter in self._letters
                ]) + ' '
            )
        if draw_numbers:
            max_width = max(map(lambda x: len(str(x)), range(1, self.n + 1)))
            idx_format = '{0:>' + str(max_width) + '}'
            str_idxs = [
                ' ' * max_width
                if idx % 2 == 0 or draw_chars and idx + 1 == len(field_lines) else
                idx_format.format((idx + 1) // 2)
                for idx in range(len(field_lines))
            ]
            field_lines = [
                f'{str_idxs[idx]} {field_line}'
                for idx, field_line in enumerate(field_lines)
            ]

        return '\n'.join(field_lines)

    def validate_input(self, line: str) -> Tuple[int, int, int]:
        if self._input_pattern.match(line) is None:
            return None, None, self._VALIDATE_INVALID_FIELD

        first, second = self._input_pattern.findall(line)[0]
        if int(first) == 0 or second not in self._letters_map:
            return None, None, self._VALIDATE_INVALID_FIELD

        idx, jdx = int(first) - 1, self._letters_map[second]

        if 0 <= idx < self._field.shape[0] and 0 <= jdx < self._field.shape[0]:
            if self._field[idx, jdx] == self._EMPTY_TAG:
                return idx, jdx, self._VALIDATE_SUCCESS
            return None, None, self._VALIDATE_TAKEN_FIELD

        return None, None, self._VALIDATE_INVALID_FIELD

    def start_game(self):
        message = 'This is a Tic-tac-toe game!\n'
        while True:
            current_player = (
                self.player_00
                if self._current_state == self._PLAYER_00_TAG
                else self.player_01
            )

            other_player = (
                self.player_01
                if self._current_state == self._PLAYER_00_TAG
                else self.player_00
            )

            message += '\n' + self.show_board() + '\n'
            message += f'Player {current_player.name}. It`s your move. Please, enter position to go:' + '\n'
            message += '> '

            current_player.set(message)
            move_idx, move_jdx, success = self._retrive_step(current_player)
            while success != self._VALIDATE_SUCCESS:
                if success == self._VALIDATE_INVALID_FIELD:
                    message = 'Invalid field name. Please, choose other position to go:' + '\n'
                else:
                    message = 'This field is already taken. Please, choose other position to go:' + '\n'
                message += '> '

                current_player.set(message)
                move_idx, move_jdx, success = self._retrive_step(current_player)

            self.apply_move(move_idx, move_jdx)

            winner = self.check_winner()
            if winner == self._current_state:
                message = self.show_board() + '\n'
                message += f'Congratulations Player {current_player.name}. You won!' + '\n'
                current_player.set(message)

                message = self.show_board() + '\n'
                message += f'Player {other_player.name}. You lose!' + '\n'
                other_player.set(message)
                break
            if winner == self._GAME_DRAW:
                message = self.show_board() + '\n'
                message += f'Player {current_player.name} game is over. It is a draw.' + '\n'
                self.player_00.set(message)
                
                message = self.show_board() + '\n'
                message += f'Player {other_player.name} game is over. It is a draw.' + '\n'
                self.player_01.set(message)
                break

            self._current_state = (
                self._PLAYER_00_TAG
                if self._current_state == self._PLAYER_01_TAG
                else self._PLAYER_01_TAG
            )

            message = ''

    def apply_move(self, move_idx: int, move_jdx: int):
        if self._current_state == self._PLAYER_00_TAG:
            self._field[move_idx, move_jdx] = self._TIC_TAG
        else:
            self._field[move_idx, move_jdx] = self._TAC_TAG

    def check_winner(self) -> int:
        max_lengths = defaultdict(int)
        for idx in range(self._field.shape[0]):
            max_lengths = max_update_dict(max_lengths, check_line(self._field[idx]))
        for idx in range(self._field.shape[1]):
            max_lengths = max_update_dict(max_lengths, check_line(self._field[:, idx]))
        for idx in range(-self._field.shape[0] + 1, self._field.shape[1]):
            max_lengths = max_update_dict(max_lengths, check_line(self._field[::-1, :].diagonal(idx)))
        for idx in range(self._field.shape[1] - 1, -self._field.shape[0], -1):
            max_lengths = max_update_dict(max_lengths, check_line(self._field.diagonal(idx)))

        if max_lengths[self._TIC_TAG] >= self.p:
            return self._PLAYER_00_TAG
        if max_lengths[self._TAC_TAG] >= self.p:
            return self._PLAYER_01_TAG
        if np.all(self._field != self._EMPTY_TAG):
            return self._GAME_DRAW

        return self._GAME_CONTINUE

    def _retrive_step(self, player: Player) -> Tuple[int, int, int]:
        line = player.step()
        return self.validate_input(line)

"""
ticktackgame.utils
================
"""

from enum import Enum
from typing import Dict, List
from collections import defaultdict
from itertools import product, chain

import numpy as np


class BColors(str, Enum):
    """
    ASCII console color codes
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TicTacTable(str, Enum):
    """
    Unicode table symbols
    """
    TIC_CHR = BColors.OKGREEN + '\u00D7' + BColors.ENDC
    TAC_CHR = BColors.FAIL + '\u25CB' + BColors.ENDC
    EMPTY_CHR = ' '
    H_DELIMETER = '\u2506'
    V_DELIMETER = '\u2504'
    CROSS_DELIMETER = '\u253C'
    LT_ANGLE_DELIMETER = '\u250C'
    LB_ANGLE_DELIMETER = '\u2514'
    RT_ANGLE_DELIMETER = '\u2510'
    RB_ANGLE_DELIMETER = '\u2518'
    L_SIDE_DELIMETER = '\u2502'
    L_SIDE_CROSS_DELIMETER = '\u251C'
    R_SIDE_DELIMETER = '\u2502'
    R_SIDE_CROSS_DELIMETER = '\u2524'
    T_SIDE_DELIMETER = '\u2500'
    T_SIDE_CROSS_DELIMETER = '\u252C'
    B_SIDE_DELIMETER = '\u2500'
    B_SIDE_CROSS_DELIMETER = '\u2534'


def get_combinations(n_combs: int, values: str) -> List[str]:
    """
    Return first @n_combs lexigraphicly (w.r. to symbol indeces) mininal lines that consisted of @values elements
    :param int n_combs: Number of combinations to generate
    :param str values: Elements to generate combinations
    :return List[str]
    """
    if len(values) == 0:
        if n_combs == 0:
            return []
        raise ValueError(f'Cannot generate n={n_combs} combinations from empty set')

    if len(values) == 1:
        comb_deepth = n_combs
    else:
        comb_deepth = np.ceil(
            np.log(n_combs * (len(values) - 1) + len(values)) /
            np.log(len(values)) - 1
        ).astype(np.int32)
    combinations = sum((
        list(product(values, repeat=idx + 1))
        for idx in range(comb_deepth)
        ), start=[]
    )
    combinations = list(map(''.join, combinations))
    return combinations[:n_combs]


def check_line(values: List[int]) -> Dict[int, int]:
    """
    For each unique value in @values return maximum number of consecutive value elements
    :param List[int] values
    :return Dict[int, int]
    """
    max_length = defaultdict(int)
    current_value, current_len = None, -1
    for value in values:
        if current_value == value:
            current_len += 1
        else:
            if current_value is not None:
                max_length[current_value] = max(max_length[current_value], current_len)
            current_len = 1
            current_value = value
    if current_value is not None:
        max_length[current_value] = max(max_length[current_value], current_len)
    return max_length


def max_update_dict(left: Dict[int, int], right: Dict[int, int]) -> Dict[int, int]:
    """
    Join two dicts. For each key that presented in the both dicts return maximum of corresponding values
    :param Dict[int, int] left
    :param Dict[int, int] right
    :return Dict[int, int]
    """
    return defaultdict(int, {
        key: max(left.get(key, -np.inf), right.get(key, -np.inf))
        for key in chain(left.keys(), right.keys())
    })


class Player:
    """
    Abstract player class that can somehow interact with enviroment
    """

    def __init__(self):
        pass

    def set(self, message: str):
        """
        Get message from enviroment
        :param str message
        """
        raise NotImplementedError()

    def step(self) -> str:
        """
        Return action to the enviroment
        :return str
        """
        raise NotImplementedError()


class StdinPlayer(Player):
    """
    Player that reads input from stdin and sent it to the enviroment.
    Each message will be print to the stdout
    """

    def __init__(self, name):
        super().__init__()

        self.name = name

    def set(self, message):
        print(message, end='')

    def step(self):
        return input().strip()

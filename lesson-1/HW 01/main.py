import argparse
from tictacgame import TicTacGame, StdinPlayer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--n_rows', type=int, default=3)
    parser.add_argument('-k', '--n_columns', type=int, default=3)
    parser.add_argument('-p', '--n_marks', type=int, default=3)
    args = parser.parse_args()

    game = TicTacGame(
        StdinPlayer(name='00'), StdinPlayer(name='01'),
        n_rows=args.n_rows, n_columns=args.n_columns, n_marks=args.n_marks
    )
    game.start_game()

from ticktackgame import TicTacGame, StdinPlayer

if __name__ == '__main__':
    game = TicTacGame(StdinPlayer(name='00'), StdinPlayer(name='01'), n=2, k=2, p=2)
    game.start_game()

from ticktackgame import TicTacGame, StdinPlayer

if __name__ == '__main__':
    game = TicTacGame(StdinPlayer(name='00'), StdinPlayer(name='01'), n=3, k=3, p=3)
    game.start_game()

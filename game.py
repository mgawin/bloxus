import bloxusgame as bg

game = bg.Game()
game.show()
game.playerA.rotate(1)
game.move(game.playerA.put(1), 1, 1)
game.show()

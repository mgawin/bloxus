import bloxusgame as bg

game = bg.Game()
game.show()
game.playerA.rotate(1)
game.move(game.playerB.put(1), 0, 9)
game.show()

import bloxusgame as bg

game = bg.Game()
game.show()
game.playerA.rotate(1)
game.move(game.playerB.put(3), 5, 9)
game.show()
game.move(game.playerA.put(1), 9, 6)
game.show()

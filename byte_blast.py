from thumby import Sprite
from thumby import display


class Game:
    # BITMAP: width: 5, height: 5
    block_bit_map = bytearray([19, 6, 12, 25, 19])

    def __init__(self):
        self.board = [[False for _ in range(8)] for _ in range(8)]
        self.score = 0
        self.board[1][3] = True
        self.board[0][3] = True

        self.GRID_START = (0, 0)
        self.brick_sprite = Sprite(5, 5, block_bit_map)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col]:
                    # Col is X, Row is Y
                    self.brick_sprite.x = col * 5
                    self.brick_sprite.y = row * 5
                    display.drawSprite(self.brick_sprite)


game = Game()
display.setFPS(60)
while 1:
    # clear screen
    display.fill(0)

    # draw game
    game.draw_board()

    # thumby.display.drawText("HELLO WORLD", 15, 15)
    display.update()

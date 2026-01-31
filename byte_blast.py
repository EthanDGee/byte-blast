from thumby import Sprite
from thumby import display
from thumby import buttonA, buttonB
import random


# BITMAP: width: 5, height: 5
PLACED_BIT_MAP = bytearray([19, 6, 12, 25, 19])

# BITMAP: width: 5, height: 5
PIECE_BIT_MAP = bytearray([31, 17, 17, 17, 31])

SHAPE_KEYS = ("I", "O", "T", "S", "Z", "J", "L")
TETROMINOES = {
    "I": [(0, 1), (1, 1), (2, 1), (3, 1)],
    "O": [(1, 0), (2, 0), (1, 1), (2, 1)],
    "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
    "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
    "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
    "J": [(0, 0), (0, 1), (1, 1), (2, 1)],
    "L": [(2, 0), (0, 1), (1, 1), (2, 1)],
}


class Game:
    def __init__(self):
        self.board = [[False for _ in range(8)] for _ in range(8)]
        self.score = 0
        self.board[1][3] = True
        self.board[0][3] = True

        self.GRID_START = (0, 0)
        self.brick_sprite = Sprite(5, 5, PLACED_BIT_MAP)
        self.piece_sprite = Sprite(5, 5, PIECE_BIT_MAP)

        self.piece = self.get_random_piece()
        self.position = (3, 3)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col]:
                    # Col is X, Row is Y
                    self.brick_sprite.x = col * 5
                    self.brick_sprite.y = row * 5
                    display.drawSprite(self.brick_sprite)

    def draw_piece(self):
        for dx, dy in self.piece:
            # Calculate actual screen position
            self.piece_sprite.x = (self.position[0] + dx) * 5
            self.piece_sprite.y = (self.position[1] + dy) * 5
            display.drawSprite(self.piece_sprite)

    def rotate_piece(self, clock_wise):
        if clock_wise:
            new_shape = [(-dy, dx) for dx, dy in self.piece]
        else:
            new_shape = [(dy, -dx) for dx, dy in self.piece]

        if self.is_out_of_bounds(self.position[0], self.position[1], new_shape):
            self.piece = new_shape

    def is_out_of_bounds(self, col, row, shape):
        # Check if the move results tin the piece being out of bound
        for dx, dy in shape:
            new_col = col + dx
            new_row = row + dy
            # Check grid boundaries
            if new_col < 0 or new_col >= 8 or new_row < 0 or new_row >= 8:
                return False

        return True

    @staticmethod
    def get_random_piece():
        key = random.choice(SHAPE_KEYS)
        return TETROMINOES[key]


game = Game()
display.setFPS(60)
while 1:
    # clear screen
    display.fill(0)

    # draw game
    game.draw_board()
    game.draw_piece()

    # handle input
    if buttonA.justPressed():
        game.rotate_piece(clock_wise=True)
    if buttonB.justPressed():
        game.rotate_piece(clock_wise=False)

    # thumby.display.drawText("HELLO WORLD", 15, 15)
    display.update()

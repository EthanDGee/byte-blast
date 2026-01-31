from thumby import Sprite
from thumby import display
from thumby import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR
import random
import time

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

        if self.is_in_bounds(self.position[0], self.position[1], new_shape):
            self.piece = new_shape

    def move_piece(self, x_change, y_change):
        new_x = self.position[0] + x_change
        new_y = self.position[1] + y_change

        if self.is_in_bounds(new_x, new_y, self.piece):
            self.position = (new_x, new_y)

    def is_in_bounds(self, col, row, shape):
        # Check if the move results in the piece being out of bound
        for dx, dy in shape:
            new_col = col + dx
            new_row = row + dy
            # Check grid boundaries
            if new_col < 0 or new_col >= 8 or new_row < 0 or new_row >= 8:
                return False

        return True

    def piece_can_be_placed(self):
        for dx, dy in self.piece:
            x = self.position[0] + dx
            y = self.position[1] + dy

            if self.board[y][x]:
                return False

        return True

    def place_piece(self):
        if not self.piece_can_be_placed():
            return

        for dx, dy in self.piece:
            x = self.position[0] + dx
            y = self.position[1] + dy

            self.board[y][x] = True

        self.score_board()
        self.piece = self.get_random_piece()
        self.position = (3, 3)

    def score_board(self):
        row_scored = [True for _ in range(8)]
        col_scored = [True for _ in range(8)]

        for x in range(8):
            for y in range(8):
                # if they are true the entire row/col they are a full line
                col_scored[x] = col_scored[x] and self.board[x][y]
                row_scored[y] = row_scored[y] and self.board[x][y]

        # count total lines scored for cleaner code
        total_lines_scored = sum(row_scored) + sum(col_scored)

        # exit early if no lines scored
        if total_lines_scored == 0:
            return

        # calculate score
        self.score += int(total_lines_scored * 500 * (1.2**total_lines_scored))

        # clear the scored rows
        for y, full in enumerate(row_scored):
            if full:
                for x in range(8):
                    self.board[x][y] = False

        # clear the scored columns
        for x, full in enumerate(col_scored):
            if full:
                for y in range(8):
                    self.board[x][y] = False

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
        game.place_piece()

    if buttonB.justPressed():
        game.rotate_piece(clock_wise=False)

    if buttonU.justPressed():
        game.move_piece(0, -1)

    if buttonD.justPressed():
        game.move_piece(0, 1)

    if buttonL.justPressed():
        game.move_piece(-1, 0)

    if buttonR.justPressed():
        game.move_piece(1, 0)

    # thumby.display.drawText("HELLO WORLD", 15, 15)
    display.update()


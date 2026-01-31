from thumby import Sprite
from thumby import display
from thumby import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR
import random
import time

# Placed BITMAP checkerboard pattern: width: 5, height: 5
PLACED_BIT_MAP_A = bytearray([10, 21, 10, 21, 10])
PLACED_BIT_MAP_B = bytearray([21, 10, 21, 10, 21])

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
        self.game_over = False

        self.GRID_START = (0, 0)
        # 2 patterns 1 for each of the alternating patterns
        self.brick_sprite = Sprite(5, 5, PLACED_BIT_MAP_A + PLACED_BIT_MAP_B)
        self.piece = self.get_random_piece()
        self.position = (3, 3)
        self.queue = [self.get_random_piece() for _ in range(3)]

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col]:
                    # alternate between the block patterns to create checkerboard
                    if (row + col) % 2 == 0:
                        self.brick_sprite.setFrame(0)
                    else:
                        self.brick_sprite.setFrame(1)

                    # Col is X, Row is Y
                    self.brick_sprite.x = col * 5
                    self.brick_sprite.y = row * 5
                    display.drawSprite(self.brick_sprite)

    def draw_current_piece(self):
        for dx, dy in self.piece:
            # Calculate actual screen position
            x = (self.position[0] + dx) * 5
            y = (self.position[1] + dy) * 5
            display.drawRectangle(x, y, 5, 5, 1)

    @staticmethod
    def draw_queue_piece(piece, position):
        for dx, dy in piece:
            # Calculate actual screen position
            x = position[0] + (dx * 3)
            y = position[1] + (dy * 3)
            display.drawRectangle(x, y, 3, 3, 1)

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

        # move to next piece in queue
        self.piece = self.queue.pop(0)
        self.queue.append(self.get_random_piece())

        self.check_game_over()
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
        self.score += int(total_lines_scored * 5 * (1.2**total_lines_scored))

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

    def check_game_over(self):
        # loop over game board with piece in all 4 directions until a viable place spot is found

        starting_piece = self.piece
        starting_position = self.position

        has_valid_move = False

        for i in range(4):
            for x in range(8):
                for y in range(8):
                    if not self.is_in_bounds(x, y, self.piece):
                        continue

                    self.position = (x, y)
                    if self.piece_can_be_placed():
                        has_valid_move = True
                        break

                if has_valid_move:
                    break

            if has_valid_move:
                break

            # rotate piece
            self.piece = [(-dy, dx) for dx, dy in self.piece]

        # reset to earlier version
        self.piece = starting_piece
        self.position = starting_position

        self.game_over = not has_valid_move

    @staticmethod
    def get_random_piece():
        key = random.choice(SHAPE_KEYS)
        return TETROMINOES[key]


game = Game()
display.setFPS(60)
display.setFont("/lib/font3x5.bin", 3, 5, 1)

while not game.game_over:
    # clear screen
    display.fill(0)

    # draw game
    game.draw_board()
    game.draw_current_piece()

    # divider line (board takes up 40*40)
    display.drawLine(40, 0, 40, 40, 1)

    # Draw Scoreboard
    display.drawText("Score", 44, 3, 1)
    display.drawText(f"{game.score}", 44, 10, 1)

    # Draw queue pieces with diagonal spacing
    for i, piece in enumerate(game.queue):
        game.draw_queue_piece(piece, (44 + i * 7, 17 + i * 7))

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

    display.update()

# TODO: build a game over screen

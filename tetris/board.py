from colorama import init as colorama_init
from colorama import Fore
from .piece import Piece
from .bit import Bit

import random
import os


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return f"({self.x}, {self.y})"


class Board:

    def __init__(self, width, height, initial_piece: Piece):
        self.board_width = width
        self.board_height = height
        self.board = [
            [Bit() for _ in range(width)]
                for _ in range(height)
        ]
        self.active_piece = None
        self.next_piece = None
        self.score = 0
        self.spawn(piece=initial_piece)


    def spawn(self, piece: Piece):
        
        if piece == None:
            piece = Piece.pick_random()
            
        spawn_coordinate = random.randint(0, self.board_width - 4)
        self.active_piece = piece
        self.active_position = Coordinate(spawn_coordinate, 0)
            
        if self.next_piece == None:
            self.next_piece = Piece.pick_random()


    def collision(self, piece: Piece, offset=Coordinate(0, 0)):

        piece_data = piece._rotated
        new_position = self.active_position + offset

        piece_height = len(piece_data)
        piece_width = len(piece_data[0])

        if new_position.y + piece_height > self.board_height:
            return True
        if new_position.x < 0:
            return True
        if new_position.x + piece_width > self.board_width:
            return True
        
        for j, row in enumerate(piece_data):

            for i, bit in enumerate(row):

                if bit.empty:
                    continue

                if not self.board[new_position.y + j][new_position.x + i].empty:
                    return True
        
        return False


    def freeze(self, piece: Piece, position: Coordinate):
        
        if position.y < 2:
            self.game_over()
            
        piece_data = piece._rotated
        piece_height = len(piece_data)
        piece_width = len(piece_data[0])

        for j in range(piece_height):
            for i in range(piece_width):
                if not piece_data[j][i].empty:
                    self.board[position.y + j][position.x + i] = piece_data[j][i]


    def down(self):
        offset = Coordinate(0, 1)
        if not self.collision(self.active_piece, offset):
            self.active_position += offset


    def left(self):
        offset = Coordinate(-1, 0)
        if not self.collision(self.active_piece, offset):
            self.active_position += offset


    def right(self):
        offset = Coordinate(1, 0)
        if not self.collision(self.active_piece, offset):
            self.active_position += offset


    def rotate(self):
        self.active_piece.rotation = (self.active_piece.rotation + 90) % 360
        offset = self.fix_offbounds_rotation(self.active_piece)
        self.active_position += offset


    def new_frame(self):
        if self.collision(self.active_piece, Coordinate(0, 1)):
            self.freeze(self.active_piece, self.active_position)
            self.check_full_rows()
            next_piece = self.next_piece
            self.next_piece = None
            self.spawn(piece=next_piece)
        print(chr(27) + "[2J")
        print(self)
        
    
    def game_over(self):
        print(chr(27) + "[2J")
        print(self)
        print("--------- GAME OVER ---------")
        os._exit(0)


    def melt(self, row: int):
        self.board.pop(row)
        self.board = [
            [Bit() for _ in range(self.board_width)],
            *[r for r in self.board],
        ]


    def check_full_rows(self):
        score_multiplier = 1
        for j in range(self.board_height):
            is_row_full = True
            for i in range(self.board_width):
                if self.board[j][i].empty:
                    is_row_full = False
                    break
            if is_row_full:
                self.melt(j)
                self.score += score_multiplier
                score_multiplier += 1


    def fix_offbounds_rotation(self, piece: Piece):
        piece_data = piece._rotated
        piece_width = len(piece_data[0])
        offset = max(self.active_position.x + piece_width - self.board_width, 0)
        return Coordinate(-offset, 0) 


    def __str__(self):
        rows = []
        rows.append(f"Next piece:\n{str(self.next_piece)}")
        for j in range(self.board_height):
            row = f"{j:02d} "
            for i in range(self.board_width):
                bit = self.board[j][i]
                active_piece = self.active_piece._rotated
                piece_width = len(active_piece[0])
                piece_height = len(active_piece)
                if (
                    (self.active_position.x <= i < (self.active_position.x + piece_width))
                    and
                    (self.active_position.y <= j < (self.active_position.y + piece_height))
                    and
                    (bit.empty)
                ):
                    piece_x = i - self.active_position.x
                    piece_y = j - self.active_position.y
                    row += str(active_piece[piece_y][piece_x]) # .color + 2*Bit.SQ + Fore.RESET
                else:
                    row += str(bit)

            rows.append(row)
            
        rows.append('    0 1 2 3 4 5 6 7 8 9')
        rows.append(f"Score: {self.score}")

        return '\n'.join(rows)


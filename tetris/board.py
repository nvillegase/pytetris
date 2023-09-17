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
        self.width = width
        self.height = height
        self.board = [
            [Bit(False, Fore.BLACK) for _ in range(width)]
                for _ in range(height)
        ]
        self.active_piece = None
        self.next_piece = None
        self.score = 0
        self.spawn(piece=initial_piece)


    def spawn(self, piece: Piece):
        
        if piece == None:
            piece = Piece.pick_random()
            
        spawn_coordinate = random.randint(0, self.width - 4)
        self.active_piece = piece
        self.active_position = Coordinate(spawn_coordinate, 0)
            
        if self.next_piece == None:
            self.next_piece = Piece.pick_random()


    def collision(self, piece: Piece, offset: Coordinate):

        piece_data = piece._rotated
        new_position = self.active_position + offset

        piece_height = len(piece_data)
        piece_width = len(piece_data[0])

        if new_position.y + piece_height > self.height:
            return True
        if new_position.x < 0:
            return True
        if new_position.x + piece_width > self.width:
            return True
        
        for j, row in enumerate(piece_data):

            for i, bit in enumerate(row):

                if not bit.occupied:
                    continue

                if self.board[new_position.y + j][new_position.x + i].occupied:
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
                if piece_data[j][i].occupied:
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
            [Bit() for _ in range(self.width)],
            *[r for r in self.board],
        ]


    def check_full_rows(self):
        score_multiplier = 1
        for j in range(self.height):
            is_full = True
            for i in range(self.width):
                if not self.board[j][i].occupied:
                    is_full = False
                    break
            if is_full:
                self.melt(j)
                self.score += score_multiplier
                score_multiplier += 1


    def __str__(self):
        rows = []
        rows.append(f"Next piece:\n{str(self.next_piece)}")
        for j in range(self.height):
            row = f"{j:02d} "
            for i in range(self.width):
                bit = self.board[j][i]
                active_piece = self.active_piece._rotated
                piece_width = len(active_piece[0])
                piece_height = len(active_piece)

                if (
                    (self.active_position.x <= i < (self.active_position.x + piece_width))
                    and
                    (self.active_position.y <= j < (self.active_position.y + piece_height))
                    and
                    (not bit.occupied)
                ):
                    piece_x = i - self.active_position.x
                    piece_y = j - self.active_position.y
                    row += active_piece[piece_y][piece_x].color + 2*Bit.SQ + Fore.RESET
                else:
                    if bit.occupied:
                        row += bit.color + 2*Bit.SQ + Fore.RESET
                    else:
                        row += bit.color + 2*Bit.SQ + Fore.RESET

            rows.append(row)
            
        rows.append('    0 1 2 3 4 5 6 7 8 9')
        rows.append(f"Score: {self.score}")
        

        return '\n'.join(rows)


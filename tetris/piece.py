from colorama import Fore
from .bit import Bit
from enum import Enum

import random


class PieceType(Enum):
    L = 'L'
    O = 'O'
    S = 'S'
    I = 'I'
    T = 'T'
    Z = 'Z'


class Piece:

    def __init__(self, piece_type: PieceType, rotation):
        
        if piece_type == PieceType.L.value:
            color = Fore.YELLOW
            self.repr = [
                [Bit(), Bit(), Bit(True, color)],
                [Bit(True, color), Bit(True, color), Bit(True, color)]]
        elif piece_type == PieceType.O.value:
            color = Fore.RED
            self.repr = [
                [Bit(True, color), Bit(True, color)],
                [Bit(True, color), Bit(True, color)]
            ]
        elif piece_type == PieceType.S.value:
            color = Fore.GREEN
            self.repr = [
                [Bit(), Bit(True, color), Bit(True, color)],
                [Bit(True, color), Bit(True, color), Bit()]
            ]
            
        elif piece_type == PieceType.I.value:
            color = Fore.BLUE
            self.repr = [
                [Bit(True, color), Bit(True, color), Bit(True, color), Bit(True, color)]
            ]
        
        elif piece_type == PieceType.T.value:
            color = Fore.CYAN
            self.repr = [
                [Bit(), Bit(True, color), Bit()],
                [Bit(True, color), Bit(True, color), Bit(True, color)]
            ]
            
        elif piece_type == PieceType.Z.value:
            color = Fore.WHITE
            self.repr = [
                [Bit(True, color), Bit(True, color), Bit()],
                [Bit(), Bit(True, color), Bit(True, color)]
            ]
            
        self.piece_type = piece_type
        
        if rotation not in [0, 90, 180, 270]:
            raise ValueError('Invalid rotation')
        
        self.rotation = rotation


    @property
    def _rotated(self):
        if self.rotation == 0:
            rotated = self.repr
        elif self.rotation == 270:
            rotated = self.__r90(self.repr)
        elif self.rotation == 180:
            rotated = self.__r90(self.__r90(self.repr))
        elif self.rotation == 90:
            rotated = self.__r90(self.__r90(self.__r90(self.repr)))
        return rotated
    
    
    def __r90(self, piece):
        
        height = len(piece)
        width = len(piece[0])
        rotated = []
        
        for i in range(width):
            row = []
            for j in range(height):
                row.append(piece[j][i])
            rotated.append(row)
            
        return rotated[::-1]


    @classmethod
    def pick_random(cls):
        rand_type = random.choice([t.value for t in PieceType])
        rand_rotation = random.choice([0, 90, 180, 270])
        return Piece(piece_type=rand_type, rotation=rand_rotation)


    def __str__(self):
        piece_str = ''
        for row in self._rotated:
            row_str = ''.join(str(bit) for bit in row)                
            piece_str += row_str + '\n'
        return piece_str

from tetris.piece import Piece
from tetris.board import Board

from time import sleep

from getkey import getkey, keys
import threading


def step():
    while True:
        board.down()
        board.new_frame()
        sleep(1)


board = Board(10, 15, initial_piece=Piece.pick_random())


if __name__ == '__main__':
    
    step_thread = threading.Thread(target=step)
    step_thread.start()
    
    while True:
        key = getkey(blocking=True)
        if key == keys.UP:
            board.rotate()
        elif key == keys.LEFT:
            board.left()
        elif key == keys.RIGHT:
            board.right()
        elif key == keys.DOWN:
            board.down()
        board.new_frame()

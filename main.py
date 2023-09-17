from tetris.piece import Piece
from tetris.board import Board

from time import sleep

import keyboard
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
        event = keyboard.read_event()
        if not event.event_type == keyboard.KEY_DOWN:
            continue
        if event.name == 'left':
            board.left()
        elif event.name == 'right':
            board.right()
        elif event.name == 'up':
            board.rotate()
        elif event.name == 'down':
            board.down()
        board.new_frame()

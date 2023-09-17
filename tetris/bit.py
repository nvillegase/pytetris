from colorama import Fore

class Bit:


    SQ = "▓"


    def __init__(
            self,
            color: Fore = Fore.BLACK
        ):
        self.color = color


    @property
    def empty(self):
        return self.color == Fore.BLACK


    def __str__(self):
        return self.color + 2*Bit.SQ + Fore.RESET

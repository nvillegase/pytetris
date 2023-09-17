from colorama import Fore

class Bit:
    
    SQ = "▓"
    
    def __init__(
            self,
            occupied: bool = False,
            color: Fore = Fore.BLACK
        ):
        self.occupied = occupied
        self.color = color
    
    def __str__(self):
        return self.color + 2*Bit.SQ + Fore.RESET

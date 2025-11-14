

class GameState:
    puzzlestate:int
    changed:bool

    def __init__(self):
        self.puzzlestate = 0
        self.changed = 0
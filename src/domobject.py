import pygame
from pygame.locals import *
from pygame.math import Vector2
from gamestate import GameState
from text import Text
from visibleobject import VisibleObject

class DomObject(VisibleObject):

    gamestate:GameState
    tile:pygame.Surface

    def __init__(self, gamestate:GameState, properties:dict, tile:pygame.Surface, position:Vector2, size:Vector2):
        super().__init__()
        self.tile = tile
        self.properties = properties
        self.position = position
        self.size = size
        self.gamestate = gamestate

    def render(self, dest_surf, viewoffset:Vector2):
        dest_surf.blit(self.tile, self.position - viewoffset)

    def talk(self) -> Text:
        g = self.gamestate.puzzlestate
        if g == 1 or g == 0:
            if g == 1:
                self.gamestate.puzzlestate = 2
            self.gamestate.changed = True
            return "Have you asked mum?"
        elif g == 2:
            self.gamestate.puzzlestate = 2
            self.gamestate.changed = True
            return "I told you, ask your mum!"
        elif g == 4:
            self.gamestate.puzzlestate = 5
            self.gamestate.changed = True
            return "You win!"
        elif g == 5:
            return "I told you, you won!"

    @property
    def enabled(self) -> bool:
        if 'enable' in self.properties:
            pp = str.split(self.properties['enable'], '=')
            if len(pp) == 2:
                (p,v) = pp
                if p == 'puzzlestate' and str(self.gamestate.puzzlestate) in str.split(v, ','):
                    return True
        
        return False



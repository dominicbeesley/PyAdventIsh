import pygame
from pygame.locals import *
from pygame.math import Vector2
from text import Text
from visibleobject import VisibleObject

class StaceyObject(VisibleObject):

    tile:pygame.Surface

    def __init__(self, tile:pygame.Surface, position:Vector2, size:Vector2):
        super().__init__()
        self.tile = tile
        self.position = position
        self.size = size

    def render(self, dest_surf, viewoffset:Vector2):
        dest_surf.blit(self.tile, self.position - viewoffset)

    def talk(self) -> Text:
        return "I'm stacey, poop poop!"


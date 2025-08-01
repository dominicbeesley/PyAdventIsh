import pygame
from pygame.locals import *
from pygame.math import Vector2

class Player:
    def __init__(self, tiles:pygame.Surface, position:Vector2, collmask:pygame.mask):
        self.tiles = tiles
        self.position = position
        self.orientation = Vector2(0,0)
        self.aniframe = 0
        self.collmask = collmask

    def render(self, dest_surf, viewoffset:Vector2):

        r = 0
        if self.orientation.y > 0:
            r = 0
        elif self.orientation.y < 0:
            r = 2
        elif self.orientation.x > 0:
            r = 1
        elif self.orientation.x < 0:
            r = 3

        dest_surf.blit(self.tiles, self.position - viewoffset, pygame.Rect(((self.aniframe // 5) % 4)*16, 6 + r * 32, 16, 24))

    def update(self, moveVector: Vector2, scene_collmask:pygame.mask) -> bool:
        new_position = self.position + moveVector

        bump = False
        if not scene_collmask.overlap(self.collmask, new_position):
            self.position = new_position
        else:
            if moveVector.x != 0 and moveVector.y != 0:
                new_position.x = self.position.x + moveVector.x
                new_position.y = self.position.y
                if not scene_collmask.overlap(self.collmask, new_position):
                    self.position = new_position
                else:
                    new_position.x = self.position.x
                    new_position.y = self.position.y + moveVector.y
                    if not scene_collmask.overlap(self.collmask, new_position):
                        self.position = new_position
                    else:
                        bump = True                        
            else:
                bump = True
    
        if (moveVector.x != 0) or (moveVector.y != 0):
            self.orientation = Vector2(moveVector)
            self.aniframe = self.aniframe + 1

        if bump:
            print("bump")
        return bump
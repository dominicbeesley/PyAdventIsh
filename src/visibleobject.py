from __future__ import annotations
from abc import ABC, abstractmethod
import pygame
from pygame.locals import *
from pygame.math import Vector2
from renderable import Renderable
from text import Text

class VisibleObject(Renderable, ABC):
    pass

    position:Vector2
    size:Vector2

    @property
    def rect(self) -> pygame.Rect:
        return Rect(self.position, self.size)
    
    @staticmethod
    def cmp_position(a:VisibleObject, b:VisibleObject):
        if a.position.y > b.position.y:
            return 1
        elif a.position.y < b.position.y:
            return -1
        else:
            if a.position.x > b.position.x:
                return 1
            elif a.position.x < b.position.x:
                return -1
            else:
                return 0
            
    @abstractmethod
    def talk(self) -> str:
        pass

    @property
    @abstractmethod
    def enabled(self) -> bool:
        pass

from abc import ABC, abstractmethod
import pygame
from pygame.locals import *
from pygame.math import Vector2

class Renderable(ABC):
    @abstractmethod
    def render(self, dest_surf, viewoffset:Vector2):
        ...
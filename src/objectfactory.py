

from pygame import Surface, Vector2
from domobject import DomObject
from gamestate import GameState
from staceyobject import StaceyObject
from visibleobject import VisibleObject


class ObjectFactory:
    
    @staticmethod
    def Create(gamestate:GameState, type:str, properties:dict, image:Surface, pos:Vector2, size:Vector2) -> VisibleObject:
        if type == "stacey":
            return StaceyObject(gamestate, properties, image, pos, size)
        elif type == "dom":
            return DomObject(gamestate, properties, image, pos, size)
        else:
            return None

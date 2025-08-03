import re
from typing import Tuple
import pygame
from pygame.locals import *
from pygame.font import *

class Text:
    def __init__(self, message:str, fontSize:int, renderSize:Tuple[float, float]):
        self.renderSize = renderSize
        self.fontSize = fontSize
        self.font = Font(None, fontSize)
        self.message = message
        #split into words as prelude to wordwrap
        words = [x for x in re.split(r'(\ +|\n|\t+)', message) if x and not x.startswith(' ')]

        self.lines = []
        line = ''
        for w in words:
            if w == '\n':
                self.lines.append(line)
                line = ''
            else:
                if line:
                    nl = line + ' ' + w
                else:
                    nl = w
                (sx, sy) = self.font.size(nl)
                if sx > renderSize[0]:
                    self.lines.append(line)
                    #check if word is too big
                    while w:
                        (sx, sy) = self.font.size(w)
                        if sx > renderSize[0]:
                            for n in range(len(w),1,-1):
                                if n == len(w):
                                    ww = w
                                else:
                                    ww = w[0:n] + '-'
                                (sx, sy) = self.font.size(ww)
                                if sx < renderSize[0] or n == 1:
                                    self.lines.append(ww)
                                    w = w[n:]
                                    break                                
                        else:
                            line = w
                            w = None
                else:
                    line = nl

        if line:
            self.lines.append(line)


        self.foreColour = (255, 255, 255)
        self.backColour = (0,0,0)


    def render(self, surface:pygame.Surface, dest:Tuple[float, float]):
        x,y = dest
        for l in self.lines:
            ts = self.font.render(l, True, self.foreColour, self.backColour)
            surface.blit(ts, (x, y))
            y = y + ts.get_height()
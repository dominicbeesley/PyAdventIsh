import pygame
from pygame.locals import *
from player import Player
from pygame.math import Vector2

import pytmx


DISP_WIDTH=160
DISP_HEIGHT=256
DISP_SCALE_X=4
DISP_SCALE_Y=2
FPS=50

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.buffer_size = self.buffer_width, self.buffer_height = DISP_WIDTH, DISP_HEIGHT
        self.scaled_size = self.scaled_width, self.scaled_height = DISP_WIDTH*DISP_SCALE_X, DISP_HEIGHT*DISP_SCALE_Y
        self.playerMoveVector = Vector2()

 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.scaled_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.buffer_surf = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
        self.ishchar_tiles = pygame.image.load("ish1.png")
        self.clock = pygame.time.Clock()
        
        #TODO: make a better payermask
        pms = pygame.Surface((16, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(pms, (0,0,0), pygame.Rect(0,16,16,8))
        playermask = pygame.mask.from_surface(pms)
        
        self.player = Player(self.ishchar_tiles,Vector2(64,168), playermask)

        self.loadmap("ishnew")
        self.aniframe = 0
        self._running = True


    def loadmap(self, mapname):
        
        self.tmxdata = pytmx.util_pygame.load_pygame(f"maps/{mapname}.tmx")

        self.tilewidth_px = self.tmxdata.tilewidth      
        self.tileheight_px = self.tmxdata.tileheight    
        self.scenewidth = self.tmxdata.width            
        self.sceneheight = self.tmxdata.height          
        self.scenewidth_px = self.tmxdata.width * self.tilewidth_px
        self.sceneheight_px = self.tmxdata.height * self.tileheight_px

        self.back_surf = pygame.Surface((self.scenewidth_px, self.sceneheight_px))
        self.under_surf = pygame.Surface((self.scenewidth_px, self.sceneheight_px), pygame.SRCALPHA)
        self.over_surf = pygame.Surface((self.scenewidth_px, self.sceneheight_px), pygame.SRCALPHA)
        coll_surf = pygame.Surface((self.scenewidth_px, self.sceneheight_px), pygame.SRCALPHA)

        self.objects = self.tmxdata.layers[3]
        for x,y,gid, in self.tmxdata.layers[0]:
            tile = self.tmxdata.get_tile_image_by_gid(gid)
            if tile:
                self.back_surf.blit(tile, (x * self.tilewidth_px, y * self.tileheight_px))
        
        for x,y,gid, in self.tmxdata.layers[1]:
            tile = self.tmxdata.get_tile_image_by_gid(gid)
            tilep = self.tmxdata.get_tile_properties_by_gid(gid)
            if tile:                
                if tilep and 'nocollide' in tilep:
                    self.over_surf.blit(tile, (x * self.tilewidth_px, y * self.tileheight_px))
                else:
                    self.under_surf.blit(tile, (x * self.tilewidth_px, y * self.tileheight_px))
                
        for x,y,gid, in self.tmxdata.layers[2]:
            tile = self.tmxdata.get_tile_image_by_gid(gid)
            if tile:
                coll_surf.blit(tile, (x * self.tilewidth_px, y * self.tileheight_px))


        self.coll_mask = pygame.mask.from_surface(coll_surf)

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_RIGHT:
                self.playerMoveVector.x = 1
            elif event.key == pygame.K_LEFT:
                self.playerMoveVector.x = -1
            elif event.key == pygame.K_DOWN:
                self.playerMoveVector.y = 1
            elif event.key == pygame.K_UP:
                self.playerMoveVector.y = -1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_RIGHT:
                self.playerMoveVector.x = 0
            elif event.key == pygame.K_LEFT:
                self.playerMoveVector.x = 0
            elif event.key == pygame.K_DOWN:
                self.playerMoveVector.y = 0
            elif event.key == pygame.K_UP:
                self.playerMoveVector.y = 0

    def on_loop(self):
        self.bump = self.player.update(self.playerMoveVector, self.coll_mask)
        self.clock.tick(FPS)      

        p_rect = pygame.Rect(self.player.position.x, self.player.position.y, self.tilewidth_px, self.tileheight_px)
        for o in self.objects:
            o_rect = pygame.Rect(o.x, o.y, o.width, o.height)
            if o_rect.colliderect(p_rect):
                if o.type == "teleport" and 'teleport' in o.properties:
                    #decode teleport property
                    teleport_str = o.properties['teleport']
                    (dest, dest_x, dest_y) = teleport_str.split(',')
                    self.loadmap(dest)
                    self.player.position.x = int(dest_x)*self.tilewidth_px
                    self.player.position.y = int(dest_y)*self.tileheight_px
                    print("teleport")


    def on_render(self):

        dw2 = DISP_WIDTH // 2
        dh2 = DISP_HEIGHT // 2

        viewoffset = self.player.position - Vector2(dw2, dh2)
        if viewoffset.x >= self.scenewidth_px - DISP_WIDTH:
            viewoffset.x =self.scenewidth_px - 1 - DISP_WIDTH 
        if viewoffset.x < 0:
            viewoffset.x = 0

        if viewoffset.y >= self.sceneheight_px - DISP_HEIGHT:
            viewoffset.y =self.sceneheight_px - 1 - DISP_HEIGHT 
        if viewoffset.y < 0:
            viewoffset.y = 0

        self.buffer_surf.fill((128,100,0), Rect(0,0,DISP_WIDTH, DISP_HEIGHT))
        self.buffer_surf.blit(self.back_surf, -viewoffset)
        self.buffer_surf.blit(self.under_surf, -viewoffset)
        self.player.render(self.buffer_surf, viewoffset)
        self.buffer_surf.blit(self.over_surf, -viewoffset)
        
#        yy = ((self.player.position.y + 20) // self.tileheight_px) * self.tileheight_px
#        self.buffer_surf.blit(self.over_surf, (-viewoffset.x , -viewoffset.y + yy), pygame.Rect(0, yy, self.scenewidth_px, self.sceneheight_px - yy))

        if self.bump and (self.aniframe % 2):
            t = self.player.collmask.to_surface(setcolor=(255,0,0), unsetcolor=None)
            t2 = self.coll_mask.to_surface(setcolor=(128,128,0,128), unsetcolor=None)
            self.buffer_surf.blit(t2, -viewoffset)
            self.buffer_surf.blit(t, self.player.position - viewoffset)

        pygame.transform.scale(self.buffer_surf, self.scaled_size, self._display_surf)
        pygame.display.flip()
        
        self.aniframe = self.aniframe + 1

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()


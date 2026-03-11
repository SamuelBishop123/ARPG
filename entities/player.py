import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.topleft= (x,y)
    def update(self,collisions):
        keys=pygame.key.get_pressed()
        dx=0
        dy=0
        if keys[pygame.K_UP]:
            dy-=PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            dy+=PLAYER_SPEED
        if keys[pygame.K_LEFT]:
            dx-=PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            dx+=PLAYER_SPEED
        self.move(dx,dy,collisions)
    def move(self, dx, dy, collisions):
        self.rect.x += dx
        for wall in collisions:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                if dx < 0:
                    self.rect.left = wall.right
        self.rect.y += dy
        for wall in collisions:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top   
                if dy < 0:
                    self.rect.top = wall.bottom   
        
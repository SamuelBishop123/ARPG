import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x,y,direction,speed=1,damage=10):
        super().__init__()
        self.image=pygame.image.load("Asset/Weapons/Shuriken.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(8,8))
        self.rect=self.image.get_rect(center=(x,y))
        self.direction=direction
        self.speed=speed
        self.damage=damage
        self.vx=0
        self.vy=0
        if direction=="right":
            self.vx=speed
        elif direction=="left":
            self.vx=-speed
        elif direction=="up":
            self.vy=-speed
        elif direction=="down":
            self.vy=speed
    def update(self):
        self.rect.x+=self.vx
        self.rect.y+=self.vy
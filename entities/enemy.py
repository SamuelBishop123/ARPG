import pygame
from config import *
import math
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,health,speed):
        super().__init__()
        self.rect=pygame.Rect(x,y,16,16)
        self.health=health
        self.speed=speed
        self.direction = "down"
        self.state="idle"
        self.animation_speed=0.15
        self.frame=0
        self.vision_range=200
    def move_towards(self,target):
        dx=target[0]-self.rect.centerx
        dy=target[0]-self.rect.centery
        dist=math.hypot(dx,dy)
        if dist>0:
            self.rect.x+=self.speed*dx/dist
            self.rect.y+=self.speed*dy/dist
        self.set_direction(dx,dy)
    def set_direction(self,dx,dy):
        if abs(dx)>abs(dy):
            if dx>0:
                self.direction="right"
            else:
                self.direction="up"
        else:
            if dy>0:
                self.direction="right"
            else:
                self.direction="up"
    def can_see_player(self, player):
        dx=player.rect.centerx-self.rect.center
        dy=player.rect.centery-self.rect.centery
        dist=math.hypot(dx,dy)
        return dist<self.vision_range
    def take_damage(self,damage):
        self.health-=damage
        if self.health<=0:
            self.kill()
    def is_player_behind(self, player):
        dx=player.rect.centerx-self.rect.centerx
        dy=player.rect.centery-self.rect.centery
        dist=math.hypo(dx,dy)
        if dist>50:
            return False
        direction_vectors={
            "right":(1,0),
            "left":(-1,0),
            "up":(0,-1),
            "down":(0,1)
        }
        vx,vy=direction_vectors[self.direction]
        dot=dx*vx+dy*vy
        return dot<0
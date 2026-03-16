import pygame
from config import *
import math
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,health,speed,vision_range,damage):
        super().__init__()
        self.rect=pygame.Rect(x,y,16,16)
        self.health=health
        self.speed=speed
        self.direction = "down"
        self.state="idle"
        self.animation_speed=0.15
        self.frame=0
        self.vision_range=vision_range
        self.attack_range=35
        self.attack_damage=10
        self.attack_cooldown=800
        self.last_attack=0
        self.attacking=False
        self.attack_timer=0
        self.damage=damage
    def move_towards(self,target,stop_distance):
        dx=target[0]-self.rect.centerx
        dy=target[1]-self.rect.centery
        dist=math.hypot(dx,dy)
        if dist>stop_distance:
            self.rect.x+=self.speed*dx/dist
            self.rect.y+=self.speed*dy/dist
            self.state="walk"
        else:
            self.state="idle"
        self.set_direction(dx,dy)
    def set_direction(self,dx,dy):
        if abs(dx)>abs(dy):
            if dx>0:
                self.direction="right"
            else:
                self.direction="left"
        else:
            if dy>0:
                self.direction="down"
            else:
                self.direction="up"
    def take_damage(self,damage,player):
        if self.dead:
            return
        self.health-=damage
        dx=self.rect.centerx-player.rect.centerx
        dy=self.rect.centery-player.rect.centery
        dist=math.hypot(dx,dy)
        if dist!=0:
            knockback=20
            self.rect.x+=(dx/dist)*knockback
            self.rect.y+=(dy/dist)*knockback
        if self.health<=0:
            self.dead=True
            self.state="death"
    def is_player_behind(self, player):
        dx=player.rect.centerx-self.rect.centerx
        dy=player.rect.centery-self.rect.centery
        dist=math.hypot(dx,dy)
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
    def attack_player(self,player):
        now=pygame.time.get_ticks()
        if now-self.last_attack<self.attack_cooldown:
            return
        self.attacking=True
        self.attack_timer=15
        self.state="attack"
        player.take_damage(self.attack_damage)
        self.last_attack=now
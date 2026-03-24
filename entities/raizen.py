import pygame
from entities.enemy import Enemy
import math

class Raizen(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=450, speed=1.5, vision_range=500,damage=25,attack_damage=50)
        self.animations={
            "idle":{},
            "walk":{
                "down":[],
                "up":[],
                "left":[],
                "right":[]
            },
            "attack":{},
            "death":{}
        }
        self.animation_speed=0.15
        self.frame=0
        self.state="idle"
        self.direction="down"
        self.animations["idle"]["down"]=pygame.image.load("Asset/Enemies/Raizen/idle/Idle (1).png").convert_alpha()
        self.animations["idle"]["up"]=pygame.image.load("Asset/Enemies/Raizen/idle/Idle (2).png").convert_alpha()
        self.animations["idle"]["left"]=pygame.image.load("Asset/Enemies/Raizen/idle/Idle (3).png").convert_alpha()
        self.animations["idle"]["right"]=pygame.image.load("Asset/Enemies/Raizen/idle/Idle (4).png").convert_alpha()
        self.animations["attack"]["down"]=pygame.image.load("Asset/Enemies/Raizen/attack/Attack (1).png").convert_alpha()
        self.animations["attack"]["up"]=pygame.image.load("Asset/Enemies/Raizen/attack/Attack (2).png").convert_alpha()
        self.animations["attack"]["left"]=pygame.image.load("Asset/Enemies/Raizen/attack/Attack (3).png").convert_alpha()
        self.animations["attack"]["right"]=pygame.image.load("Asset/Enemies/Raizen/attack/Attack (4).png").convert_alpha()
        self.animations["death"]=pygame.image.load("Asset/Enemies/Raizen/Dead.png").convert_alpha()
        self.dead=False
        self.death_timer=0
        for i in range(1,5):
            self.animations["walk"]["down"].append(pygame.image.load(f"Asset/Enemies/Raizen/walk/Down/WalkDown ({i}).png").convert_alpha())
            self.animations["walk"]["up"].append(pygame.image.load(f"Asset/Enemies/Raizen/walk/Up/WalkUp ({i}).png").convert_alpha())
            self.animations["walk"]["right"].append(pygame.image.load(f"Asset/Enemies/Raizen/walk/Right/WalkRight ({i}).png").convert_alpha())
            self.animations["walk"]["left"].append(pygame.image.load(f"Asset/Enemies/Raizen/walk/Left/WalkLeft ({i}).png").convert_alpha())
        self.image=self.animations["idle"]["down"]
        self.rect=self.image.get_rect(topleft=(x,y))
        self.weapon=pygame.image.load("Asset/Weapons/Katana/SpriteBack.png").convert_alpha()
        self.attack_cooldown=400
        self.last_attack=0
        self.attack_timer=0
        self.attack_range=32
        self.dashing=False
        self.dash_speed=6
        self.dash_duration=20
        self.dash_timer=0
        self.dash_cooldown=300
        self.last_dash=0
        self.projectile_cooldown=250
        self.last_projectile=0
        self.max_health=self.health    
    def update(self,player,collision):
        if self.dead:
            self.animate()
            return
        dx=player.rect.centerx-self.rect.centerx
        dy=player.rect.centery-self.rect.centery
        dist=math.hypot(dx,dy)
        if self.dashing:
            dx=self.dash_dx*self.dash_speed
            dy=self.dash_dy*self.dash_speed
            self.move(dx,0,collision)
            self.move(0,dy,collision)
            self.dash_timer-=1
            if self.rect.colliderect(player.rect):
                player.take_damage(40)
            if self.dash_timer<=0:
                self.dashing=False
                self.attack_count=0
            self.animate()
            return
        if self.attack_count>=self.attack_limit:
            if not self.dashing:
                self.dash_attack(player)
            return
        if self.can_see_player(player):
            if dist>self.attack_range:
                self.state="walk"
                self.move_towards(player.rect.center,32,collision)
            else:
                self.state="idle"
                self.attack_player(player)
        else:
            self.state="idle"
        self.animate()
    def animate(self):
        if self.dead:
            self.death_timer+=1
            self.image=self.animations["death"]
            if self.death_timer>100:
                self.kill()
            return
        if self.attacking:
            self.image=self.animations["attack"][self.direction]
            self.attack_timer-=1
            if self.attack_timer<=0:
                self.attacking=False
                self.state="idle"
            return
        if self.state=="idle":
            self.image=self.animations["idle"][self.direction]
        else:
            self.frame+=self.animation_speed
            frames=self.animations["walk"][self.direction]
            if self.frame>=len(frames):
                self.frame=0
            self.image=frames[int(self.frame)]
    def draw(self,screen,camera_x,camera_y):
        screen.blit(self.image,(self.rect.x-camera_x,self.rect.y-camera_y))
        wx=self.rect.centerx-camera_x
        wy=self.rect.centery-camera_y
        weapon=self.weapon
        if self.attacking:
            if self.direction=="down":
                rotated=pygame.transform.rotate(weapon,0)
                pos=(wx-8,wy+8)
            elif self.direction=="right":
                rotated=pygame.transform.rotate(weapon,90)
                pos=(wx+8,wy+1)
            elif self.direction=="up":
                rotated=pygame.transform.rotate(weapon,180)
                pos=(wx-8,wy-16)
            elif self.direction=="left":
                rotated=pygame.transform.rotate(weapon,-90)
                pos=(wx-16,wy+1)
            screen.blit(rotated,pos)
            self.draw_health_bar(screen,camera_x,camera_y)
    def can_see_player(self, player):
        dx=player.rect.centerx-self.rect.centerx
        dy=player.rect.centery-self.rect.centery
        dist=math.hypot(dx,dy)
        return dist<=self.vision_range
    def dash_attack(self,player):
        now=pygame.time.get_ticks()
        if self.dashing:
            return
        if now-self.last_dash>=self.dash_cooldown:
            self.dashing=True
            self.dash_timer=self.dash_duration
            self.last_dash=now
            dx=player.rect.centerx-self.rect.centerx
            dy=player.rect.centery-self.rect.centery
            dist=math.hypot(dx,dy)
            if dist!=0:
                self.dash_dx=dx/dist
                self.dash_dy=dy/dist
    def draw_health_bar(self,screen,camera_x,camera_y):
        bar_width=60
        bar_height=6
        x=self.rect.centerx-camera_x-bar_width//2
        y=self.rect.y-camera_y-10
        pygame.draw.rect(screen,(100,100,100),(x,y,bar_width,bar_height))
        health_ratio=self.health/self.max_health
        pygame.draw.rect(screen,(255,0,0),(x,y,int(bar_width*health_ratio),bar_height))
        pygame.draw.rect(screen,(255,255,255),(x,y,bar_width,bar_height),1)
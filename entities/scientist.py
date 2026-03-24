import pygame
from entities.enemy import Enemy
import math

class Scientist(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=40, speed=1,vision_range=100,damage=50,attack_damage=10)
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
        self.animations["idle"]["down"]=pygame.image.load("Asset/Enemies/Scientist/idle/Idle (1).png").convert_alpha()
        self.animations["idle"]["up"]=pygame.image.load("Asset/Enemies/Scientist/idle/Idle (2).png").convert_alpha()
        self.animations["idle"]["left"]=pygame.image.load("Asset/Enemies/Scientist/idle/Idle (3).png").convert_alpha()
        self.animations["idle"]["right"]=pygame.image.load("Asset/Enemies/Scientist/idle/Idle (4).png").convert_alpha()
        self.animations["attack"]["down"]=pygame.image.load("Asset/Enemies/Scientist/attack/Attack (1).png").convert_alpha()
        self.animations["attack"]["up"]=pygame.image.load("Asset/Enemies/Scientist/attack/Attack (2).png").convert_alpha()
        self.animations["attack"]["left"]=pygame.image.load("Asset/Enemies/Scientist/attack/Attack (3).png").convert_alpha()
        self.animations["attack"]["right"]=pygame.image.load("Asset/Enemies/Scientist/attack/Attack (4).png").convert_alpha()
        self.animations["death"]=pygame.image.load("Asset/Enemies/Scientist/Dead.png").convert_alpha()
        self.dead=False
        self.death_timer=0
        for i in range(1,5):
            self.animations["walk"]["down"].append(pygame.image.load(f"Asset/Enemies/Scientist/walk/Down/WalkDown ({i}).png").convert_alpha())
            self.animations["walk"]["up"].append(pygame.image.load(f"Asset/Enemies/Scientist/walk/Up/WalkUp ({i}).png").convert_alpha())
            self.animations["walk"]["right"].append(pygame.image.load(f"Asset/Enemies/Scientist/walk/Right/WalkRight ({i}).png").convert_alpha())
            self.animations["walk"]["left"].append(pygame.image.load(f"Asset/Enemies/Scientist/walk/Left/WalkLeft ({i}).png").convert_alpha())
        self.image=self.animations["idle"]["down"]
        self.rect=self.image.get_rect(topleft=(x,y))
        self.max_health=self.health
        self.attack_range=150
        self.shoot_cooldown=1000
        self.last_shot=0
        self.projectiles=[]
    def update(self,player,collision):
        if self.dead:
            self.animate()
            return
        dx=player.rect.centerx-self.rect.centerx
        dy=player.rect.centery-self.rect.centery
        dist=math.hypot(dx,dy)
        self.set_direction(dx,dy)
        if self.can_see_player(player)and dist<=self.attack_range:
            now=pygame.time.get_ticks()
            if now-self.last_shot>=self.shoot_cooldown:
                self.state="attack"
                self.shoot(player)
            else:
                self.state="idle"
        else:
            self.state="idle"
        self.update_projectiles(player,collision)
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
        self.draw_health_bar(screen,camera_x,camera_y)
        for bullet in self.projectiles:
            pygame.draw.rect(screen,(0,255,0),(bullet["x"]-camera_x,bullet["y"]-camera_y,6,6))
    def can_see_player(self, player):
        dx=player.rect.centerx-self.rect.centerx
        dy=player.rect.centery-self.rect.centery
        dist=math.hypot(dx,dy)
        return dist<self.vision_range
    def draw_health_bar(self,screen,camera_x,camera_y):
        bar_width=20
        bar_height=6
        x=self.rect.centerx-camera_x-bar_width//2
        y=self.rect.y-camera_y-10
        pygame.draw.rect(screen,(100,100,100),(x,y,bar_width,bar_height))
        health_ratio=self.health/self.max_health
        pygame.draw.rect(screen,(255,0,0),(x,y,int(bar_width*health_ratio),bar_height))
        pygame.draw.rect(screen,(255,255,255),(x,y,bar_width,bar_height),1)
    def shoot(self,player):
        now=pygame.time.get_ticks()
        if now-self.last_shot<self.shoot_cooldown:
            return
        dx=player.rect.centerx-self.rect.centerx
        dy=player.rect.centery-self.rect.centery
        dist=math.hypot(dx,dy)
        if dist!=0:
            dx/=dist
            dy/=dist
            bullet={
                "x":self.rect.centerx,
                "y":self.rect.centery,
                "dx":dx,
                "dy":dy,
                "speed":5
            }
            self.projectiles.append(bullet)
            self.last_shot=now
    def update_projectiles(self,player,collision):
        for bullet in self.projectiles[:]:
            bullet["x"]+=bullet["dx"]*bullet["speed"]
            bullet["y"]+=bullet["dy"]*bullet["speed"]
            rect=pygame.Rect(bullet["x"],bullet["y"],6,6)
            if rect.colliderect(player.rect):
                player.take_damage(self.attack_damage)
                self.projectiles.remove(bullet)
                continue
            for tile in collision:
                if rect.colliderect(tile):
                    self.projectiles.remove(bullet)
                    break
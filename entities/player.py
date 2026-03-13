import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animations={
            "idle":{},
            "attack":{},
            "walk":{
                "down":[],
                "up":[],
                "left":[],
                "right":[],
            }
        }
        self.animations["idle"]["down"]=pygame.image.load(f"Asset/Player/Idle/Idle (1).png").convert_alpha()
        self.animations["idle"]["up"]=pygame.image.load(f"Asset/Player/Idle/Idle (2).png").convert_alpha()
        self.animations["idle"]["left"]=pygame.image.load(f"Asset/Player/Idle/Idle (3).png").convert_alpha()
        self.animations["idle"]["right"]=pygame.image.load(f"Asset/Player/Idle/Idle (4).png").convert_alpha()
        self.animations["attack"]["up"]=pygame.image.load(f"Asset/Player/Attack/Attack (1).png").convert_alpha()
        self.animations["attack"]["left"]=pygame.image.load(f"Asset/Player/Attack/Attack (2).png").convert_alpha()
        self.animations["attack"]["right"]=pygame.image.load(f"Asset/Player/Attack/Attack (3).png").convert_alpha()
        self.animations["attack"]["down"]=pygame.image.load(f"Asset/Player/Attack/Attack (4).png").convert_alpha()
        for i in range(1,5):
            self.animations["walk"]["down"].append(pygame.image.load(f"Asset/Player/Walk/front/WalkFront ({i}).png").convert_alpha())
            self.animations["walk"]["up"].append(pygame.image.load(f"Asset/Player/Walk/back/WalkBack ({i}).png").convert_alpha())
            self.animations["walk"]["left"].append(pygame.image.load(f"Asset/Player/Walk/left/WalkLeft ({i}).png").convert_alpha())
            self.animations["walk"]["right"].append(pygame.image.load(f"Asset/Player/Walk/right/WalkRight ({i}).png").convert_alpha())
        self.state="idle"
        self.direction="down"
        self.frame=0
        self.attack_timer=0
        self.animation_speed=0.15
        self.image=self.animations["idle"]["down"]
        self.rect=self.image.get_rect()
        self.rect.topleft= (x,y)
        self.attacking=False
    def update(self,collisions):
        keys=pygame.key.get_pressed()
        dx=0
        dy=0
        moving=False
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking=True
            self.attack_timer=0
            self.state="attack"
        if not self.attacking:
            if keys[pygame.K_UP]:
                dy-=PLAYER_SPEED
                self.direction="up"
                moving=True
            if keys[pygame.K_DOWN]:
                dy+=PLAYER_SPEED
                self.direction="down"
                moving=True
            if keys[pygame.K_LEFT]:
                dx-=PLAYER_SPEED
                self.direction="left"
                moving=True
            if keys[pygame.K_RIGHT]:
                dx+=PLAYER_SPEED
                self.direction="right"
                moving=True
            if moving:
                self.state="walk"
            else:
                self.state="idle"
        if self.attacking:
            self.attack_timer+=1
            if self.attack_timer>=10:
                self.attacking=False
                self.attack_timer=0
        self.animate()
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
    def animate(self):
        if self.state == "idle":
            self.image=self.animations["idle"][self.direction]
        elif self.state == "attack":
            self.image=self.animations["attack"][self.direction]
        else:
            self.frame+=self.animation_speed
            frames=self.animations["walk"][self.direction]
            if self.frame>=len(frames):
                self.frame=0
            self.image=frames[int(self.frame)]
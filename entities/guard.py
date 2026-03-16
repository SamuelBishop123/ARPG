import pygame
from entities.enemy import Enemy
import math

class Guard(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=50, speed=1,vision_range=100)
        offset=50
        self.patrol_points=[(x,y),(x+offset,y),(x+offset,y+offset),(x,y+offset)]
        self.patrol_index=0
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
        self.animations["idle"]["down"]=pygame.image.load("Asset/Enemies/Guard/idle/Idle (1).png").convert_alpha()
        self.animations["idle"]["up"]=pygame.image.load("Asset/Enemies/Guard/idle/Idle (2).png").convert_alpha()
        self.animations["idle"]["left"]=pygame.image.load("Asset/Enemies/Guard/idle/Idle (3).png").convert_alpha()
        self.animations["idle"]["right"]=pygame.image.load("Asset/Enemies/Guard/idle/Idle (4).png").convert_alpha()
        self.animations["attack"]["down"]=pygame.image.load("Asset/Enemies/Guard/attack/Attack (1).png").convert_alpha()
        self.animations["attack"]["up"]=pygame.image.load("Asset/Enemies/Guard/attack/Attack (2).png").convert_alpha()
        self.animations["attack"]["left"]=pygame.image.load("Asset/Enemies/Guard/attack/Attack (3).png").convert_alpha()
        self.animations["attack"]["right"]=pygame.image.load("Asset/Enemies/Guard/attack/Attack (4).png").convert_alpha()
        self.animations["death"]=pygame.image.load("Asset/Enemies/Guard/Dead.png").convert_alpha()
        self.dead=False
        self.death_timer=0
        for i in range(1,5):
            self.animations["walk"]["down"].append(pygame.image.load(f"Asset/Enemies/Guard/walk/Down/WalkDown ({i}).png").convert_alpha())
            self.animations["walk"]["up"].append(pygame.image.load(f"Asset/Enemies/Guard/walk/Up/WalkUp ({i}).png").convert_alpha())
            self.animations["walk"]["right"].append(pygame.image.load(f"Asset/Enemies/Guard/walk/Right/WalkRight ({i}).png").convert_alpha())
            self.animations["walk"]["left"].append(pygame.image.load(f"Asset/Enemies/Guard/walk/Left/WalkLeft ({i}).png").convert_alpha())
        self.image=self.animations["idle"]["down"]
        self.rect=self.image.get_rect(topleft=(x,y))
        self.weapon=pygame.image.load("Asset/Weapons/Katana/SpriteBack.png").convert_alpha()
    def update(self,player):
        if self.dead:
            self.animate()
            return
        dx=player.rect.centerx-self.rect.centerx
        dy=player.rect.centery-self.rect.centery
        dist=math.hypot(dx,dy)
        if self.can_see_player(player):
            if dist>self.attack_range:
                self.state="walk"
                self.move_towards(player.rect.center,32)
            else:
                self.state="idle"
                self.attack_player(player)
        else:
            self.patrol()
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
    def patrol(self):
        if not self.patrol_points:
            return
        target=self.patrol_points[self.patrol_index]
        dx=target[0]-self.rect.centerx
        dy=target[1]-self.rect.centery
        dist=math.hypot(dx,dy)
        if dist<5:
            self.patrol_index=(self.patrol_index+1)%len(self.patrol_points)
            target=self.patrol_points[self.patrol_index]
            dx=target[0]-self.rect.centerx
            dy=target[1]-self.rect.centery
            dist=math.hypot(dx,dy)
        else:
            self.state="walk"
            self.move_towards(target,0)
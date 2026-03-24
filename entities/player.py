import pygame
from config import *
from weapons.projectile import Projectile

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
        self.attack_cooldown=200
        self.last_attack=0
        self.shoot_cooldown=400
        self.last_shot=0
        self.reading=False
        self.max_health=600
        self.health=600
        self.invincible=False
        self.invincible_timer=0
        self.knockback=pygame.Vector2(0,0)
    def update(self,collisions,projectiles,document):
        keys=pygame.key.get_pressed()
        dx=0
        dy=0
        moving=False
        if self.reading:
            return
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
            if keys[pygame.K_f]:
                self.shoot(projectiles)
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

    def attack(self,enemies_group):
        if self.reading:
            return
        now=pygame.time.get_ticks()
        if now-self.last_attack<self.attack_cooldown:
            return
        self.last_attack=now
        if not self.attacking:
            return
        attack_rect=self.get_attack_rect()
        for enemy in enemies_group:
            if attack_rect.colliderect(enemy.rect):
                if enemy.is_player_behind(self):
                    enemy.take_damage(999,self)
                else:
                    enemy.take_damage(enemy.damage,self)                
    def get_attack_rect(self):
        size=32
        if self.direction=="right":
            return pygame.Rect(self.rect.right, self.rect.centery-20,size,40)
        elif self.direction=="left":
            return pygame.Rect(self.rect.left-size, self.rect.centery-20,size,40)
        elif self.direction=="up":
            return pygame.Rect(self.rect.centerx-20, self.rect.top-size,40,size)
        elif self.direction=="down":
            return pygame.Rect(self.rect.centerx-20, self.rect.bottom,40,size)
    def take_damage(self, damage):
        if self.invincible:
            return
        self.health-=damage
    def shoot(self,projectiles):
        now=pygame.time.get_ticks()
        if now-self.last_shot<self.shoot_cooldown:
            return
        self.last_shot=now
        px=self.rect.centerx
        py=self.rect.centery
        self.state="attack"
        projectile=Projectile(px,py,self.direction)
        projectiles.add(projectile)
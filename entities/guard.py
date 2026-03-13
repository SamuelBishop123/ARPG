import pygame
from entities.enemy import Enemy

class Guard(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=50, speed=2)
        self.animations={
            "idle":{},
            "walk":{
                "down":[],
                "up":[],
                "left":[],
                "right":[]
            }
        }
        self.animations["idle"]["down"]=pygame.image.load("Asset/Enemies/Guard/idle/Idle (1).png").convert_alpha()
        self.animations["idle"]["up"]=pygame.image.load("Asset/Enemies/Guard/idle/Idle (2).png").convert_alpha()
        self.animations["idle"]["left"]=pygame.image.load("Asset/Enemies/Guard/idle/Idle (3).png").convert_alpha()
        self.animations["idle"]["right"]=pygame.image.load("Asset/Enemies/Guard/idle/Idle (4).png").convert_alpha()
        for i in range(1,5):
            self.animations["walk"]["down"].append(pygame.image.load(f"Asset/Enemies/Guard/walk/Down/WalkDown ({i}).png"))
            self.animations["walk"]["up"].append(pygame.image.load(f"Asset/Enemies/Guard/walk/Up/WalkUp ({i}).png"))
            self.animations["walk"]["right"].append(pygame.image.load(f"Asset/Enemies/Guard/walk/Right/WalkRight ({i}).png"))
            self.animations["walk"]["down"].append(pygame.image.load(f"Asset/Enemies/Guard/walk/Left/WalkLeft ({i}).png"))
        self.image=self.animations["idle"]["down"]
        self.rect=self.image.get_rect(topleft=(x,y))
        self.weapon=pygame.image.load("Asset/Weapons/Katana/SpriteBack.png").convert_alpha()
    def update(self,player):
        if self.can_see_player(player):
            self.state="walk"
            self.move_towards(player.rect.center)
        else:
            self.state="idle"
        self.animate()
    def animate(self):
        if self.state=="idle":
            self.animations["idle"][self.direction]
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
        if self.direction=="right":
            screen.blit(self.weapon,(wx+10,wy))
        if self.direction=="left":
            screen.blit(self.weapon,(wx-20,wy))
        if self.direction=="up":
            screen.blit(self.weapon,(wx,wy-20))
        if self.direction=="down":
            screen.blit(self.weapon,(wx,wy+10))
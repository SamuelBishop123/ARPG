import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, entity,image_path):
        super().__init__()
        self.entity=entity
        self.original_image=pygame.image.load(image_path).convert_alpha()
        self.image=self.original_image
        self.rect=self.image.get_rect()
    def update(self):
        if self.entity.direction=="down":
            angle=0
            anchor=self.entity.rect.midbottom
            self.image=pygame.transform.rotate(self.original_image,angle)
            self.rect=self.image.get_rect(midtop=anchor)
            self.rect.x-=4
        elif self.entity.direction=="up":
            angle=180
            anchor=self.entity.rect.midtop
            self.image=pygame.transform.rotate(self.original_image,angle)
            self.rect=self.image.get_rect(midbottom=anchor)
            self.rect.x-=4
        elif self.entity.direction=="left":
            angle=-90
            anchor=self.entity.rect.midleft
            self.image=pygame.transform.rotate(self.original_image,angle)
            self.rect=self.image.get_rect(midright=anchor)
            self.rect.y+=4
        if self.entity.direction=="right":
            angle=90
            anchor=self.entity.rect.midright
            self.image=pygame.transform.rotate(self.original_image,angle)
            self.rect=self.image.get_rect(midleft=anchor)
            self.rect.y+=4
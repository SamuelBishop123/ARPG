import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, x,y,text):
        super().__init__()
        self.image=pygame.image.load("Asset/NPC/Idle.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.text=text
        self.pages=text.split("---")
        self.page_index=0
        self.talking=False
    def draw(self,surface,camera_x,camera_y):
        surface.blit(self.image,(self.rect.x-camera_x,self.rect.y-camera_y))
    def next_page(self):
        self.page_index+=1
        if self.page_index>=len(self.pages):
            self.page_index=0
            self.talking=False
    def draw_text(self,screen,font,width,height):
        box_width=width-80
        box_height=140
        box_x=40
        box_y=height-box_height-40
        box_surface=pygame.Surface((box_width,box_height))
        box_surface.set_alpha(210)
        box_surface.fill((60,60,60))
        pygame.draw.rect(screen,(200,200,200),(box_x,box_y,box_width,box_height),2)
        screen.blit(box_surface,(box_x,box_y))
        text_x=box_x+20
        text_y=box_y+20
        lines=self.text.split("\n")
        for line in lines:
            text_surface=font.render(line,True,(255,255,255))
            screen.blit(text_surface,(text_x,text_y))

import pygame

class Doc(pygame.sprite.Sprite):
    def __init__(self, x,y,image_path,text):
        super().__init__()
        self.image=pygame.image.load(image_path).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.text=text
        self.reading=False
        self.scroll_y=0
        self.scroll_speed=5
        self.lines=[]
        self.text_height=0
    def draw(self,surface,camera_x,camera_y):
        surface.blit(self.image,(self.rect.x-camera_x,self.rect.y-camera_y))
    def draw_text(self,screen,font,width,height):
        overlay=pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((80,80,80))
        screen.blit(overlay,(0,0))
        lines=self.text.split("\n")
        x=30
        y=30
        y=height//2-(len(lines)*15)
        for line in lines:
            text_surface=font.render(line,True,(255,255,255))
            screen.blit(text_surface,(x,y))
            y+=30

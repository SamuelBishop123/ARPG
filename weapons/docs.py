import pygame

class Doc(pygame.sprite.Sprite):
    def __init__(self, x,y,image_path,text):
        super().__init__()
        self.image=pygame.image.load(image_path).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.text=text
        self.reading=False
    def draw(self,surface,camera_x,camera_y):
        surface.blit(self.image,(self.rect.x-camera_x,self.rect.y-camera_y))
    def draw_text(self,screen,font,width,height):
        overlay=pygame.Surface((width, height))
        overlay.set_alpha(200)
        overlay.fill((0,0,0))
        lines=self.text.split("\n")
        y=height//2-(len(lines)*15)
        for line in lines:
            text_surface=font.render(line,True,(255,255,255))
            x=width//2-text_surface.get_width()//2
            screen.blit(text_surface,(x,y))
            y+=30
import pygame
class Cutscene:
    def __init__(self,pages):
        self.pages=pages
        self.page_index=0
        self.active=True
    def next_page(self):
        self.page_index+=1
        if self.page_index>=len(self.pages):
            self.active=False
    def draw(self,screen,font,width,height):
        overlay=pygame.Surface((width,height))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        box_width=width-80
        box_height=150
        box_x=40
        box_y=height-box_height-40
        box=pygame.Surface((box_width,box_height))
        box.set_alpha(220)
        box.fill((40,40,40))
        pygame.draw.rect(screen,(200,200,200),(box_x,box_y,box_width,box_height),2)
        text=self.pages[self.page_index]
        lines=text.split("\n")
        text_x=box_x+20
        text_y=box_y+20
        for line in lines:
            txt=font.render(line,True,(255,255,255))
            screen.blit(txt,(text_x,text_y))
            text_y+=25
        hint=font.render("Press E to Continue",True,(180,180,180))
        screen.blit(hint,(box_x+box_width-220,box_y+box_height-30))
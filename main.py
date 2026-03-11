import pygame
from config import *
from world.map_loader import MapLoader
from entities.player import Player

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Shadow of the Iron Banner")

game_map = MapLoader("maps/Map.tmx")

player_x, player_y = game_map.get_spawn("player_spawn")

player = Player(player_x, player_y, "Asset/Player/Idle/Idle (1).png")

VIEW_WIDTH = 300
VIEW_HEIGHT = 200

view_surface = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))

camera_x = 0
camera_y = 0

clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    player.update(game_map.collisions)
    camera_x = player.rect.centerx - VIEW_WIDTH // 2
    camera_y = player.rect.centery - VIEW_HEIGHT // 2
    view_surface.fill((0, 0, 0))
    game_map.draw(view_surface, camera_x, camera_y)
    view_surface.blit(
        player.image,
        (player.rect.x - camera_x, player.rect.y - camera_y)
    )
    screen.fill((0, 0, 0))
    scaled_surface=pygame.transform.scale(view_surface,(WIDTH, HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
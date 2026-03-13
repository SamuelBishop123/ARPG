import pygame
from config import *
from world.map_loader import MapLoader
from entities.player import Player
from weapons.weapon import Weapon
from entities.guard import Guard
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Shadow of the Iron Banner")

game_map = MapLoader("maps/Map.tmx")

player_x, player_y = game_map.get_spawn("player_spawn")

player = Player(player_x, player_y)
enemies=pygame.sprite.Group()
for enemy in game_map.enemy_spawns:
    if enemy["name"]=="guard":
        enemies.add(Guard(enemy["x"],enemy["y"]))
print(game_map.enemy_spawns)
VIEW_WIDTH = 300
VIEW_HEIGHT = 200

view_surface = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))

camera_x = 0
camera_y = 0

weapon=Weapon(player,"Asset/Weapons/Katana/SpriteBack.png")

clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    player.update(game_map.collisions)
    enemies.update(player)
    for t in game_map.transitions:
        if player.rect.colliderect(t["rect"]):
            game_map=MapLoader("maps/"+t["target_map"])
            player_x,player_y=game_map.get_spawn(t["spawn"])
            player.rect.topleft=(player_x,player_y)
            break
    if player.attacking:
        weapon.update()
    camera_x = player.rect.centerx - VIEW_WIDTH // 2
    camera_y = player.rect.centery - VIEW_HEIGHT // 2
    camera_x=max(0,min(camera_x,game_map.width-VIEW_WIDTH))
    camera_y=max(0,min(camera_y,game_map.height-VIEW_HEIGHT))
    view_surface.fill((0,0,0))
    game_map.draw(view_surface, camera_x, camera_y)
    view_surface.blit(
        player.image,
        (player.rect.x - camera_x, player.rect.y - camera_y)
    )
    if player.attacking:
        view_surface.blit(weapon.image,(weapon.rect.x-camera_x,weapon.rect.y-camera_y))
    for enemy in enemies:
        enemy.draw(view_surface,camera_x,camera_y)
    scaled_surface=pygame.transform.scale(view_surface,(WIDTH, HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
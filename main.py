import pygame
from config import *
from world.map_loader import MapLoader
from entities.player import Player
from weapons.weapon import Weapon
from entities.guard import Guard
from weapons.docs import Doc
from entities.npc import NPC
from entities.raizen import Raizen
from systems.cutscene import Cutscene
from entities.general import General

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Shogun of The Iron Banner: Fort Kugane")

game_map = MapLoader("maps/Map.tmx")

player_x, player_y = game_map.get_spawn("player_spawn")

projectiles=pygame.sprite.Group()
document=pygame.sprite.Group()
enemies=pygame.sprite.Group()
npcs=pygame.sprite.Group()

raizen_cutscene=Cutscene([
    "Raizen: So, The rat which have destroyed my pawns has come to me",
    "Akira: I didnt came for your words. I came for answers",
    "Raizen: Answers?",
    "Raizen: (Chuckles softly)",
    "Raizen: You've been cutting my men... and you still dont know what you're fighting?",
    "Akira: I know enough. You exceute innocents. You spread fear.",
    "Raizen: Fear is not spread... it is revealed. People obey because they're weak.",
    "Akira: No. They obey because of monsters like you.",
    "Raizen: Monster... I was called that long before.",
    "Raizen: Do you think japan can be changed? Kings fall... Empires rot... Power is the only truth",
    "Akira: Then I will change it.",
    "Raizen: ...Good",
    "Raizen: Then come, the famous Oni No Kage. Let this be the place where your story ends"

])
cutscene_active=False
raizen_triggered=False

entering_password=False
password_input=""
current_door=None
wrong_password_timer=0

player = Player(player_x, player_y)
def spawn_enemies():
    enemies.empty()
    for enemy in game_map.enemy_spawns:
        if enemy["name"]=="guard":
            enemies.add(Guard(enemy["x"],enemy["y"]))
        if enemy["name"]=="boss":
            enemies.add(Raizen(enemy["x"],enemy["y"]))
        if enemy["name"]=="general":
            enemies.add(General(enemy["x"],enemy["y"]))
def spawn_documents():
    document.empty()
    for doc in game_map.documents:
        if doc["name"]=="scroll":
            document.add(Doc(doc["x"],doc["y"],"Asset/Docs/scroll.png",doc["text"]))
        if doc["name"]=="letter":
            document.add(Doc(doc["x"],doc["y"],"Asset/Docs/letter.png",doc["text"]))
def spawn_npcs():
    npcs.empty()
    for npc in game_map.npcs:
        npcs.add(NPC(npc["x"],npc["y"],npc["text"]))
VIEW_WIDTH = 300
VIEW_HEIGHT = 200

view_surface = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))

camera_x = 0
camera_y = 0

weapon=Weapon(player,"Asset/Weapons/Katana/SpriteBack.png")

font=pygame.font.SysFont(None,24)

clock = pygame.time.Clock()
run = True

spawn_documents()
spawn_enemies()
spawn_npcs()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if entering_password and event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                if password_input.strip().lower()==current_door["password"].lower():
                    game_map=MapLoader("maps/"+current_door["target_map"])
                    player_x,player_y=game_map.get_spawn(current_door["spawn"])
                    player.rect.topleft=(player_x,player_y)
                    spawn_enemies()
                    spawn_documents()
                    spawn_npcs()
                else:
                    wrong_password_timer=60
                entering_password=False
            elif event.key == pygame.K_BACKSPACE:
                password_input=password_input[:-1]
            elif event.key==pygame.K_ESCAPE:
                entering_password=False
            else:
                if len(password_input)<30 and event.unicode.isprintable():
                    password_input+=event.unicode
        if event.type==pygame.KEYDOWN and cutscene_active:
            if event.key==pygame.K_e:
                raizen_cutscene.next_page()
                if not raizen_cutscene.active:
                    cutscene_active=False
                    player.reading=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_e:
                for npc in npcs:
                    if npc.talking:
                        npc.next_page()
                        player.reading=npc.talking
                        break
                    if player.rect.colliderect(npc.rect):
                        npc.talking=True
                        player.reading=True
                        break
                for doc in document:
                    if player.rect.colliderect(doc.rect):
                        doc.reading=not doc.reading
                        player.reading=doc.reading
                for door in game_map.password_doors:
                    if player.rect.colliderect(door["rect"]):
                        entering_password=True
                        password_input=""
                        current_door=door
    if not player.reading and not entering_password and not cutscene_active:
        player.update(game_map.collisions,projectiles,document)
        enemies.update(player,game_map.collisions)
    player.attack(enemies)
    projectiles.update()
    for enemy in enemies:
        if isinstance(enemy,Raizen)and not raizen_triggered:
            if player.rect.colliderect(enemy.rect.inflate(200,200)):
                cutscene_active=True
                raizen_triggered=True
    for projectile in projectiles:
        for enemy in enemies:
            if projectile.rect.colliderect(enemy.rect):
                enemy.take_damage(10,player)
                projectile.kill()
    for t in game_map.transitions:
        if player.rect.colliderect(t["rect"]):
            game_map=MapLoader("maps/"+t["target_map"])
            player_x,player_y=game_map.get_spawn(t["spawn"])
            player.rect.topleft=(player_x,player_y)
            spawn_enemies()
            spawn_documents()
            break
    if player.attacking:
        weapon.update()
    camera_x = player.rect.centerx - VIEW_WIDTH // 2
    camera_y = player.rect.centery - VIEW_HEIGHT // 2
    camera_x=max(0,min(camera_x,game_map.width-VIEW_WIDTH))
    camera_y=max(0,min(camera_y,game_map.height-VIEW_HEIGHT))
    view_surface.fill((0,0,0))
    game_map.draw(view_surface, camera_x, camera_y)
    for doc in document:
        doc.draw(view_surface,camera_x,camera_y)
    view_surface.blit(
        player.image,
        (player.rect.x - camera_x, player.rect.y - camera_y)
    )
    if player.attacking:
        view_surface.blit(weapon.image,(weapon.rect.x-camera_x,weapon.rect.y-camera_y))
    for enemy in enemies:
        enemy.draw(view_surface,camera_x,camera_y)
    for projectile in projectiles:
        view_surface.blit(projectile.image,(projectile.rect.x-camera_x,projectile.rect.y-camera_y))
    for doc in document:
        if player.rect.colliderect(doc.rect) and not doc.reading:
            hint=font.render("Press E to read",True,(255,255,255))
            view_surface.blit(hint,(doc.rect.x-camera_x-10,doc.rect.y-camera_y-20))
    for npc in npcs:
        npc.draw(view_surface,camera_x,camera_y)
        for door in game_map.password_doors:
            if player.rect.colliderect(door["rect"]):
                hint=font.render("Press E to enter password",True,(255,255,255))
                view_surface.blit(hint,(door["rect"].x-camera_x-20,door["rect"].y-camera_y-20))
    scaled_surface=pygame.transform.scale(view_surface,(WIDTH, HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    for npc in npcs:
        if npc.talking:
            npc.draw_text(screen,font,WIDTH,HEIGHT)
    for doc in document:
        if doc.reading:
            doc.draw_text(screen,font,WIDTH,HEIGHT)
    if entering_password:
        box=pygame.Surface((400,120))
        box.fill((50,50,50))
        screen.blit(box,(WIDTH//2-200,HEIGHT//2-60))
        title=font.render("Enter Password:-",True,(255,255,255))
        screen.blit(title,(WIDTH//2-180,HEIGHT//2-50))
        pw=font.render(password_input,True,(255,255,255))
        screen.blit(pw,(WIDTH//2-180,HEIGHT//2-10))
    if wrong_password_timer>0:
        error=font.render("Wrong Password!",True,(255,0,0))
        screen.blit(error,(WIDTH//2-100,HEIGHT//2+40))
        wrong_password_timer-=1
    if cutscene_active:
        player.reading=True
        raizen_cutscene.draw(screen,font,WIDTH,HEIGHT)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
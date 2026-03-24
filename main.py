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
from entities.robot import Robot
from entities.scientist import Scientist

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Shogun of The Iron Banner: Fort Kugane")

# 🎮 GAME STATE
game_state = "menu"
menu_selected = 0

# 🎨 FONTS
font = pygame.font.Font(None, 24)
font_big = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 24)

# 📂 MAP
game_map = MapLoader("maps/Map.tmx")
player_x, player_y = game_map.get_spawn("player_spawn")

# 📦 GROUPS
projectiles = pygame.sprite.Group()
document = pygame.sprite.Group()
enemies = pygame.sprite.Group()
npcs = pygame.sprite.Group()

raizen_cutscene = Cutscene([
    "Raizen: So, The rat which have destroyed my pawns has come to me",
    "Akira: I didnt came for your words. I came for answers",
    "Raizen: Answers?",
    "Raizen: (Chuckles softly)",
    "Raizen: You've been cutting my men... and still don't know?",
    "Akira: I know enough.",
    "Raizen: Fear is revealed, not spread.",
    "Akira: People obey because of monsters like you.",
    "Raizen: Power is the only truth",
    "Akira: Then I will change it.",
    "Raizen: Good... come then."
])

cutscene_active = False
raizen_triggered = False

# 🔐 PASSWORD
entering_password = False
password_input = ""
current_door = None
wrong_password_timer = 0

# 🧍 PLAYER
player = Player(player_x, player_y)
weapon = Weapon(player, "Asset/Weapons/Katana/SpriteBack.png")

# 🧠 SPAWN FUNCTIONS
def spawn_enemies():
    enemies.empty()
    for enemy in game_map.enemy_spawns:
        if enemy["name"] == "guard":
            enemies.add(Guard(enemy["x"], enemy["y"]))
        if enemy["name"] == "boss":
            enemies.add(Raizen(enemy["x"], enemy["y"]))
        if enemy["name"] == "general":
            enemies.add(General(enemy["x"], enemy["y"]))
        if enemy["name"] == "robot":
            enemies.add(Robot(enemy["x"], enemy["y"]))
        if enemy["name"] == "scientist":
            enemies.add(Scientist(enemy["x"], enemy["y"]))

def spawn_documents():
    document.empty()
    for doc in game_map.documents:
        if doc["name"] == "scroll":
            document.add(Doc(doc["x"], doc["y"], "Asset/Docs/scroll.png", doc["text"]))
        if doc["name"] == "letter":
            document.add(Doc(doc["x"], doc["y"], "Asset/Docs/letter.png", doc["text"]))

def spawn_npcs():
    npcs.empty()
    for npc in game_map.npcs:
        npcs.add(NPC(npc["x"], npc["y"], npc["text"]))

spawn_enemies()
spawn_documents()
spawn_npcs()

# 🎥 CAMERA
VIEW_WIDTH = 300
VIEW_HEIGHT = 200
view_surface = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))
camera_x = 0
camera_y = 0

clock = pygame.time.Clock()
run = True

# 🎨 UI
def draw_menu():
    screen.fill((15, 15, 25))
    title = font_big.render("IRON BANNER", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))

    options = ["Start Game", "Quit"]
    for i, option in enumerate(options):
        color = (255, 215, 0) if i == menu_selected else (200, 200, 200)
        text = font_small.render(option, True, color)
        screen.blit(text, text.get_rect(center=(WIDTH//2, 300 + i * 50)))

def draw_story():
    screen.fill((20, 20, 30))
    lines = [
        "The Kingdom  has  fallen...",
        "Raizen rules with fear.",
        "You are the last shadow.",
        "",
        "Press ENTER to begin"
    ]
    for i, line in enumerate(lines):
        text = font_small.render(line, True, (220, 220, 220))
        screen.blit(text, text.get_rect(center=(WIDTH//2, 200 + i * 40)))

def draw_pause():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    text = font_big.render("PAUSED", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

def draw_game_over():
    screen.fill((10, 10, 10))
    text = font_big.render("Victory", True, (255, 215, 0))
    screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
    sub = font_small.render("Raizen is defeated", True, (200, 200, 200))
    screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2)))
    restart = font_small.render("Press R to restart", True, (150, 150, 150))
    screen.blit(restart, restart.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))
def draw_defeat():
    screen.fill((10, 10, 10))
    text = font_big.render("Defeat!!", True, (255, 215, 0))
    screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
    sub = font_small.render("Mission failed", True, (200, 200, 200))
    screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2)))
    restart = font_small.render("Press R to restart", True, (150, 150, 150))
    screen.blit(restart, restart.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))

# 🔁 LOOP
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # MENU
        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_selected = (menu_selected - 1) % 2
                elif event.key == pygame.K_DOWN:
                    menu_selected = (menu_selected + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if menu_selected == 0:
                        game_state = "story"
                    else:
                        run = False

        # STORY
        elif game_state == "story":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "playing"

        # PAUSE
        elif game_state in ["playing", "paused"]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "paused" if game_state == "playing" else "playing"
        if game_state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                run = False
        if game_state != "playing":
            continue
        if entering_password and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if password_input.strip().lower() == current_door["password"].lower():
                    game_map = MapLoader("maps/" + current_door["target_map"])
                    player.rect.topleft = game_map.get_spawn(current_door["spawn"])
                    spawn_enemies()
                    spawn_documents()
                    spawn_npcs()
                else:
                    wrong_password_timer = 60
                entering_password = False

            elif event.key == pygame.K_BACKSPACE:
                password_input = password_input[:-1]

            elif event.key == pygame.K_ESCAPE:
                entering_password = False

            else:
                if len(password_input) < 30 and event.unicode.isprintable():
                    password_input += event.unicode        
        if event.type == pygame.KEYDOWN and cutscene_active:
            if event.key == pygame.K_e:
                raizen_cutscene.next_page()
                if not raizen_cutscene.active:
                    cutscene_active = False
                    player.reading = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                for npc in npcs:
                    if npc.talking:
                        npc.next_page()
                        player.reading = npc.talking
                        break
                    if player.rect.colliderect(npc.rect):
                        npc.talking = True
                        player.reading = True
                        break

                for doc in document:
                    if player.rect.colliderect(doc.rect):
                        doc.reading = not doc.reading
                        player.reading = doc.reading

                for door in game_map.password_doors:
                    if player.rect.colliderect(door["rect"]):
                        entering_password = True
                        password_input = ""
                        current_door = door
    if game_state == "playing":
        if not player.reading and not entering_password and not cutscene_active:
            player.update(game_map.collisions, projectiles, document)
            enemies.update(player, game_map.collisions)
        player.attack(enemies)
        projectiles.update()
        for enemy in enemies:
            if isinstance(enemy, Raizen) and enemy.dead:
                game_state = "game_over"
        for enemy in enemies:
            if isinstance(enemy, Raizen) and not raizen_triggered:
                if player.rect.colliderect(enemy.rect.inflate(200, 200)):
                    cutscene_active = True
                    raizen_triggered = True
        for projectile in projectiles:
            for enemy in enemies:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.take_damage(enemy.damage,player)
                    projectile.kill()
        for t in game_map.transitions:
            if player.rect.colliderect(t["rect"]):
                game_map = MapLoader("maps/" + t["target_map"])
                player.rect.topleft = game_map.get_spawn(t["spawn"])
                spawn_enemies()
                spawn_documents()
                break
        if player.attacking:
            weapon.update()
        if player.health<=0:
            game_state="defeat"
    camera_x = player.rect.centerx - VIEW_WIDTH // 2
    camera_y = player.rect.centery - VIEW_HEIGHT // 2
    camera_x = max(0, min(camera_x, game_map.width - VIEW_WIDTH))
    camera_y = max(0, min(camera_y, game_map.height - VIEW_HEIGHT))
    view_surface.fill((0, 0, 0))
    game_map.draw(view_surface, camera_x, camera_y)
    for doc in document:
        doc.draw(view_surface, camera_x, camera_y)
    view_surface.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))
    if player.attacking:
        view_surface.blit(weapon.image, (weapon.rect.x - camera_x, weapon.rect.y - camera_y))
    for enemy in enemies:
        enemy.draw(view_surface, camera_x, camera_y)
    for projectile in projectiles:
        view_surface.blit(projectile.image, (projectile.rect.x - camera_x, projectile.rect.y - camera_y))
    for npc in npcs:
        npc.draw(view_surface, camera_x, camera_y)
    for doc in document:
        if player.rect.colliderect(doc.rect) and not doc.reading:
            hint=font.render("Press E to Read",True,(255,255,255))
            view_surface.blit(hint,(doc.rect.x-camera_x-10,doc.rect.y-camera_y-20))
    for door in game_map.password_doors:
        if player.rect.colliderect(door["rect"]):
            hint=font.render("Press E to enter password",True,(255,255,255))
            view_surface.blit(hint,(door["rect"].x-camera_x-20,door["rect"].y-camera_y-20))
    scaled_surface = pygame.transform.scale(view_surface, (WIDTH, HEIGHT))
    if game_state == "menu":
        draw_menu()
    elif game_state == "story":
        draw_story()
    elif game_state == "playing":
        screen.blit(scaled_surface, (0, 0))
        bar_width=200
        bar_height=20
        health_ratio=player.health/player.max_health
        pygame.draw.rect(screen,(255,0,0),(20,20,bar_width,bar_height))
        pygame.draw.rect(screen,(0,255,0),(20,20,bar_width*health_ratio,bar_height))
        pygame.draw.rect(screen,(255,255,255),(20,20,bar_width,bar_height),2)
        for npc in npcs:
            if npc.talking:
                npc.draw_text(screen, font, WIDTH, HEIGHT)
        for doc in document:
            if doc.reading:
                doc.draw_text(screen, font, WIDTH, HEIGHT)
        if entering_password:
            box = pygame.Surface((400, 120))
            box.fill((50, 50, 50))
            screen.blit(box, (WIDTH//2 - 200, HEIGHT//2 - 60))
            title = font.render("Enter Password:", True, (255, 255, 255))
            screen.blit(title, (WIDTH//2 - 180, HEIGHT//2 - 50))
            pw = font.render(password_input, True, (255, 255, 255))
            screen.blit(pw, (WIDTH//2 - 180, HEIGHT//2 - 10))
        if wrong_password_timer > 0:
            error = font.render("Wrong Password!", True, (255, 0, 0))
            screen.blit(error, (WIDTH//2 - 100, HEIGHT//2 + 40))
            wrong_password_timer -= 1
        if cutscene_active:
            player.reading = True
            raizen_cutscene.draw(screen, font, WIDTH, HEIGHT)
    elif game_state == "paused":
        screen.blit(scaled_surface, (0, 0))
        draw_pause()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state=="defeat":
        draw_defeat()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
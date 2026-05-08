import pygame

image_path = "/data/data/org.platformer.platformer/files/app"

clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((1280, 748))
pygame.display.set_caption("Platformer")
icon = pygame.image.load("image_path + images/icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("image_path + images/NighBg.png").convert()

nazad = [
    pygame.image.load(image_path + "images/nazad/1.png").convert_alpha(),
    pygame.image.load(image_path + "images/nazad/2.png").convert_alpha(),
    pygame.image.load(image_path + "images/nazad/3.png").convert_alpha(),
    pygame.image.load(image_path + "images/nazad/4.png").convert_alpha(),
    pygame.image.load(image_path + "images/nazad/5.png").convert_alpha(),
    pygame.image.load(image_path + "images/nazad/6.png").convert_alpha(),
    pygame.image.load(image_path + "images/nazad/7.png").convert_alpha(),
    pygame.image.load(image_path + "images/nazad/8.png").convert_alpha(),
    pygame.image.load(image_path + "images/nazad/9.png").convert_alpha(),
]

vpered = [
    pygame.image.load(image_path + "images/vpered/1.png").convert_alpha(),
    pygame.image.load(image_path + "images/vpered/2.png").convert_alpha(),
    pygame.image.load(image_path + "images/vpered/3.png").convert_alpha(),
    pygame.image.load(image_path + "images/vpered/4.png").convert_alpha(),
    pygame.image.load(image_path + "images/vpered/5.png").convert_alpha(),
    pygame.image.load(image_path + "images/vpered/6.png").convert_alpha(),
    pygame.image.load(image_path + "images/vpered/7.png").convert_alpha(),
    pygame.image.load(image_path + "images/vpered/8.png").convert_alpha(),
    pygame.image.load(image_path + "images/vpered/9.png").convert_alpha(),
]

ghost = pygame.image.load(image_path + "images/ghost.png").convert_alpha()
ghost_list_in_game = []

player_animation = 0
bg_x = 0

player_speed = 5
player_x = 100
player_y = 550  # Твой уровень земли

jump = False
jump_count = 10

bg_sound = pygame.mixer.Sound(image_path + "sounds/bg.mp3")
bg_sound.play(loops=-1)

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

label = pygame.font.Font(+ "pifonts/font.ttf", 40)
lose = label.render("Вы пimage_path роиграли!", True, (0, 255, 0))
restart = label.render("Играть заново", True, (0, 0, 0))
restart_rect = restart.get_rect(topleft=(500, 400))

bullets_left = 5
bullet = pygame.image.load(image_path + "images/bullet.png").convert_alpha()
bullets = []

gameplay = True

running = True

while running:

    # 1. РИСУЕМ ФОН
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + 1280, 0))

    if gameplay:
            player_rect = vpered[0].get_rect(topleft=(player_x, player_y))

            if ghost_list_in_game:
                for (i, el) in enumerate(ghost_list_in_game):
                    screen.blit(ghost, el)
                    el.x -=10

                    if el.x < -10:
                        ghost_list_in_game.pop(i)

                    if player_rect.colliderect(el):
                        gameplay = False


            keys = pygame.key.get_pressed()

        # 2. ОПРЕДЕЛЯЕМ КАКОЙ СПРАЙТ РИСОВАТЬ
            if keys[pygame.K_a]:
                current_sprite = nazad[player_animation]
            elif keys[pygame.K_d]:
                current_sprite = vpered[player_animation]
            else:
                current_sprite = vpered[0] # Стоит на месте

            # 3. ЛОГИКА ДВИЖЕНИЯ
            if keys[pygame.K_a] and player_x > 0:
                player_x -= player_speed
            elif keys[pygame.K_d] and player_x < 1220:
                player_x += player_speed

            # 4. ЛОГИКА ПРЫЖКА
            if not jump:
                if keys[pygame.K_SPACE]:
                    jump = True
            else:
                if jump_count >= -10: # ИСПРАВЛЕНО: было -7, стало -10 для симметрии
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) * 0.5
                    else:
                        player_y += (jump_count ** 2) * 0.5
                    jump_count -= 1
                else:
                    jump = False
                    jump_count = 10

            # 5. ОГРАНИЧИТЕЛЬ ПОЛА (чтобы не проваливался)
            if player_y > 550:
                player_y = 550
                jump = False
                jump_count = 10

            # 6. РИСУЕМ ИГРОКА (всегда)
            screen.blit(current_sprite, (player_x, player_y))

            # 7. ОБНОВЛЕНИЕ АНИМАЦИИ И ФОНА
            if keys[pygame.K_a] or keys[pygame.K_d]:
                if player_animation == 8:
                    player_animation = 0
                else:
                    player_animation += 1

            bg_x -= 2
            if bg_x <= -1280:
                bg_x = 0

            # Движение пуль (ЭТОТ БЛОК ДОЛЖЕН БЫТЬ ВНЕ IF KEYS)
            if bullets:
                for (i, el) in enumerate(bullets):
                    screen.blit(bullet, (el.x, el.y))
                    el.x += 20 # Сделаем скорость побольше, чтобы не копились
                    
                    # Чтобы пули не копились в памяти, удаляем их за экраном
                    if el.x > 1285:
                        bullets.pop(i)

                    if ghost_list_in_game:
                        for (index, ghost_el)  in enumerate(ghost_list_in_game):
                            if el.colliderect(ghost_el):
                                ghost_list_in_game.pop(index)
                                bullets.pop(index)
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose, (500, 300)) # Поменял координаты на центр
        screen.blit(restart, restart_rect)

        mouse = pygame.mouse.get_pos()
        if restart_rect.collidepoint(mouse)and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 100
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(1282, 520)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
                bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
                bullets_left -=1

    clock.tick(20) 

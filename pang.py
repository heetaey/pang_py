import pygame

# initialize the pang_game
pygame.init()

# set up screen size
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# set up startup screen
pygame.display.set_caption("Pang Game")

# FPS set
clock = pygame.time.Clock()

background = pygame.image.load("/Users/heetaeyang/Documents/Project/pang_py/resources/background"
                               ".png")

# character sprites
character = pygame.image.load("/Users/heetaeyang/Documents/Project/pang_py/resources/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_xpos = (screen_width / 2) - (character_width / 2)
character_ypos = screen_height - character_height

# axis
x = 0
y = 0

# character movement speed
character_speed = .6

# enemy character
enemy = pygame.image.load("/Users/heetaeyang/Documents/Project/pang_py/resources/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_xpos = (screen_width / 2) - (enemy_width / 2)
enemy_ypos = (screen_height / 2) - (enemy_height / 2)

# Font for in-game
game_font = pygame.font.Font(None, 40)

# Game timer
total_time = 10

# Game starter
start_time = pygame.time.get_ticks()

# running environment
running = True
while running:
    # FPS
    dt = clock.tick(60)
    # print("FPS: ", str(clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= character_speed
            elif event.key == pygame.K_RIGHT:
                x += character_speed
            elif event.key == pygame.K_UP:
                y -= character_speed
            elif event.key == pygame.K_DOWN:
                y += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y = 0

    # character position
    character_xpos += x * dt
    character_ypos += y * dt

    # limit 'x-axis' of the character not to surpass the program size
    if character_xpos < 0:
        character_xpos = 0
    elif character_xpos > screen_width - character_width:
        character_xpos = screen_width - character_width

    # limit 'y-axis' of the character not to surpass the program size
    if character_ypos < 0:
        character_ypos = 0
    elif character_ypos > screen_height - character_height:
        character_ypos = screen_height - character_height

    # character contact w/ enemy
    character_rect = character.get_rect()
    character_rect.left = character_xpos
    character_rect.top = character_ypos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_xpos
    enemy_rect.top = enemy_ypos

    # checking the contact
    if character_rect.colliderect(enemy_rect):
        print("HIT!")
        running = False

    # update sprites
    screen.blit(background, (0, 0))
    screen.blit(character, (character_xpos, character_ypos))
    screen.blit(enemy, (enemy_xpos, enemy_ypos))

    # set timer / time elapsed
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))

    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        print("Time Out!")
        running = False

    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()

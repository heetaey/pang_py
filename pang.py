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

# load sprites
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

# run
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

    # limit the character not to surpass the program size
    if character_xpos < 0:
        character_xpos = 0
    elif character_xpos > screen_width - character_width:
        character_xpos = screen_width - character_width

    if character_ypos < 0:
        character_ypos = 0
    elif character_ypos > screen_height - character_height:
        character_ypos = screen_height - character_height

    # update sprites
    screen.blit(background, (0, 0))
    screen.blit(character, (character_xpos, character_ypos))
    pygame.display.update()

pygame.quit()

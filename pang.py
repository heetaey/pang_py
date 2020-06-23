import os
import pygame

# initialize the pang_game
pygame.init()

# set up screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# set up startup screen
pygame.display.set_caption("Pang Game")

# FPS set
clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "resources")

# set background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# set stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# player sprites
player = pygame.image.load(os.path.join(image_path, "character.png"))
player_size = player.get_rect().size
player_width = player_size[0]
player_height = player_size[1]
player_xpos = (screen_width / 2) - (player_width / 2)
player_ypos = screen_height - player_height - stage_height

# axis
player_to_x_LEFT = 0
player_to_x_RIGHT = 0

# player movement speed
player_speed = 10

# player weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []
weapon_speed = 10

# Ball creations
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# Ball speed
ball_speed_y = [-18, -15, -12, -9]

# Ball
balls = [{
    "pos_x": 50,
    "pos_y": 50,
    "img_idx": 0,
    "to_x": 3,  # movement to x-axis
    "to_y": -6,  # movement to y-axis
    "init_speed_y": ball_speed_y[0]  # initial speed of y
}]

# running environment
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type in [pygame.KEYDOWN]:
            if event.key == pygame.K_LEFT:
                player_to_x_LEFT -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_to_x_RIGHT += player_speed
            elif event.key == pygame.K_SPACE:
                weapon_xpos = player_xpos + (weapon_width / 2) - 3
                weapon_ypos = player_ypos
                weapons.append([weapon_xpos, weapon_ypos])

        if event.type in [pygame.KEYUP]:
            if event.key == pygame.K_LEFT:
                player_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                player_to_x_RIGHT = 0

    # player position
    player_xpos += player_to_x_LEFT + player_to_x_RIGHT

    # limit 'x-axis' of the player not to surpass the program size
    if player_xpos < 0:
        player_xpos = 0
    elif player_xpos > screen_width - player_width:
        player_xpos = screen_width - player_width

    # weapon position
    # w[0] w[1]: only w[1] value will change as it always move up
    # 100, 200 -> 180, 160, 140, 120...
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # when it hits the top, it will disappear
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # ball position
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # logic when it hits the end of width
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # logic when it hit the end of the heights
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_speed_y"]
        # else, the ball movement speed increases
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # update sprites
    screen.blit(background, (0, 0))
    for weapon_xpos, weapon_ypos in weapons:
        screen.blit(weapon, (weapon_xpos, weapon_ypos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(player, (player_xpos, player_ypos))

    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()

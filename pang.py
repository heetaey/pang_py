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

weapon_to_remove = -1
ball_to_remove = -1

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

    # collision logics
    player_rect = player.get_rect()
    player_rect.left = player_xpos
    player_rect.top = player_ypos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # ball rect update
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # collision detect
        if player_rect.colliderect(ball_rect):
            running = False
            break

        # ball and weapon collision
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # if balloon size is not the smallest one
                if ball_img_idx < 3:
                    # retreive current ball size info
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # ball bouncing to left
                    balls.append({
                            "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                            "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                            "img_idx": ball_img_idx + 1,
                            "to_x": -3,  # movement to x-axis
                            "to_y": -6,  # movement to y-axis
                            "init_speed_y": ball_speed_y[ball_img_idx + 1]  # initial speed of y
                        })

                    # ball bouncing to right
                    balls.append({
                            "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                            "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                            "img_idx": ball_img_idx + 1,
                            "to_x": 3,  # movement to x-axis
                            "to_y": -6,  # movement to y-axis
                            "init_speed_y": ball_speed_y[ball_img_idx + 1]  # initial speed of y
                        })


                break

    # remove balls
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

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

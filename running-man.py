import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/1000)-start_time
    score_surface = test_font.render(f'Score:  {current_time}', True, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -=5

            if obstacle_rect.bottom >= 300: screen.blit(sheep_surface, obstacle_rect)
            else: screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >-100]

        return obstacle_list

    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return  False
    return True

def player_animation():
    global player,player_index

    if player_rect.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = True
start_time = 0
score = 0

# Initialize mixer for sounds
pygame.mixer.init()

    
jump_sound = pygame.mixer.Sound('jump_sound.wav')  

sky_surface = pygame.image.load('Graphics/Full-Background.png').convert()
ground_surface = pygame.image.load('Graphics/2.png').convert()

sheep1 = pygame.image.load('Graphics/monster1.png').convert_alpha()
sheep2 = pygame.image.load('Graphics/monster3.png').convert_alpha()
sheep_frames = [sheep1,sheep2]
sheep_frame_index = 0
sheep_surface = sheep_frames[sheep_frame_index]

fly_surface1 = pygame.image.load('Graphics/bat_1.png').convert_alpha()
fly_surface2 = pygame.image.load('Graphics/bat_2.png').convert_alpha()
fly_frames = [fly_surface1,fly_surface2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

text_surface = test_font.render('Game Over', False,(79, 119, 45))
text_rect = text_surface.get_rect(center=(400, 30))

game_message = test_font.render('Press space to start again', False, (144, 169, 85))
game_message_rect = game_message.get_rect(center=(400, 360))

player1 = pygame.image.load('Graphics/frame-0.png').convert_alpha()
player2 = pygame.image.load('Graphics/frame-1.png').convert_alpha()
player_walk = [player1,player2]
player_index = 0
player_jump = pygame.image.load('Graphics/frame.png')
player = player_walk[player_index]

player_rect = player.get_rect(midbottom=(80, 300))
player_gravity = 0

player_stand = pygame.image.load('Graphics/frame-2.png')
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(midbottom = (400, 300))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

sheep_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(sheep_animation_timer,200)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           exit()

       if game_active:
           if event.type == pygame.MOUSEMOTION and player_rect.bottom >= 300:
               if player_rect.collidepoint(event.pos):
                   player_gravity = -20

           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                   player_gravity = -20
                   # Play the jump sound when the player jumps
                   jump_sound.play()

       else:
           if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
               game_active = True
               start_time = int(pygame.time.get_ticks()/1000)

       if game_active:
           if event.type == obstacle_timer:
               if randint(0,2):
                   obstacle_rect_list.append(sheep_surface.get_rect(bottomright=(randint(900,1100), 301)))
               else:
                   obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900,1100), 190)))

           if event.type == sheep_animation_timer:
               if sheep_frame_index == 0: sheep_frame_index = 1
               else: sheep_frame_index = 0
               sheep_surface = sheep_frames[sheep_frame_index]

           if event.type == fly_animation_timer:
               if fly_frame_index == 0: fly_frame_index = 1
               else: fly_frame_index = 0
               fly_surface = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((236, 243, 158))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}',False,(79, 119, 45))
        score_message_rect =score_message.get_rect(center= (400,360))
        screen.blit(score_message,score_message_rect)

        screen.blit(text_surface, text_rect)
        if score==0:
            screen.blit(game_message,game_message_rect)

    pygame.display.update()
    clock.tick(60)
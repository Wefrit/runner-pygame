import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump= pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 210
        else:
            snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center=(400,50))
    screen.blit(score_surface, score_rect)
    return current_time

def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5
            if enemy_rect.bottom == 300:
                screen.blit(snail_surface, enemy_rect)
            else:
                screen.blit(fly_surface, enemy_rect)
        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
        return enemy_list
    else:
        return []

def collisions(player, enemies):
    if enemies:
        for enemy_rect in enemies:
            if player.colliderect(enemy_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,enemy_group,False):
        enemy_group.empty()
        return False
    return True

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300: 
        player_surface = player_jump
    else:
        player_index += 0.2
        if player_index >= (len(player_walk)):
            player_index  = 0
        player_surface = player_walk[int(player_index)]

    # player walking(floor)
    # jump (air)

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.3)
bg_music.play(loops = -1)


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

enemy_group = pygame.sprite.Group()

# background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# enemies
    # snail
snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_move = [snail1, snail2]
snail_index = 0
snail_surface = snail_move[snail_index]

    # fly
fly1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
fly2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
fly_move = [fly1, fly2]
fly_index = 0
fly_surface = fly_move[fly_index]

    # enemies list
enemy_rect_list = []

# player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_jump= pygame.image.load('graphics/player/jump.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# intro screen 
    # player image
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(405,206))
    # game name
game_name = test_font.render('Runner', False,(111,196,169))
game_name_rect = game_name.get_rect(center=(400,80))

# timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer,1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,400)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer,200)

# ingame loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            # realligning character
            if player_rect.x != 80 and player_rect.y != 300:
                player_rect.x = 80
                player_rect.y = 300
            # timers
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['fly', 'snail'])))
                # if randint(0,2):
                #     enemy_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100),300)))
                # else:                
                #     enemy_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100),210)))
            if event.type == snail_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0    
                snail_surface = snail_move[snail_index]        
            if event.type == fly_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_move[fly_index]
        else:
            # activating game with Space key      
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
            # restarting time for score
            start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # surfaces
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()

        # player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom  = 300
        # player_animation()
        # screen.blit(player_surface, player_rect)
        player.draw(screen)
        player.update()

        enemy_group.draw(screen)
        enemy_group.update()

        # enememy movement
        # enemy_rect_list = enemy_movement(enemy_rect_list)

        # collision 
        game_active = collision_sprite()
        # game_active = collisions(player_rect, enemy_rect_list)
        

    else:
        screen.fill((94,129,162))
        screen.blit(game_name, game_name_rect)
        enemy_rect_list.clear()
        player_gravity = 0
        if score == 0:
        # initial message
            game_message = test_font.render('Press space to run', False, (111,196,169))
            game_message_rect = game_message.get_rect(center = (400,320))
            screen.blit(game_message, game_message_rect)
            screen.blit(player_stand, player_stand_rect)
        else:
            # animating player stand
            screen.blit(player_stand, player_rect)
            if player_rect.x < player_stand_rect.x: 
                player_rect.x += 2.5
            if player_rect.y > player_stand_rect.y:
                player_rect.y -= 2.4

            # new game message + score
                #score
            score_message = test_font.render(f'Your Score: {score}',False,(111,196,169))
            score_message_rect = score_message.get_rect(center=(400, 320))
                # message
            game_message = test_font.render('Press space to try again', False, (111,196,169))
            game_message_rect = game_message.get_rect(center = (400,350))
            screen.blit(score_message,score_message_rect)
            screen.blit(game_message,game_message_rect)
    
    
    # update everything
    pygame.display.update()
    clock.tick(60)

import pgzrun
from pgzero.actor import Actor
import pgzero.music as music
import random

WIDTH = 800
HEIGHT = 600
GROUND_LEVEL = HEIGHT - 50
PLAYER_START_X = 50
PLAYER_HEIGHT = 50

player = Actor('player', (PLAYER_START_X, GROUND_LEVEL - PLAYER_HEIGHT))
button_play = Actor('button_start', (WIDTH // 2, 150))
button_exit = Actor('button_exit', (WIDTH // 2, 300))
button_music = Actor('button_music', (WIDTH // 2, 450))
button_menu = Actor('button_menu', (WIDTH - 50, 50))

game_state = 'menu'
music_on = True
is_jumping = False
jump_speed = 20
gravity = 0.5
player_speed = 4

music.play('music.ogg')

class Enemy(Actor):
    def __init__(self, x, y):
        super().__init__('mummra_right', (x, y))
        self.speed = 2
        self.direction = 1
        self.walking = False
        self.animation_counter = 0

    def update(self):
        self.x += self.speed * self.direction
        self.walking = True

        if self.left <= 0 or self.right >= WIDTH:
            self.direction *= -1
            self.animation_counter = 0

        if self.walking:
            self.animation_counter += 1
            if self.animation_counter % 10 == 0:
                base_image = 'mummra_right' if self.direction == 1 else 'mummra_left'
                walk_image = base_image + '_walk'
                self.image = walk_image if self.animation_counter // 10 % 2 == 0 else base_image

    def draw(self):
        super().draw()

enemies = []
enemy_spawn_interval = 200
enemy_spawn_timer = 0

platforms = []

def draw():
    screen.clear()

    if game_state == 'menu':
        screen.fill((200, 200, 200))
        screen.draw.text("Menu Principal", center=(WIDTH // 2, 50), fontsize=60)
        button_play.draw()
        button_exit.draw()
        button_music.draw()

    elif game_state == 'playing':
        screen.fill((135, 206, 235))
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for platform in platforms:
            platform.draw()
        button_menu.draw()

    elif game_state == 'ended':
        screen.fill((0, 0, 0))
        screen.draw.text("Jogo encerrado!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60)

def update():
    global game_state, enemy_spawn_timer

    if game_state == 'playing':
        update_player()

        for enemy in enemies:
            enemy.update()

        for enemy in enemies:
            if player.colliderect(enemy):
                game_state = 'menu'
                sounds.yay.play()
                reset_game()
                break

        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemy_spawn_timer = 0
            spawn_enemy()

def spawn_enemy():
    x = random.randint(50, WIDTH - 50)
    y = GROUND_LEVEL - PLAYER_HEIGHT
    enemy = Enemy(x, y)
    enemies.append(enemy)

def update_player():
    global is_jumping, jump_speed

    if is_jumping:
        player.y -= jump_speed
        jump_speed -= gravity
        player.image = 'jump'

    if player.y >= GROUND_LEVEL - PLAYER_HEIGHT:
        player.y = GROUND_LEVEL - PLAYER_HEIGHT
        is_jumping = False
        jump_speed = 20
        player.image = 'player'

    if keyboard.left:
        player.x -= player_speed
        player.image = 'move_left'
    elif keyboard.right:
        player.x += player_speed
        player.image = 'move_right'
    elif not is_jumping:
        player.image = 'player'

    if keyboard.up and not is_jumping:
        is_jumping = True

    for platform in platforms:
        if player.colliderect(platform):
            if player.bottom <= platform.top + 10:
                player.y = platform.top - PLAYER_HEIGHT
                is_jumping = False
                jump_speed = 20
                break

def on_mouse_down(pos):
    global game_state, music_on

    if game_state == 'menu':
        if button_exit.collidepoint(pos):
            game_state = 'ended'
        elif button_play.collidepoint(pos):
            game_state = 'playing'
            reset_game()
        elif button_music.collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play('music.ogg')
                button_music.image = 'button_music'
            else:
                music.stop()
                button_music.image = 'mute_button_music'
    elif game_state == 'playing':
        if button_menu.collidepoint(pos):
            game_state = 'menu'

def reset_game():
    global is_jumping, jump_speed
    player.pos = (PLAYER_START_X, GROUND_LEVEL - PLAYER_HEIGHT)
    is_jumping = False
    jump_speed = 20
    enemies.clear()

platform1 = Actor('platform', (100, GROUND_LEVEL - 150))
platform2 = Actor('platform', (300, GROUND_LEVEL - 200))
platforms.append(platform1)
platforms.append(platform2)

pgzrun.go()
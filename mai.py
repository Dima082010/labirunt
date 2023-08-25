import pygame
pygame.init()
import os

def fila_path(file_name):
    folder = os.path.abspath(__file__ + '/..')
    path = os.path.join(folder, file_name)
    return path

WIN_WIDTH = 1200
WIN_HEIGHT = 700
FPS = 40
LVL_1 = (18, 17, 17)
LVL_1_CLICK = (38, 37, 37)
LVL_2 = (64, 23, 4)
LVL_2_CLICK = (84, 43, 24)
LVL_3 = (46, 124, 7)
LVL_3_CLICK = (66, 144, 27)
TEXT = (255, 255, 255)
EXIT = (18, 78, 7)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

fon = pygame.image.load(fila_path(r"images\turma.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

fon_menu = pygame.image.load(fila_path(r'images\main.jpg'))
fon_menu = pygame.transform.scale(fon_menu, (WIN_WIDTH, WIN_HEIGHT))

win_image = pygame.image.load(fila_path(r'images\winn.jpg'))
win_image = pygame.transform.scale(win_image, (WIN_WIDTH, WIN_HEIGHT))

over_image = pygame.image.load(fila_path(r'images\game_over.jpg'))
over_image = pygame.transform.scale(over_image, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(fila_path(r'music\fon_music_menu.mp3'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


music_key = pygame.mixer.Sound(fila_path(r'music\vzyali-v-ruki-svyazku-klyuchey.ogg'))

music_door = pygame.mixer.Sound(fila_path(r'music\skrip-dvernoy-ruchki.ogg'))

music_shot = pygame.mixer.Sound(fila_path(r'music\vyistrel-iz-blastera.ogg'))
music_shot.set_volume(0.2)

music_bruck = pygame.mixer.Sound(fila_path(r'music\facebook_sms.ogg'))

music_eat = pygame.mixer.Sound(fila_path(r'music\poedanie-ukus-yabloka.ogg'))

music_closed_door = pygame.mixer.Sound(fila_path(r'music\door.ogg'))

music_gear = pygame.mixer.Sound(fila_path(r'music\gear.ogg'))

music_boss = pygame.mixer.Sound(fila_path(r'music\gear.ogg'))



class Game_sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(fila_path(image_name))
        self.image = pygame.transform.scale(self.image, (width, height))

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Buton():
    def __init__(self, x, y, width, height, text, size, no_click, click, text_color, p_x, p_y):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = pygame.font.SysFont('calibri', size).render(text, True, text_color)
        self.no_click = no_click
        self.click = click
        self.color = no_click
        self.p_x = p_x
        self.p_y = p_y
    
    def show(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + self.p_x, self.rect.y + self.p_y))



class Player(Game_sprite):
    def __init__(self, x, y, width, height, image_name, can_shot):
        super().__init__(x, y, width, height, image_name)
        self.speedx = 0
        self.speedy = 0
        self.direction = 'left'
        self.image_l = self.image
        self.image_r = pygame.transform.flip(self.image, True, False)
        self.is_key = 0
        self.can_shot = can_shot
        self.is_gear = False
        self.image_gear_l = pygame.image.load(fila_path(r'images\lufi.png'))
        self.image_gear_l = pygame.transform.scale(self.image_gear_l, (width, height))
        self.image_gear_r = pygame.transform.flip(self.image_gear_l, True, False)
        self.image_player_l = self.image_l
        self.image_player_r = self.image_r
        self.counter = 600

    def gear_on(self):
        self.is_gear = True
        if self.direction == 'left':
            self.image = self.image_gear_l
        elif self.direction == 'right':
            self.image = self.image_gear_r
        self.image_r = self.image_gear_r
        self.image_l = self.image_gear_l
    
    def gear_off(self):
        self.is_gear = False
        if self.direction == 'left':
            self.image = self.image_player_l
        elif self.direction == 'right':
            self.image = self.image_player_r
        self.image_r = self.image_player_r
        self.image_l = self.image_player_l

    def update(self):
        if self.speedx < 0 and self.rect.left > 0 or self.speedx > 0 and self.rect.right < WIN_WIDTH:           
            self.rect.x += self.speedx
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speedx < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)
        elif self.speedx > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)        

        if self.speedy < 0 and self.rect.top > 0 or self.speedy > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speedy

        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speedy < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        elif self.speedy > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)

        if self.is_gear == True:
            self.counter -= 1
            if self.counter == 0:
                self.is_gear = False
                self.gear_off()
                self.counter = 600
        
    def shot(self):
        if self.direction == 'right':
            bullet = Bulet(self.rect.right, self.rect.centery, 20, 20, r'images\ball.png', 6)
        elif self.direction == 'left':
            bullet = Bulet(self.rect.left - 20, self.rect.centery, 20, 20, r'images\ball.png', -6)
        bullets.add(bullet)

class Enemy(Game_sprite):
    def __init__(self, x, y, width, height, image_name, min_kord, max_kord, direction, speed):
        super().__init__(x, y, width, height, image_name)
        self.min_kord = min_kord
        self.max_kord = max_kord
        self.direction = direction
        self.speed = speed
        if direction == 'left' or direction == 'right':
            self.image_l = self.image
            self.image_r = pygame.transform.flip(self.image, True, False)
    
    def update(self):
        if self.direction == 'left' or self.direction == 'right':
            if self.direction == 'left':
                self.rect.x -= self.speed
            elif self.direction == 'right':
                self.rect.x += self.speed
            
            if self.rect.left <= self.min_kord:
                self.direction = 'right'
                self.image = self.image_r
            elif self.rect.right >= self.max_kord:
                self.direction = 'left'
                self.image = self.image_l

        elif self.direction == 'up' or self.direction == 'down':
            if self.direction == 'up':
                self.rect.y -= self.speed
            elif self.direction == 'down':
                self.rect.y += self.speed
            
            if self.rect.top <= self.min_kord:
                self.direction = 'down'
            elif self.rect.bottom >= self.max_kord:
                self.direction = 'up'

class Shot(Enemy):
    def __init__(self, x, y, width, height, image_name, min_kord, max_kord, direction, speed, timer):
        super().__init__(x, y, width, height, image_name, min_kord, max_kord, direction, speed)
        self.timer = timer
        self.max_timer = timer

    def update(self):
        super().update()
        self.timer -= 1
        if self.timer == 0:
            self.timer = self.max_timer
            self.shot()

    def shot(self):
        if self.direction == 'right':
            bullet = Bulet(self.rect.right, self.rect.centery, 20, 20, r'images\ball_2.png', 6)
        else:
            bullet = Bulet(self.rect.left - 20, self.rect.centery, 20, 20, r'images\ball_2.png', -6)
        bullets_enemy.add(bullet)


class Super_Shot(Shot):
    def __init__(self, x, y, width, height, image_name, min_kord, max_kord, direction, speed, timer):
        super().__init__(x, y, width, height, image_name, min_kord, max_kord, direction, speed, timer)
        self.health = 5


class Bulet(Game_sprite):
    def __init__(self, x, y, width, height, image_name, speed_ball):
        super().__init__(x, y, width, height, image_name)
        self.speed = speed_ball

    def update(self):
        self.rect.x += self.speed
        if self.rect.left >= WIN_WIDTH or self.rect.right <= 0:
            self.kill()

enemys = pygame.sprite.Group()



frukt3 = Game_sprite(90, 240, 40, 60, r"images\frukt2.png")


bullets = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()

walls_bruck = pygame.sprite.Group()

walls = pygame.sprite.Group()


btn_1 = Buton(550, 350, 70, 50, 'lvl 1', 30, LVL_1, LVL_1_CLICK, TEXT, 10, 10)
btn_2 = Buton(550, 420, 70, 50, 'lvl 2', 30, LVL_2, LVL_2_CLICK, TEXT, 10, 10)
btn_3 = Buton(550, 490, 70, 50, 'lvl 3', 30, LVL_3, LVL_3_CLICK, TEXT, 10, 10)
btn_exit = Buton(550, 560, 70, 50, 'exit', 30, EXIT, LVL_3_CLICK, TEXT, 10, 10)

def create_lvl_1():
    global player, frukt, key, bonus, exit, wall6
    player = Player(5, 6, 50, 70, r'images\Luffy.png', 0)
    frukt = Game_sprite(90, 140, 40, 60, r'images\frukt.png')
    bonus = Game_sprite(250, 250, 50, 70, r'images\bonus.png')
    key = Game_sprite(1000, 20, 50, 70, r'images\keys.png')
    exit = Game_sprite(5, 600, 100, 50, r'images\exit.png')


    fon = pygame.image.load(fila_path(r"images\turma.jpg"))
    fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))
    
    pygame.mixer.music.load(fila_path(r'music\lvl1_music.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    bullets.empty()
    bullets_enemy.empty()

    enemys.empty()
    enemy = Enemy(600, 480, 50, 70, r'images\gggg.png', 0, 600, 'left', 4)
    enemys.add(enemy)
    enemy2 = Enemy(150, 140, 50, 70, r'images\Crocodile.png', 150, 680, 'right', 5)
    enemys.add(enemy2)
    enemy3 = Shot(1150, 110, 50, 90, r'images\katakuri.png', 0, 200, 'up', 5, 50)
    enemys.add(enemy3)
    enemy4 = Enemy(1150, 630, 50, 70, r'images\leopard.png', 155, 1150, 'left', 7)
    enemys.add(enemy4)

    walls.empty()
    wall1 = Game_sprite(85, 6, 5, 200, r'images\wol.jpg') 
    walls.add(wall1)
    wall2 = Game_sprite(85, 206, 250, 5, r'images\wol.jpg')
    walls.add(wall2)
    wall3 = Game_sprite(335, 206, 5, 200, r'images\wol.jpg')
    walls.add(wall3)
    wall4 = Game_sprite(600, 300, 200, 5, r'images\wol.jpg')
    walls.add(wall4)
    wall5 = Game_sprite(5, 565, 1000, 5, r'images\wol.jpg')
    walls.add(wall5)
    wall6 = Game_sprite(150, 570, 5, 250, r'images\wol.jpg')
    walls.add(wall6)
    wall7 = Game_sprite(800, 306, 5, 250, r'images\wol.jpg')
    walls.add(wall7)
    wall8 = Game_sprite(220, 210, 5, 190, r'images\wol.jpg')
    walls.add(wall8)
    wall9 = Game_sprite(950, 200, 250, 5, r'images\wol.jpg')
    walls.add(wall9)
    wall11 = Game_sprite(600, 300, 5, 250, r'images\wol.jpg')
    walls.add(wall11)
    wall12 = Game_sprite(2500, 6, 5, 100, r'images\wol.jpg')
    walls.add(wall12)
    wall13 = Game_sprite(650, 0, 5, 150, r'images\wol.jpg')
    walls.add(wall13)
    wall14 = Game_sprite(800, 150, 5, 150, r'images\wol.jpg')
    walls.add(wall14)
    wall15 = Game_sprite(800, 320, 200, 5, r'images\wol.jpg')
    walls.add(wall15)
    wall16 = Game_sprite(1000, 450, 200, 5, r'images\wol.jpg')
    walls.add(wall16)



    

def create_lvl_2():
    global player, exit_2, frukt_2, bonus_2
    exit_2 = Game_sprite(600, 625, 100, 50, r'images\exit.png')
    frukt_2 = Game_sprite(700, 255, 40, 60, r"images\Mochi.png")
    player = Player(20, 630, 50, 70, r'images\Luffy.png', 1)
    bonus_2 = Game_sprite(38, 196, 50, 70, r'images\bonus.png')

    fon = pygame.image.load(fila_path(r"images\turma.jpg"))
    fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

    pygame.mixer.music.load(fila_path(r'music\fon_music_lvl2.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    bullets.empty()
    bullets_enemy.empty()

    enemys.empty()
    #! Створи ворогів діма!
    enemy1_2 = Enemy(290, 35, 50, 70, r'images\prison.png', 35, 400, 'down', 4)
    enemys.add(enemy1_2)
    enemy2_2 = Shot(1100, 0, 50, 90, r'images\katakuri.png', 0, 400, 'down', 4, 50)
    enemys.add(enemy2_2)
    enemy3_2 = Enemy(15, 500, 50, 70, r'images\Crocodile.png', 0, 780, 'left', 5)
    enemys.add(enemy3_2)
    enemy4_2 = Enemy(575, 20, 60, 80, r'images\leopard.png', 575, 1020, 'right', 5)
    enemys.add(enemy4_2)
    enemy5_2 = Enemy(565, 170, 40, 60, r'images\gggg.png', 565, 914, 'right', 5)
    enemys.add(enemy5_2)
    enemy6_2 = Enemy(1111, 410, 50, 60, r'images\lo.png', 410, 690, 'down', 4)
    enemys.add(enemy6_2)

    walls_bruck.empty()

    wall_bruck1_2 = Game_sprite(400, 570, 200, 5, r'images\wol.jpg')
    walls_bruck.add(wall_bruck1_2)
    wall_bruck2_2 = Game_sprite(195, 152, 5, 150, r'images\wol.jpg')
    walls_bruck.add(wall_bruck2_2)
    wall_bruck3_2 = Game_sprite(550, 350, 200, 5, r'images\wol.jpg')
    walls_bruck.add(wall_bruck3_2)
    wall_bruck4_2 = Game_sprite(1040, 100, 5, 200, r'images\wol.jpg')
    walls_bruck.add(wall_bruck4_2)
    wall_bruck5_2 = Game_sprite(745, 575, 5, 200, r'images\wol.jpg')
    walls_bruck.add(wall_bruck5_2)

    walls.empty()
    #! створити стіни!
    wall1_2 = Game_sprite(0, 570, 400, 5, r'images\wol.jpg')
    walls.add(wall1_2)
    wall2_2 = Game_sprite(550, 570, 5, 130, r'images\wol.jpg')
    walls.add(wall2_2)
    wall3_2 = Game_sprite(100, 450, 290, 5, r'images\wol.jpg')
    walls.add(wall3_2)
    wall4_2 = Game_sprite(389, 100, 5, 355, r'images\wol.jpg')
    walls.add(wall4_2)
    wall5_2 = Game_sprite(0, 300, 200, 5, r'images\wol.jpg')
    walls.add(wall5_2)
    wall6_2 = Game_sprite(0, 150, 200, 5, r'images\wol.jpg')
    walls.add(wall6_2)
    wall7_2 = Game_sprite(550, 570, 500, 5, r'images\wol.jpg')
    walls.add(wall7_2)
    wall8_2 = Game_sprite(550, 0, 5, 450, r'images\wol.jpg')
    walls.add(wall8_2)
    wall9_2 = Game_sprite(550, 105, 250, 5, r'images\wol.jpg')
    walls.add(wall9_2)
    wall10_2 = Game_sprite(925, 105, 5, 470, r'images\wol.jpg')
    walls.add(wall10_2)
    wall11_2 = Game_sprite(800, 350, 5, 220, r'images\wol.jpg')
    walls.add(wall11_2)
    wall12_2 = Game_sprite(675, 350, 125, 5, r'images\wol.jpg')
    walls.add(wall12_2)
    wall13_2 = Game_sprite(675, 225, 5, 125, r'images\wol.jpg')
    walls.add(wall13_2)
    wall14_2 = Game_sprite(675, 225, 125, 5, r'images\wol.jpg')
    walls.add(wall14_2)
    wall15_2 = Game_sprite(1040, 0, 5, 100, r'images\wol.jpg')
    walls.add(wall15_2)
    wall16_2 = Game_sprite(1040, 200, 5, 200, r'images\wol.jpg')
    walls.add(wall16_2)
    wall17_2 = Game_sprite(1040, 400, 155, 5, r'images\wol.jpg')
    walls.add(wall17_2)




def create_lvl_3():
    global player, bonus_3, exit_3, frukt_3
    exit_3 = Game_sprite(1060, 500, 100, 50, r'images\exit.png')
    frukt_3 = Game_sprite(440, 250, 50, 70, r'images\frukt2.png')
    bonus_3 = Game_sprite(1100, 630, 50, 60, r"images\bonus.png")
    player = Player(50, 630, 50, 70, r'images\Luffy.png', 2)
    bullets.empty()
    bullets_enemy.empty()

    enemys.empty()

    enemy1_3 = Enemy(50, 200, 50, 70, r'images\gggg.png', 0, 600, 'down', 4)
    enemys.add(enemy1_3)
    enemy2_3 = Enemy(880, 115, 50, 70, r'images\Crocodile.png', 100, 600, 'left', 4)
    enemys.add(enemy2_3)
    enemy3_3 = Enemy(1050, 620, 60, 80, r'images\leopard.png', 200, 1050, 'left', 6)
    enemys.add(enemy3_3)
    enemy5_3 = Shot(1100, 0, 50, 90, r'images\katakuri.png', 0, 450, 'down', 4, 50)
    enemys.add(enemy5_3)
    enemy6_3 = Shot(630, 235, 50, 90, r'images\katakuri.png', 235, 575, 'down', 4, 50)
    enemys.add(enemy6_3)

    walls_bruck.empty()

    wall_bruck1_3 = Game_sprite(155, 600, 5, 200, r'images\wol.jpg')
    walls_bruck.add(wall_bruck1_3)
    wall_bruck2_3 = Game_sprite(500, 600, 200, 5, r'images\wol.jpg')
    walls_bruck.add(wall_bruck2_3)
    wall_bruck3_3 = Game_sprite(160, 455, 340, 5, r'images\wol.jpg')
    walls_bruck.add(wall_bruck3_3)
    wall_bruck4_3 = Game_sprite(500, 200, 100, 5, r'images\wol.jpg')
    walls_bruck.add(wall_bruck4_3)
    wall_bruck5_3 = Game_sprite(890, 0, 5, 200, r'images\wol.jpg')
    walls_bruck.add(wall_bruck5_3)

    walls.empty()

    wall1_3 = Game_sprite(0, 600, 500, 5, r'images\wol.jpg')
    walls.add(wall1_3)
    wall2_3 = Game_sprite(495, 200, 5, 400, r'images\wol.jpg')
    walls.add(wall2_3)
    wall3_3 = Game_sprite(595, 600, 600, 5, r'images\wol.jpg')
    walls.add(wall3_3)
    wall4_3 = Game_sprite(155, 195, 350, 5, r'images\wol.jpg')
    walls.add(wall4_3)
    wall5_3 = Game_sprite(155, 200, 5, 260, r'images\wol.jpg')
    walls.add(wall5_3)
    wall6_3 = Game_sprite(595, 200, 5, 400, r'images\wol.jpg')
    walls.add(wall6_3)
    wall7_3 = Game_sprite(595, 200, 300, 5, r'images\wol.jpg')
    walls.add(wall7_3)
    wall8_3 = Game_sprite(1050, 0, 5, 450, r'images\wol.jpg')
    walls.add(wall8_3)
    wall9_3 = Game_sprite(1050, 450, 200, 5, r'images\wol.jpg')
    walls.add(wall9_3)
    



def create_lvl_4():
    global player, txt_health_boss 
    player = Player(0, 630, 50, 70, r'images\Luffy.png', 1)
    bullets.empty()
    bullets_enemy.empty()
    enemys.empty()
    boss = Super_Shot(1000, 0, 100, 200, r'images\prison.png', 0, 700, 'down', 3, 110)
    enemys.add(boss)
    txt_health_boss = pygame.font.SysFont('calibri', 100).render('BOSS HP: ' + str(boss.health), True, TEXT)
    walls_bruck.empty()
    
    walls.empty()

    wall1_4 = Game_sprite(150, 0, 5, 100, r'images\wol.jpg')
    walls.add(wall1_4)
    wall2_4 = Game_sprite(150, 200, 5, 100, r'images\wol.jpg')
    walls.add(wall2_4)
    wall3_4 = Game_sprite(150, 400, 5, 100, r'images\wol.jpg')
    walls.add(wall3_4)
    wall4_4 = Game_sprite(150, 600, 5, 100, r'images\wol.jpg')
    walls.add(wall4_4)
    wall5_4 = Game_sprite(250, 100, 5, 100, r'images\wol.jpg')
    walls.add(wall5_4)
    wall6_4 = Game_sprite(250, 300, 5, 100, r'images\wol.jpg')
    walls.add(wall6_4)
    wall7_4 = Game_sprite(250, 500, 5, 100, r'images\wol.jpg')
    walls.add(wall7_4)
    wall8_4 = Game_sprite(350, 0, 5, 100, r'images\wol.jpg')
    walls.add(wall8_4)
    wall9_4 = Game_sprite(350, 200, 5, 100, r'images\wol.jpg')
    walls.add(wall9_4)
    wall10_4 = Game_sprite(350, 400, 5, 100, r'images\wol.jpg')
    walls.add(wall10_4)
    wall11_4 = Game_sprite(350, 600, 5, 100, r'images\wol.jpg')
    walls.add(wall11_4)




lvl = 0
game = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        if lvl == 1 or lvl == 2 or lvl == 3 or lvl == 4:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speedx = 5
                    player.direction = 'right'
                    player.image = player.image_r
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speedx = -5
                    player.direction = 'left'
                    player.image = player.image_l
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speedy = -5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speedy = 5
                if event.key == pygame.K_TAB:
                    if len(bullets.sprites()) < player.can_shot:
                        player.shot()
                        music_shot.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speedx = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speedx = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speedy = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speedy = 0

        elif lvl == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn_1.rect.collidepoint(x, y):
                    btn_1.color = btn_1.click
                elif btn_2.rect.collidepoint(x, y):
                    btn_2.color = btn_2.click
                elif btn_3.rect.collidepoint(x, y):
                    btn_3.color = btn_3.click
                elif btn_exit.rect.collidepoint(x, y):
                    btn_exit.color = btn_exit.click
                else:
                    btn_1.color = btn_1.no_click
                    btn_2.color = btn_2.no_click
                    btn_3.color = btn_3.no_click
                    btn_exit.color = btn_exit.no_click

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if btn_1.rect.collidepoint(x, y):
                    create_lvl_1()
                    lvl = 1
                elif btn_2.rect.collidepoint(x, y):
                    create_lvl_2()
                    lvl = 2
                elif btn_3.rect.collidepoint(x, y):
                    create_lvl_3()
                    lvl = 3
                elif btn_exit.rect.collidepoint(x, y):
                    game = False


    if lvl == 1:
        window.blit(fon, (0, 0))
        player.show()
        player.update()
        frukt.show()
        bonus.show()
        key.show()
        exit.show()
        enemys.draw(window)
        enemys.update()
        walls.draw(window)
        bullets.draw(window)
        bullets.update()
        bullets_enemy.draw(window)
        bullets_enemy.update()
        
    
        if pygame.sprite.spritecollide(player, enemys, False) and player.is_gear == False or pygame.sprite.spritecollide(player, bullets_enemy, True) and player.is_gear == False:
            lvl = 11
            pygame.mixer.music.load(fila_path(r'music\__kirbydx__wah-wah-sad-trombone (1).ogg'))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            
        if pygame.sprite.collide_rect(player, frukt):
            player.can_shot += 1
            music_eat.play()
            frukt.rect.y = -600

        if pygame.sprite.collide_rect(player, key):
            player.is_key = 1
            music_key.play()
            key.rect.y = -500

        if player.rect.collidepoint(155, 630) and player.is_key != -1:
            if player.is_key == 1:
                music_door.play()
                wall6.kill()
                player.is_key = -1
            else:
                music_closed_door.play()
                print('В тебе немає ключа!')

        if pygame.sprite.collide_rect(player, exit):
            create_lvl_2()
            lvl = 2
            
        
        if pygame.sprite.collide_rect(player, bonus):
            player.gear_on()
            music_gear.play()
            bonus.rect.y = -100

        pygame.sprite.groupcollide(bullets, walls, True, False)
        pygame.sprite.groupcollide(bullets, enemys, True, True)
    
    elif lvl == 2:
        window.blit(fon, (0, 0))
        player.show()
        player.update()
        frukt_2.show()
        bonus_2.show()
        exit_2.show()
        enemys.draw(window)
        enemys.update()
        walls.draw(window)
        bullets.draw(window)
        bullets.update()
        bullets_enemy.draw(window)
        bullets_enemy.update()
        walls_bruck.draw(window)

        pygame.sprite.groupcollide(bullets, walls, True, False)
        pygame.sprite.groupcollide(bullets, enemys, True, True)

        if pygame.sprite.spritecollide(player, walls_bruck, True):
            music_bruck.play()

        if pygame.sprite.collide_rect(player, bonus_2):
            player.gear_on()
            music_gear.play()
            bonus_2.rect.y = -100

        if pygame.sprite.collide_rect(player, exit_2):
            create_lvl_3()
            lvl = 3

        if pygame.sprite.collide_rect(player, frukt_2):
            player.can_shot += 1
            music_eat.play()
            frukt_2.rect.y = -600

        if pygame.sprite.spritecollide(player, enemys, False) and player.is_gear == False or pygame.sprite.spritecollide(player, bullets_enemy, True) and player.is_gear == False:
            lvl = 11
            pygame.mixer.music.load(fila_path(r'music\__kirbydx__wah-wah-sad-trombone (1).ogg'))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)

    elif lvl == 3:
        window.blit(fon, (0, 0))
        player.show()
        player.update()
        enemys.draw(window)
        enemys.update()
        walls.draw(window)
        bullets.draw(window)
        bullets.update()
        bonus_3.show()
        frukt_3.show()
        exit_3.show()
        bullets_enemy.draw(window)
        bullets_enemy.update()
        walls_bruck.draw(window)

        pygame.sprite.groupcollide(bullets, walls, True, False)
        pygame.sprite.groupcollide(bullets, enemys, True, True)

        if pygame.sprite.spritecollide(player, walls_bruck, True):
            music_bruck.play()

        if pygame.sprite.collide_rect(player, bonus_3):
            player.gear_on()
            music_gear.play()
            bonus_3.rect.y = -100

        if pygame.sprite.collide_rect(player, exit_3):
            create_lvl_4()
            lvl = 4
            

        if pygame.sprite.collide_rect(player, frukt_3):
            player.can_shot += 1
            music_eat.play()
            frukt_3.rect.y = -600

        if pygame.sprite.spritecollide(player, enemys, False) and player.is_gear == False or pygame.sprite.spritecollide(player, bullets_enemy, True) and player.is_gear == False:
            lvl = 11
            pygame.mixer.music.load(fila_path(r'music\__kirbydx__wah-wah-sad-trombone (1).ogg'))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)

    elif lvl == 4:
        window.blit(fon, (0, 0))
        player.show()
        player.update()
        enemys.draw(window)
        enemys.update()
        walls.draw(window)
        bullets.draw(window)
        bullets.update()
        bullets_enemy.draw(window)
        bullets_enemy.update()
        walls_bruck.draw(window)
        window.blit(txt_health_boss, (400, 0))


        pygame.sprite.groupcollide(bullets, walls, True, False)
        
        if pygame.sprite.spritecollide(player, enemys, False) and player.is_gear == False or pygame.sprite.spritecollide(player, bullets_enemy, True) and player.is_gear == False:
            lvl = 11
            pygame.mixer.music.load(fila_path(r'music\__kirbydx__wah-wah-sad-trombone (1).ogg'))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            
        health = pygame.sprite.groupcollide(enemys, bullets, False, True)
        if health:
            for b in health:
                b.health -= 1
                txt_health_boss = pygame.font.SysFont('calibri', 100).render('BOSS HP: ' + str(b.health), True, TEXT)
                player.rect.x = 0
                player.rect.y = 630
                b.max_timer -= 20
                if b.health == 0:
                    lvl = 10
                    
                    pygame.mixer.music.load(fila_path(r'music\win_music.mp3'))
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play(-1)
                else:
                    music_boss.play()




    elif lvl == 0:
        window.blit(fon_menu, (0, 0))
        btn_1.show()
        btn_2.show()
        btn_3.show()
        btn_exit.show()

    elif lvl == 10:
        window.blit(win_image, (0, 0))
    
    elif lvl == 11:
        window.blit(over_image, (0, 0))

    clock.tick(FPS)
    pygame.display.update()
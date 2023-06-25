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

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

fon = pygame.image.load(fila_path(r"images\turma.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

win_image = pygame.image.load(fila_path(r'images\wol.jpg'))
win_image = pygame.transform.scale(win_image, (WIN_WIDTH, WIN_HEIGHT))

over_image = pygame.image.load(fila_path(r'images\turma.jpg'))
over_image = pygame.transform.scale(over_image, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(fila_path(r'music\lvl1_music.mp3'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


class Game_sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(fila_path(image_name))
        self.image = pygame.transform.scale(self.image, (width, height))

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Game_sprite):
    def __init__(self, x, y, width, height, image_name):
        super().__init__(x, y, width, height, image_name)
        self.speedx = 0
        self.speedy = 0
        self.direction = 'left'
        self.image_l = self.image
        self.image_r = pygame.transform.flip(self.image, True, False)

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





player = Player(5, 6, 50, 70, r'images\Luffy.png')
enemy = Game_sprite(1100, 500, 50, 70, r'images\prison.png')
enemy2 = Game_sprite(1100, 500, 50, 70, r'images\Crocodile.png')
enemy3 = Game_sprite(1100, 500, 50, 70, r'images\katakuri.png')
enemy4 = Game_sprite(1100, 500, 50, 70, r'images\leopard.png')
finish = Game_sprite(90, 140, 40, 60, r'images\frukt.png')
finish2 = Game_sprite(90, 240, 40, 60, r"images\Mochi.png")
finish3 = Game_sprite(90, 240, 40, 60, r"images\frukt2.png")

walls = pygame.sprite.Group()
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
wall6 = Game_sprite(50, 565, 5, 250, r'images\wol.jpg')
walls.add(wall6)
wall7 = Game_sprite(800, 306, 5, 250, r'images\wol.jpg')
walls.add(wall7)
#wall8 = Game_sprite(550, 556, 250, 5, r'images\wol.jpg')
#walls.add(walls)
wall9 = Game_sprite(950, 200, 250, 5, r'images\wol.jpg')
walls.add(wall9)
wall10 = Game_sprite(950, 0, 5, 200, r'images\wol.jpg')
walls.add(wall10)


lvl = 1
game = True

while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if lvl == 1:
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speedx = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speedx = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speedy = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speedy = 0






    if lvl == 1:
        window.blit(fon, (0, 0))
        player.show()
        player.update()
        enemy.show()
        finish.show()
        enemy2.show()
        enemy3.show()
        enemy4.show()
        walls.draw(window)

        if pygame.sprite.collide_rect(player, finish):
            lvl = 10
            pygame.mixer.music.load(fila_path(r'music\win_music.mp3'))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)

    
    elif lvl == 10:
        window.blit(win_image, (0, 0))
    
    elif lvl == 11:
        window.blit(over_image, (0, 0))

    clock.tick(FPS)
    pygame.display.update()
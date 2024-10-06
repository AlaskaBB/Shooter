from pygame import *
from random import randint
from time import time as timer
from pygame.font import  SysFont

score = 0
lost = 0
goal = 30
max_lost = 3
life = 3



class GameSprite(sprite.Sprite):


    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0



class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)

win = font1.render('ПОБЕДА', True, (255, 255, 255))
lose = font1.render('ПОРАЖЕНИЕ', True, (191, 0, 0))

#pics
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Космический шутер')

background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add (monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)


finish = False
run = True

reload_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not reload_time:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and not reload_time:
                    last_time = timer()
                    reload_time = True


    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)


        if reload_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезарядка, жди...', 1, 'indianred')
                window.blit(reload, (230, 460))
            else:
                num_fire = 0
                reload_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        if lost >= max_lost or sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        if life == 3:
            life_color = 'lawngreen'
        if life == 2:
            life_color = 'gold'
        if life == 1:
            life_color = 'red'

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()
    time.delay(50)


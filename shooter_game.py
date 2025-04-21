#Создай собственный Шутер!

from pygame import *
from random import randint
x1 = 100
y1 = 100

clock = time.Clock()

window  = display.set_mode((700, 500))
display.set_caption('The shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 36)

game = True

game_over = False
game_won = False

win_text = font1.render('You win!', True, (0, 255, 0))
lose_text = font1.render('You lose...', True, (255, 0, 0))
FPS = 60

score = 0
skipped = 0

score_text = font1.render('Счет:' + str(score), True, (255, 255, 255))
skipped_text = font1.render('Пропущено:' + str(skipped), True, (255, 255, 255))

bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (75, 75))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__(sprite_image, sprite_x, sprite_y, sprite_speed)

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            global bullets
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 7)
            bullets.add(bullet)
            fire_sound.play()


class Enemy(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__(sprite_image, sprite_x, sprite_y, sprite_speed)

    def update(self):
        global skipped
        self.rect.y += self.speed
        if self.rect.y > 435:
            self.rect.y = -20
            self.rect.x = randint(20, 615)
            skipped += 1

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

class Bullet(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__(sprite_image, sprite_x, sprite_y, sprite_speed)

    def update(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 7)
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

def display_message(text):
    message = font1.render(text, True, (255, 0, 0))
    win.blit(message, (win_width // 2 - message.get_width() // 2, win_height // 2 - message.get_height() // 2))
    display.update()
    time.delay(3000)

player = Player('rocket.png', 350, 400, 10)

enemy1 = Enemy('ufo.png', randint(20,615), -75, 2)  
enemy2 = Enemy('ufo.png', randint(20,615), -100, 2)
enemy3 = Enemy('ufo.png', randint(20,615), -75, 2)
enemy4 = Enemy('ufo.png', randint(20,615), -65, 2)
enemy5 = Enemy('ufo.png', randint(20,615), -125, 2)

monsters = sprite.Group()
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)


while game:
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()


    if game_over != True:
        window.blit(background, (0, 0))
        window.blit(score_text, (20, 10))
        window.blit(skipped_text, (20, 40))
        bullets.draw(window)
        bullets.update()
        monsters.update()
        player.reset()
        monsters.draw(window)
        
        monsters.update()
        player.update()
        
        for bullet in bullets:
            collided_enemies = sprite.spritecollide(bullet, monsters, True)
            if collided_enemies:
                score += 1
                
            if bullet.rect.y < 0:
                bullet.kill()
    
    else:
        if game_won:
            window.blit(win_text, (170, 200))
        else:
            window.blit(lose_text, (170, 200))
    score_text = font1.render('Счет:' + str(score), True, (255, 255, 255))
    skipped_text = font1.render('Пропущено:' + str(skipped), True, (255, 255, 255))
    clock.tick(FPS)
    display.update()





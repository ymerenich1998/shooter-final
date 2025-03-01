from pygame import *
from random import randint

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного гравця
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed 
           
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height - 80:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
            

# ініціалізація Pygame:
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

finish = False
run = True
clock = time.Clock()
FPS = 60

player_life = 3 # кількість життів
score = 0 # збито кораблів
goal = 10 #Кількість кораблів
lost = 0 # пропущено кораблів
max_lost = 10 # максимальна кількість пропущених кораблів
num_fire = 0 # кількість пострілів
rel_time = False # час відновлення

font.init()
font1 = font.SysFont("Arial",   )
font2 = font.SysFont("Arial", 48)
text_win = font2.render("Ви перемогли!", True, (255, 215, 0))
text_lose = font2.render("Ви програли!", True, (180, 0, 0))
reload = font1.render("Підзарядка...", True, (255, 255, 255))


ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), 0, 80, 50, randint(1, 3))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy("asteroid.png", randint(80, win_width - 80), 0, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = time.get_ticks()
                    rel_time = True
                

    if not finish:
        # Добавляємо фон
        window.blit(background, (0, 0))
        
        text_score = font1.render("Рахунок: " + str(score), 1, (255, 255, 255))
        text_lost = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_current_life = font1.render("Життя: " + str(player_life), 1, (255, 255, 255))

        if rel_time == True:
            now_time = time.get_ticks()
            if now_time - last_time < 2500:
                window.blit(reload, (win_width // 2 - reload.get_width() // 2, win_height - reload.get_height() - 10))
            else:
                num_fire = 0
                rel_time = False

        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))
        window.blit(text_current_life, ((win_width - text_current_life.get_width() - 10), 20))

        # Рухаємо спрайти
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        # Малюємо спрайти
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        # Перевірка зіткнення куль та монстрів
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), 0, 80, 50, randint(1, 3))
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(text_lose, (win_width // 2 - text_lose.get_width() // 2, win_height // 2 - text_lose.get_height() // 2))

        collides_asteroids = sprite.spritecollide(ship, asteroids, False)
        for c in collides_asteroids:
            player_life = player_life - 1
            if player_life > 0:
               c.rect.x = randint(80, win_width - 80)
               c.rect.y = 0
            else:
                finish = True
                window.blit(text_lose, (win_width // 2 - text_lose.get_width() // 2, win_height // 2 - text_lose.get_height() // 2))

        if score >= goal:
            finish = True
            window.blit(text_win, (win_width // 2 - text_win.get_width() // 2, win_height // 2 - text_win.get_height() // 2))

        display.update()
    clock.tick(FPS)
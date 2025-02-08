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
        pass

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height - 80:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
            

# ініціалізація Pygame:
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

finish = False
run = True
clock = time.Clock()
FPS = 60

score = 0 # збито кораблів
lost = 0 # пропущено кораблів

font.init()
font1 = font.Font(None, 36)

ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), 0, 80, 50, randint(1, 5))
    monsters.add(monster)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        # Добавляємо фон
        window.blit(background, (0, 0))
        
        text_score = font1.render("Рахунок: " + str(score), 1, (255, 255, 255))
        text_lost = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))

        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))

        # Рухаємо спрайти
        ship.update()
        monsters.update()

        # Малюємо спрайти
        ship.reset()
        monsters.draw(window)

    display.update()
    clock.tick(FPS)
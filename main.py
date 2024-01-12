from pygame import *


window = display.set_mode((700, 500))
display.set_caption("Asteroids")

clock = time.Clock()

game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, GImage, x, y, width, height, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(GImage), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x <= 635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,30,-15)
        bullets.add(bullet)

bullets = sprite.Group()


from random import*

missed = 0
class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(0,650)
            self.rect.y = randint(-100,-70)
            missed += 1

class Bullet(GameSprite):
    def update(self):
      self.rect.y += self.speed
      if self.rect.y < 0:
          self.kill()      

asteroids = sprite.Group()
for i in range(6):
    asteroid = Enemy("asteroid.png",randint(0,650), randint(-100,-70),50,50,randint(1,2))
    asteroids.add(asteroid)



background = transform.scale(image.load("galaxy.jpg"), (700, 500))

ship = Player("rocket.png", 20, 400, 65, 95, 8)

mixer.init()
fire_sound = mixer.Sound("fire.ogg")


reload_time = False
num_fire = 0
from time import time as timer

font.init()
mainfont = font.SysFont("Arial",60)
score = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type  == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 20 and reload_time == False:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1
                elif num_fire >= 20 and reload_time == False:
                    reload_time = True
                    reload_start = timer()

            

    if not finish:
        window.blit(background, (0,0))
        missed_text = mainfont.render("Missed:" + str(missed),True,(0,255,0))
        window.blit(missed_text,(10,10))

        scored_text = mainfont.render("Scored   :" + str(score),True,(0,255,0))
        window.blit(scored_text,(10,50))

         
        ship.draw()
        ship.update()

        asteroids.update()
        asteroids.draw(window)


        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(asteroids,bullets,True,True)
        for tnite in collides:
            asteroid = Enemy("asteroid.png",randint(0,650), randint(-100,-70),50,50,randint(1,2))
            asteroids.add(asteroid)
            score += 1

        if reload_time:
            reload_end = timer()
            if reload_end - reload_start < 3:
                reloading = mainfont.render("RELOADING",True,(255,0,0))
                window.blit(reloading,(220,220))
            else: 
                num_fire = 0
                reload_time = False

        if sprite.spritecollide(ship,asteroids,False):
            reloading = mainfont.render("YOU LOSE",True,(250,0,0))
            window.blit(reloading,(220,220))
            finish = True

        if missed >= 10:
            reloading = mainfont.render("YOU LOSE",True,(250,0,0))
            window.blit(reloading,(220,220))
            finish = True
            
        
    display.update()
    clock.tick(60)
# Envisage - Ryan Bradshaw
import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

class Spritesheet:
    # loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Retrieve an image out of the spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2 + 20, height // 2 + 20))

        return image

class Char(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.shield = 100
        self.now = pg.time.get_ticks()
        self.last_update = 0

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                                self.game.spritesheet.get_image(690, 406, 120, 201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walking_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                                self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame, True, False))
        self.jumping_frame = [self.game.spritesheet.get_image(382, 763, 150, 181)]

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        self.rect.y += 1
        # Delete sprite = False
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits and not self.jumping:
            self.game.long_jump.play()
            self.jumping = True
            self.vel.y = -CHAR_JUMP

    def shoot(self):
        self.bullet = Bullet(self.rect.right, self.rect.centery)

    def update(self):
        self.animate()
        self.acc = vec(0, CHAR_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -CHAR_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = CHAR_ACC
            if self.game.score >= 100 and self.game.score < 500:
                self.acc.x += 0.2
            if self.game.score >= 500:
                self.acc.x += 0.7

        self.acc.x += self.vel.x * CHAR_FRIC
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # Walk animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame +1 ) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # Idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        if self.game.score < 100:
            images = [self.game.spritesheet.get_image(0, 96, 380, 94),
                      self.game.spritesheet.get_image(382, 408, 200, 100)]

        if self.game.score >= 100 and self.game.score < 500:
            images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                      self.game.spritesheet.get_image(213, 1662, 201, 100)]

        if self.game.score >= 500:
            images = [self.game.spritesheet.get_image(0, 768, 380, 94),
                      self.game.spritesheet.get_image(213, 1764, 201, 100)]

        if self.game.score == 100:
            # So that the sound only plays once
            self.game.new_zone.play()
        elif self.game.score == 500:
            self.game.new_zone.play()

        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < QUESTION_FREQ:
            Question(self.game, self)

class Question(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.questions
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['question'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)

        # Stage 1 mob sprites
        self.stage_1_up = self.game.spritesheet.get_image(801,609,110,141)
        self.stage_1_up.set_colorkey(BLACK)
        self.stage_1_down = self.game.spritesheet.get_image(800,860,110,141)
        self.stage_1_down.set_colorkey(BLACK)

        # Stage 2 mob sprites
        self.stage_2_up = self.game.spritesheet.get_image(568, 1534, 122, 135)
        self.stage_2_up.set_colorkey(BLACK)
        self.stage_2_down = self.game.spritesheet.get_image(566, 510, 122, 139)
        self.stage_2_down.set_colorkey(BLACK)

        # Stage 3 mob sprites
        self.stage_3_up = self.game.spritesheet.get_image(382, 635, 174, 126)
        self.stage_3_up.set_colorkey(BLACK)
        self.stage_3_down = self.game.spritesheet.get_image(382, 510, 182, 123)
        self.stage_3_down.set_colorkey(BLACK)

        if self.game.score < 100:
            self.image = self.stage_1_up
        if self.game.score >= 100 and self.game.score < 500:
            self.image = self.stage_2_up
        if self.game.score >= 500:
            self.image = self.stage_3_up

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + self.rect.width + random.randrange(0, 1500)
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)
        self.speedx = random.randrange(1, 3)
        self.speedy = 0
        self.accy = 0.2

    def update(self):
        self.rect.x -= self.speedx
        self.speedy += self.accy
        if self.speedy > 3 or self.speedy < -3:
            self.accy *= -1
        center = self.rect.center

        if self.accy < 0 and self.game.score < 100:
            self.image = self.stage_1_up
        if self.accy > 0 and self.game.score < 100:
            self.image = self.stage_1_down

        if self.accy < 0 and self.game.score >= 100 and self.game.score < 500:
            self.image = self.stage_2_up
        if self.accy > 0 and self.game.score >= 100 and self.game.score < 500:
            self.image = self.stage_2_down

        if self.accy < 0 and self.game.score >= 500:
            self.image = self.stage_3_up
        if self.accy > 0 and self.game.score >= 500:
            self.image = self.stage_3_down

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.speedy
        if self.rect.right <= 0:
            self.rect.x = WIDTH + self.rect.width + random.randrange(0, 500)
            self.rect.y = random.randrange(0, HEIGHT - self.rect.height)
            # !Could implement way to make mobs faster over time here:
            if self.game.score < 100:
                self.speedx = random.randrange(1, 3)
            if self.game.score >= 100 and self.game.score < 500:
                self.speedx = random.randrange(2, 5)
            if self.game.score >= 500:
                self.speedx = random.randrange(3, 7)

class Bullet(pg.sprite.Sprite):
    # removed game from parameters
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.speedx = -10
        else:
            self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()

# class Background(pg.sprite.Sprite):
#     def __init__(self, game):
#         self.groups = game.all_sprites, game.background
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#
#         self.cloud_bg = pg.image.load(path.join(self.img_dir, "cloud_bg.png"))
#         self.cloud_bg.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.x = random.randrange(WIDTH, WIDTH*2)
#         self.rect.y = random.randrange(HEIGHT-self.rect.height)
#
#     def update(self):
#         if self.rect.right < 0:
#             self.kill()

# Envisage - Ryan Bradshaw
# Comments with '!' at the beginning mean to-do
import pygame as pg
from sprites import *
from settings import *
from questions import *
import random
from os import path

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        #self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.mouse.set_visible(False)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # Highscore
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, "img")
        with open(path.join(self.dir, HS_File), "r+") as file:
            try:
                self.highscore = int(file.read())
            except:
                self.highscore = 0
        # Spritesheet
        self.spritesheet = Spritesheet(path.join(self.img_dir, SPRITESHEET))
        self.my_spritesheet = Spritesheet(path.join(self.img_dir, MY_SPRITESHEET))

        # Sounds
        self.snd_dir = path.join(self.dir, "snd")
        self.long_jump = pg.mixer.Sound(path.join(self.snd_dir, "long_jump.wav"))
        self.short_jump = pg.mixer.Sound(path.join(self.snd_dir, "short_jump.wav"))
        self.pistol_shoot = pg.mixer.Sound(path.join(self.snd_dir, "pistol_shoot.wav"))
        self.mob_hit = pg.mixer.Sound(path.join(self.snd_dir, "mob_hit.wav"))
        self.correct_answer = pg.mixer.Sound(path.join(self.snd_dir, "correct_answer.wav"))
        self.incorrect_answer = pg.mixer.Sound(path.join(self.snd_dir, "incorrect_answer.wav"))
        self.new_zone = pg.mixer.Sound(path.join(self.snd_dir, "new_zone.wav"))
        self.game_over = pg.mixer.Sound(path.join(self.snd_dir, "game_over.wav"))
        self.char_hit = pg.mixer.Sound(path.join(self.snd_dir, "char_hit.wav"))

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.questions = pg.sprite.Group()
        self.background = pg.sprite.Group()
        now = pg.time.get_ticks()
        self.current_frame = 0
        for i in range(8):
                Mob(game)
        self.char = Char(self)
        self.mob = Mob(self)
        for plat in PLATFORM_LIST:
            Platform(self,*plat)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        if self.char.vel.y > 0:
            # Character collides with platform
            plat_hits = pg.sprite.spritecollide(self.char, self.platforms, False)
            for plat_hit in plat_hits:
                if self.char.pos.x < plat_hit.rect.right + 20 and \
                self.char.pos.x > plat_hit.rect.left - 20:
                    if self.char.pos.y < plat_hit.rect.centery + 1:
                        self.char.pos.y = plat_hit.rect.top +  1
                        self.char.vel.y = 0
                        self.char.jumping = False

            # Character's bullet collides with mob
            #if self.score < 100:
            mob_hits = pg.sprite.groupcollide(self.bullets, self.mobs, True, True)
            if mob_hits:
                self.mob_hit.play()
                self.score += 10
                Mob(game)

            # Character touches question block
            question_hits = pg.sprite.spritecollide(self.char, self.questions, True)
            if question_hits:
                # Hit a question block - Display screen with question and answer
                if self.score < 100:
                    random_num = random.randrange(0, len(question_prompts_easy))
                    self.question_screen(random_num)
                if self.score >= 100:
                    random_num = random.randrange(0, len(question_prompts_med))
                    self.question_screen(random_num)


        # If character reaches right hand side of screen
        if self.char.rect.right >= WIDTH - 700:
            # if random.randrange(100) < 1:
            #     Background(self)
            self.char.pos.x -= max(abs(self.char.vel.x), 1)
            for sprite in self.background:
                sprite.rect.x -= max(abs(self.char.vel.x), 1)
            for plat in self.platforms:
                plat.rect.x -= max(abs(self.char.vel.x), 1)
                if plat.rect.right <= 0:
                    plat.kill()
                    self.score += 10
            for mob in self.mobs:
                mob.rect.x -= max(abs(self.char.vel.x), 1)
            for question in self.questions:
                question.rect.x -= max(abs(self.char.vel.x), 1)

        if self.char.rect.bottom > HEIGHT or self.char.rect.right <= 0:
            self.playing = False

        if self.score < 100:
            platform_count = 18
        if self.score >= 100 and self.score < 500:
            platform_count = 15
        if self.score >= 500:
            platform_count = 10

        while len(self.platforms) < platform_count:
            #Platform(self, random.randrange(WIDTH, 3.5 * WIDTH), random.randrange(150, HEIGHT))
            width_list = WIDTH, WIDTH + 100, WIDTH + 800, WIDTH + 1200, WIDTH + 1500
            height_list = HEIGHT - 280, HEIGHT - 470, HEIGHT - 750, HEIGHT - 920
            Platform(self, random.choice(width_list), random.choice(height_list))

        # Mob hits character
        hits = pg.sprite.spritecollide(self.char, self.mobs, True)
        for hit in hits:
            self.char_hit.play()
            if self.score < 100:
                self.char.shield -= 10
            if self.score >= 100 and self.score < 500:
                self.char.shield -= 20
            if self.score > 500:
                self.char.shield -= 30
            Mob(game)
            if self.char.shield <= 0:
                self.playing = False
                self.game_over_screen()

        # Shield recharge
        now = pg.time.get_ticks()
        self.last_update = 0
        if now - self.last_update > 8000:
            if self.char.shield <= 100:
                self.last_update = now
                self.char.shield += 0.015

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.char.jump()
                if event.key == pg.K_SPACE:
                    self.char.shoot()
                    self.pistol_shoot.play()
                    b = Bullet(self.char.rect.right, self.char.rect.centery)
                    self.all_sprites.add(b)
                    self.bullets.add(b)
                # Enter pause screen
                if event.key == pg.K_p:
                    self.pause_screen()
                # Exit full screen
                if event.key == pg.K_g:
                    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
                    pg.mouse.set_visible(True)
                # Enter full screen
                if event.key == pg.K_f:
                    self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
                    pg.mouse.set_visible(False)
                # Ground slam / Platform drop
                if event.key == pg.K_DOWN:
                    self.char.vel.y = 34
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.char.jump_cut()

    def draw(self):
        if self.score < 100:
            self.screen.fill(BLACK)
            self.draw_text("STAGE 1", 30, WHITE, WIDTH / 2, HEIGHT / 50)
        if self.score >= 100 and self.score < 500:
            self.screen.fill(LIGHTBLUE)
            self.draw_text("STAGE 2", 30, WHITE, WIDTH / 2, HEIGHT / 50)
        if self.score >= 500:
            self.screen.fill(LIGHTERBLUE)
            self.draw_text("STAGE 3", 30, WHITE, WIDTH / 2, HEIGHT / 50)
        self.all_sprites.draw(self.screen)

        # So the character is always in front
        self.screen.blit(self.char.image, self.char.rect)
        self.draw_text(str(self.score), 30, WHITE, WIDTH / 2, HEIGHT - 19/20 * HEIGHT)
        self.shield_bar(self.screen, 20, 20, self.char.shield)
        pg.display.flip()

    def start_screen(self):
        start = True
        while start:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    # Help screen
                    if event.key == pg.K_h:
                        self.help_screen()
                    else:
                        start = False
            self.screen.fill(LIGHTBLUE)
            self.draw_text(TITLE, 120, WHITE, WIDTH / 2 ,HEIGHT / 10)
            self.draw_text("Highscore: " + str(self.highscore), 40, WHITE, WIDTH / 2, HEIGHT / 4)
            #self.draw_text("Arrows to move, up arrow to jump (hold up arrow for big jump), down arrow to slam/drop.", 40, WHITE, WIDTH / 2, HEIGHT / 2.5)
            self.draw_text("Press h for help screen", 40, WHITE, WIDTH / 2, HEIGHT / 2.5)
            #self.draw_text("Space to shoot.", 40 , WHITE, WIDTH / 2, HEIGHT / 1.9)
            self.draw_text("Press ANY key to play.", 40, WHITE, WIDTH / 2, HEIGHT / 1.5)
            #self.draw_text("p to pause, g exits fullscreen, f enters fullscreen.", 40, WHITE, WIDTH / 2, HEIGHT / 1.2)
            self.draw_text("q to quit.", 40, WHITE, WIDTH / 2, HEIGHT / 1.1)
            pg.display.flip()
        #self.wait_for_key()

    def help_screen(self):
        # Works on my monitor (2560x1440 resolution)
        help_gui = pg.image.load(path.join(self.img_dir, "how_to_play_template.png"))
        pg.transform.scale(self.screen, (1920, 1080))
        self.screen.blit(help_gui, (0,0))
        pg.display.flip()
        self.wait_for_key()

    def game_over_screen(self):
        if not self.running:
            return
        over = True
        self.game_over.play()
        while over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    # Help screen
                    if event.key == pg.K_h:
                        self.help_screen()
                    else:
                        over = False

            self.screen.fill(RED)
            self.draw_text("Game Over", 120, WHITE, WIDTH / 2, HEIGHT - 900)
            self.draw_text("Press ANY key to play.", 40, WHITE, WIDTH / 2, HEIGHT / 1.5)
            self.draw_text("Press h for help screen", 40, WHITE, WIDTH / 2, HEIGHT / 1.3)
            self.draw_text("q to quit.", 40, WHITE, WIDTH / 2, HEIGHT / 1.1)
            if self.score >= self.highscore:
                self.draw_text("New high score!", 80, WHITE, WIDTH / 2, HEIGHT / 2)
                with open(path.join(self.dir, HS_File), "w") as file:
                    file.write(str(self.score))
                self.highscore = self.score
            else:
                self.draw_text("High score: " + str(self.highscore), 80, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Score: " + str(self.score), 80, WHITE, WIDTH / 2, HEIGHT / 3)
            pg.display.flip()
        #self.wait_for_key()

    def pause_screen(self):
        paused = True
        while paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    # Continue
                    if event.key == pg.K_c:
                        paused = False
                    # Help screen
                    if event.key == pg.K_h:
                        self.help_screen()
                    # Quit
                    if event.key == pg.K_q:
                        paused = False
                        self.playing = False
                        self.running = False
                    # Restart
                    if event.key == pg.K_r:
                        paused = False
                        self.playing = False
            self.screen.fill(WHITE)
            self.draw_text("Paused", 120, BLACK, WIDTH / 2, HEIGHT - 900)
            self.draw_text("C to continue, R to restart, H for help, Q to quit", 20, BLACK, WIDTH / 2, HEIGHT / 3)
            pg.display.update()

    def question_screen(self, question_num):
        # !Randomise question from text file and display appropriate answers
        # !correct_answer == 'K_c', if event.key == pg.correct_answer....
        # !questions file: question | answers | correct key
        # !for i in range difficulty draw potential answers

        self.question_num = question_num
        paused = True
        while paused:
            self.screen.fill(WHITE)
            if self.score < 100:
                self.draw_text(question_prompts_easy[self.question_num], 80, BLACK, WIDTH / 2, HEIGHT - 900)
                self.draw_text(answer_prompts_easy[self.question_num][0], 20, BLACK, WIDTH / 2, HEIGHT / 3)
                self.draw_text(answer_prompts_easy[self.question_num][1], 20, BLACK, WIDTH / 2, HEIGHT // 2.5)
            if self.score >= 100:
                self.draw_text(question_prompts_med[self.question_num], 80, BLACK, WIDTH / 2, HEIGHT - 900)
                self.draw_text(answer_prompts_med[self.question_num][0], 20, BLACK, WIDTH / 2, HEIGHT / 3)
                self.draw_text(answer_prompts_med[self.question_num][1], 20, BLACK, WIDTH / 2, HEIGHT // 2.5)
            self.draw_text("Press 'q' to quit question prompt", 20, BLACK, WIDTH / 2, HEIGHT // 1.5)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                        paused = False
                        self.playing = False
                        self.running = False
                if event.type == pg.KEYDOWN:
                    if self.score < 100:
                        if event.key == answers_easy[self.question_num]:
                            self.correct_answer.play()
                            self.score += 50
                            if self.char.shield <= 90:
                                self.char.shield += 10
                            else:
                                self.char.shield += 100 - self.char.shield
                            paused = False

                        if event.key != answers_easy[self.question_num]:
                            if event.key == pg.K_a or event.key == pg.K_b:
                                self.incorrect_answer.play()
                                paused = False
                            else:
                                paused = True
                        if event.key == pg.K_q:
                            paused = False

                    if self.score >= 100:
                        if event.key == answers_med[self.question_num]:
                            self.correct_answer.play()
                            self.score += 50
                            if self.char.shield <= 80:
                                self.char.shield += 20
                            else:
                                self.char.shield += 100 - self.char.shield
                            paused = False

                        if event.key != answers_med[self.question_num]:
                            if event.key == pg.K_a or event.key == pg.K_b:
                                self.incorrect_answer.play()
                                paused = False
                            else:
                                paused = True
                        if event.key == pg.K_q:
                            paused = False

            pg.display.update()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        waiting = False
                        self.running = False
                    if event.key == pg.K_h:
                        self.help_screen()
                    else:
                        waiting = False
            pg.display.flip()

    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name, size)
        # Anti-aliasing = True
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def shield_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 300
        BAR_HEIGHT = 30
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, GREEN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

game = Game()
game.start_screen()
while game.running:
    game.new()
    game.game_over_screen()
pg.quit()

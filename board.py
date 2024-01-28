import pygame
import random
import os
import sqlite3
import sys
import time

word = ''
correct = ''


class Rating:
    def __init__(self, gt):
        pygame.init()
        self.width = 800
        self.height = 400
        self.gt = gt
        # self.tim = True
        # if self.tim:
        #     current_time = time.time()
        #
        #     self.elapsed_time = current_time - board.start_time
        #     minutes, seconds = divmod(self.elapsed_time, 60)
        #     hours, minutes = divmod(minutes, 60)
        #
        #     self.time_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
        #     board.start_time = 0.0
        #     self.tim = False
        con = sqlite3.connect('my_game_database1')
        cur = con.cursor()
        cur.execute(
            f'''INSERT INTO rating(level, login, time)
            VALUES({game_start_screen2.level}, '{log.login_text}', {self.gt})''')
        con.commit()
        con.close()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rating")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.background_path = os.path.join("data", "background.png")
        self.background_image = pygame.image.load(self.background_path)
        con = sqlite3.connect('my_game_database1')
        cur = con.cursor()
        # result = cur.execute(
        #     f'''SELECT DISTINCT time, login FROM rating
        #     WHERE level = {} ORDER BY time ASC LIMIT 6''').fetchall()
        result = cur.execute(
            f'''SELECT MIN(time), login FROM rating WHERE level = {game_start_screen2.level}
            GROUP BY login ORDER BY time ASC LIMIT 6''').fetchall()
        print(result)
        con.commit()
        con.close()
        self.login_time_data = [('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', '')]
        for i in range(len(result)):
            self.login_time_data[i] = (result[i][-1], self.timeeee(result[i][0]))
        self.blue_button_rect = pygame.Rect(100, self.height - 100, 150, 50)
        self.green_button_rect = pygame.Rect(self.width - 250, self.height - 100, 150, 50)

    def run(self):
        while True:
            self.handle_events()
            self.draw()

    def timeeee(self, t):
        self.elapsed_time = t
        minutes, seconds = divmod(self.elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)

        self.time_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
        return self.time_str

    def handle_events(self):
        global correct
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.blue_button_rect.collidepoint(event.pos):
                    con = sqlite3.connect('my_game_database1')
                    cur = con.cursor()
                    result = cur.execute(
                        f'''SELECT word FROM {game_start_screen.lang} WHERE level = {game_start_screen2.level}''').fetchall()
                    result = [''.join(el) for el in result]
                    con.commit()
                    try:
                        correct = random.choice(result)
                    except IndexError:
                        u = UltraWin()
                        u.run()
                    con.close()
                    b = Board(800, 400)
                    b.run()
                elif self.green_button_rect.collidepoint(event.pos):
                    con = sqlite3.connect('my_game_database1')
                    cur = con.cursor()
                    game_start_screen2.level += 1
                    result = cur.execute(
                        f'''SELECT word FROM {game_start_screen.lang} WHERE level = {game_start_screen2.level}''').fetchall()
                    result = [''.join(el) for el in result]
                    con.commit()
                    try:
                        correct = random.choice(result)
                    except IndexError:
                        u = UltraWin()
                        u.run()
                    con.close()
                    b = Board(800, 400)
                    b.run()

    def draw(self):
        self.window.blit(self.background_image, (0, 0))

        text_surface = self.font.render(f"Ваш результат: {self.timeeee(self.gt)}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2, 20))
        self.window.blit(text_surface, text_rect)
        text_surface1 = self.font.render(f"Лучшие результаты:", True,
                                        (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 1.9, 70))
        self.window.blit(text_surface1, text_rect)

        for i, (login, result_time) in enumerate(self.login_time_data):
            login_surface = self.font.render(login, True, (255, 255, 255))
            time_surface = self.font.render(result_time, True, (255, 255, 255))

            login_rect = login_surface.get_rect(topleft=(300, 100 + i * 30))
            time_rect = time_surface.get_rect(topright=(self.width - 300, 100 + i * 30))

            self.window.blit(login_surface, login_rect)
            self.window.blit(time_surface, time_rect)

        pygame.draw.rect(self.window, (0, 0, 255), self.blue_button_rect)
        pygame.draw.rect(self.window, (0, 255, 0), self.green_button_rect)

        # Написание текста на кнопках
        font = pygame.font.Font(None, 24)
        blue_button_text = font.render('Играть снова', True, (255, 255, 255))
        green_button_text = font.render('Дальше', True, (255, 255, 255))
        self.window.blit(blue_button_text, (125, self.height - 85))
        self.window.blit(green_button_text, (self.width - 210, self.height - 85))
        pygame.display.update()
        self.clock.tick(60)


class Login:
    def __init__(self):
        # Инициализация Pygame
        # pygame.init()
        self.is_running = True
        # self.clock = pygame.time.Clock()

        # Размеры окна
        self.width, self.height = 800, 400

        # Создание окна
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Registration')

        # Загрузка фонового изображения
        image_path = os.path.join('data', 'background.png')
        self.background_image = pygame.image.load(image_path).convert()

        # Создание поля ввода
        self.text_input_rect = pygame.Rect((self.width - 300) // 2, (self.height - 40) // 2, 300, 40)
        self.is_text_input_active = False
        self.login_text = ''
        self.open_game = False
        self.login_text = ''

        # Создание кнопки
        self.button_rect = pygame.Rect(self.width - 150, self.height - 75, 100, 50)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.draw()
            # self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка нажатия на кнопку
                if self.button_rect.collidepoint(event.pos):
                    print('Нажата кнопка Войти')
                    # con = sqlite3.connect('my_game_database1')
                    # cur = con.cursor()
                    # cur.execute(f'''INSERT INTO rating(login) VALUES('{self.login_text}')''')
                    # con.commit()
                    # con.close()
                    self.open_game = True
                    self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('Логин: ', self.login_text)
                elif event.key == pygame.K_BACKSPACE:
                    self.login_text = self.login_text[:-1]
                else:
                    if len(self.login_text) < 16:
                        self.login_text += event.unicode

    def draw(self):
        # image_path = os.path.join('data', 'background.png')
        # self.background_image = pygame.image.load(image_path).convert()
        self.win.blit(self.background_image, (0, 0))
        # Отображение заголовка 'Вход в игру'
        pygame.font.init()
        font = pygame.font.Font(None, 48)
        title_text = font.render('Вход в игру', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, 50))
        self.win.blit(title_text, title_rect)
        # Обновление поля ввода
        if self.is_text_input_active:
            pygame.draw.rect(self.win, (0, 0, 255), self.text_input_rect, 2)
        else:
            pygame.draw.rect(self.win, (0, 0, 255), self.text_input_rect, 2)
        pygame.font.init()
        font = pygame.font.Font(None, 32)
        text = font.render(self.login_text, True, (255, 255, 255))
        self.win.blit(text, (self.text_input_rect.x + 5, self.text_input_rect.y + 5))

        pygame.draw.rect(self.win, (0, 255, 0), self.button_rect)
        button_text = font.render('Войти', True, (255, 255, 255))
        self.win.blit(button_text, (self.button_rect.x + 15, self.button_rect.y + 15))

        # Обновление экрана
        pygame.display.flip()


class UltraWin:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()

        # Размеры окна
        self.width, self.height = 800, 400

        # Создание окна
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Win')

        # Загрузка фонового изображения
        image_path = os.path.join('data', 'background.png')
        self.background_image = pygame.image.load(image_path).convert()

        # Шрифт и текст
        font = pygame.font.Font(None, 36)
        self.text = font.render('Вы победили!\nУрони кончились', True,
                                (255, 255, 255))
        self.green_button_rect = pygame.Rect(self.width - 250, self.height - 100, 150, 50)

    def run(self):
        global correct
        # Основной цикл игры
        while True:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.green_button_rect.collidepoint(event.pos):
                        print('Закрыть')
                        pygame.quit()
                        sys.exit()

            # Отрисовка фонового изображения
            self.win.blit(self.background_image, (0, 0))

            # Отрисовка текста по середине
            text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))
            self.win.blit(self.text, text_rect)
            pygame.draw.rect(self.win, (0, 255, 0), self.green_button_rect)

            # Написание текста на кнопках
            font = pygame.font.Font(None, 24)
            green_button_text = font.render('Закрыть', True, (255, 255, 255))
            self.win.blit(green_button_text, (self.width - 210, self.height - 85))

            # Обновление экрана
            pygame.display.flip()


class Lose:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()

        # Размеры окна
        self.width, self.height = 800, 400

        # Создание окна
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Lose')

        # Загрузка фонового изображения
        image_path = os.path.join('data', 'background.png')
        self.background_image = pygame.image.load(image_path).convert()

        # Шрифт и текст
        font = pygame.font.Font(None, 36)
        self.text = font.render('Вы проиграли!\nПерепройдите этот уровень', True,
                                (255, 255, 255))

        # Создание кнопок
        self.blue_button_rect = pygame.Rect(100, self.height - 100, 150, 50)
        self.green_button_rect = pygame.Rect(self.width - 250, self.height - 100, 150, 50)

    def run(self):
        global correct
        # Основной цикл игры
        while True:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.blue_button_rect.collidepoint(event.pos):
                        print('Нажата синяя кнопка - Играть снова')
                        try:
                            con = sqlite3.connect('my_game_database1')
                            cur = con.cursor()
                            result = cur.execute(
                                f'''SELECT word FROM {game_start_screen.lang} WHERE level = {game_start_screen2.level}''').fetchall()
                            result = [''.join(el) for el in result]
                            con.commit()
                            correct = random.choice(result)
                            con.close()
                            b = Board(800, 400)
                            b.run()
                        except IndexError:
                            u = UltraWin()
                            u.run()

            # Отрисовка фонового изображения
            self.win.blit(self.background_image, (0, 0))

            # Отрисовка текста по середине
            text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))
            self.win.blit(self.text, text_rect)

            # Отрисовка кнопок
            pygame.draw.rect(self.win, (0, 0, 255), self.blue_button_rect)

            # Написание текста на кнопках
            font = pygame.font.Font(None, 24)
            blue_button_text = font.render('Играть снова', True, (255, 255, 255))
            self.win.blit(blue_button_text, (125, self.height - 85))
            # Обновление экрана
            pygame.display.flip()


# class Win:
#     def __init__(self):
#         # Инициализация Pygame
#         pygame.init()
#
#         # Размеры окна
#         self.width, self.height = 800, 400
#
#         # Создание окна
#         self.win = pygame.display.set_mode((self.width, self.height))
#         pygame.display.set_caption('Win')
#
#         # Загрузка фонового изображения
#         image_path = os.path.join('data', 'background.png')
#         self.background_image = pygame.image.load(image_path).convert()
#
#         # Шрифт и текст
#         font = pygame.font.Font(None, 36)
#         current_time = time.time()
#
#         self.elapsed_time = current_time - board.start_time
#         minutes, seconds = divmod(self.elapsed_time, 60)
#         hours, minutes = divmod(minutes, 60)
#
#         time_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
#         self.text = font.render(
#             f'Вы победили!\nВы можете перейти на следующий уровень\nили перепройти этот. {time_str}', True,
#             (255, 255, 255))
#
#         # Создание кнопок
#         self.blue_button_rect = pygame.Rect(100, self.height - 100, 150, 50)
#         self.green_button_rect = pygame.Rect(self.width - 250, self.height - 100, 150, 50)
#
#     def run(self):
#         global correct
#         # Основной цикл игры
#         while True:
#             # Обработка событий
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     if self.blue_button_rect.collidepoint(event.pos):
#                         print('Нажата синяя кнопка - Играть снова')
#                         con = sqlite3.connect('my_game_database1')
#                         cur = con.cursor()
#                         result = cur.execute(
#                             f'''SELECT word FROM {game_start_screen.lang} WHERE level = {game_start_screen2.level}''').fetchall()
#                         result = [''.join(el) for el in result]
#                         con.commit()
#                         correct = random.choice(result)
#                         con.close()
#                         b = Board(800, 400)
#                         b.run()
#                     elif self.green_button_rect.collidepoint(event.pos):
#                         print('Нажата зелёная кнопка - Дальше')
#                         con = sqlite3.connect('my_game_database1')
#                         cur = con.cursor()
#                         game_start_screen2.level += 1
#                         result = cur.execute(
#                             f'''SELECT word FROM {game_start_screen.lang} WHERE level = {game_start_screen2.level}''').fetchall()
#                         result = [''.join(el) for el in result]
#                         con.commit()
#                         correct = random.choice(result)
#                         con.close()
#                         b = Board(800, 400)
#                         b.run()
#
#             # Отрисовка фонового изображения
#             self.win.blit(self.background_image, (0, 0))
#
#             # Отрисовка текста по середине
#             text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))
#             self.win.blit(self.text, text_rect)
#
#             # Отрисовка кнопок
#             pygame.draw.rect(self.win, (0, 0, 255), self.blue_button_rect)
#             pygame.draw.rect(self.win, (0, 255, 0), self.green_button_rect)
#
#             # Написание текста на кнопках
#             font = pygame.font.Font(None, 24)
#             blue_button_text = font.render('Играть снова', True, (255, 255, 255))
#             green_button_text = font.render('Дальше', True, (255, 255, 255))
#             self.win.blit(blue_button_text, (125, self.height - 85))
#             self.win.blit(green_button_text, (self.width - 210, self.height - 85))
#
#             # Обновление экрана
#             pygame.display.flip()


class StartScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.lang = None
        self.do_not_open = False

    def run(self):
        while self.is_running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.do_not_open = True
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.blue_button_rect.collidepoint(event.pos):
                    self.lang = 'ru'
                    self.is_running = False
                elif self.green_button_rect.collidepoint(event.pos):
                    self.lang = 'eng'
                    self.is_running = False

    def draw(self):
        self.screen.fill((255, 255, 255))  # Заливка фона белым цветом
        background_image = pygame.image.load(os.path.join('data', 'background.png'))
        self.screen.blit(background_image, (0, 0))  # Рисуем картинку на фоне

        self.blue_button_rect = pygame.draw.rect(self.screen, (0, 0, 255), (100, 200, 600, 100))
        pygame.font.init()
        font = pygame.font.Font(None, 30)
        text1 = font.render('Начать играть используя русский язык', True, (255, 255, 255))
        text_rect1 = text1.get_rect(center=self.blue_button_rect.center)
        self.screen.blit(text1, text_rect1)

        self.green_button_rect = pygame.draw.rect(self.screen, (0, 255, 0), (100, 350, 600, 100))
        text2 = font.render('Начать играть используя английский язык', True, (255, 255, 255))
        text_rect2 = text2.get_rect(center=self.green_button_rect.center)
        self.screen.blit(text2, text_rect2)

        pygame.display.flip()


class SecondStartScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.level = None
        self.do_not_open = False

    def run(self):
        while self.is_running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.do_not_open = True
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.blue_button_rect.collidepoint(event.pos):
                    self.level = 1
                    self.is_running = False
                elif self.green_button_rect.collidepoint(event.pos):
                    self.level = 2
                    self.is_running = False
                elif self.red_button_rect.collidepoint(event.pos):
                    self.level = 3
                    self.is_running = False

    def draw(self):
        self.screen.fill((255, 255, 255))  # Заливка фона белым цветом
        background_image = pygame.image.load(os.path.join('data', 'background.png'))
        self.screen.blit(background_image, (0, 0))  # Рисуем картинку на фоне

        self.blue_button_rect = pygame.draw.rect(self.screen, (0, 0, 255), (100, 100, 600, 100))
        pygame.font.init()
        font = pygame.font.Font(None, 30)
        text1 = font.render('Лёгкий', True, (255, 255, 255))
        text_rect1 = text1.get_rect(center=self.blue_button_rect.center)
        self.screen.blit(text1, text_rect1)

        self.green_button_rect = pygame.draw.rect(self.screen, (0, 255, 0), (100, 250, 600, 100))
        text2 = font.render('Средний', True, (255, 255, 255))
        text_rect2 = text2.get_rect(center=self.green_button_rect.center)
        self.screen.blit(text2, text_rect2)

        self.red_button_rect = pygame.draw.rect(self.screen, (255, 0, 0), (100, 400, 600, 100))
        text3 = font.render('Сложный', True, (255, 255, 255))
        text_rect3 = text3.get_rect(center=self.red_button_rect.center)
        self.screen.blit(text3, text_rect3)

        pygame.display.flip()


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Создаем поверхность для спрайта ракеты
        # self.image.fill((255, 0, 0))  # Заливаем спрайт ракеты красным цветом
        fullname = os.path.join('data', 'rocket.png')
        self.image = pygame.image.load(fullname)
        self.image = pygame.transform.scale(self.image, (100, 45))  # поменять размер ракеты
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.word = ''

    def update(self, keys):
        if keys[pygame.K_UP]:  # Если нажата клавиша вверх
            if self.rect.y - self.speed >= -7:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.y - self.speed <= 353:  # Если нажата клавиша вниз
                self.rect.y += self.speed

    def check_collision(self, letter):
        if pygame.sprite.collide_rect(self, letter):  # Если ракета сталкивается с буквой
            self.word += letter.letter  # Добавляем букву к переменной word


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fullname = os.path.join('data', 'pngegg.png')
        self.image = pygame.image.load(fullname)
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x -= 5


class Wormhole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fullname = os.path.join('data', 'wormhole.png')
        self.image = pygame.image.load(fullname)
        self.image = pygame.transform.scale(self.image, (100, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x -= 5


class Smallasteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, number):
        super().__init__()
        self.number = number
        path = number_asterois[self.number]
        fullname = os.path.join('data', path)
        self.image = pygame.image.load(fullname)
        self.image = pygame.transform.scale(self.image, (60, 65))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x -= 5


class Letter(pygame.sprite.Sprite):
    def __init__(self, x, y, letter):
        super().__init__()
        self.letter = letter
        self.letter_timer = 0
        path = alphabet_images[self.letter]
        fullname = os.path.join('data', path)
        self.image = pygame.image.load(fullname)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x -= 5


class FastLetter(pygame.sprite.Sprite):
    def __init__(self, x, y, letter):
        super().__init__()
        self.letter = letter
        self.letter_timer = 0
        path = alphabet_images[self.letter]
        fullname = os.path.join('data', path)
        self.image = pygame.image.load(fullname)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x -= 5


class Star:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.x -= self.speed


class Board:
    def __init__(self, width, height):
        self.game_time = None
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))  # Создание окна заданного размера
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Game')
        self.is_running = True
        self.stars = []
        self.count = 0
        self.create_stars()  # Создание звёзд
        self.rocket = Rocket(100, 200)
        self.letters = pygame.sprite.Group()
        self.fastletters = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.small_asteroids = pygame.sprite.Group()
        self.wormholes = pygame.sprite.Group()
        self.start_time = time.time()
        # self.create_letters()
        # Установка таймера для запуска букв
        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # Запуск каждые 2 секунды
        pygame.time.set_timer(pygame.USEREVENT + 2, 15000)
        pygame.time.set_timer(pygame.USEREVENT + 3, 10000)
        pygame.time.set_timer(pygame.USEREVENT + 4, 20000)
        pygame.time.set_timer(pygame.USEREVENT + 5, 1000)

    # def create_letters(self):
    #     # n = 1000
    #     for _ in range(100):
    #         x = random.randint(800, 1600)
    #         y = random.randint(0, self.height - 50)
    #         letter = chr(random.randint(65, 90))
    #         letter_sprite = Letter(x, y, letter)
    #         self.letters.add(letter_sprite)

    def create_stars(self):
        for _ in range(100):
            x = random.randint(0, self.width)  # Случайное положение звезды по x
            y = random.randint(0, self.height)  # Случайное положение звезды по y
            speed = random.uniform(0.75, 2)  # Случайная скорость звезды
            star = Star(x, y, speed)  # Создание экземпляра звезды
            self.stars.append(star)  # Добавление звезды в список звезд

    def run(self):
        while self.is_running:
            if correct.lower() in self.rocket.word.lower():
                print(self.game_time)
                win = Rating(self.game_time)
                win.run()
                self.is_running = False
            # elif correct.lower() in self.rocket.word.lower() and game_start_screen2.level == 3:
            #     u = UltraWin()
            #     print(self.game_time)
            #     u.run()
            #     self.is_running = False
            self.handle_events()  # Обработка событий
            self.update()  # Обновление позиций звезд
            self.draw()  # Отрисовка звезд
            self.clock.tick(60)  # Задержка на 60 кадров в секунду

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Проверка на событие закрытия окна
                self.is_running = False
            elif event.type == pygame.USEREVENT + 1:
                letter = random.choice(list(alphabet_images.keys()))
                x = random.randint(800, 1600)
                y = random.randint(50, self.height - 50)
                letter_sprite = Letter(x, y, letter)
                self.letters.add(letter_sprite)
            elif event.type == pygame.USEREVENT + 2:
                x = random.randint(800, 1600)
                y = random.randint(50, self.height - 50)
                asteroid_sprite = Asteroid(x, y)
                self.asteroids.add(asteroid_sprite)
            elif event.type == pygame.USEREVENT + 3:
                number = random.choice(list(number_asterois.keys()))
                x = random.randint(800, 1600)
                y = random.randint(50, self.height - 50)
                small_asteroid_sprite = Smallasteroid(x, y, number)
                self.small_asteroids.add(small_asteroid_sprite)
            elif event.type == pygame.USEREVENT + 4:
                x = random.randint(800, 1600)
                y = random.randint(50, self.height - 50)
                wormhole_sprite = Wormhole(x, y)
                self.wormholes.add(wormhole_sprite)
            elif event.type == pygame.USEREVENT + 5:
                letter = random.choice(list(correct.upper()))
                x = random.randint(800, 1600)
                y = random.randint(50, self.height - 50)
                letter_sprite = FastLetter(x, y, letter)
                self.fastletters.add(letter_sprite)

    def update(self):
        for star in self.stars:
            star.update()  # Обновление позиции звезды
            if star.x < -10:  # Если звезда вышла за пределы окна
                star.x = self.width + 10  # Перемещаем звезду за пределы окна справа
                star.y = random.randint(0, self.height)  # Устанавливаем случайное положение звезды по y
        keys = pygame.key.get_pressed()  # Получаем все нажатые клавиши
        self.rocket.update(keys)  # Обновляем положение ракеты

        for letter in self.letters:
            if pygame.sprite.collide_rect(self.rocket, letter):
                self.rocket.word += letter.letter
                letter.kill()
        self.letters.update()
        for fastletter in self.fastletters:
            if pygame.sprite.collide_rect(self.rocket, fastletter):
                self.rocket.word += fastletter.letter
                fastletter.kill()
        self.fastletters.update()
        for asteroid in self.asteroids:
            if pygame.sprite.collide_rect(self.rocket, asteroid):
                self.rocket.word = ''
                asteroid.kill()
        self.asteroids.update()
        for small_asteroid in self.small_asteroids:
            if pygame.sprite.collide_rect(self.rocket, small_asteroid):
                try:
                    self.rocket.word = self.rocket.word[:-int(small_asteroid.number)]
                except IndexError:
                    self.rocket.word = ''
                small_asteroid.kill()
        self.small_asteroids.update()
        for wormhole in self.wormholes:
            if pygame.sprite.collide_rect(self.rocket, wormhole):
                wormhole.kill()
                l = Lose()
                l.run()
        self.wormholes.update()

    # def update_sprites(self):
    #     self.rocket.update(pygame.key.get_pressed())
    #     self.letters.update()
    #     for star in self.stars:
    #         star.update()
    #
    #     current_time = pygame.time.get_ticks()
    #     if current_time - self.letter_timer > 2000:  # Если прошло 2 секунды
    #         letter = random.choice(list(alphabet_images.keys()))
    #         x = random.randint(800, 1600)
    #         y = random.randint(50, self.height - 50)
    #         letter_sprite = Letter(x, y, letter)
    #         self.letters.add(letter_sprite)
    #         self.letter_timer = current_time  # Обновляем таймер

    def draw(self):
        self.screen.fill((0, 0, 0))  # Заливка окна черным цветом
        # background_image = pygame.image.load(os.path.join('data', 'sky.png'))
        # self.screen.blit(background_image, (0, 0))
        for star in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (star.x, star.y), 2)  # Отрисовка звезды
        self.screen.blit(self.rocket.image, self.rocket.rect)  # Отображение спрайта ракеты

        for letter in self.letters:
            self.screen.blit(letter.image, letter.rect)  # Отображение спрайтов букв
        for fastletter in self.fastletters:
            self.screen.blit(fastletter.image, fastletter.rect)  # Отображение спрайтов букв
        for asteroid in self.asteroids:
            self.screen.blit(asteroid.image, asteroid.rect)
        for small_asteroid in self.small_asteroids:
            self.screen.blit(small_asteroid.image, small_asteroid.rect)
        for wormhole in self.wormholes:
            self.screen.blit(wormhole.image, wormhole.rect)
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        word_text = font.render(self.rocket.word, True, (225, 0, 0))
        word_rect = word_text.get_rect(center=(self.width // 2, self.height - self.height + 20))
        self.screen.blit(word_text, word_rect)

        correct_text = font.render(correct, True, (225, 0, 0))
        correct_rect = correct_text.get_rect(bottomleft=(10, self.height - 10))
        self.screen.blit(correct_text, correct_rect)
        current_time = time.time()  # текущее время
        self.game_time = current_time - self.start_time  # вычисляем прошедшее время

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    log = Login()
    log.run()
    if log.open_game is True:
        game_start_screen = StartScreen(800, 600)
        game_start_screen.run()
        if not game_start_screen.do_not_open:
            if game_start_screen.lang == 'ru':
                alphabet_images = {'А': 'а.png', 'Б': 'б.png', 'В': 'в.png', 'Г': 'г.png', 'Д': 'д.png', 'Е': 'е.png',
                                   'Ж': 'ж.png', 'З': 'з.png', 'И': 'и.png', 'Й': 'й.png', 'К': 'к.png', 'Л': 'л.png',
                                   'М': 'м.png', 'Н': 'н.png', 'О': 'о.png', 'П': 'п.png', 'Р': 'р.png',
                                   'С': 'с.png', 'Т': 'т.png', 'У': 'у.png', 'Ф': 'ф.png', 'Х': 'х.png',
                                   'Ц': 'ц.png', 'Ч': 'ч.png', 'Ш': 'ш.png', 'Щ': 'щ.png', 'Ъ': 'ъ.png',
                                   'Ы': 'ы.png', 'Ь': 'ь.png', 'Э': 'э.png', 'Ю': 'ю.png', 'Я': 'я.png',}
                # alphabet_images = {'А': 'а.png', 'Ё': 'ё.png'}
            else:
                alphabet_images = {'A': 'a.png', 'B': 'b.png', 'C': 'c.png', 'D': 'd.png', 'E': 'e.png', 'F': 'f.png',
                                   'G': 'g.png',
                                   'H': 'h.png', 'I': 'i.png', 'J': 'j.png', 'K': 'k.png',
                                   'L': 'l.png', 'M': 'm.png', 'N': 'n.png', 'O': 'o.png', 'P': 'p.png', 'Q': 'q.png',
                                   'R': 'r.png',
                                   'S': 's.png', 'T': 't.png', 'U': 'u.png', 'V': 'v.png', 'W': 'w.png',
                                   'X': 'x.png', 'Y': 'y.png', 'Z': 'z.png'}
            game_start_screen2 = SecondStartScreen(800, 600)
            game_start_screen2.run()
            if not game_start_screen2.do_not_open:
                con = sqlite3.connect('my_game_database1')
                cur = con.cursor()
                result = cur.execute(
                    f'''SELECT word FROM {game_start_screen.lang} WHERE level = {game_start_screen2.level}''').fetchall()
                result = [''.join(el) for el in result]
                con.commit()
                con.close()
                number_asterois = {'1': '1.png', '2': '2.png', '3': '3.png', '4': '4.png'}
                correct = random.choice(result)
                board = Board(800, 400)
                board.run()

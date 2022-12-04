import pygame
import time
import random


# Размер окна
window_x = 720
window_y = 480
# Размер кусочка поля
size = 20

# Цвета
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
light_blue = pygame.Color(0, 255, 255)
yellow = pygame.Color(255, 255, 0)
orange = pygame.Color(255, 140, 0)
purple = pygame.Color(255, 0, 255)

# подключаем pygame
pygame.init()

# Шрифты
little_font = pygame.font.SysFont("arial", 35)
default_font = pygame.font.SysFont("arial", 50)
big_font = pygame.font.SysFont("arial", 60)


# Класс Змея
class Snake:

    # иницилизация: если True, значит игроков 2 и добавляем другую змейку
    def __init__(self, color = green, is_second = False):
        self.score = 0
        if is_second:
            self.position = [600, 420]
            self.body = [[600, 420], [620, 420], [640, 420]]
            self.direction = "LEFT"
            self.change_to = "LEFT"
            self.color = blue
            self.control = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        else:
            self.position = [100, 60]
            self.body = [[100, 60], [80, 60], [60, 60]]
            self.direction = "RIGHT"
            self.change_to = "RIGHT"
            self.color = color
            self.control = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]

            
    # Обработка изменения направления
    def changing_direction(self, key):
        if key == self.control[0]:
            self.change_to = "UP"
        elif key == self.control[1]:
            self.change_to = "DOWN"
        elif key == self.control[2]:
            self.change_to = "LEFT"
        elif key == self.control[3]:
            self.change_to = "RIGHT"
        else:
            try:
                if key == self.control[4]:
                    self.change_to = "UP"
                elif key == self.control[5]:
                    self.change_to = "DOWN"
                elif key == self.control[6]:
                    self.change_to = "LEFT"
                elif key == self.control[7]:
                    self.change_to = "RIGHT"
            except:
                pass
        
        # Запрет на смену направления на противоположное
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
        return 1


    # Меняем позицию головы в соответствии с направлением
    def move(self):
        if self.direction == "UP":
            self.position[1] -= size
        elif self.direction == "DOWN":
            self.position[1] += size
        elif self.direction == "LEFT":
            self.position[0] -= size
        elif self.direction == "RIGHT":
            self.position[0] += size


def game_over(game_app, snake_num):
    game_window.fill(black)

    # Выводим различные варианты финальных экранов
    if len(game_app.snakes) == 2:
        # Тот, кто врезался - проигрывает
        if snake_num == 0:
            game_over_surface1 = big_font.render(
                "Blue snake WINS", True, blue
            )

        elif snake_num == 1:
            game_over_surface1 = big_font.render(
                "Green snake WINS", True, green
            )

        else:
            # При одновременном столкновении побеждает длинейший
            if game_app.snakes[0].score > game_app.snakes[1].score:
                game_over_surface1 = big_font.render(
                    "Green snake WINS", True, green
                )

            elif game_app.snakes[0].score < game_app.snakes[1].score:
                game_over_surface1 = big_font.render(
                    "Blue snake WINS", True, blue
                )
            # Если и длины равны - ничья
            else:
                game_over_surface1 = big_font.render(
                    "DRAW", True, white
                )

    # В соло режиме выводим счёт
    else:
        game_over_surface1 = default_font.render(
            "Your score: " + str(game_app.snakes[0].score), True, white
        )

    # Рисуем надписи и подсказку
    game_over_rect = game_over_surface1.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 3)
    game_window.blit(game_over_surface1, game_over_rect)

    game_over_surface0 = little_font.render(
        "Q - exit    R - restart", True, white
    )
    game_over_rect = game_over_surface0.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4 * 3)
    game_window.blit(game_over_surface0, game_over_rect)

    pygame.display.flip()

    # Обработка нажатий для выхода
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    return
        

class GameApp:
    # fps
    fps = pygame.time.Clock()
    # позиция яблока
    fruit_position = [100, 60]

    def __init__(self, two_gamers, difficulty, color):

        # Массив для змеи/змей
        self.snakes = []
        # Добавляем первую змею
        self.snakes.append(Snake())

        # В зависимости от числа игроков добавляем вторую
        # змею или управление к первой
        if two_gamers:
            self.snakes.append(Snake(is_second = True))
        else:
            self.snakes[0].color = color
            self.snakes[0].control.append(pygame.K_UP)
            self.snakes[0].control.append(pygame.K_DOWN)
            self.snakes[0].control.append(pygame.K_LEFT)
            self.snakes[0].control.append(pygame.K_RIGHT)

        # выставление параметров в зависимости от сложности
        if difficulty == 'easy':
            self.snake_speed = 10
            self.plus_speed = 0
            self.plus_score = 10     
        elif difficulty == 'medium':
            self.snake_speed = 10
            self.plus_speed = 1
            self.plus_score = 25
        elif difficulty == 'hard':
            self.snake_speed = 12
            self.plus_speed = 2
            self.plus_score = 50


    # меняем позицию и рисуем фрукт
    def respawn_fruit(self):

        game_window.fill(black)

        # Проверка на попаданеие в тела змеек
        if len(self.snakes) == 2:
            while self.fruit_position in self.snakes[0].body or self.fruit_position in self.snakes[1].body:
                self.fruit_position = [
                    random.randrange(1, (window_x // size)) * size,
                    random.randrange(1, (window_y // size)) * size,
                ]
        else:
            while self.fruit_position in self.snakes[0].body:
                self.fruit_position = [
                    random.randrange(1, (window_x // size)) * size,
                    random.randrange(1, (window_y // size)) * size,
                ]

        pygame.draw.rect(
            game_window, white, pygame.Rect(self.fruit_position[0] + 1, self.fruit_position[1] + 1, size - 2, size - 2)
        )


    def crush(self):
        check = 0
        # Обрабатываем столкновения
        for i in range(len(self.snakes)):
            # Со стенами
            if self.snakes[i].position[0] < 0 or self.snakes[i].position[0] > window_x - size or self.snakes[i].position[1] < 0 or self.snakes[i].position[1] > window_y - size:
                check += i + 1
                pass
            try:
                # Со своим телом и телом другой змейки
                if self.snakes[0].position in self.snakes[i].body:
                    check += 1
                if self.snakes[1].position in self.snakes[i].body:
                    check += 2
                # Головами
                if self.snakes[0].position[0] == self.snakes[1].position[0] and self.snakes[0].position[1] == self.snakes[1].position[1]:
                    check = 3
                    break
            except:
                pass
        # Если столкнулись - запускаем game_over
        if check > 0:
            game_over(self, check - 1)
            return True
        return False


    def eating(self):
        for snake in self.snakes:
            # Добавляем элемент в тело спереди
            snake.body.insert(0, list(snake.position))
            # Если фрукт съеден увеличиваем скорость, прибавляем счёт и
            # респавним фрукт
            if snake.position[0] == self.fruit_position[0] and snake.position[1] == self.fruit_position[1]:
                self.snake_speed += self.plus_speed
                snake.score += self.plus_score
                self.respawn_fruit()
            else:
                # Удаляем хвост, если не съеден
                snake.body.pop()


    def draw_snakes(self):
        # Отрисовка змей
        for snake in self.snakes:
            for pos in snake.body:
                pygame.draw.rect(
                    game_window, snake.color, pygame.Rect(pos[0] + 1, pos[1] + 1, size - 2, size - 2)
                )
        
        pygame.display.flip()

   
# Функция отрисовывающая меню выбора
def draw_page(args):
    game_window.fill(black)
    # Количество строк
    n = len(args)
    # Заголовок
    text = big_font.render(args[0][0], True, args[0][1])
    rect = text.get_rect()
    rect.topleft = (window_x / 16, 50)
    game_window.blit(text, rect)

    # Вырианты выбора
    for i in range(1, n):
        text = default_font.render(args[i][0], True, args[i][1])

        rect = text.get_rect()
        rect.topleft = (window_x / 10, 80 + i * 60)
        game_window.blit(text, rect)

    pygame.display.flip()


def players_choose():

    draw_page([['Выберите режим игры:', green], ['1. One player', blue], ['2. Two players', blue]])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_1:
                    game_window.fill(black)
                    return False
                elif event.key == pygame.K_2:
                    game_window.fill(black)
                    return True


def difficulty_choose():
    game_window.fill(black)

    draw_page([['Выберите сложность:', blue], ['1. Easy', yellow], ['2. Medium', orange], ['3. Hard', red]])
    
    # Обработка выбора сложности
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_1:
                    game_window.fill(black)
                    return 'easy'
                elif event.key == pygame.K_2:
                    game_window.fill(black)
                    return 'medium'
                elif event.key == pygame.K_3:
                    game_window.fill(black)
                    return 'hard'


# Если игрок 1 - выбираем цвет
def color_choose():
    game_window.fill(black)

    draw_page([['Выберите цвет:', light_blue], ['1. Green', green], ['2. Blue', blue], ['3. Yellow', yellow], ['4. Orange', orange], ['5. Purple', purple]])
    
    # Обработка выбора сложности
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_1:
                    game_window.fill(black)
                    return green
                elif event.key == pygame.K_2:
                    game_window.fill(black)
                    return blue
                elif event.key == pygame.K_3:
                    game_window.fill(black)
                    return yellow
                elif event.key == pygame.K_4:
                    game_window.fill(black)
                    return orange
                elif event.key == pygame.K_5:
                    game_window.fill(black)
                    return purple


# Основная программа

# Иницилизируем дисплей
pygame.display.set_caption("Snake 2")
game_window = pygame.display.set_mode((window_x, window_y))

# Создаём класс GameApp
game = GameApp(False, 'easy', green)

while True:

    # Для перезапуска игры
    del game

    # Выбор режимов игры
    # Кол-во игроков
    two_players = players_choose()
    # Цвет змейки (только для соло)
    sn_color = green
    if not two_players:
        sn_color = color_choose()
    # Сложность
    difficulty = difficulty_choose()
    game = GameApp(two_players, difficulty, sn_color)

    while True:
        
        # Считываем нажатия
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                # Запоминаем действий
                action = False
                for snake in game.snakes:
                    # Для каждой из змей проверяем изменение направления
                    action += snake.changing_direction(event.key)

                # Если действие совершено - выходим из цикла
                # (иначе змейка могла на месте развернуться)
                if action:
                    break
        
        # Двигаем змей
        for snake in game.snakes:
            snake.move()

        # Проверяем на столкновение
        if game.crush():
            break

        # Респавним фрукт
        game.respawn_fruit()

        # Движение/поедание фрукта
        game.eating()

        # Отрисовываем позиции змей/змеи
        game.draw_snakes()


        game.fps.tick(game.snake_speed)
        

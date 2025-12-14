import pygame
import random
import sqlite3


pygame.init()

WIDTH, HEIGHT = 640, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Жизнь студента")

conn = sqlite3.connect("mydb.db")
cur = conn.cursor()

font = pygame.font.Font(None, 32)

bg = pygame.image.load("data/univer.jpg")
icon = pygame.image.load("data/student_icon.png")
main_hall = pygame.image.load("data/main_hall.jpg")
misis_street_view = pygame.image.load("data/misis_street_view.jpg")
library_front = pygame.image.load("data/library_front.jpg")
wardrobe = pygame.image.load("data/wardrobe.jpg")
dormitory = pygame.image.load("data/dormitory_test.jpg")
laba = pygame.image.load("data/laba_test.jpg")
lection = pygame.image.load("data/lection.jpg")
lection2 = pygame.image.load("data/lection2.jpg")
pygame.display.set_icon(icon)

#индикаторы здоровья
heart1 = pygame.image.load("data/characteristics/heart1.png")
heart2 = pygame.image.load("data/characteristics/heart2.png")
heart3 = pygame.image.load("data/characteristics/heart3.png")
hp = 3
total_hp = heart3

clock = pygame.time.Clock()
fps = 60

# состояния экранов
STATE_MENU = "menu"
STATE_ENTER_NAME = "enter_name"
STATE_LEADERS = "leaders"
STATE_ABOUT = "about"
STATE_GAME = "next"      # экран после ввода имени
STATE_STREET = "street"
STATE_MAIN_HALL = "main_hall"
STATE_WARDROBE = 'wardrobe'
state_library = 'library'
state_library_learn = 'library_learn'
state_library_phone = 'library_phone'
state_dormitory = 'dormitory' #общага
state_dormitory_morning_waking = 'dormitory_morning_waking'
state_dormitory_morning_breakfast = 'dormitory_morning_breakfast'
state_dormitory_morning_prospal = 'dormitory_morning_prospal'
state_dormitory_morning_breakfast_good = 'dormitory_morning_breakfast_good'
state_dormitory_morning_breakfast_bad = 'dormitory_morning_breakfast_bad'
state_first_class = 'first_class'
state_first_class_1 = 'first_class_1'
state_first_class_good = 'first_class_good'
state_first_class_bad = 'first_class_bad'
state_second_class = 'second_class'
state_second_class_end = 'second_class_end'
state_evening = 'evening'
state_night = 'night'
state_start = 'start'



time = ['morning', 'first class', 'second class', 'evening', 'night']
current_day = 1
current_time = 'morning'


current_state = STATE_MENU
current_player_name = ""

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surf):
        pygame.draw.rect(surf, (50, 50, 50), self.rect)
        pygame.draw.rect(surf, (200, 200, 200), self.rect, 2)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# кнопки главного меню
btn_new = Button("Новая игра", 220, 120, 200, 40)
btn_continue = Button("Продолжить", 220, 170, 200, 40)
btn_about = Button("О нас", 220, 220, 200, 40)
btn_leaders = Button("Таблица лидеров", 220, 270, 200, 40)
btn_start_game = Button("Начать игру", 170, 200, 200, 40)

#кнокпка для начала игры после вступления
btn_dalshe = Button("Дальше", 430, 310, 200, 40)

# кнопка, которая всегда ведёт в главное меню
btn_main_menu = Button("Главное меню", 10, 10, 170, 40)

btn_next = Button("->", 620, 340, 20, 20)

# поле ввода имени
input_rect = pygame.Rect(170, 150, 300, 40)
active_input = False
name_text = ""

#кнопки для перехода по локациям
btn_library_front = Button("Идти в сторону библиотеки", 170, 120, 300, 40)
btn_main_hall = Button("Идти в главный зал", 170, 170, 300, 40)
btn_misis_street_view = Button("Выйти на улицу", 170, 170, 300, 40)
btn_wardrobe = Button("Пойти в гардероб", 170, 220, 300, 40)


#кнопки для тестовой версии индикатора здоровья
btn_hp_minus = Button("Уменьшить здоровье", 380, 310, 250, 40)
btn_hp_plus = Button("Увеличить здоровье", 380, 260, 250, 40)

#waking up
btn_sleep = Button("Полежать ещё 10 минут", 20, 190, 300, 40)
btn_wakeup = Button("Встать, чтобы все успеть", 20, 140, 300, 40)

#breakfast
btn_healthy_food = Button("Приготовить что-нибудь", 320, 140, 300, 40)
btn_fast_food = Button("Съесть доширак", 320, 190, 300, 40)
btn_not_eat = Button("Не есть", 320, 240, 300, 40)

#лаба
btn_uchil = Button("Ответить на вопрос", 170, 140, 300, 40)
btn_improvise = Button("Импровизировать", 170, 190, 300, 40)
btn_cheat = Button("Попробовать списать", 170, 240, 300, 40)

#лекция
btn_skip_lecture = Button("Прогулять в библиотеке", 170, 140, 300, 40)
btn_go_lecture = Button("Пойти на лекцию", 170, 190, 300, 40)

#В библиотеке
btn_library_learn = Button("Учиться", 170, 190, 300, 40)
btn_library_phone = Button("Сидеть в телефоне", 170, 240, 300, 40)

#Параметры
learning = 0
sleep_time = 1
chance = random.randint(1,100)
skip_classes = 0
rezults = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # нажатия мышью
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == STATE_MENU:
                if btn_new.is_clicked(event.pos):
                    current_state = STATE_ENTER_NAME
                elif btn_leaders.is_clicked(event.pos):
                    current_state = STATE_LEADERS
                    # здесь потом будешь подгружать таблицу лидеров из БД
                elif btn_continue.is_clicked(event.pos):
                    # здесь загрузка сохранения из БД/файла
                    pass
                elif btn_about.is_clicked(event.pos):
                    current_state = STATE_ABOUT
            else:
                # "Главное меню" работает на всех экранах кроме STATE_MENU
                if btn_main_menu.is_clicked(event.pos):
                    current_state = STATE_MENU

            # активация поля ввода имени
            if current_state == STATE_ENTER_NAME:
                active_input = input_rect.collidepoint(event.pos)
                current_player_name = name_text
                if btn_start_game.is_clicked(event.pos) and current_player_name != "":
                    cur.execute(f"INSERT INTO baza (Name, curr_state) VALUES ({current_player_name, current_state})")
                    conn.commit()
                    print("Игрок:", current_player_name)
                    current_state = STATE_GAME

            elif current_state == STATE_GAME:
                if btn_dalshe.is_clicked(event.pos):
                    current_state = state_start

            if current_state == state_start:
                if current_day < 10:
                    current_state = state_dormitory


            if btn_next.is_clicked(event.pos):
                if current_state == state_dormitory:
                    current_state = state_dormitory_morning_waking
                elif current_state == state_dormitory_morning_prospal:
                    skip_classes += 1
                    current_state = state_second_class
                elif current_state == state_dormitory_morning_breakfast_good:
                    current_state = state_first_class
                elif current_state == state_dormitory_morning_breakfast_bad:
                    current_state = state_first_class
                elif current_state == state_first_class:
                    current_state = state_first_class_1
                elif current_state == state_first_class_good or current_state == state_first_class_bad:
                    current_state = state_second_class
                elif current_state == state_dormitory_morning_breakfast_bad or current_state == state_dormitory_morning_breakfast_good:
                    current_state = state_first_class
                elif current_state == state_library_learn or current_state == state_second_class_end:
                    current_state = state_evening


            # События с утра
            if current_state == state_dormitory_morning_waking:
                if btn_sleep.is_clicked(event.pos):
                    chance = random.randint(1,100)
                    if chance >= 51:
                        current_state = state_dormitory_morning_breakfast
                    else:
                        current_state = state_dormitory_morning_prospal
                        skip_classes += 1
                elif btn_wakeup.is_clicked(event.pos):
                    current_state = state_dormitory_morning_breakfast

            if current_state == state_dormitory_morning_breakfast:
                if btn_healthy_food.is_clicked(event.pos):
                    current_state = state_dormitory_morning_breakfast_good
                elif btn_fast_food.is_clicked(event.pos):
                    chance = random.randint(1,100)
                    if chance >= 65:
                        current_state = state_dormitory_morning_breakfast_good
                    else:
                        current_state = state_dormitory_morning_breakfast_bad
                elif btn_not_eat.is_clicked(event.pos):
                    chance = random.randint(1,100)
                    if chance >= 50:
                        current_state = state_dormitory_morning_breakfast_good
                    else:
                        current_state = state_dormitory_morning_breakfast_bad


            #События на первой паре
            if current_state == state_first_class_1:
                if btn_cheat.is_clicked(event.pos):
                    chance = random.randint(1,100)
                    if chance > 50:
                        current_state = state_first_class_good
                    else:
                        current_state = state_first_class_bad
                elif btn_improvise.is_clicked(event.pos):
                    chance = random.randint(1,100)
                    if chance > 60:
                        current_state = state_first_class_good
                    else:
                        current_state = state_first_class_bad
                elif btn_uchil.is_clicked(event.pos):
                    current_state = state_first_class_good

            #события на второй паре
            if current_state == state_second_class:
                if btn_skip_lecture.is_clicked(event.pos):
                    current_state = state_library
                elif btn_go_lecture.is_clicked(event.pos):
                    current_state = state_second_class_end

            if current_state == state_library:
                if btn_library_learn.is_clicked(event.pos):
                    learning += 1
                    current_state = state_library_learn
                elif btn_library_phone.is_clicked(event.pos):
                    current_state = state_library_phone


        # ввод текста имени
        if current_state == STATE_ENTER_NAME and event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_RETURN:
                    current_player_name = name_text
                    # здесь ты можешь создать запись в БД для игрока
                    # create_player_if_not_exists(current_player_name)
                    print("Игрок:", current_player_name)
                    current_state = STATE_GAME
                elif event.key == pygame.K_BACKSPACE:
                    name_text = name_text[:-1]
                else:
                    if len(name_text) < 16:
                        name_text += event.unicode

    # рисуем фон
    screen.blit(bg, (0, 0))

    # главный экран
    if current_state == STATE_MENU:
        btn_new.draw(screen)
        btn_continue.draw(screen)
        btn_about.draw(screen)
        btn_leaders.draw(screen)

    # экран ввода имени
    elif current_state == STATE_ENTER_NAME:
        btn_main_menu.draw(screen)
        label = font.render("Введите имя:", True, (255, 255, 255))
        screen.blit(label, (170, 120))

        color = (0, 200, 0) if active_input else (100, 100, 100)
        pygame.draw.rect(screen, color, input_rect, 2)

        text_surf = font.render(name_text, True, (255, 255, 255))
        screen.blit(text_surf, (input_rect.x + 5, input_rect.y + 5))

        btn_start_game.draw(screen)

    # заглушка для таблицы лидеров
    elif current_state == STATE_LEADERS:
        btn_main_menu.draw(screen)
        title = font.render("Таблица лидеров", True, (255, 255, 0))
        screen.blit(title, (200, 60))
        # тут позже выведешь список из БД

    # заглушка для "О нас"
    elif current_state == STATE_ABOUT:
        btn_main_menu.draw(screen)
        text = font.render("Экран 'О нас'", True, (255, 255, 0))
        screen.blit(text, (230, 60))
        # тут позже сделаешь описание проекта

    # экран после ввода имени(вступление)
    elif current_state == STATE_GAME:
        screen.blit(misis_street_view, (0, 0))
        btn_main_menu.draw(screen)
        title = font.render("Привет, " + current_player_name + ", начинаем игру!", True, (255, 255, 0))
        screen.blit(title, (40, 80))
        btn_dalshe.draw(screen)

    #Все для утра
    elif current_state == state_dormitory:
        screen.blit(dormitory, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Комната в общаге. За окном серое утро.", True, (255, 255, 0))
        text2 = font.render("Будильник орёт уже вторую минуту.", True, (255,255,0))
        screen.blit(text1, (40, 80))
        screen.blit(text2, (40, 100))

        btn_next.draw(screen)

    elif current_state == state_dormitory_morning_waking:
        screen.blit(dormitory, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Пора вставать на пары! Что же я выберу?", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        btn_sleep.draw(screen)
        btn_wakeup.draw(screen)

    elif current_state == state_dormitory_morning_prospal:
        screen.blit(dormitory, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Я проспал! Похоже получаю пропуск за первую пару.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        btn_next.draw(screen)

    elif current_state == state_dormitory_morning_breakfast:
        screen.blit(dormitory, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Я встал вовремя. Можно позавтракать.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))
        text2 = font.render("Что я буду есть?", True, (255, 255, 0))
        screen.blit(text2, (40, 100))

        btn_healthy_food.draw(screen)
        btn_fast_food.draw(screen)
        btn_not_eat.draw(screen)

    elif current_state == state_dormitory_morning_breakfast_good:
        screen.blit(dormitory, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Я хорошо поел.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))
        text2 = font.render("Пора идти на пары.", True, (255, 255, 0))
        screen.blit(text2, (40, 100))

        btn_next.draw(screen)

    elif current_state == state_dormitory_morning_breakfast_bad:
        screen.blit(dormitory, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Стоило поесть полезной еды.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        #Вот здесь реализовать уменьшение здоровья

        btn_next.draw(screen)

    #Все для первой пары
    elif current_state == state_first_class:
        screen.blit(laba, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Первой парой лабораторная работа по вычмашу.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        btn_next.draw(screen)

    elif current_state == state_first_class_1:
        screen.blit(laba, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Преподаватель:", True, (255, 255, 0))
        screen.blit(text1, (40, 80))
        text2 = font.render("Отвечай на вопросы.", True, (255, 255, 0))
        screen.blit(text2, (40, 100))

        if learning >= 1:
            btn_uchil.draw(screen)
        else:
            btn_cheat.draw(screen)
            btn_improvise.draw(screen)

    elif current_state == state_first_class_good:
        screen.blit(laba, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Фух! Сдал!", True, (255, 255, 0))
        screen.blit(text1, (40, 80))
        text2 = font.render("Что там дальше?", True, (255, 255, 0))
        screen.blit(text2, (40, 100))

        #нужно будет поменять значение переменной rezults


        btn_next.draw(screen)

    elif current_state == state_first_class_bad:
        screen.blit(laba, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Эх, не повезло!", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        #нужно будет поменять значение переменной rezults

        btn_next.draw(screen)

    elif current_state == state_second_class:
        screen.blit(lection, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Сейчас у меня лекция по математике.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))
        text2 = font.render("Что же выбрать?", True, (255, 255, 0))
        screen.blit(text2, (40, 100))

        btn_go_lecture.draw(screen)
        btn_skip_lecture.draw(screen)

    elif current_state == state_second_class_end:
        screen.blit(lection, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Вот и закончилась пара.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        btn_next.draw(screen)

    elif current_state == state_library:
        screen.blit(library_front, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Что я буду делать в библиотеке.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        btn_library_learn.draw(screen)
        btn_library_phone.draw(screen)

    elif current_state == state_library_learn:
        screen.blit(library_front, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Я отлично поработал.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        btn_next.draw(screen)

    elif current_state == state_library_phone:
        screen.blit(library_front, (0, 0))
        screen.blit(total_hp, (190, 10))
        btn_main_menu.draw(screen)

        text1 = font.render("Возможно стоило учиться.", True, (255, 255, 0))
        screen.blit(text1, (40, 80))

        btn_next.draw(screen)



    pygame.display.update()
    clock.tick(fps)


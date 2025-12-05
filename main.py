import pygame


pygame.init()

WIDTH, HEIGHT = 640, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Жизнь студента")

font = pygame.font.Font(None, 32)

bg = pygame.image.load("data/univer.jpg")
icon = pygame.image.load("data/student_icon.png")
main_hall = pygame.image.load("data/main_hall.jpg")
misis_street_view = pygame.image.load("data/misis_street_view.jpg")
library_front = pygame.image.load("data/library_front.jpg")
wardrobe = pygame.image.load("data/wardrobe.jpg")
pygame.display.set_icon(icon)

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
STATE_LIBRARY_FRONT = 'library_front'
STATE_WARDROBE = 'wardrobe'

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

# поле ввода имени
input_rect = pygame.Rect(170, 150, 300, 40)
active_input = False
name_text = ""

#кнопки для перехода по локациям
btn_library_front = Button("Идти в сторону библиотеки", 170, 120, 300, 40)
btn_main_hall = Button("Идти в главный зал", 170, 170, 300, 40)
btn_misis_street_view = Button("Выйти на улицу", 170, 170, 300, 40)
btn_wardrobe = Button("Пойти в гардероб", 170, 220, 300, 40)

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
                    print("Игрок:", current_player_name)
                    current_state = STATE_GAME

            elif current_state == STATE_GAME:
                if btn_dalshe.is_clicked(event.pos):
                    current_state = STATE_STREET

            elif current_state == STATE_STREET:
                if btn_main_hall.is_clicked(event.pos):
                    current_state = STATE_MAIN_HALL

            elif current_state == STATE_MAIN_HALL:
                if btn_wardrobe.is_clicked(event.pos):
                    current_state = STATE_WARDROBE
                if btn_misis_street_view.is_clicked(event.pos):
                    current_state = STATE_STREET
                if btn_library_front.is_clicked(event.pos):
                    current_state = STATE_LIBRARY_FRONT

            elif current_state == STATE_WARDROBE:
                if btn_main_hall.is_clicked(event.pos):
                    current_state = STATE_MAIN_HALL

            elif current_state == STATE_LIBRARY_FRONT:
                if btn_main_hall.is_clicked(event.pos):
                    current_state = STATE_MAIN_HALL

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

    #Игра началась
    elif current_state == STATE_STREET:
        screen.blit(misis_street_view, (0, 0))
        btn_main_menu.draw(screen)
        btn_main_hall.draw(screen)
        title = font.render("Куда ты хочешь пойти?", True, (255, 255, 0))
        screen.blit(title, (40, 80))

    elif current_state == STATE_MAIN_HALL:
        screen.blit(main_hall, (0, 0))
        btn_main_menu.draw(screen)
        btn_library_front.draw(screen)
        btn_wardrobe.draw(screen)
        btn_misis_street_view.draw(screen)
        title = font.render("Куда ты хочешь пойти?", True, (255, 255, 0))
        screen.blit(title, (40, 80))

    elif current_state == STATE_WARDROBE:
        screen.blit(wardrobe, (0, 0))
        btn_main_menu.draw(screen)
        btn_main_hall.draw(screen)
        title = font.render("Куда ты хочешь пойти?", True, (255, 255, 0))
        screen.blit(title, (40, 80))

    elif current_state == STATE_LIBRARY_FRONT:
        screen.blit(library_front, (0, 0))
        btn_main_menu.draw(screen)
        btn_main_hall.draw(screen)
        title = font.render("Куда ты хочешь пойти?", True, (255, 255, 0))
        screen.blit(title, (40, 80))

    pygame.display.update()
    # clock.tick(fps)



import pygame
import sys
import math
import random

pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Замок с секретами")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
DARK_GRAY = (50, 50, 50)

CENTER = (W // 2, H // 2)
INNER_RADIUS = 100
OUTER_RADIUS = 200

ball_radius = 10
ball_ugol = 0
ball_speed = 0.1

sectors = []
min_sector_ugol = math.radians(30)
max_sector_ugol = math.radians(80)
min_gap = math.radians(15)

game_won = False
game_lost = False
message = ""
message_timer = 0

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)

def generate_sectors():
    """Генерация случайных непересекающихся секторов"""
    global sectors
    sectors.clear()
    num_sectors = random.randint(1, 3)
    full_circle = 2 * math.pi
    for _ in range(num_sectors):
        for _ in range(100):
            sector_ugol = random.uniform(min_sector_ugol, max_sector_ugol)
            start_ugol = random.uniform(0, full_circle - sector_ugol)
            end_ugol = start_ugol + sector_ugol
            
            valid = True
            for s_start, s_end in sectors:
                if (end_ugol > s_start and start_ugol < s_end):
                    valid = False
                    break
                
                gap1 = abs(start_ugol - s_end) % full_circle
                gap2 = abs(end_ugol - s_start) % full_circle
                if gap1 < min_gap or gap2 < min_gap:
                    valid = False
                    break
            
            if valid:
                sectors.append((start_ugol, end_ugol))
                break
    
    if not sectors:
        start_ugol = random.uniform(0, full_circle - min_sector_ugol)
        end_ugol = start_ugol + min_sector_ugol
        sectors.append((start_ugol, end_ugol))

def draw_circles():
    """Рисует концентрические круги"""
    pygame.draw.circle(screen, WHITE, CENTER, OUTER_RADIUS)
    pygame.draw.circle(screen, BLACK, CENTER, INNER_RADIUS)
    
    pygame.draw.circle(screen, DARK_GRAY, CENTER, INNER_RADIUS, 3)
    pygame.draw.circle(screen, DARK_GRAY, CENTER, OUTER_RADIUS, 3)

def draw_sectors():
    """Рисует зеленые сектора"""
    for start_ugol, end_ugol in sectors:
        points = []
        num_segments = 50
        
        for i in range(num_segments + 1):
            ugol = start_ugol + (end_ugol - start_ugol) * i / num_segments
            x = CENTER[0] + OUTER_RADIUS * math.cos(ugol)
            y = CENTER[1] + OUTER_RADIUS * math.sin(ugol)
            points.append((x, y))
        
        for i in range(num_segments, -1, -1):
            ugol = start_ugol + (end_ugol - start_ugol) * i / num_segments
            x = CENTER[0] + INNER_RADIUS * math.cos(ugol)
            y = CENTER[1] + INNER_RADIUS * math.sin(ugol)
            points.append((x, y))
        
        if len(points) > 2:
            pygame.draw.polygon(screen, GREEN, points)
        
        pygame.draw.arc(screen, (0, 200, 0), 
                       (CENTER[0] - OUTER_RADIUS, CENTER[1] - OUTER_RADIUS, 
                        OUTER_RADIUS * 2, OUTER_RADIUS * 2),
                       start_ugol, end_ugol, 3)

def draw_ball():
    """Рисует красный шарик"""
    ball_distance = (INNER_RADIUS + OUTER_RADIUS) // 2
    ball_x = CENTER[0] + ball_distance * math.cos(ball_ugol)
    ball_y = CENTER[1] + ball_distance * math.sin(ball_ugol)
    
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.circle(screen, BLACK, (int(ball_x), int(ball_y)), ball_radius, 2)

def is_ball_in_sector():
    """Проверяет, находится ли шарик внутри зеленого сектора"""
    normalized_ugol = ball_ugol % (2 * math.pi)
    
    for start_ugol, end_ugol in sectors:
        if start_ugol <= end_ugol:
            if start_ugol <= normalized_ugol <= end_ugol:
                return True
        else:
            if normalized_ugol >= start_ugol or normalized_ugol <= end_ugol:
                return True
    
    return False

def draw_ui():
    """Рисует интерфейс"""
    pass
    

    

    
    status_color = GREEN if is_ball_in_sector() else RED
    status_text = "В СЕКТОРЕ" if is_ball_in_sector() else "НЕ В СЕКТОРЕ"
    status = small_font.render(status_text, True, status_color)
    screen.blit(status, (W - 150, 50))
    
    if message and message_timer > 0:
        color = GREEN if "УСПЕХ" in message else RED
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(W // 2, H - 50))
        screen.blit(text, text_rect)

def show_message(msg, duration=60):
    """Показывает сообщение"""
    global message, message_timer
    message = msg
    message_timer = duration

generate_sectors()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            elif event.key == pygame.K_r:
                generate_sectors()
                ball_ugol = 0
                game_won = False
                game_lost = False
                message = ""
            
            elif event.key == pygame.K_SPACE and not game_won and not game_lost:
                if is_ball_in_sector():
                    game_won = True
                    show_message("УСПЕХ! Замок открыт!", 120)
                else:
                    game_lost = True
                    show_message("ПРОВАЛ! Попробуй еще раз (R)", 90)
    
    if not game_won and not game_lost:
        ball_ugol += ball_speed
        ball_ugol %= 2 * math.pi
    
    if message_timer > 0:
        message_timer -= 1
        if message_timer == 0:
            message = ""
    
    screen.fill((255, 255, 255))  # Светло-серый фон
    
    draw_circles()
    draw_sectors()
    draw_ball()
    draw_ui()
    
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
sys.exit()
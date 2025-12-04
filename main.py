import pygame

wight = 640
height = 360
fps = 60
title = "Жизнь студента"

pygame.init()
screen1 = pygame.display.set_mode((wight, height))
pygame.display.set_caption(title)
icon = pygame.image.load("data/student_icon.png")
bg = pygame.image.load("data/univer.jpg")
pygame.display.set_icon(icon)
running = True
while running:
    screen1.blit(bg, (0, 0))
    pygame.draw.rect(screen1, "White", (300, 200, 60, 60))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
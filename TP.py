import pygame
import random
import time
from OnLib import *


def InsideTriangle(x, y, points):
    denominator = (points[1][1] - points[2][1])*(points[0][0] - points[2]
                                                 [0]) + (points[2][0] - points[1][0])*(points[0][1] - points[2][1])
    u = ((points[1][1] - points[2][1])*(x - points[2][0]) +
         (points[2][0] - points[1][0])*(y - points[2][1])) / denominator
    v = ((points[2][1] - points[0][1])*(x - points[2][0]) +
         (points[0][0] - points[2][0])*(y - points[2][1])) / denominator
    w = 1 - u - v
    return 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1


def InsideSquare(x, y, points):
    return points[0][0] < x < points[0][0] + 800 and points[0][1] < y < points[0][1] + 800


def find_midpoint(point1, point2):
    x_mid = (point1[0] + point2[0]) / 2
    y_mid = (point1[1] + point2[1]) / 2
    return x_mid, y_mid


def MakeXYToSquare(points):
    x = y = 0
    while (not InsideSquare(x, y, points)):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
    return x, y


def MakeXYToTriangle(points):
    x = y = 0
    while (not InsideTriangle(x, y, points)):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
    return x, y


def PaintSquare(x, y, points):
    for _ in range(1_000):
        pygame.draw.rect(sf, (224, 84, 184), (x, y, 1, 1))
        peak = random.randint(0, 7)
        x = (x + 2 * points[peak][0]) / 3
        y = (y + 2 * points[peak][1]) / 3
    return x, y


def PaintTriangle(x, y, points):
    for i in range(1_000):
        pygame.draw.rect(sf, (224, 84, 184), (x, y, 1, 1))
        peak = random.randint(0, 2)
        x, y = find_midpoint((x, y), points[peak])
    return x, y


pygame.init()

size = 1000
padding = 30

sf = pygame.display.set_mode((size, size))
sf.fill((1, 135, 134))

x = 0
y = 0

butT = ButtonWithOutline(sf, (size // 2 - 200, 200, 400, 100),
                         ((3, 218, 198), (235, 241, 241), (44, 63, 80)), 'Triangle')

butS = ButtonWithOutline(sf, (size // 2 - 200, 400, 400, 100),
                         ((3, 218, 198), (235, 241, 241), (44, 63, 80)), 'Square')

but_back = ButtonWithOutline(sf, (10, 10, 100, 80),
                             ((3, 218, 198), (235, 241, 241), (44, 63, 80)), 'Back')

fl_menu = True
fl_shape = 0

running = True
while running:
    pygame.display.flip()
    time.sleep(0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            break
    if fl_menu and running:
        butT.PaintButton()
        butS.PaintButton()
        if butT.MouseTracking(event):
            fl_menu = False
            fl_shape = 1
            sf.fill((1, 135, 134))
            points = [(size // 2, padding), (padding, size - padding),
                      (size - padding, size - padding)]
            pygame.draw.polygon(sf, (3, 218, 198), points)
            x, y = MakeXYToTriangle(points)
        if butS.MouseTracking(event):
            fl_shape = 2
            fl_menu = False
            sf.fill((1, 135, 134))
            pygame.draw.rect(sf, (3, 218, 198), (100, 100, 800, 800))
            points = [(100, 100), (100, 900), (900, 100), (900, 900),
                      (500, 100), (900, 500), (500, 900), (100, 500)]
            x, y = MakeXYToSquare(points)
    elif running:
        but_back.PaintButton()
        if fl_shape == 1:
            x, y = PaintTriangle(x, y, points)
        elif fl_shape == 2:
            x, y = PaintSquare(x, y, points)
        if but_back.MouseTracking(event):
            fl_menu = True
            fl_shape = 0
            sf.fill((1, 135, 134))

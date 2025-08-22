import pygame
import pygame as py
pygame.init()
pygame.font.init()
from math import *

WIN_SZ = 778
RT_SPD = 0.02

window = py.display.set_mode((WIN_SZ,WIN_SZ))
clock  = py.time.Clock()
pm_txt = [[1, 0, 0],[0, 1, 0],[0, 0, 1]]

pm = pm_txt

BS_F = py.font.SysFont('Comic Sans MS', 32, (0, 255, 0))

cps =  [n for n in range(8)]
cps[0] = [[1], [1], [1]] #1
cps[1] = [[-1], [-1], [-1]] #2
cps[2] = [[1], [-1], [1]] #3
cps[3] = [[-1], [1], [1]] #4
cps[4] = [[-1], [1], [-1]] #5
cps[5] = [[1], [-1], [-1]] #6
cps[6] = [[1], [1], [-1]] #7
cps[7] = [[-1], [-1], [1]] #8

def mm2(a, b):
    a_rows = len(a)
    b_rows = len(b)

    b_cols = len(b[0])
    a_cols = len(a[0])

    p = [[0 for _ in range(b_cols)] for _ in range(a_rows)]

    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    p[i][j] += a[i][k] * b[k][j]
    else:
        print("ERR0R :( , INCOMPATIBLE MATRIX SIZES")

    return p

def cp(i, j, points):
    py.draw.line(window, (0, 180, 0), (points[i][0], points[i][1]), (points[j][0], points[j][1]))

scale = 100
aX = aY = aZ = 0

def format_matrix(matrix):
    rows = []
    for row in matrix:
        row_str = "["
        for val in row:
            row_str += f"{val:.2f}"
        row_str += "]"
        rows.append(row_str)
    return " ".join(rows)

def format_angle(angle):
    return f"{angle % (2*pi):6.2f}"

while True:
    clock.tick(64)

    window.fill((0,0,0))
    roX = [[1, 0, 0],
                    [0, cos(aX), -sin(aX)],
                    [0, sin(aX), cos(aX)]]

    roY = [[cos(aY), 0, sin(aY)],
                    [0, 1, 0],
                    [-sin(aY), 0, cos(aY)]]

    roZ = [[cos(aZ), -sin(aZ), 0],
                    [sin(aZ), cos(aZ), 0],
                    [0, 0, 1]]

    aX += 0.01
    aY += 0.01

    points = [0 for _ in range(len(cps))]
    i = 0
    for point in cps:
        rX = mm2(roX, point)
        rY = mm2(roY, rX)
        rZ = mm2(roZ, rY)
        p2D = mm2(pm, rZ)

        x = (p2D[0][0] * scale) + WIN_SZ/2
        y = (p2D[1][0] * scale) + WIN_SZ/2

        points[i] = (x, y)
        i += 1

        py.draw.circle(window, (0,255,0), (x,y), 10)

    cp(0, 2, points)
    cp(2, 5, points)
    cp(5, 6, points)
    cp(6, 4, points)
    cp(4, 3, points)
    cp(3, 7, points)
    cp(7, 2, points)
    cp(7, 1, points)
    cp(1, 5, points)
    cp(1, 4, points)
    cp(3, 0, points)
    cp(0, 6, points)

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()

    keys = py.key.get_pressed()
    if keys[py.K_SPACE]:
        aX = aY = aZ = 90

    mpm_txt = format_matrix(pm_txt)
    max_txt = format_angle(aX)
    may_txt = format_angle(aY)
    maz_txt = format_angle(aZ)

    lines = [
        "pm: " + mpm_txt,
        "Angle x: " + max_txt,
        "Angle y: " + may_txt,
        "Angle z: " + maz_txt
    ]

    y_pos = 10
    for line in lines:
        txt_s = BS_F.render(line, True, (0,255,0))
        window.blit(txt_s, (10, y_pos))
        y_pos += 50

    py.display.update()
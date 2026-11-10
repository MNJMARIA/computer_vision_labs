import random
import time

import numpy as np
import math as mt

from graphics import GraphWin, Point, Line, Polygon, color_rgb


def task_3d(win):

    #cx, cy, cz = 350, 250, 0
    h, r = 140, 60


    # точка на відстані r під кутом a, має відступи
    # вздовж x: r * cos θ
    # вздовж z: r * sin θ

    def make_pyramid(cx, cy, cz):
        # центр піраміди (cx, cy, cz) має бути серединою мас,
        # тобто середнім положенням усіх чотирьох вершин,
        # так піраміда крутиться навколо власної осі
        # відступ основи від центру по висоті - d, висота піраміди - h
        # (d + d + d + (d − h)) / 4 = (4d − h) / 4 = d − h/4 = 0
        # (35+35+35−105)/4 = 0
        pyramid = np.array([[cx + r * mt.cos(mt.radians(90)), cy + h / 4, cz + r * mt.sin(mt.radians(90)), 1],  # A
                            [cx + r * mt.cos(mt.radians(210)), cy + h / 4, cz + r * mt.sin(mt.radians(210)), 1],  # B
                            [cx + r * mt.cos(mt.radians(330)), cy + h / 4, cz + r * mt.sin(mt.radians(330)), 1],  # C
                            [cx, cy - 3 * h / 4, cz, 1]])  # D - вершина піраміди
        return pyramid





    # print(np.round(pyramid, 1))
    # print(pyramid[:, 1].mean()) # має бути 250
    # print(pyramid[:, 1].max() - pyramid[:, 1].min()) # має бути 140

    # win = GraphWin("pyramid", 700, 500)
    # win.setBackground("white")




    #Проєкція на xy: z = 0
    def project_xy():
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 1]])

    # вершини піраміди лежать рядками, тому другу матрицю тарнспонуємо (для закріплення)
    # бо одинична матриця не змінить вигляду ставши транспонованою
    # flat = pyramid.dot(project_xy().T)
    # print(np.round(flat, 1))

    #ребра піраміди (між якими вершинами - 0=A, 1=B, 2=C, 3=D)
    # EDGES = np.array([[0, 1], [1, 2], [0, 2], [0, 3], [1, 3], [2, 3]])

    # грані піраміди
    FACES = [(0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3)]
    # вісь z ближче до глядача, тому будемо вважати що чим більша сума


    # #ребро AB
    # a, b = EDGES[0]
    # c, d = EDGES[-1]
    # #flat[a, 0] це x вершини з номером a, flat[a, 1] це її y (рядок a, стовпець 0 або 1)
    # ab = Line(Point(flat[a, 0], flat[a, 1]), Point(flat[b, 0], flat[b, 1]))
    # bc = Line(Point(flat[b, 0], flat[b, 1]), Point(flat[c, 0], flat[c, 1]))
    # ca = Line(Point(flat[c, 0], flat[c, 1]), Point(flat[a, 0], flat[a, 1]))
    # ad = Line(Point(flat[a, 0], flat[a, 1]), Point(flat[d, 0], flat[d, 1]))
    # bd = Line(Point(flat[b, 0], flat[b, 1]), Point(flat[d, 0], flat[d, 1]))
    # cd = Line(Point(flat[c, 0], flat[c, 1]), Point(flat[d, 0], flat[d, 1]))
    # ab.draw(win)
    # bc.draw(win)
    # ca.draw(win)
    # ad.draw(win)
    # bd.draw(win)
    # cd.draw(win)

    #АБО
    #for a, b in EDGES:
    #    Line(Point(flat[a, 0], flat[a, 1]), Point(flat[b, 0], flat[b, 1])).draw(win)
    #COLORS = ["#4a4e69", "#9a8c98", "#c9ada7", "#f2e9e4"]
    SHADE = [0.6, 0.8, 1.0, 0.7]   # яскравість граней у порядку FACES


    # матриця переміщення
    def move_matrix_3d(dx, dy, dz):
        return np.array([[1, 0, 0, dx],
                         [0, 1, 0, dy],
                         [0, 0, 1, dz],
                         [0, 0, 0, 1]])

    # матриця обертання навколо y
    #вісь навколо якої крутимо - не змінюється(не містить sin/cos)
    def rotate_matrix_3d_y(angle):
        a = mt.radians(angle)
        return np.array([[mt.cos(a), 0, mt.sin(a), 0],
                         [0, 1, 0, 0],
                         [-mt.sin(a), 0, mt.cos(a), 0],
                         [0, 0, 0, 1]])

    # матриця обертання навколо x
    def rotate_matrix_3d_x(angle):
        a = mt.radians(angle)
        return np.array([[1, 0, 0, 0],
                         [0, mt.cos(a), -mt.sin(a), 0],
                         [0, mt.sin(a), mt.cos(a), 0],
                         [0, 0, 0, 1]])

    # матриця обертання навколо z
    def rotate_matrix_3d_z(angle):
        a = mt.radians(angle)
        return np.array([[mt.cos(a), -mt.sin(a), 0, 0],
                         [mt.sin(a), mt.cos(a), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])



    def fade(base, t): # base = (r, g, b), 0-255
        # При t=0 виходить 255(білий), піраміда невидима, а при t=1 виходить c, повний колір
        # для кожного каналу c: 255 - (255 - c) * t, тобто відступ від білого (255) до кольору c
        return color_rgb(*[int(255 - (255 - c) * t) for c in base])

    # p = np.array([[1, 0, 0, 1]])
    # print(np.round(p.dot(rotate_matrix_y(90).T), 3))
    #
    # p = np.array([[0, 0, 1, 1]])
    # print(np.round(p.dot(rotate_matrix_y(90).T), 3))

    # #перетворення плаского трикутника на піраміду
    # #перемістити центр у (0,0,0), повернути навколо Y, повернути навколо X, повернути центр назад
    # M_view = move_matrix(cx, cy, cz).dot(rotate_matrix_x(-35.264).dot(rotate_matrix_y(45).dot(move_matrix(-cx, -cy, -cz))))
    # frame = pyramid.dot(M_view.T)
    # flat = frame.dot(project_xy().T)
    # print(np.round(flat[:, :2], 1))
    #
    # for a, b in EDGES:
    #     Line(Point(flat[a, 0], flat[a, 1]), Point(flat[b, 0], flat[b, 1])).draw(win)


    while not win.checkMouse():
        cx = random.randint(110, 590)  # вікно 700
        cy = random.randint(110, 390)  # вікно 500
        cz = 0
        pyramid = make_pyramid(cx, cy, cz)
        #новий base на кожну появу - колір змінюється
        base = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        N = 120 # кадрів в одній появі: range(0, 360, 3) дає 120
        # обертання піраміди навколо своєї осі
        for spin in range(0, 360, 3):
            k = spin // 3  # номер кадру 0-119
            # t від 0 (невидимо) до 1 (повний колір)
            # перші 20 кадрів t росте 0->1, потім 1, останні 20 кадрів t падає 1->0
            t = min(1, k / 20, (N - k) / 20)
            # 35,264 це кут нахилу ізометрії, arcsin(tan 30) = 35,264
            M_view = move_matrix_3d(cx, cy, cz).dot(
                (rotate_matrix_3d_x(-35.264).dot(rotate_matrix_3d_y(45 + spin).dot(move_matrix_3d(-cx, -cy, -cz)))))
            frame = pyramid.dot(M_view.T)
            flat = frame.dot(project_xy().T)
            order = sorted(range(4), key=lambda i: frame[list(FACES[i]), 2].mean())
            polys = []
            for i in order:
                a, b, c = FACES[i]
                poly = Polygon(Point(flat[a, 0], flat[a, 1]), Point(flat[b, 0], flat[b, 1]), Point(flat[c, 0], flat[c, 1]))
                # SHADE[i] затемнює base для грані i, а fade додає згасання
                poly.setFill(fade(tuple(c * SHADE[i] for c in base), t))
                poly.setOutline(fade((0, 0, 0), t))
                poly.draw(win)
                polys.append(poly)
            # lines = []
            # for a, b in EDGES:
            #     line = Line(Point(flat[a, 0], flat[a, 1]), Point(flat[b, 0], flat[b, 1]))
            #     line.setFill(fade((0, 0, 0), t))
            #     line.draw(win)
            #     lines.append(line)
            win.update()
            time.sleep(0.03)
            # for line in lines:  # стираємо кадр
            #     line.undraw()
            for poly in polys:
                poly.undraw()




    # M_test = move_matrix(cx, cy, cz).dot(rotate_matrix_y(90).dot(move_matrix(-cx, -cy, -cz)))
    # print(np.round(pyramid.dot(M_test.T), 1))

    # win.getMouse()
    #win.close()
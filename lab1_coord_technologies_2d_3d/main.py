import time

from graphics import *
import numpy as np
import math as mt

from pyramid import task_3d


def task_2d(win):

    # розмір вікна (700,500) - центр вікна (350,250)
    cx, cy = 350, 250

    # ширина прямокутника - 160, висота - 90
    w, h = 160, 90

    # зберігаємо кути прямокутника таблицею з одиницями
    rect = np.array([[cx - w/2, cy - h/2, 1],
                     [cx + w/2, cy - h/2, 1],
                     [cx + w/2, cy + h/2, 1],
                     [cx - w/2, cy + h/2, 1]])

    label = Text(Point(350, 20), "Наведіть мишку на вікно")
    label.draw(win)

    def on_move(event):
        label.setText("x = " + str(event.x) + ", y = " + str(event.y))

    win.bind("<Motion>", on_move)


    def draw_figure(win, figure, color):
        # rect маємо як таблицю 4 рядки(0,1,2,3) на 3 стовпці(0,1,2),
        # де x, y в перших двох стовпцях
        poly = Polygon([Point(figure[0, 0], figure[0, 1]),
                        Point(figure[1, 0], figure[1, 1]),
                        Point(figure[2, 0], figure[2, 1]),
                        Point(figure[3, 0], figure[3, 1])
                        ])
        poly.setFill(color)
        poly.draw(win)
        return poly

    # матриця переміщення
    def move_matrix_2d(dx, dy):
        return np.array([[1, 0, dx],
                      [0, 1, dy],
                      [0, 0, 1]])

    # матриця обертання навколо z
    def rotate_matrix_2d(angle):
        a = mt.radians(angle)
        return np.array([[mt.cos(a), -mt.sin(a), 0],
                      [mt.sin(a), mt.cos(a), 0],
                      [0, 0, 1]])


    # для правильного зміщення нам треба щоб перемножилась 1 з rect з dx
    # множення матрицю це рядок першої почленно на стовпець другої
    # тому виконуємо транспонування другої матриці(рядки в стовпці)
    # .dot - множення матриці прямокутника на матрицю переміщення
    step1 = rect.dot(move_matrix_2d(-cx, -cy).T)  # центр в (0, 0)
    # транспонуємо матрицю з тієї ж причини, що і матрицю переміщення
    # вершини прямокутника(rect) записані рядками,
    # а матриці переміщення/обертання для вершин-стовпців,
    # тому транспонуємо їх, щоб були для вершин-рядків
    step2 = step1.dot(rotate_matrix_2d(30).T)
    step3 = step2.dot(move_matrix_2d(cx, cy).T)

    # верифікація: скалярний розрахунок для першої вершини при куті 30
    a = mt.radians(30)
    x0, y0 = rect[0, 0], rect[0, 1]
    x_new = cx + (x0 - cx) * mt.cos(a) - (y0 - cy) * mt.sin(a)
    y_new = cy + (x0 - cx) * mt.sin(a) + (y0 - cy) * mt.cos(a)
    print("скалярно:", x_new, y_new)
    print("матрично:", step3[0, :2])


    # ---------- Операція 1: обертання навколо центру ----------
    poly = draw_figure(win, rect, "blue")

    for angle in range(0, 360, 5):
        #транспонування можна виконати до результату, бо це правило лін.алгебри
        # Транспонування добутку = добуток транспонованих у зворотному порядку
        # (A * B).T = B.T * A.T
        # T(cx, cy) * R(30) * T(-cx, -cy)
        M_total = move_matrix_2d(cx, cy).dot(rotate_matrix_2d(angle).dot(move_matrix_2d(-cx, -cy))) # дії виконуються справа наліво
        result = rect.dot(M_total.T)
        poly.undraw()
        poly = draw_figure(win, result, "blue")
        win.update()
        time.sleep(0.03)


    # ---------- Операція 2: обертання + переміщення, циклічно ----------
    r = mt.hypot(w, h)/2  # півдіагональ прямокутника
    limit = cx - r - 10 #наскільки можемо зсунутись від центру прямокутника
    shift, step, angle = 0, 4, 0

    #крутимось доки не клацнули мишкою
    while not win.checkMouse():
        shift = shift + step
        if abs(shift) >= limit: #дійшли до краю - назад
            step = -step
        angle = angle + 5
        # T(shift, 0) * T(cx, cy) * R(angle) * T(-cx, -cy)
        M = move_matrix_2d(shift, 0).dot(move_matrix_2d(cx, cy).dot(rotate_matrix_2d(angle).dot(move_matrix_2d(-cx, -cy))))
        frame = rect.dot(M.T)
        poly.undraw()
        poly = draw_figure(win, frame, "orange")
        win.update()
        time.sleep(0.03)

    poly.undraw() #зникнення прямокутника
    label.undraw()
    win.unbind("<Motion>")



if __name__ == '__main__':
    win = GraphWin("Лабораторна 1 - ДОСЛІДЖЕННЯ ТЕХНОЛОГІЙ ПОБУДОВИ ТА ПЕРЕТВОРЕННЯ "
               "КООРДИНАТ ПЛОЩИННИХ (2D) ТА ПРОСТОРОВИХ (3D) ОБ’ЄКТІВ", 700, 500, autoflush=False)
    win.setBackground("white")
    win.update()
    task_2d(win)
    task_3d(win)
    win.close()
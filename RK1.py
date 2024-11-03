from PIL import Image
import random
import time
import sys

sys.setrecursionlimit(10000000)

###Код с семинара
def draw_line(img, x1=0, y1=0, x2=0, y2=0):
    eps = 0
    dx = x2 - x1
    dy = y2 - y1
    y = y1
    for i in range (int(x1), int(x2 + 1)):
        eps += 2 * dy
        if (eps > dx):
            eps -= 2 * dx
            y = y + 1
        img.putpixel((int(i), int(y)),(0, 0, 255))

def code(x, y, xl, xr, yd, yu):
    res = 0
    if x < xl:
        res = res | 8
    elif x > xr:
        res = res | 4
    if y < yd:
        res = res | 1
    elif y < yu:
        res = res | 2
    return res

def is_draw_identical(code_a,code_b):
    return code_a == code_b == 0

def is_not_drawable(code_a, code_b):
    return (code_a & code_b) != 0

def cut_line(img, xl, xr, yd, yu, xa, ya, xb, yb):
    code_a = code(xa, ya, xl, xr, yd, yu)
    code_b = code(xb, yb, xl, xr, yd, yu)
    if is_draw_identical(code_a, code_b):
        draw_line(img, xa, ya, xb, yb)
    elif not is_not_drawable(code_a, code_b):
        cut_line(img, xl, xr, yd, yu, xa, ya, xa + xb >> 1, ya + yb >> 1)
        cut_line(img, xl, xr, yd, yu, xa + xb >> 1, ya + yb >> 1, xb, yb)

###Код из статьи
def clip_and_draw_line(img, x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    if not (x1 < xmin and x2 < xmin) and not (x1 > xmax and x2 > xmax):
        if not (y1 < ymin and y2 < ymin) and not (y1 > ymax and y2 > ymax):
            x = [x1, x2]
            y = [y1, y2]
            i = 0
            while i < 2:
                if x[i] < xmin:
                    x[i] = xmin
                    y[i] = ((y2 - y1) / (x2 - x1)) * (xmin - x1) + y1
                elif x[i] > xmax:
                    x[i] = xmax
                    y[i] = ((y2 - y1) / (x2 - x1)) * (xmax - x1) + y1
                
                if y[i] < ymin:
                    y[i] = ymin
                    x[i] = ((x2 - x1) / (y2 - y1)) * (ymin - y1) + x1
                elif y[i] > ymax:
                    y[i] = ymax
                    x[i] = ((x2 - x1) / (y2 - y1)) * (ymax - y1) + x1
                i += 1

            if not (x[0] < xmin and x[1] < xmin) and not (x[0] > xmax and x[1] > xmax):
                draw_line(img, x[0], y[0], x[1], y[1])


###Сравнение
def generate_lines(num_lines, xmin, ymin, xmax, ymax):
    lines = []
    for i in range(num_lines):
        x1, y1 = random.randint(xmin - 50, xmax + 50), random.randint(ymin - 50, ymax + 50)
        x2, y2 = random.randint(xmin - 50, xmax + 50), random.randint(ymin - 50, ymax + 50)
        lines.append((x1, y1, x2, y2))
    return lines
                
def test_cod1(img, xmin, ymin, xmax, ymax, lines):
    start = time.perf_counter()
    cutted_lines = []
    for line in lines:
        result = cut_line(img, xmin, ymin, xmax, ymax, *line)
        if result:
            cutted_lines.append(result)
    finish = time.perf_counter()
    return finish - start, len(cutted_lines)

def test_cod2(img, x_min, y_min, x_max, y_max, lines):
    start = time.perf_counter()
    cutted_lines = []
    for line in lines:
        result = clip_and_draw_line(img, x_min, y_min, x_max, y_max, *line)
        if result:
            cutted_lines.append(result)
    finish = time.perf_counter()
    return finish - start, len(cutted_lines)

xmin, ymin, xmax, ymax = 50, 10, 150, 100
num_lines = 1000000 

lines = generate_lines(num_lines, xmin, ymin, xmax, ymax)

img1 = Image.new('RGB', (500,500), 'white')
img2 = Image.new('RGB', (500,500), 'white')


time_cod1, cutted_cod1 = test_cod1(img1, xmin, ymin, xmax, ymax, lines)
print(f"Время работы cod1: {time_cod1:.4f} сек/n Отсеченные линии: {cutted_cod1}")

time_cod2, cutted_cod2 = test_cod2(img2, xmin, ymin, xmax, ymax, lines)
print(f"Время работы cod1: {time_cod2:.4f} сек/n Отсеченные линии: {cutted_cod2}")

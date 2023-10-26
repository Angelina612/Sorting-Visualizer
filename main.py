import pygame
import random
import math

pygame.init()

SPEED = 120


class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192),
    ]

    font_type = "Arial"
    font_size = 30
    font_size_large = 40
    FONT = pygame.font.SysFont(font_type, font_size)
    LARGE_FONT = pygame.font.SysFont(font_type, font_size_large)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD)/len(lst))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD)/(self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        lst.append(random.randint(min_val, max_val))

    return lst


def draw(draw_info, algo_name, ascending):
    draw_info.screen.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}", True, draw_info.GREEN)
    draw_info.screen.blit(title, (draw_info.width //
                          2 - title.get_width() // 2, 5))
    controls = draw_info.FONT.render(
        "R - Reset || SPACE - Start Sorting || A - Ascending || D - Descending", True, draw_info.BLACK)
    draw_info.screen.blit(controls, (draw_info.width //
                          2 - controls.get_width() // 2, 45))

    sorting_text = draw_info.FONT.render(
        "I - Insertion Sort | B - Bubble Sort | Q - Quick Sort | Merge Sort", True, draw_info.BLACK)
    draw_info.screen.blit(sorting_text, (draw_info.width //
                          2 - sorting_text.get_width() // 2, 75))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.start_x, draw_info.TOP_PAD, draw_info.width -
                      draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.screen,
                         draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val)*draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.screen, color,
                         (x, y, draw_info.block_width, val*draw_info.block_height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info, ascending=True):
    clock = pygame.time.Clock()
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            if (ascending and lst[j] > lst[j + 1]) or (not ascending and lst[j] < lst[j + 1]):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(
                    draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                clock.tick(SPEED)
                yield True

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN,
                      i: draw_info.RED}, True)
            yield True

    return lst


def partition(draw_info, l, r, ascending=True):
    clock = pygame.time.Clock()
    lst = draw_info.lst

    pivot = lst[l]
    i = l - 1
    for j in range(l, r):
        ascending_sort = lst[j] <= pivot and ascending
        descending_sort = lst[j] >= pivot and not ascending
        if ascending_sort or descending_sort:
            i = i + 1
            (lst[i], lst[j]) = (lst[j], lst[i])
            draw_list(draw_info, clear_bg=True)
            clock.tick(SPEED)

    (lst[i + 1], lst[r]) = (lst[r], lst[i + 1])
    draw_list(draw_info, clear_bg=True)
    clock.tick(SPEED)
    return i + 1


def quick_sort_util(draw_info, l, r, ascending=True):

    if l < r:
        pi = partition(draw_info, l, r, ascending)

        quick_sort_util(draw_info, l, pi - 1, ascending)

        quick_sort_util(draw_info, pi + 1, r, ascending)


def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    quick_sort_util(draw_info, l=0, r=len(lst)-1, ascending=ascending)
    yield True
    return lst


def merge(draw_info, l, m, r, ascending=True):
    clock = pygame.time.Clock()
    n1 = m - l + 1
    n2 = r - m

    L = [0] * (n1)
    R = [0] * (n2)

    lst = draw_info.lst

    for i in range(0, n1):
        L[i] = lst[l + i]

    for j in range(0, n2):
        R[j] = lst[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        ascending_sort = L[i] <= R[j] and ascending
        descending_sort = L[i] >= R[j] and not ascending

        if ascending_sort or descending_sort:
            lst[k] = L[i]
            draw_list(draw_info, clear_bg=True)
            clock.tick(SPEED)
            i += 1
        else:
            lst[k] = R[j]
            draw_list(draw_info, clear_bg=True)
            clock.tick(SPEED)
            j += 1
        k += 1

    while i < n1:
        lst[k] = L[i]
        draw_list(draw_info, clear_bg=True)
        clock.tick(SPEED)
        i += 1
        k += 1

    while j < n2:
        lst[k] = R[j]
        draw_list(draw_info, clear_bg=True)
        clock.tick(SPEED)
        j += 1
        k += 1


def merge_sort_util(draw_info, l, r, ascending=True):
    if l < r:
        m = l+(r-l)//2
        merge_sort_util(draw_info, l, m, ascending)
        merge_sort_util(draw_info, m+1, r, ascending)
        merge(draw_info, l, m, r, ascending)


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    merge_sort_util(draw_info, 0, len(lst)-1, ascending)
    yield True
    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 100
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(SPEED)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False

        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(
                    draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"

    pygame.quit()


if __name__ == "__main__":
    main()

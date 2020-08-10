import pygame
import os
import time
import random

# Constants
pygame.init()
WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('comicsans', 30)
pygame.display.set_caption("Sorting Visualizer, By: Arjun Sahlot")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.png")))
TOPBARHEIGHT = 80

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TURQUOISE = (0, 255, 166)

'''
class MergeSort(Algorithm):
    def __init__(self):
        super().__init__("MergeSort")

    def algorithm(self, window, pillars=[]):
        if pillars == []:
            pillars = self.pillars
        if len(pillars) < 2:
            return pillars
        mid = len(pillars) // 2
        left = self.algorithm(pillars[:mid])
        right = self.algorithm(pillars[mid:])
        return self.merge(window, left, right)

    def merge(self, window, left, right):
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            self.update_display(window)
        result += left[i:]
        result += right[j:]
        self.pillars = result
        self.update_display(window)
        return result
'''


# Functions
def generate_pillars(n):
    return [[random.randrange(100, 650, 5), WHITE] for _ in range(n)]


def pillar_width_gap(n):
    pillargap = 3 if n < 200 else 0
    pillarwidth = (WIDTH - 20) / (n + pillargap + 1)
    return pillarwidth, pillargap


def display_window(window, pillars, pillarwidth, pillargap):
    global visualize_button
    window.fill((0, 0, 0))
    # draw top bar
    window.fill(GREY, rect=(0, 0, WIDTH, TOPBARHEIGHT))
    # draw text
    visualize_text = font.render("Visualize!", 1, BLUE)
    window.blit(visualize_text,
                (WIDTH // 2 - visualize_text.get_width() // 2, TOPBARHEIGHT // 2 - visualize_text.get_height() // 2))
    # draw button around text
    visualize_button = pygame.draw.rect(window, BLUE, (
        WIDTH // 2 - visualize_text.get_width() // 2 - 5, TOPBARHEIGHT // 2 - visualize_text.get_height() // 2 - 3,
        visualize_text.get_width() + 10, visualize_text.get_height() + 6), 3)
    # draw pillars
    for i in range(len(pillars)):
        window.fill(pillars[i][1],
                    rect=(10 + i * (pillarwidth + pillargap), pillars[i][0], pillarwidth, HEIGHT - pillars[i][0]))
    pygame.display.update()


def update_pillars(window, pillars, pillarwidth, pillargap, swap1, swap2, merge=False):
    pygame.time.delay(75)
    for i in range(len(pillars)):
        if not merge:
            if swap1 == pillars[i][0]:
                pillars[i][1] = RED
            elif swap2 == pillars[i][0]:
                pillars[i][1] = GREEN
    else:
        pillars[swap1][1] = RED
        pillars[swap2][1] = GREEN

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    display_window(window, pillars, pillarwidth, pillargap)

    for i in range(len(pillars)):
        pillars[i][1] = WHITE


def selection_sort(window, pillars, pillarwidth, pillargap):
    for i in range(len(pillars)):
        min_idx = i
        for j in range(i + 1, len(pillars)):
            if pillars[j][0] < pillars[min_idx][0]:
                min_idx = j
        pillars[i][0], pillars[min_idx][0] = pillars[min_idx][0], pillars[i][0]
        update_pillars(window, pillars, pillarwidth, pillargap, pillars[i][0], pillars[min_idx][0])


def bubble_sort(window, pillars, pillarwidth, pillargap):
    for i in range(len(pillars)):
        for j in range(len(pillars) - 1 - i):
            if pillars[j][0] > pillars[j + 1][0]:
                pillars[j][0], pillars[j + 1][0] = pillars[j + 1][0], pillars[j][0]
        update_pillars(window, pillars, pillarwidth, pillargap, pillars[j][0], pillars[j + 1][0])


def insertion_sort(window, pillars, pillarwidth, pillargap):
    for i in range(len(pillars)):
        cursor = pillars[i][0]
        idx = i
        while idx > 0 and pillars[idx - 1][0] > cursor:
            pillars[idx][0] = pillars[idx - 1][0]
            idx -= 1
        pillars[idx][0] = cursor
        update_pillars(window, pillars, pillarwidth, pillargap, pillars[idx][0], pillars[i][0])


def partition(window, pillars, pillarwidth, pillargap, start, end):
    x = pillars[end][0]
    i = start - 1
    for j in range(start, end + 1, 1):
        if pillars[j][0] <= x:
            i += 1
            if i < j:
                pillars[i][0], pillars[j][0] = pillars[j][0], pillars[i][0]
                update_pillars(window, pillars, pillarwidth, pillargap, pillars[i][0], pillars[j][0])
    return i


def quick_sort(window, pillars, pillarwidth, pillargap, start, end):
    if start < end:
        pivot = partition(window, pillars, pillarwidth, pillargap, start, end)
        quick_sort(window, pillars, pillarwidth, pillargap, start, pivot - 1)
        quick_sort(window, pillars, pillarwidth, pillargap, pivot + 1, end)


def merge(window, pillars, pillarwidth, pillargap, left, middle, right):
    n1 = middle - left + 1
    n2 = right - middle

    L = [0] * n1
    R = [0] * n2

    for i in range(0, n1):
        L[i] = pillars[left + i][0]

    for j in range(0, n2):
        R[j] = pillars[middle + 1 + j][0]

    i = 0
    j = 0
    k = left

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            pillars[k][0] = L[i]
            i += 1
        else:
            pillars[k][0] = R[j]
            j += 1
        k += 1

    while i < n1:
        pillars[k][0] = L[i]
        i += 1
        k += 1

    while j < n2:
        pillars[k][0] = R[j]
        j += 1
        k += 1

    update_pillars(window, pillars, pillarwidth, pillargap, left, right, True)


def merge_sort(window, pillars, pillarwidth, pillargap, left, right):
    if left < right:
        mid = (left + (right - 1)) // 2
        merge_sort(window, pillars, pillarwidth, pillargap, left, mid)
        merge_sort(window, pillars, pillarwidth, pillargap, mid + 1, right)
        merge(window, pillars, pillarwidth, pillargap, left, mid, right)


def main(window):
    n = 100
    pillars = generate_pillars(n)
    # get pillar width and gap
    pillarwidth, pillargap = pillar_width_gap(len(pillars))
    run = True
    algorithm = "Merge"
    while run:
        display_window(window, pillars, pillarwidth, pillargap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if visualize_button.collidepoint(event.pos):
                    if algorithm == "Selection":
                        selection_sort(window, pillars, pillarwidth, pillargap)
                    elif algorithm == "Bubble":
                        bubble_sort(window, pillars, pillarwidth, pillargap)
                    elif algorithm == "Insertion":
                        insertion_sort(window, pillars, pillarwidth, pillargap)
                    elif algorithm == "Quick":
                        quick_sort(window, pillars, pillarwidth, pillargap, 0, n - 1)
                    else:
                        merge_sort(window, pillars, pillarwidth, pillargap, 0, n - 1)

        pygame.display.update()

    pygame.quit()


# Run
main(WINDOW)

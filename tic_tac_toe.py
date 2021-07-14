import pygame
import os
from tkinter import *
from tkinter import messagebox


WIDTH, HEIGHT = 500, 500
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
ONE_THIRD_WIDTH = WIDTH / 3
ONE_THIRD_HEIGHT = HEIGHT / 3

CROSS_IMAGE = pygame.image.load(os.path.join('images', 'cross.png')).convert_alpha()
CROSS = pygame.transform.smoothscale(CROSS_IMAGE, (int(window.get_width()/3 * 0.9), int(window.get_height()/3 * 0.9)))

CIRCLE_IMAGE = pygame.image.load(os.path.join('images', 'circle.png')).convert_alpha()
CIRCLE = pygame.transform.smoothscale(CIRCLE_IMAGE, (int(window.get_width()/3 * 0.9), int(window.get_height()/3 * 0.9)))

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

LINE_WIDTH = 10


def draw(board):
    window.fill(WHITE)

    # DRAW LINES
    pygame.draw.line(window, BLACK, (ONE_THIRD_WIDTH, 0), (ONE_THIRD_WIDTH, HEIGHT), LINE_WIDTH)
    pygame.draw.line(window, BLACK, (2 * ONE_THIRD_WIDTH, 0), (2 * ONE_THIRD_WIDTH, HEIGHT), LINE_WIDTH)
    pygame.draw.line(window, BLACK, (0, ONE_THIRD_HEIGHT), (WIDTH, ONE_THIRD_HEIGHT), LINE_WIDTH)
    pygame.draw.line(window, BLACK, (0, 2 * ONE_THIRD_HEIGHT), (WIDTH, 2 * ONE_THIRD_HEIGHT), LINE_WIDTH)

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "X":
                window.blit(CROSS, (j * window.get_width() / 3 + LINE_WIDTH, i * window.get_width() / 3 + LINE_WIDTH))

            elif board[i][j] == "O":
                window.blit(CIRCLE, (j * window.get_width() / 3 + LINE_WIDTH, i * window.get_width() / 3 + LINE_WIDTH))

    pygame.display.update()


def get_clicked_square(position_x, position_y):
    rel_position_x = position_x / WIDTH
    rel_position_y = position_y / HEIGHT
    if rel_position_x < (1/3):
        col = 0
    elif rel_position_x < (2/3):
        col = 1
    else:
        col = 2
    if rel_position_y < (1/3):
        row = 0
    elif rel_position_y < (2/3):
        row = 1
    else:
        row = 2
    return row, col


def get_sign(player):
    if player % 2 == 1:
        return "X"
    else:
        return "O"


def move(board, row, col, player):
    sign = get_sign(player)
    board[row][col] = sign
    game_ended = True
    for i in board:
        for j in i:
            if not j:
                game_ended = False
                break
    if game_ended:
        return True, board, True

    for i in range(3):
        if board[row][i] != sign:
            break
        if i == 2:
            return True, board, False

    for i in range(3):
        if board[i][col] != sign:
            break
        if i == 2:
            return True, board, False

    if row == col:
        for i in range(3):
            if board[i][i] != sign:
                break
            if i == 2:
                return True, board, False

    if row + col == 2:
        for i in range(3):
            if board[2-i][i] != sign:
                break
            if i == 2:
                return True, board, False

    return False, board, False


def main():
    clock = pygame.time.Clock()
    run = True
    board = [["", "", ""],
             ["", "", ""],
             ["", "", ""]]
    player = 1
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = get_clicked_square(position[0], position[1])
                if board[row][col]:
                    continue
                game_ended, board, tie = move(board, row, col, player)
                if game_ended:
                    draw(board)
                    Tk().wm_withdraw()  # to hide the main window
                    if tie:
                        messagebox.showinfo("It's a tie!", "Exit")
                    else:
                        winner = 1 if player % 2 == 1 else 2
                        messagebox.showinfo(f'Congrats player {winner}', 'Exit')
                    run = False
                player += 1

        draw(board)

    pygame.quit()


if __name__ == "__main__":
    main()
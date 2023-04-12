import pygame
import math
import sys
from copy import deepcopy
import numpy as np

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 50
RADIUS = int(SQUARE_SIZE / 2 - 5)
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Connect 4')


# Function to draw the game board
def draw_board():
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, GRAY, (col * SQUARE_SIZE + int(SQUARE_SIZE / 2), (row + 1) * SQUARE_SIZE + int(SQUARE_SIZE / 2)), RADIUS)


# Function to draw the game pieces
def draw_pieces(board):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + int(SQUARE_SIZE / 2), (row + 1) * SQUARE_SIZE + int(SQUARE_SIZE / 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + int(SQUARE_SIZE / 2), (row + 1) * SQUARE_SIZE + int(SQUARE_SIZE / 2)), RADIUS)


# Function to drop a game piece in the specified column
def drop_piece(col, piece, board):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = piece
            return board
    
    return board

def undo_move(col, piece, board):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][col] == piece:
            board[row][col] = 0
            return board

    return board


def is_valid_space(col, board):
    if board[0][col] == 0:
        return True

    return False
           

# Function to check if a player wins
def check_win(piece, board):
    # Check horizontal
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece:
                return True

    # Check vertical
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                return True

    # Check diagonal (positive slope)
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece:
                return True

    # Check diagonal (negative slope)
    for row in range(ROW_COUNT - 3):
        for col in range(3, COLUMN_COUNT):
            if board[row][col] == piece and board[row + 1][col - 1] == piece and board[row + 2][col - 2] == piece and board[row + 3][col - 3] == piece:
                return True

    return False

    
def check_draw(board):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board[row][col] == 0:
                return False
    return True

def MiniMax(new_board, maximisingPlayer, alpha, beta, depth, yellowPieces, redPieces):

    #print("New_Board: " + str(new_board[5][:]))

    player = 2
    opponent = 1

    if check_win(player, new_board):
        return 1e6 + yellowPieces

    if check_win(opponent, new_board):
        return -1e6 - redPieces

    if check_draw(new_board):
        return 0

    if depth == 0:
        return evaluate_score(new_board, 2)
    
    if maximisingPlayer:
        max_value = -math.inf
        for i in range(COLUMN_COUNT):
            if is_valid_space(i, new_board):
                child = deepcopy(new_board)
                child = drop_piece(i, player, child)
                max_value = max(max_value, MiniMax(child, False, alpha, beta, depth - 1, yellowPieces - 1, redPieces))
                alpha = max(alpha, max_value)
                if (alpha >= beta):
                    break

        return max_value

    else:
        min_value = math.inf
        for i in range(COLUMN_COUNT):
            if is_valid_space(i, new_board):
                child = deepcopy(new_board)
                child = drop_piece(i, opponent, child)
                min_value = min(min_value, MiniMax(child, True, alpha, beta, depth - 1, yellowPieces, redPieces - 1))
                beta = min(beta, min_value)
                if (alpha >= beta):
                    break

        return min_value

def evaluate_window(window, piece):
    score = 0
    
    if piece == 2:
        opp_piece = 1
    else:
        opp_piece = 2

    if piece == 2:
        if (np.count_nonzero(window == piece) == 4) and np.count_nonzero(window == 0):
            score += 100

        elif (np.count_nonzero(window == piece) == 3) and np.count_nonzero(window == 1):
            score += 5

        elif (np.count_nonzero(window == piece) == 2) and np.count_nonzero(window == 2):
            score += 2

    else:
        if (np.count_nonzero(window == opp_piece) == 4) and np.count_nonzero(window == 0):
            score += -4

    return score


def evaluate_score(board, piece):
    window_length = 4
    score = 0

    # # Score center column
    # center_column  = board[:, 3]
    # center_count = np.count_nonzero(center_column == piece)
    # score += (center_count * 3)

    #check columns
    for c in range(COLUMN_COUNT):
        col_array = board[:, c]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:(r+window_length)]
            score += evaluate_window(window, piece)

    #check rows
    for r in range(ROW_COUNT):
        row_array = board[r, :]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:(c+window_length)]
            score += evaluate_window(window, piece)

    # Check diagonal (positive slope)
    for i in range(ROW_COUNT - 3):
        for j in range(COLUMN_COUNT - 3):
            window = [board[i, j], board[i + 1, j + 1], board[i + 2, j + 2], board[i + 3, j + 3]]
            score += evaluate_window(window, piece)

    # Check diagonal (negative slope)
    for i in range(ROW_COUNT - 3):
        for j in range(3, COLUMN_COUNT):
                window = [board[i, j], board[i + 1, j - 1], board[i + 2, j - 2], board[i + 3, j - 3]]
                score += evaluate_window(window, piece)
    return score


def find_best_move(board):
    bestVal = -math.inf 
    bestMove = -1
    new_board = deepcopy(board)
    depth = 5
    
    for x in range(COLUMN_COUNT):
        if is_valid_space(x, new_board):
            new_board = drop_piece(x, 2, new_board)
            value = MiniMax(new_board, False, -math.inf, math.inf, depth, 21, 21)
            print("Val: " +str(value))
            #print(new_board[:][:])
            new_board = undo_move(x, 2, new_board)

            if (value > bestVal):
                bestVal = value
                bestMove = x

    return bestMove

def gameWin_display(turn, board):
    winner = "Player 1 (Red)" if turn == 1 else "Player 2 (Yellow)"
    font = pygame.font.SysFont(None, 35)
    text = font.render(f"{winner} wins!", True, RED if turn == 1 else YELLOW)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, text.get_height() // 2))
    draw_pieces(board)
    pygame.display.update()
    pygame.time.delay(8000)

    return

def gameDraw_display(board):    

    font = pygame.font.SysFont(None, 35)
    text = font.render("Draw!", True, YELLOW)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, text.get_height() // 2))
    draw_pieces(board)
    pygame.display.update()
    pygame.time.delay(8000)

    return

def play_game():
    
    # Game Board
    #board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
    board = np.zeros(shape=(ROW_COUNT,COLUMN_COUNT), dtype=np.uint8)
    turn = 1
    game_over = False


    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION and turn == 1:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                pos_x = event.pos[0]
                pygame.draw.circle(screen, RED if turn == 1 else YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and turn ==1:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                pos_x = event.pos[0]
                col = pos_x // SQUARE_SIZE

                if is_valid_space(col, board):
                    board = drop_piece(col, turn, board)
                    draw_pieces(board)
                    pygame.display.update()

                    if check_win(turn, board):
                        game_over = True
                        gameWin_display(turn, board)
                        return

                    if check_draw(board):
                        game_over = True
                        gameDraw_display(board)
                        return

                    turn = 3 - turn

        if turn == 2:
            column = find_best_move(board)
            # AI drops piece
            # print(column)
            print(board[:][:])
            board = drop_piece(column, 2, board)

            if check_win(turn, board):
                game_over = True
                gameWin_display(turn, board)
                return

            if check_draw(board):
                game_over = True
                gameDraw_display(board)
                return

            # switch player
            turn = 3 - turn

        draw_board()
        draw_pieces(board)
        pygame.display.update()

play_game()
pygame.quit()
sys.exit()
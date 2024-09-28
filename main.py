import pygame
import random

# 기본 설정
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 레벨별 설정
LEVELS = {
    "easy": {"rows": 9, "cols": 9, "mines": 10, "title": "Minesweeper - Easy"},
    "medium": {"rows": 16, "cols": 16, "mines": 40, "title": "Minesweeper - Medium"},
    "hard": {"rows": 24, "cols": 24, "mines": 99, "title": "Minesweeper - Hard"}
}

# 게임 창 설정
font = pygame.font.SysFont('Arial', 25)

# 지뢰 보드 초기화
def create_board(rows, cols, mines):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

    while len(mine_positions) < mines:
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)
        mine_positions.add((x, y))

    for (x, y) in mine_positions:
        board[y][x] = -1  # -1은 지뢰를 의미

    for y in range(rows):
        for x in range(cols):
            if board[y][x] == -1:
                continue
            # 주변 지뢰 카운트
            count = 0
            for i in range(max(0, y-1), min(rows, y+2)):
                for j in range(max(0, x-1), min(cols, x+2)):
                    if board[i][j] == -1:
                        count += 1
            board[y][x] = count
    return board

# 보드 그리기
def draw_board(screen, board, revealed, flags, tile_size):
    rows, cols = len(board), len(board[0])
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, DARK_GRAY if revealed[y][x] else GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            if revealed[y][x]:
                if board[y][x] == -1:
                    pygame.draw.circle(screen, RED, rect.center, tile_size // 3)
                elif board[y][x] > 0:
                    text = font.render(str(board[y][x]), True, BLACK)
                    screen.blit(text, text.get_rect(center=rect.center))
            elif flags[y][x]:
                pygame.draw.circle(screen, GREEN, rect.center, tile_size // 3)

# 빈 칸 열기 (재귀적으로 빈 칸 확장)
def reveal_tile(board, revealed, x, y, tile_size):
    if revealed[y][x]:
        return
    revealed[y][x] = True
    if board[y][x] == 0:
        for i in range(max(0, y-1), min(len(board), y+2)):
            for j in range(max(0, x-1), min(len(board[0]), x+2)):
                if not revealed[i][j]:
                    reveal_tile(board, revealed, j, i, tile_size)

# 게임 종료 확인
def check_win(board, revealed):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != -1 and not revealed[y][x]:
                return False
    return True

# 레벨 선택 화면
def draw_menu(screen):
    screen.fill(WHITE)
    text_easy = font.render("Press 1 for Easy (9x9, 10 Mines)", True, BLACK)
    text_medium = font.render("Press 2 for Medium (16x16, 40 Mines)", True, BLACK)
    text_hard = font.render("Press 3 for Hard (24x24, 99 Mines)", True, BLACK)

    screen.blit(text_easy, (50, 100))
    screen.blit(text_medium, (50, 150))
    screen.blit(text_hard, (50, 200))
    pygame.display.flip()

# 메인 게임 루프
def main():
    running = True
    game_over = False
    won = False
    level = None

    # 레벨 선택
    while level is None:
        screen = pygame.display.set_mode((400, 300))
        draw_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = "easy"
                elif event.key == pygame.K_2:
                    level = "medium"
                elif event.key == pygame.K_3:
                    level = "hard"

    # 선택된 레벨에 따른 설정
    settings = LEVELS[level]
    rows, cols, mines = settings['rows'], settings['cols'], settings['mines']
    tile_size = 600 // max(rows, cols)  # 보드 크기 비례 조정
    screen = pygame.display.set_mode((cols * tile_size, rows * tile_size))
    pygame.display.set_caption(settings['title'])

    board = create_board(rows, cols, mines)
    revealed = [[False for _ in range(cols)] for _ in range(rows)]
    flags = [[False for _ in range(cols)] for _ in range(rows)]

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                x //= tile_size
                y //= tile_size

                if event.button == 1:  # 좌클릭
                    if board[y][x] == -1:
                        game_over = True
                    else:
                        reveal_tile(board, revealed, x, y, tile_size)
                    if check_win(board, revealed):
                        won = True
                        game_over = True
                elif event.button == 3:  # 우클릭 (깃발)
                    flags[y][x] = not flags[y][x]

        draw_board(screen, board, revealed, flags, tile_size)

        if game_over:
            if won:
                text = font.render("You Won!", True, BLACK)
            else:
                text = font.render("Game Over!", True, RED)
            screen.blit(text, text.get_rect(center=(cols * tile_size // 2, rows * tile_size // 2)))

        pygame.display.flip()

if __name__ == "__main__":
    main()
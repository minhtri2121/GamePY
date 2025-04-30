import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 15
WIN_CONDITION = 5
SEARCH_DEPTH = 3

board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
player_turn = 'X'
vs_ai = True

def is_valid(i, j):
    return 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE

def reset_game():
    global board, player_turn
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    player_turn = 'X'
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j].config(text=' ', state=tk.NORMAL)

def switch_mode():
    global vs_ai
    vs_ai = not vs_ai
    mode_btn.config(text="Chế độ: " + ("Đấu AI 🤖" if vs_ai else "2 Người 👥"))
    reset_game()

def check_winner(player):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != player:
                continue
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                count = 1
                for step in range(1, WIN_CONDITION):
                    ni, nj = i + dx * step, j + dy * step
                    if is_valid(ni, nj) and board[ni][nj] == player:
                        count += 1
                    else:
                        break
                if count >= WIN_CONDITION:
                    return True
    return False

def is_full():
    return all(cell != ' ' for row in board for cell in row)

def evaluate_line(line, player):
    score = 0
    opp = 'O' if player == 'X' else 'X'
    patterns = {
        player*5: 100000,
        player*4 + ' ': 10000,
        ' ' + player*4: 10000,
        player*3 + ' ': 1000,
        ' ' + player*3: 1000,
        player*2 + ' ': 100,
        ' ' + player*2: 100,
        opp*5: -100000,
        opp*4 + ' ': -8000,
        ' ' + opp*4: -8000,
        opp*3 + ' ': -500,
        ' ' + opp*3: -500,
    }
    for pattern, value in patterns.items():
        if pattern in line:
            score += value
    return score

def heuristic(player):
    total = 0
    for i in range(BOARD_SIZE):
        row = ''.join(board[i])
        col = ''.join([board[j][i] for j in range(BOARD_SIZE)])
        total += evaluate_line(row, player)
        total += evaluate_line(col, player)
    for d in range(-BOARD_SIZE+1, BOARD_SIZE):
        diag1 = ''.join([board[i][i - d] for i in range(max(0, d), min(BOARD_SIZE, BOARD_SIZE + d)) if is_valid(i, i - d)])
        diag2 = ''.join([board[i][BOARD_SIZE - 1 - i + d] for i in range(max(0, -d), min(BOARD_SIZE, BOARD_SIZE - d)) if is_valid(i, BOARD_SIZE - 1 - i + d)])
        total += evaluate_line(diag1, player)
        total += evaluate_line(diag2, player)
    return total

def get_candidates():
    candidates = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != ' ':
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i + dx, j + dy
                        if is_valid(ni, nj) and board[ni][nj] == ' ':
                            candidates.add((ni, nj))
    return list(candidates) if candidates else [(BOARD_SIZE//2, BOARD_SIZE//2)]

def minimax(depth, maximizing, alpha, beta):
    if check_winner('O'):
        return (None, 1000000)
    if check_winner('X'):
        return (None, -1000000)
    if depth == 0 or is_full():
        return (None, heuristic('O') - heuristic('X'))

    best_move = None
    moves = get_candidates()

    if maximizing:
        max_eval = -float('inf')
        for (i, j) in moves:
            board[i][j] = 'O'
            _, eval = minimax(depth - 1, False, alpha, beta)
            board[i][j] = ' '
            if eval > max_eval:
                max_eval = eval
                best_move = (i, j)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return (best_move, max_eval)
    else:
        min_eval = float('inf')
        for (i, j) in moves:
            board[i][j] = 'X'
            _, eval = minimax(depth - 1, True, alpha, beta)
            board[i][j] = ' '
            if eval < min_eval:
                min_eval = eval
                best_move = (i, j)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return (best_move, min_eval)

def make_ai_move():
    (i, j), _ = minimax(SEARCH_DEPTH, True, -float('inf'), float('inf'))
    if i is not None:
        make_move(i, j)

def make_move(i, j):
    global player_turn
    if board[i][j] != ' ':
        return
    board[i][j] = player_turn
    buttons[i][j].config(text=player_turn, state=tk.DISABLED)

    if check_winner(player_turn):
        messagebox.showinfo("Kết thúc", f"{player_turn} thắng!")
        disable_board()
        return
    elif is_full():
        messagebox.showinfo("Hòa", "Không còn ô trống!")
        return

    player_turn = 'O' if player_turn == 'X' else 'X'

    if vs_ai and player_turn == 'O':
        root.after(100, make_ai_move)

def disable_board():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j].config(state=tk.DISABLED)

# Giao diện
root = tk.Tk()
root.title("Cờ Caro 15x15")

for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        btn = tk.Button(root, text=' ', width=2, height=1,
                        font=('Arial', 14),
                        command=lambda i=i, j=j: make_move(i, j))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn

mode_btn = tk.Button(root, text="Chế độ: Đấu AI 🤖", command=switch_mode)
mode_btn.grid(row=BOARD_SIZE, column=0, columnspan=BOARD_SIZE//2, sticky="we")

reset_btn = tk.Button(root, text="Chơi lại 🔁", command=reset_game)
reset_btn.grid(row=BOARD_SIZE, column=BOARD_SIZE//2, columnspan=BOARD_SIZE//2, sticky="we")

root.mainloop()

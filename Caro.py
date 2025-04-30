import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 15
WIN_CONDITION = 5
SEARCH_DEPTH = 2

board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
player_turn = 'X'
vs_ai = True

#Kiểm tra ô
def is_valid(i, j):
    return 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE

#Làm mới bàn cờ
def reset_game():
    global board, player_turn
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    player_turn = 'X'
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j].config(text=' ', state=tk.NORMAL)

#Thay đổi chế độ
def switch_mode():
    global vs_ai
    vs_ai = not vs_ai
    mode_btn.config(text="Chế độ: " + ("Đấu AI 🤖" if vs_ai else "2 Người 👥"))
    reset_game()

#Kiểm tra thắng thua trò chơi
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

#Kiểm tra hoà
def is_full():
    return all(cell != ' ' for row in board for cell in row)

#Training AI

#Kiểm tra hàng cột để tối ưu nước đi
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

#Tính điểm cho Player
def heuristic(player):
    total = 0
    for i in range(BOARD_SIZE):
        row = ''.join(board[i])
        col = ''.join([board[j][i] for j in range(BOARD_SIZE)])
        total += evaluate_line(row, player)
        total += evaluate_line(col, player)
    for d in range(-BOARD_SIZE+1, BOARD_SIZE):
        diag1 = ''.join([board[i][i - d] for i in range(max(0, d), min(BOARD_SIZE, BOARD_SIZE + d)) if is_valid(i, i - d)])
        diag2 = ''.join([board[i][BOARD_SIZE - 1 - (i - d)] for i in range(max(0, d), min(BOARD_SIZE, BOARD_SIZE + d)) if is_valid(i, BOARD_SIZE - 1 - (i - d))])
        total += evaluate_line(diag1, player)
        total += evaluate_line(diag2, player)
    return total

#Dự đoán nước đi cho AI
def minimax(depth, maximizingPlayer, alpha, beta):
    if check_winner('O'):
        return 1000000
    if check_winner('X'):
        return -1000000
    if depth == 0 or is_full():
        return heuristic('O') - heuristic('X')
    
    moves = generate_moves()

    if maximizingPlayer:
        maxEval = -float('inf')
        for (i, j) in moves:
            board[i][j] = 'O'
            eval = minimax(depth-1, False, alpha, beta)
            board[i][j] = ' '
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for (i, j) in moves:
            board[i][j] = 'X'
            eval = minimax(depth-1, True, alpha, beta)
            board[i][j] = ' '
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

#Tạo dânh sách các nước đi hợp lệ cho AI
def generate_moves():
    moves = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != ' ':
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        ni, nj = i + dx, j + dy
                        if is_valid(ni, nj) and board[ni][nj] == ' ':
                            moves.add((ni, nj))
    return list(moves)

#Quyết định nước đi của AI
def ai_move():
    best_score = -float('inf')
    best_move = None
    for (i, j) in generate_moves():
        board[i][j] = 'O'
        score = minimax(SEARCH_DEPTH-1, False, -float('inf'), float('inf'))
        board[i][j] = ' '
        if score > best_score:
            best_score = score
            best_move = (i, j)
    if best_move:
        make_move(*best_move)

#Xử lý nước đi
def make_move(i, j):
    global player_turn
    if board[i][j] != ' ':
        return
    board[i][j] = player_turn
    buttons[i][j].config(text=player_turn, state=tk.DISABLED)
    if check_winner(player_turn):
        messagebox.showinfo("Kết thúc", f"{player_turn} thắng!")
        reset_game()
        return
    elif is_full():
        messagebox.showinfo("Kết thúc", "Hòa!")
        reset_game()
        return
    if vs_ai and player_turn == 'X':
        player_turn = 'O'
        ai_move()
        player_turn = 'X'
    else:
        player_turn = 'O' if player_turn == 'X' else 'X'

#Main
root = tk.Tk()
root.title("Caro 15x15")

top_frame = tk.Frame(root)
top_frame.pack()

mode_btn = tk.Button(top_frame, text="Chế độ: Đấu AI 🤖", command=switch_mode)
mode_btn.pack(side=tk.LEFT, padx=5)

reset_btn = tk.Button(top_frame, text="Chơi lại 🔄", command=reset_game)
reset_btn.pack(side=tk.LEFT, padx=5)

board_frame = tk.Frame(root)
board_frame.pack()

for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        btn = tk.Button(board_frame, text=' ', width=2, height=1,
                        command=lambda i=i, j=j: make_move(i, j))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn

root.mainloop()
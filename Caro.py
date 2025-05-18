import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 15
WIN_CONDITION = 5
SEARCH_DEPTH = 3

board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
player_turn = 'X'
vs_ai = True
last_move = None

#Kiểm tra ô
def is_valid(i, j):
    return 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE

#Làm mới bàn cờ
def reset_game():
    
    global board, player_turn, last_move
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    player_turn = 'X'
    last_move = None
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j].config(text=' ', state=tk.NORMAL, bg='SystemButtonFace')

#Thay đổi chế độ
def switch_mode():
    global vs_ai
    vs_ai = not vs_ai
    mode_btn.config(text="Chế độ: " + ("Đấu AI 🤖" if vs_ai else "2 Người 👥"))
    reset_game()

#Kiểm tra thắng thua trò chơi
def check_winner(player):
    # Kiểm tra 5 ô liên tiếp
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE - 4):
            # Hàng ngang
            if all(board[i][j+k] == player for k in range(5)):
                return True
            # Hàng dọc
            if all(board[j+k][i] == player for k in range(5)):
                return True
    # Chéo chính
    for i in range(BOARD_SIZE - 4):
        for j in range(BOARD_SIZE - 4):
            if all(board[i+k][j+k] == player for k in range(5)):
                return True
            if all(board[i+4-k][j+k] == player for k in range(5)):
                return True
    return False

#Kiểm tra hoà
def is_full():
    return all(all(cell != ' ' for cell in row) for row in board)

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

#Tạo danh sách các nước đi hợp lệ cho AI
def generate_moves():
    moves = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != ' ':
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i + dx, j + dy
                        if is_valid(ni, nj) and board[ni][nj] == ' ':
                            moves.add((ni, nj))
    # If no moves found (game start), choose center
    if not moves:
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
    # Calculate heuristic for moves to sort and limit to top 10 moves for pruning efficiency
    move_scores = []
    for i, j in moves:
        board[i][j] = 'O'
        score = heuristic('O')
        board[i][j] = ' '
        move_scores.append((score, (i, j)))
    move_scores.sort(reverse=True, key=lambda x: x[0])
    top_moves = [move[1] for move in move_scores[:10]]  # Limit to top 10 moves
    return top_moves

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
            eval = minimax(depth - 1, False, alpha, beta)
            board[i][j] = ' '
            if eval > maxEval:
                maxEval = eval
            if maxEval > alpha:
                alpha = maxEval
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for (i, j) in moves:
            board[i][j] = 'X'
            eval = minimax(depth - 1, True, alpha, beta)
            board[i][j] = ' '
            if eval < minEval:
                minEval = eval
            if minEval < beta:
                beta = minEval
            if beta <= alpha:
                break
        return minEval

#Quyết định nước đi của AI
def ai_move():
    mode_btn.config(text="AI đang nghĩ... ⏳")
    root.update()
    best_score = -float('inf')
    best_move = None
    moves = generate_moves()
    # To further optimize, evaluate only best moves first in minimax
    for (i, j) in moves:
        board[i][j] = 'O'
        score = minimax(SEARCH_DEPTH , False, -float('inf'), float('inf'))
        board[i][j] = ' '
        if score > best_score:
            best_score = score
            best_move = (i, j)
    if best_move:
        make_move(*best_move)
    mode_btn.config(text="Chế độ: Đấu AI 🤖")

#Xử lý nước đi
def make_move(i, j):
    global player_turn, last_move
    if board[i][j] != ' ':
        return

    board[i][j] = player_turn
    buttons[i][j].config(text=player_turn, state=tk.DISABLED, bg='yellow')

    # Khôi phục ô cũ về màu mặc định
    if last_move and last_move != (i, j):
        x, y = last_move
        buttons[x][y].config(bg='SystemButtonFace')

    last_move = (i, j)

    if check_winner(player_turn):
        messagebox.showinfo("Kết thúc", f"{player_turn} thắng!")
        reset_game()
        return
    elif is_full():
        messagebox.showinfo("Kết thúc", "Hòa!")
        reset_game()
        return

    player_turn = 'O' if player_turn == 'X' else 'X'

    # Gọi AI nếu là chế độ đấu với AI và đến lượt 'O'
    if vs_ai and player_turn == 'O':
        root.after(100, ai_move)

#Main
root = tk.Tk()
root.title("Caro")

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
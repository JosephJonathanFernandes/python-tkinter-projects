import tkinter as tk
from tkinter import messagebox
import random
import time

# Initialize variables
board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
player_first = True
player_score = 0
ai_score = 0
draw_score = 0

# Minimax with Alpha-Beta Pruning
def is_full(b):
    return all(cell != " " for row in b for cell in row)

def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != " ":
            return b[i][0]
    for j in range(3):
        if b[0][j] == b[1][j] == b[2][j] != " ":
            return b[0][j]
    if b[0][0] == b[1][1] == b[2][2] != " ":
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != " ":
        return b[0][2]
    return None

def minimax(b, depth, is_max, alpha, beta):
    winner = check_winner(b)
    if winner == "X": return 1
    if winner == "O": return -1
    if is_full(b): return 0

    if is_max:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = "X"
                    eval = minimax(b, depth + 1, False, alpha, beta)
                    b[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == " ":
                    b[i][j] = "O"
                    eval = minimax(b, depth + 1, True, alpha, beta)
                    b[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move():
    best_val = -float('inf')
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                move_val = minimax(board, 0, False, -float('inf'), float('inf'))
                board[i][j] = " "
                if move_val > best_val:
                    move = (i, j)
                    best_val = move_val
    return move

# GUI
root = tk.Tk()
root.title("Tic Tac Toe - AI vs Player")

score_label = tk.Label(root, text="Player: 0  AI: 0  Draws: 0", font=("Arial", 14))
score_label.grid(row=5, column=0, columnspan=3)

def update_scoreboard():
    score_label.config(text=f"Player: {player_score}  AI: {ai_score}  Draws: {draw_score}")

def get_winning_line(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != " ":
            return [(i, 0), (i, 1), (i, 2)]
    for j in range(3):
        if b[0][j] == b[1][j] == b[2][j] != " ":
            return [(0, j), (1, j), (2, j)]
    if b[0][0] == b[1][1] == b[2][2] != " ":
        return [(0, 0), (1, 1), (2, 2)]
    if b[0][2] == b[1][1] == b[2][0] != " ":
        return [(0, 2), (1, 1), (2, 0)]
    return []

def button_click(i, j):
    global player_score, ai_score, draw_score
    if board[i][j] == " " and check_winner(board) is None:
        board[i][j] = "O"
        buttons[i][j].config(text="O", state="disabled")
        winner = check_winner(board)
        if winner or is_full(board):
            end_game()
        else:
            root.update()
            time.sleep(0.3)
            ai_i, ai_j = best_move()
            board[ai_i][ai_j] = "X"
            buttons[ai_i][ai_j].config(text="X", state="disabled")
            winner = check_winner(board)
            if winner or is_full(board):
                end_game()

def end_game():
    global player_score, ai_score, draw_score
    winner = check_winner(board)
    if winner == "O":
        player_score += 1
        messagebox.showinfo("Game Over", "You win!")
    elif winner == "X":
        ai_score += 1
        messagebox.showinfo("Game Over", "AI wins!")
    else:
        draw_score += 1
        messagebox.showinfo("Game Over", "It's a draw!")

    for (i, j) in get_winning_line(board):
        buttons[i][j].config(bg="lightgreen")
    update_scoreboard()

def reset_board():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", bg="white", state="normal")
    if not player_first:
        root.update()
        time.sleep(0.3)
        ai_i, ai_j = best_move()
        board[ai_i][ai_j] = "X"
        buttons[ai_i][ai_j].config(text="X", state="disabled")

def choose_player():
    global player_first
    response = messagebox.askyesno("Choose First Player", "Do you want to play first?")
    player_first = response
    reset_board()

for i in range(3):
    for j in range(3):
        b = tk.Button(root, text=" ", width=5, height=2, font=("Segoe UI", 24, "bold"),
                      bg="white", fg="black", activebackground="lightblue",
                      command=lambda i=i, j=j: button_click(i, j))
        b.grid(row=i, column=j)
        buttons[i][j] = b

reset_button = tk.Button(root, text="Reset Game", font=("Arial", 14), command=reset_board)
reset_button.grid(row=4, column=0, columnspan=1)

choose_button = tk.Button(root, text="Choose Player First", font=("Arial", 14), command=choose_player)
choose_button.grid(row=4, column=1, columnspan=2)

choose_player()
root.mainloop()
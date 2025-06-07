import tkinter as tk
from tkinter import messagebox
import random

# Constants for players
HUMAN = "O"
AI = "X"

# Scoreboard
scores = {HUMAN: 0, AI: 0, "Draw": 0}

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe with AI (Alpha-Beta Pruning)")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = HUMAN
        self.ai_player = AI
        self.first_player = tk.StringVar(value=HUMAN)
        self.status_label = tk.Label(root, text="Choose who plays first", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, columnspan=3)

        self.create_menu()
        self.create_board()
        self.create_scoreboard()

    def create_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.grid(row=1, column=0, columnspan=3)

        tk.Radiobutton(menu_frame, text="Human", variable=self.first_player, value=HUMAN, command=self.set_first_player).pack(side=tk.LEFT)
        tk.Radiobutton(menu_frame, text="AI", variable=self.first_player, value=AI, command=self.set_first_player).pack(side=tk.LEFT)

        tk.Button(menu_frame, text="Reset Game", command=self.reset_game).pack(side=tk.LEFT)

    def create_board(self):
        board_frame = tk.Frame(self.root)
        board_frame.grid(row=2, column=0, columnspan=3)
        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text=" ", font=("Arial", 32), width=4, height=2,
                                command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def create_scoreboard(self):
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 12))
        self.score_label.grid(row=3, column=0, columnspan=3)

    def get_score_text(self):
        return f"Human: {scores[HUMAN]}  AI: {scores[AI]}  Draws: {scores['Draw']}"

    def set_first_player(self):
        self.current_player = self.first_player.get()
        self.reset_game()

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = " "
                self.buttons[i][j]["bg"] = "SystemButtonFace"
                self.buttons[i][j]["state"] = "normal"
        self.status_label.config(text=f"{self.current_player}'s turn")
        if self.first_player.get() == AI:
            self.root.after(500, self.ai_move)

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col]["text"] = self.current_player
            if self.check_game_over():
                return
            self.current_player = AI if self.current_player == HUMAN else HUMAN
            self.status_label.config(text=f"{self.current_player}'s turn")
            if self.current_player == AI:
                self.root.after(500, self.ai_move)

    def ai_move(self):
        best_score = float('-inf')
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = AI
                    score = self.minimax(self.board, 0, False, float('-inf'), float('inf'))
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        if move:
            self.make_move(move[0], move[1])

    def minimax(self, board, depth, is_max, alpha, beta):
        winner = self.check_winner()
        if winner == AI:
            return 1
        elif winner == HUMAN:
            return -1
        elif self.is_full():
            return 0

        if is_max:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = AI
                        best = max(best, self.minimax(board, depth + 1, False, alpha, beta))
                        board[i][j] = " "
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = HUMAN
                        best = min(best, self.minimax(board, depth + 1, True, alpha, beta))
                        board[i][j] = " "
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best

    def check_winner(self):
        # Rows, cols, diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]
        return None

    def is_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            self.status_label.config(text=f"{winner} wins!")
            scores[winner] += 1
            self.highlight_winner(winner)
            self.end_game()
            return True
        elif self.is_full():
            self.status_label.config(text="It's a draw!")
            scores["Draw"] += 1
            self.end_game()
            return True
        return False

    def highlight_winner(self, winner):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == winner:
                for j in range(3):
                    self.buttons[i][j]["bg"] = "lightgreen"
                return
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == winner:
                for j in range(3):
                    self.buttons[j][i]["bg"] = "lightgreen"
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == winner:
            for i in range(3):
                self.buttons[i][i]["bg"] = "lightgreen"
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == winner:
            for i in range(3):
                self.buttons[i][2 - i]["bg"] = "lightgreen"
            return

    def end_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["state"] = "disabled"
        self.score_label.config(text=self.get_score_text())


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

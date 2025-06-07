import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

# Try to load sound (optional)
try:
    import pygame
    pygame.init()
    SOUND_ENABLED = True
    CLICK_SOUND = "click.wav"  # Add your sound files
    WIN_SOUND = "win.wav"
except:
    SOUND_ENABLED = False

# Main Game Class
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe with Alpha-Beta Pruning")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None]*3 for _ in range(3)]
        self.player_turn = True
        self.first_player = tk.StringVar(value="Human")
        self.difficulty = tk.StringVar(value="Hard")
        self.score = {"Human": 0, "AI": 0, "Draws": 0}
        self.history = []

        self.create_widgets()
        self.reset_board(first_time=True)

    def create_widgets(self):
        # Top Controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Who Plays First:").pack(side=tk.LEFT)
        tk.OptionMenu(control_frame, self.first_player, "Human", "AI").pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Difficulty:").pack(side=tk.LEFT)
        tk.OptionMenu(control_frame, self.difficulty, "Easy", "Medium", "Hard").pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="New Game", command=self.reset_board).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Undo", command=self.undo_move).pack(side=tk.LEFT, padx=5)

        # Board Frame
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text=" ", width=6, height=3,
                                font=("Arial", 20), command=lambda i=i, j=j: self.make_move(i, j))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

        # Status and Score
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.score_label.pack()

    def play_sound(self, sound):
        if SOUND_ENABLED:
            try:
                pygame.mixer.Sound(sound).play()
            except:
                pass

    def update_status(self, msg):
        self.status_label.config(text=msg)

    def update_scoreboard(self):
        self.score_label.config(text=f"Human: {self.score['Human']}  |  AI: {self.score['AI']}  |  Draws: {self.score['Draws']}")

    def reset_board(self, first_time=False):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.history.clear()
        self.player_turn = self.first_player.get() == "Human"
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.config(text=" ", state=tk.NORMAL, bg="SystemButtonFace")
        self.update_status("Your turn!" if self.player_turn else "AI is thinking...")
        self.update_scoreboard()
        if not self.player_turn and not first_time:
            self.root.after(500, self.ai_move)

    def make_move(self, i, j):
        if self.board[i][j] == " " and self.player_turn:
            self.board[i][j] = "O"
            self.history.append((i, j))
            self.buttons[i][j].config(text="O")
            self.play_sound(CLICK_SOUND)
            if self.check_game("O"):
                return
            self.player_turn = False
            self.update_status("AI is thinking...")
            self.root.after(500, self.ai_move)

    def undo_move(self):
        if self.history:
            last = self.history.pop()
            self.board[last[0]][last[1]] = " "
            self.buttons[last[0]][last[1]].config(text=" ", bg="SystemButtonFace")
            self.player_turn = not self.player_turn
            self.update_status("Your turn!" if self.player_turn else "AI is thinking...")

    def ai_move(self):
        i, j = self.get_ai_move()
        self.board[i][j] = "X"
        self.buttons[i][j].config(text="X")
        self.play_sound(CLICK_SOUND)
        if self.check_game("X"):
            return
        self.player_turn = True
        self.update_status("Your turn!")

    def get_ai_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        level = self.difficulty.get()
        if level == "Easy":
            return random.choice(empty)
        elif level == "Medium":
            move = self.alpha_beta(self.board, 2, -float("inf"), float("inf"), True)[1]
            return move if move else random.choice(empty)
        else:
            move = self.alpha_beta(self.board, 9, -float("inf"), float("inf"), True)[1]
            return move if move else random.choice(empty)

    def alpha_beta(self, board, depth, alpha, beta, is_max):
        winner = self.check_winner(board)
        if winner == "X":
            return (1, None)
        elif winner == "O":
            return (-1, None)
        elif all(cell != " " for row in board for cell in row):
            return (0, None)
        if depth == 0:
            return (0, None)

        best = (-float("inf"), None) if is_max else (float("inf"), None)
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X" if is_max else "O"
                    score = self.alpha_beta(board, depth - 1, alpha, beta, not is_max)[0]
                    board[i][j] = " "
                    if is_max:
                        if score > best[0]:
                            best = (score, (i, j))
                        alpha = max(alpha, best[0])
                    else:
                        if score < best[0]:
                            best = (score, (i, j))
                        beta = min(beta, best[0])
                    if beta <= alpha:
                        break
        return best

    def check_game(self, player):
        winner = self.check_winner(self.board)
        if winner:
            self.update_status(f"{'You' if winner == 'O' else 'AI'} wins!")
            self.highlight_winner(winner)
            self.score["Human" if winner == "O" else "AI"] += 1
            self.update_scoreboard()
            self.disable_board()
            self.play_sound(WIN_SOUND)
            return True
        elif all(cell != " " for row in self.board for cell in row):
            self.update_status("It's a draw!")
            self.score["Draws"] += 1
            self.update_scoreboard()
            self.disable_board()
            return True
        return False

    def disable_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)

    def check_winner(self, b):
        # Rows, columns, diagonals
        lines = [b[i] for i in range(3)] + [[b[0][j], b[1][j], b[2][j]] for j in range(3)] + [[b[0][0], b[1][1], b[2][2]], [b[0][2], b[1][1], b[2][0]]]
        for line in lines:
            if line[0] == line[1] == line[2] and line[0] != " ":
                return line[0]
        return None

    def highlight_winner(self, winner):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == winner:
                for j in range(3):
                    self.buttons[i][j].config(bg="lightgreen")
                return
        for j in range(3):
            if b[0][j] == b[1][j] == b[2][j] == winner:
                for i in range(3):
                    self.buttons[i][j].config(bg="lightgreen")
                return
        if b[0][0] == b[1][1] == b[2][2] == winner:
            for i in range(3):
                self.buttons[i][i].config(bg="lightgreen")
        elif b[0][2] == b[1][1] == b[2][0] == winner:
            for i in range(3):
                self.buttons[i][2 - i].config(bg="lightgreen")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

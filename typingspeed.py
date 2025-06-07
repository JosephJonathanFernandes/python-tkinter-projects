import tkinter as tk
import time
import random
import os
import pygame  # For sound effects

# Initialize pygame mixer for sound
pygame.mixer.init()

def play_typing_sound():
    try:
        pygame.mixer.Sound("typing.wav").play()
    except:
        pass  # Skip if sound not found

def play_finish_sound():
    try:
        pygame.mixer.Sound("finish.wav").play()
    except:
        pass

# Sentences per level
sentences = {
    "Easy": [
        "I love Python.",
        "The sky is blue.",
        "She drinks coffee.",
        "He codes in Java.",
        "They play chess."
    ],
    "Medium": [
        "The programmer fixed a critical bug yesterday.",
        "Typing fast requires regular practice and focus.",
        "She managed to complete the project on time.",
        "Learning algorithms can be fun and rewarding.",
        "Streamlit is great for building quick apps."
    ],
    "Hard": [
        "Understanding recursion requires thinking in layers.",
        "Machine learning involves data preprocessing techniques.",
        "Multithreading can lead to race conditions and deadlocks.",
        "The database failed due to transaction isolation levels.",
        "Typing accuracy and speed are equally important in tests."
    ]
}

class TypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test - Pro Version")
        self.root.geometry("750x650")
        self.bg = "#1e1e1e"
        self.fg = "#ffffff"

        self.root.config(bg=self.bg)
        self.start_time = None
        self.time_left = 60
        self.timer_running = False
        self.history = []
        self.level = "Easy"

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Typing Speed Test", font=("Helvetica", 20, "bold"), bg=self.bg, fg=self.fg).pack(pady=10)

        self.level_var = tk.StringVar(value="Easy")
        tk.OptionMenu(self.root, self.level_var, "Easy", "Medium", "Hard").pack()

        self.timer_label = tk.Label(self.root, text="Time Left: 60s", font=("Helvetica", 14), bg=self.bg, fg=self.fg)
        self.timer_label.pack()

        self.sentence_label = tk.Label(self.root, text="", wraplength=700, font=("Helvetica", 14), bg=self.bg, fg=self.fg)
        self.sentence_label.pack(pady=10)

        self.entry = tk.Text(self.root, height=5, width=70, font=("Helvetica", 12))
        self.entry.pack(pady=10)
        self.entry.bind("<Key>", lambda e: play_typing_sound() if self.timer_running else None)

        tk.Button(self.root, text="Start Typing", command=self.start_typing, bg="green", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Button(self.root, text="Check Result", command=self.check_result, bg="blue", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg=self.bg, fg=self.fg)
        self.result_label.pack(pady=10)

        self.history_label = tk.Label(self.root, text="Your History (Last 5):", font=("Helvetica", 12), bg=self.bg, fg=self.fg)
        self.history_label.pack()
        self.history_text = tk.Text(self.root, height=5, width=70, font=("Helvetica", 10), bg="#333", fg="white")
        self.history_text.pack(pady=5)
        self.history_text.config(state=tk.DISABLED)

        self.leaderboard_label = tk.Label(self.root, text="Top 5 Leaderboard:", font=("Helvetica", 12, "bold"), bg=self.bg, fg="#ffcc00")
        self.leaderboard_label.pack()
        self.leaderboard_text = tk.Text(self.root, height=5, width=70, font=("Helvetica", 10), bg="#444", fg="cyan")
        self.leaderboard_text.pack(pady=5)
        self.leaderboard_text.config(state=tk.DISABLED)

    def get_sentence(self):
        level = self.level_var.get()
        return random.choice(sentences[level])

    def start_typing(self):
        self.entry.delete("1.0", tk.END)
        self.sentence_label.config(text=self.get_sentence())
        self.start_time = time.time()
        self.time_left = 60
        self.timer_running = True
        self.timer_label.config(text="Time Left: 60s")
        self.result_label.config(text="")
        self.update_timer()

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.timer_running = False
            self.check_result()

    def check_result(self):
        if not self.start_time:
            self.result_label.config(text="Click 'Start Typing' first.")
            return

        self.timer_running = False
        play_finish_sound()

        typed_text = self.entry.get("1.0", tk.END).strip()
        total_time = 60 - self.time_left
        word_count = len(typed_text.split())
        wpm = round(word_count / (total_time / 60)) if total_time > 0 else 0

        original = self.sentence_label.cget("text")
        correct_chars = sum(1 for a, b in zip(typed_text, original) if a == b)
        accuracy = round((correct_chars / len(original)) * 100, 2)

        result = f"{wpm} WPM | {accuracy}% Accuracy | Level: {self.level_var.get()}"
        self.result_label.config(text=result)
        self.save_result(result)
        self.update_history(result)
        self.update_leaderboard()

    def save_result(self, result):
        with open("results.txt", "a") as file:
            file.write(result + "\n")

    def update_history(self, result):
        self.history.append(result)
        if len(self.history) > 5:
            self.history.pop(0)
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        for line in self.history:
            self.history_text.insert(tk.END, line + "\n")
        self.history_text.config(state=tk.DISABLED)

    def update_leaderboard(self):
        try:
            with open("results.txt", "r") as file:
                lines = file.readlines()
            lines = sorted(lines, key=lambda x: int(x.split()[0]), reverse=True)
            top = lines[:5]
        except:
            top = []

        self.leaderboard_text.config(state=tk.NORMAL)
        self.leaderboard_text.delete("1.0", tk.END)
        for entry in top:
            self.leaderboard_text.insert(tk.END, entry)
        self.leaderboard_text.config(state=tk.DISABLED)

# Run app
root = tk.Tk()
app = TypingTest(root)
root.mainloop()

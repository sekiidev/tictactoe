import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#1e1e1e")   # 🔥 Dark background
        self.root.resizable(False, False)   # 🔒 No resizing (clean overlay)
        self.frame = None
        self.player_symbol = "X"
        self.ai_symbol = "O"
        self.vs_ai = False
        self.show_menu()

    # ---------------- MENU ---------------- #
    def show_menu(self):
        self.clear_frame()
        self.frame = tk.Frame(self.root, bg="#1e1e1e", highlightthickness=0, bd=0)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Tic Tac Toe", font=("Segoe UI", 22, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=10)

        # Choose symbol
        sym_frame = tk.Frame(self.frame, bg="#1e1e1e")
        sym_frame.pack(pady=10)
        tk.Label(sym_frame, text="Choose your symbol:", bg="#1e1e1e",
                 fg="white", font=("Segoe UI", 12)).pack(side="left", padx=5)
        self.symbol_var = tk.StringVar(value="X")
        tk.Radiobutton(sym_frame, text="X", variable=self.symbol_var, value="X",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                       activebackground="#1e1e1e", highlightthickness=0, bd=0).pack(side="left")
        tk.Radiobutton(sym_frame, text="O", variable=self.symbol_var, value="O",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                       activebackground="#1e1e1e", highlightthickness=0, bd=0).pack(side="left")

        # Mode selection
        tk.Button(self.frame, text="Play vs Player", font=("Segoe UI", 12),
                  command=lambda: self.start_game(vs_ai=False),
                  bg="#2d2d2d", fg="white", relief="flat", width=20,
                  activebackground="#3c3c3c").pack(pady=5)

        tk.Button(self.frame, text="Play vs AI", font=("Segoe UI", 12),
                  command=lambda: self.start_game(vs_ai=True),
                  bg="#2d2d2d", fg="white", relief="flat", width=20,
                  activebackground="#3c3c3c").pack(pady=5)

    # ---------------- GAME ---------------- #
    def start_game(self, vs_ai):
        self.vs_ai = vs_ai
        self.player_symbol = self.symbol_var.get()
        self.ai_symbol = "O" if self.player_symbol == "X" else "X"
        self.current_player = "X"
        self.board = [" "] * 9
        self.buttons = []

        self.clear_frame()
        self.frame = tk.Frame(self.root, bg="#1e1e1e", highlightthickness=0, bd=0)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Tic Tac Toe", font=("Segoe UI", 20, "bold"),
                 bg="#1e1e1e", fg="white").grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(9):
            btn = tk.Button(self.frame, text="", font=("Segoe UI", 24), width=5, height=2,
                            command=lambda i=i: self.on_click(i), bg="#2d2d2d", fg="white",
                            activebackground="#3c3c3c", relief="flat", highlightthickness=0, bd=0)
            btn.grid(row=1 + i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        if self.vs_ai and self.ai_symbol == "X":
            self.ai_move()

    def on_click(self, idx):
        if self.board[idx] == " " and self.current_player == self.player_symbol:
            self.make_move(idx, self.player_symbol)
            if not self.check_end():
                if self.vs_ai:
                    self.ai_move()

    def make_move(self, idx, symbol):
        self.board[idx] = symbol
        self.buttons[idx].config(text=symbol, fg="#ff4c4c" if symbol == "X" else "#4cc9ff")
        self.current_player = "O" if symbol == "X" else "X"

    # ---------------- AI ---------------- #
    def ai_move(self):
        best_score = -2
        best_move = None
        for m in self.available_moves():
            self.board[m] = self.ai_symbol
            score = self.minimax(False)
            self.board[m] = " "
            if score > best_score:
                best_score, best_move = score, m
        self.make_move(best_move, self.ai_symbol)
        self.check_end()

    def minimax(self, maximizing):
        winner = self.check_winner()
        if winner == self.ai_symbol: return 1
        if winner == self.player_symbol: return -1
        if " " not in self.board: return 0

        if maximizing:
            best = -2
            for m in self.available_moves():
                self.board[m] = self.ai_symbol
                best = max(best, self.minimax(False))
                self.board[m] = " "
            return best
        else:
            best = 2
            for m in self.available_moves():
                self.board[m] = self.player_symbol
                best = min(best, self.minimax(True))
                self.board[m] = " "
            return best

    def available_moves(self):
        return [i for i, v in enumerate(self.board) if v == " "]

    # ---------------- WIN LOGIC ---------------- #
    def check_winner(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),
                (0,3,6),(1,4,7),(2,5,8),
                (0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != " ":
                return self.board[a]
        return None

    def check_end(self):
        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!" if not self.vs_ai else
                                ("You win!" if winner == self.player_symbol else "AI wins!"))
            self.show_menu()
            return True
        elif " " not in self.board:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.show_menu()
            return True
        return False

    # ---------------- HELPERS ---------------- #
    def clear_frame(self):
        if self.frame:
            self.frame.destroy()

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

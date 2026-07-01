import tkinter as tk
from tkinter import messagebox

# ─── COLORS (pink theme) ───
BG = "#ffe6f0"
BTN_COLOR = "#ff80b3"
BTN_HOVER = "#ff4d94"
TEXT_COLOR = "#4d0026"
FONT_MAIN = ("Helvetica", 24, "bold")
FONT_LABEL = ("Helvetica", 14, "bold")

# ─── GLOBAL STATE ───
current_player = "X"
board = [""] * 9
buttons = []

# ─── WIN CONDITION (Member B writes check_winner, you just call it) ───
def check_winner(board):
    combos = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # cols
        [0,4,8],[2,4,6]           # diagonals
    ]
    for combo in combos:
        a, b, c = combo
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None

def is_draw(board):
    return all(cell != "" for cell in board)

# ─── BUTTON CLICK LOGIC ───
def on_click(index):
    global current_player
    if board[index] != "":
        return
    board[index] = current_player
    buttons[index].config(text=current_player,
                          fg="#4d0026" if current_player == "X" else "#800040")
    winner = check_winner(board)
    if winner:
        update_score(winner)
        messagebox.showinfo("🎉 We have a winner!",
                            f"{player_names[winner]} wins! 🏆")
        reset_game()
        return
    if is_draw(board):
        messagebox.showinfo("It's a draw!", "No winner this time 😅")
        reset_game()
        return
    current_player = "O" if current_player == "X" else "X"
    turn_label.config(text=f"Player {current_player}'s Turn")

# ─── RESET GAME ───
def reset_game():
    global current_player, board
    current_player = "X"
    board = [""] * 9
    for btn in buttons:
        btn.config(text="")
    turn_label.config(text=f"Player {current_player}'s Turn")

# ─── BUILD THE WINDOW (Member A's main job) ───
# ─── SCORE TRACKING (Member B) ───
scores = {"X": 0, "O": 0}
score_label = None
player_names = {"X": "Player X", "O": "Player O"}

def update_score(winner):
    scores[winner] += 1
    score_label.config(text=f"🏆 {player_names['X']}: {scores['X']}  |  {player_names['O']}: {scores['O']}")

# ─── NAME INPUT SCREEN (Member B) ───
def get_player_names():
    name_window = tk.Tk()
    name_window.title("Enter Player Names")
    name_window.configure(bg=BG)
    name_window.resizable(False, False)

    tk.Label(name_window, text="🎀 Welcome to Tic Tac Toe 🎀",
             font=FONT_LABEL, bg=BG, fg=TEXT_COLOR).pack(pady=10)

    tk.Label(name_window, text="Player X Name:",
             font=FONT_LABEL, bg=BG, fg=TEXT_COLOR).pack(pady=5)
    x_entry = tk.Entry(name_window, font=FONT_LABEL)
    x_entry.pack(pady=5)

    tk.Label(name_window, text="Player O Name:",
             font=FONT_LABEL, bg=BG, fg=TEXT_COLOR).pack(pady=5)
    o_entry = tk.Entry(name_window, font=FONT_LABEL)
    o_entry.pack(pady=5)

    def confirm():
        x_name = x_entry.get().strip() or "Player X"
        o_name = o_entry.get().strip() or "Player O"
        player_names["X"] = x_name
        player_names["O"] = o_name
        name_window.destroy()

    tk.Button(name_window, text="Start Game 🎮",
              font=FONT_LABEL, bg=BTN_COLOR, fg=TEXT_COLOR,
              activebackground=BTN_HOVER,
              command=confirm).pack(pady=15)

    name_window.mainloop()
def build_window():
    global turn_label

    root = tk.Tk()
    root.title("🎀 Tic Tac Toe")
    root.configure(bg=BG)
    root.resizable(False, False)

    # Title
    title = tk.Label(root, text="🎀 Tic Tac Toe 🎀",
                     font=("Helvetica", 20, "bold"),
                     bg=BG, fg=TEXT_COLOR)
    title.pack(pady=10)

    # Turn label
   turn_label = tk.Label(root, text=f"{player_names['X']}'s Turn",
                          font=FONT_LABEL, bg=BG, fg=TEXT_COLOR)
    turn_label.pack(pady=5)
# Score tracker
    global score_label
    score_label = tk.Label(root,
                           text=f"🏆 {player_names['X']}: 0  |  {player_names['O']}: 0",
                           font=FONT_LABEL, bg=BG, fg=TEXT_COLOR)
    score_label.pack(pady=5)

    # Game board frame
    frame = tk.Frame(root, bg=BG)
    frame.pack(pady=10)

    # 9 buttons in a 3x3 grid
    for i in range(9):
        btn = tk.Button(
            frame,
            text="",
            font=FONT_MAIN,
            width=4,
            height=2,
            bg=BTN_COLOR,
            fg=TEXT_COLOR,
            activebackground=BTN_HOVER,
            relief="raised",
            command=lambda i=i: on_click(i)
        )
        btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        buttons.append(btn)

    # Reset button
    reset_btn = tk.Button(root, text="🔄 Reset Game",
                          font=FONT_LABEL,
                          bg=BTN_COLOR, fg=TEXT_COLOR,
                          activebackground=BTN_HOVER,
                          command=reset_game)
    reset_btn.pack(pady=15)

    root.mainloop()

# ─── RUN ───
get_player_names()
build_window()

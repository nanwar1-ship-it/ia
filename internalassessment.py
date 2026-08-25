import tkinter as tk
import random
import sqlite3
import unicodedata

from databasesetup import (
    DATABASE_NAME,
    create_or_get_player,
    loginadd,
    save_game_result,
    mdp_decision,
    signupadd,

)

from databasesetup import create_database
create_database()

def word(hard):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, spanish_word, translation
        FROM words
        WHERE difficulty = ?
    """, (hard,))

    database = cursor.fetchall()
    connection.close()
    return database


def normalise_word(value):
    """Return a lowercase word with surrounding spaces removed."""
    return value.strip().lower()


def choose_word(hard):
    words = word(hard)

    if not words:
        return None

    print(random.choice(words))
    return random.choice(words)


LETTERS = "abcdefghijklmnñopqrstuvwxyzáéíóúü"
LETTERS_SET = set(LETTERS)

ROW_COUNT = 6
GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"


class SpanishWordleApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Spanish Wordle")
        self.window.geometry("790x690")
        self.window.resizable(False, False)

        self.username_entry = None
        self.password_entry = None
        self.message_label = None
        self.logged_in_user_id = None
        self.logged_in_username = None

        self.current_difficulty = 2 

        self.show_welcome_page()

    def clear_window(self):
        self.window.unbind("<Key>")
        for widget in self.window.winfo_children():
            widget.destroy()

    def show_welcome_page(self):
        self.clear_window()

        label = tk.Label(
            self.window,
            text="Bienvenido. Please sign up",
            font=("Arial", 30, "bold"),
        )
        label.place(x=140, y=200)

        signup_button = tk.Button(
            self.window,
            text="Sign up here",
            font=("Arial", 18, "bold"),
            command=self.sign_up,
        )
        signup_button.place(x=325, y=350)

        login_button = tk.Button(
            self.window,
            text="Log in here",
            font=("Arial", 18, "bold"),
            command=self.log_in,
        )
        login_button.place(x=325, y=410)

    def sign_up(self):
        self.clear_window()

        su_label = tk.Label(
            self.window, text="Sign up", font=("Arial", 30, "bold")
        )
        su_label.place(x=345, y=100)

        username_label = tk.Label(
            self.window, text="Username", font=("Arial", 18, "bold")
        )
        username_label.place(x=200, y=170)

        password_label = tk.Label(
            self.window, text="Password", font=("Arial", 18, "bold")
        )
        password_label.place(x=200, y=220)

        self.username_entry = tk.Entry(
            self.window, font=("Arial", 18, "bold")
        )
        self.username_entry.place(x=300, y=170)

        self.password_entry = tk.Entry(
            self.window, font=("Arial", 18, "bold"), show="*"
        )
        self.password_entry.place(x=300, y=220)

    
        susave_button = tk.Button(
            self.window,
            text="Sign up",
            font=("Arial", 18, "bold"),
            command=self.actually_signup,
        )
        susave_button.place(x=345, y=300)

        self.message_label = tk.Label(
            self.window, text="", font=("Arial", 16, "bold")
        )
        self.message_label.place(x=100, y=350)

        back_button = tk.Button(
            self.window, text="Back", command=self.show_welcome_page
        )
        back_button.place(x=365, y=400)

    def log_in(self):
        self.clear_window()

        li_label = tk.Label(
            self.window, text="Log in", font=("Arial", 30, "bold")
        )
        li_label.place(x=345, y=100)

        username_label = tk.Label(
            self.window, text="Username", font=("Arial", 18, "bold")
        )
        username_label.place(x=200, y=170)

        password_label = tk.Label(
            self.window, text="Password", font=("Arial", 18, "bold")
        )
        password_label.place(x=200, y=220)

        self.username_entry = tk.Entry(
            self.window, font=("Arial", 18, "bold")
        )
        self.username_entry.place(x=300, y=170)

        self.password_entry = tk.Entry(
            self.window, font=("Arial", 18, "bold"), show="*"
        )
        self.password_entry.place(x=300, y=220)

    
        lisave_button = tk.Button(
            self.window,
            text="Log in",
            font=("Arial", 18, "bold"),
            command=self.actually_login,
        )
        lisave_button.place(x=345, y=300)

        self.message_label = tk.Label(
            self.window, text="", font=("Arial", 16, "bold")
        )
        self.message_label.place(x=100, y=350)

        back_button = tk.Button(
            self.window, text="Back", command=self.show_welcome_page
        )
        back_button.place(x=365, y=400)

    def actually_signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if username == "" or password == "":
            self.message_label.config(text="Username and password are required.")
            return

        success, message = signupadd(username, password)

    
        self.message_label.config(text=message)

        if success:
            self.password_entry.delete(0, tk.END)

    def actually_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if username == "" or password == "":
            self.message_label.config(text="Username and password are required.")
            return

        success, user_id, username = loginadd(username, password)

        if success:
            self.logged_in_user_id = user_id
            self.logged_in_username = username
            self.open_game()
        else:
            self.message_label.config(text="Invalid username or password.")

    def update_mdp_difficulty(self, game_id, won, guesses_used, hints_left):
        user_id = self.logged_in_user_id
        hints_used = 3 - hints_left
        
        if won:
            if guesses_used <= 2:
                reward = 1
                action = "INCREASE"
            elif 3 <= guesses_used <= 5:
                reward = 10
                action = "MAINTAIN"
            else:
                reward = 2
                action = "DECREASE"
        else:
            reward = -5
            action = "DECREASE"

        reward -= (hints_used * 2)

        if action == "INCREASE":
            next_difficulty = min(self.current_difficulty + 1, 5)
        elif action == "DECREASE":
            next_difficulty = max(self.current_difficulty - 1, 1)
        else:
            next_difficulty = self.current_difficulty

        mdp_decision(
            game_id=game_id,
            user_id=user_id,
            attempts_used=guesses_used,
            hints_remaining=hints_left,
            correct_letters=0,
            reward=reward,
            action=action
        )

        self.current_difficulty = next_difficulty
    
    def open_game(self):
        self.clear_window()

        selected_word = choose_word(self.current_difficulty)

        if selected_word is None:
            error_label = tk.Label(
                self.window,
                text="No words are available for difficulty 4.",
                font=("Arial", 20, "bold"),
            )
            error_label.pack(pady=100)
            return
    
        word_id, computer, translation = selected_word
        computer = normalise_word(computer)

        column_count = len(computer)

        if column_count == 0:
            tk.Label(
                self.window,
                text="The selected word is empty.",
                font=("Arial", 20, "bold"),
            ).pack(pady=100)
            return
        boxes = []
        for i in range(ROW_COUNT):
            row_boxes = []
            for w in range(column_count):
                label = tk.Label(
                    self.window,
                    text=" ",
                    width=3,
                    height=2,
                    font=("Arial", 30, "bold"),
                    bg="white",
                    fg="black",
                    relief="raised",
                    borderwidth=1,
                )
                label.grid(row=i, column=w, padx=3, pady=3)
                row_boxes.append(label)
            boxes.append(row_boxes)

        message = tk.Label(
            self.window,
            text=f"Input {column_count} letters",
            font=("Arial", 22),
        )
        message.grid(
            row=ROW_COUNT,
            column=0,
            columnspan=column_count,
            pady=15,
        )

        game_row = 0
        game_guess = ""
        game_over = False
        hints = 3
        hint_position = 0

        def finish_game(won):
            nonlocal game_over
            if game_over:
                return

            game_over = True
            guesses_used = game_row + 1
    
   
            game_id = save_game_result(
            self.logged_in_user_id,
            word_id,
            won,
            guesses_used,
            )
            self.update_mdp_difficulty(
            game_id=game_id,
            won=won,
            guesses_used=guesses_used,
            hints_left=hints
            )

       
        def guess():
            nonlocal game_row, game_guess, game_over

            if game_over:
                return

            guess_word = game_guess

            remaining_counts = {}
            results = ["grey"] * column_count

            for index in range(column_count):
                if guess_word[index] == computer[index]:
                    results[index] = "green"
                else:
                    letter = computer[index]
                    remaining_counts[letter] = remaining_counts.get(letter, 0) + 1

            for index in range(column_count):
                if results[index] == "green":
                    continue

                letter = guess_word[index]

                if remaining_counts.get(letter, 0) > 0:
                    results[index] = "yellow"
                    remaining_counts[letter] -= 1

            for index, result in enumerate(results):
                if result == "green":
                    boxes[game_row][index].config(bg=GREEN)
                elif result == "yellow":
                    boxes[game_row][index].config(bg=YELLOW)
                else:
                    boxes[game_row][index].config(bg=GREY)

            if guess_word == computer:
                message.config(text="Muy bueno!")
                finish_game(True)
            elif game_row == ROW_COUNT - 1:
                message.config(text=f"Game over, it was {computer}")
                finish_game(False)
            else:
                game_row += 1
                game_guess = ""
                message.config(text=f"Input {column_count} letters")

        def keypressed(event):
            nonlocal game_guess

            if game_over:
                return

            if event.keysym == "Return":
                if len(game_guess) == column_count:
                    guess()
                else:
                    message.config(
                        text=f"Please input a {column_count} letter word"
                    )

            elif event.keysym == "BackSpace":
                if len(game_guess) > 0:
                    game_guess = game_guess[:-1]
                    boxes[game_row][len(game_guess)].config(text="")

            elif event.char:
                typed_character = normalise_word(event.char)

                if (
                    typed_character in LETTERS_SET
                    and len(game_guess) < column_count
                ):
                    boxes[game_row][len(game_guess)].config(
                        text=typed_character.upper()
                    )
                    game_guess += typed_character

        self.window.bind("<Key>", keypressed)
        self.window.focus_set()

        def give_hints():
            nonlocal hints, hint_position

            if game_over:
                return

            if hints <= 0:
                message.config(text="No hints left.")
                return

            if hint_position >= column_count:
                message.config(text="All letter positions have been revealed.")
                return
            position = hint_position

            for row_index in range(game_row, ROW_COUNT):
                if boxes[row_index][position].cget("bg") != GREEN:
                    boxes[row_index][position].config(
                        text=computer[position].upper()
                    )

            hint_position += 1
            hints -= 1
            hint_button.config(text=f"Hints: {hints}")

            if hints == 0:
                message.config(text=f"Translation: {translation}")

        hint_button = tk.Button(
            self.window,
            text=f"Hints: {hints}",
            font=("Arial", 12),
            command=give_hints,
        )
        hint_button.grid(
            row=0,
            column=column_count,
            padx=5,
            pady=5,
            sticky="ne",
        )

        logout_button = tk.Button(
            self.window,
            text="Logout",
            command=self.show_welcome_page,
        )
        logout_button.grid(
            row=1,
            column=column_count,
            padx=5,
            pady=5,
            sticky="ne",
        )



def run_app():
    window = tk.Tk()
    app = SpanishWordleApp(window)
    window.mainloop()


if __name__ == "__main__":
    run_app()

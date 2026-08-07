import tkinter as tk
import random
import sqlite3

connection = sqlite3.connect("internalassessment.db")
cursor = connection.cursor()

def word(hard):
    cursor.execute("""
    SELECT spanish_word, translation
    FROM words
    WHERE difficulty = ?
    """, (hard,))
    database = cursor.fetchall()
    return database
    
hard = 4
all = word(hard)


chosen_word = random.choice(all)
computer = chosen_word[0]
translation = chosen_word[1]

print(chosen_word)

letters = "abcdefghijklmnñopqrstuvwxyzáéíóúü"
letters_list = []
for i in letters:
    letters_list.append(i)

row = 6
column = len(computer)

GREEN  = "#6aaa64"
YELLOW = "#c9b458"
GREY   = "#787c7e"

window = tk.Tk()
window.geometry("790x690")

label = tk.Label(window, text = 'Bienvenido. Please sign up', font = ("Arial", 40, "bold"), fg = "black")
label.place(x = 140, y = 345)

def window_clear():
    for widget in window.winfo_children():
        widget.destroy()

#sign up page
def sign_up():
    window_clear()
    su_label = tk.Label(window, text = "Sign up", font = ("Arial", 30, "bold"))
    su_label.place(x = 345, y = 100)
    username_label = tk.Label(window, text = "Username", font = ("Arial", 18, "bold"))
    username_label.place  (x = 200, y = 170)
    password_label = tk.Label(window, text = "Password", font = ("Arial", 18, "bold"))
    password_label.place  (x = 200, y = 200)
    username_entry = tk.Entry(window, font = ("Arial", 18, "bold"))
    username_entry.place(x = 300, y = 170)
    password_entry = tk.Entry(window, font = ("Arial", 18, "bold"))
    password_entry.place(x = 300, y = 200)
    susave_button = tk.Button(window, text = "Sign up", font = ("Arial", 18, "bold"))
    susave_button.place(x=345, y = 300)


def log_in():
    window_clear()
    li_label = tk.Label(window, text = "Log in", font = ("Arial", 30, "bold"))
    li_label.place(x = 345, y = 100)
    username_label = tk.Label(window, text = "Username", font = ("Arial", 18, "bold"))
    username_label.place(x = 200, y = 170)
    password_label = tk.Label(window, text = "Password", font = ("Arial", 18, "bold"))
    password_label.place(x = 200, y = 200)
    username_entry = tk.Entry(window, font = ("Arial", 18, "bold"))
    username_entry.place(x = 300, y = 170)
    password_entry = tk.Entry(window, font = ("Arial", 18, "bold"))
    password_entry.place(x = 300, y = 200)
    lisave_button = tk.Button(window, text = "Log in", font = ("Arial", 18, "bold"))
    lisave_button.place(x = 345, y = 300)


signup_button = tk.Button(window, text = 'sign up here', font = ("Arial", 18, "bold" ), command = sign_up)
signup_button.place(x=325, y =445)
login_button = tk.Button(window, text = 'log in here', font = ("Arial", 18, "bold" ), command = log_in)
login_button.place(x=325, y =480)



# to do: work on data base part 
     

root = tk.Tk()
root.title("Spanish Wordle")

boxes = []
for i in range(row):
    row_boxes = []
    for w in range(column):
        label = tk.Label(root, text = " ", width = 4, height = 2, font = ("Arial", 40, "bold"), bg = "white", fg = "black", relief= "raised", borderwidth = 1)
        label.grid(row = i, column = w, padx =3, pady =3)
        row_boxes.append(label)
    boxes.append(row_boxes)

message = tk.Label(root, text = f"input {len(computer)} letters", font = ("Arial", 30))

message.grid(row=6, column=0, columnspan=column, pady=20)


game_row = 0
game_guess = ""
game_over = False



def guess():
    global game_row, game_guess, game_over
    
    complist=[]

    for e in computer:
                complist.append(e)

    for z in range(column):
            if game_guess[z] == computer[z]:
                boxes[game_row][z].config(bg = GREEN)
                complist[z] = ""

    for z in range(column):
        if game_guess[z]==computer[z]:
             continue

        for_two = 0

        for u in complist:
            if u == game_guess[z]:
                  for_two+=1

        if for_two == 0:
                boxes[game_row][z].config(bg=GREY)
        else:
             boxes[game_row][z].config(bg = YELLOW)
             complist.remove(game_guess[z])      

    if game_guess == computer:
        message.config(text = "muy bueno")
        game_over = True
    elif game_row == row-1: 
        message.config(text = f"game over, it was {computer}")
        game_over = True
    else:
        game_row += 1 
        game_guess = ""

def keypressed(type):
    global game_guess
    if game_over:
        return
    if type.keysym == "Return":
        if len(game_guess) == column:
            guess()
        else:
            message.config(text = f"please input a {column} letter word")
    elif type.keysym == "BackSpace":
        if len(game_guess) > 0:
            game_guess = game_guess[:-1]
            boxes[game_row][len(game_guess)].config(text = "")
    elif type.char in letters_list:
        if len(game_guess)<column: 
            boxes[game_row][len(game_guess)].config(text = type.char.upper())
            game_guess = game_guess + type.char.lower()

    
root.bind("<Key>",keypressed)
col = 6
hints = 3



def givehints():
    global x
    global hints
    global computer
    if hints == 3:
        for j in range(game_row, row):
            if boxes[j][0].cget("bg") != GREEN:
                boxes[j][0].config(text=computer[0].upper())
        hints -= 1
        hint_button.config(text=f"hints:{hints}")
    elif hints == 2:
        for j in range(game_row, row):
            if boxes[j][1].cget("bg") != GREEN:
                boxes[j][1].config(text=computer[1].upper())
        hints -= 1
        hint_button.config(text=f"hints:{hints}")
    elif hints == 1:
        for j in range(game_row, row):
            if boxes[j][2].cget("bg") != GREEN:
                boxes[j][2].config(text=computer[2].upper())
        hints -= 1
        hint_button.config(text=f"hints:{hints}")
        message.config(text = translation)
    else:
        message.config(text="no hints left")

hint_button = tk.Button(root, text=f"hints:{hints}", font = ("Arial", 12), command = givehints)
hint_button.grid(row = 0, column = len(computer), padx = 2, pady=2, sticky = "ne")


root.mainloop()
connection.close()

import sqlite3

connection = sqlite3.connect("internalassessment.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spanish_word TEXT NOT NULL,
    translation TEXT NOT NULL,
    difficulty INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    level INTEGER DEFAULT 1,
    games_played INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS game_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    word_id INTEGER,
    won INTEGER,
    guesses_used INTEGER
)
""")

connection.commit()

connection.close()

print("data base cooked")
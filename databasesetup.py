import sqlite3

def create_database():
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

    #table for signup and login
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
    )
    """)




    connection.commit()

    connection.close()

#function for sign up 

def signupadd(username, password):
    connection = sqlite3.connect("internalassessment.db")
    cursor = connection.cursor()

    try: 
        cursor.execute("""
        INSERT INTO users(username, password)
        VALUES (?,?)
        """, (username, password))
        connection.commit()
        return True, "Successfully signed up, please now log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        connection.close()

def loginadd(username, password):
    connection = sqlite3.connect("internalassessment.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, username
        FROM users
        WHERE username = ? and password = ?
        """, (username, password))
    user = cursor.fetchone()
    connection.close()
    if user:
        return True, user[0], user[1]
    else:
        return False, None, None
    
create_database()





    
        



print("data base cooked")

import sqlite3

DATABASE_NAME = "internalassessment.db"


def create_database():
    """
    Creates all tables required by the Spanish Wordle project.
    This function is safe to call every time the program starts because
    CREATE TABLE IF NOT EXISTS does not delete existing data.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        games_played INTEGER NOT NULL DEFAULT 0,
        games_won INTEGER NOT NULL DEFAULT 0
    )
    """)

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
        name TEXT NOT NULL UNIQUE,
        level INTEGER DEFAULT 1,
        games_played INTEGER DEFAULT 0,
        games_won INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        word_id INTEGER,
        won INTEGER NOT NULL,
        guesses_used INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user(id),
        FOREIGN KEY (word_id) REFERENCES words(id)
    )
    """)

    cursor.execcute("""
    CREATE TABLE IF NOT EXISTS mdp_decision (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        game_id INTEGER,
        user_id INTEGER,
        attempts_used INTEGER,
        hints_remaining INTEGER,
        correct_letters INTEGER,
        reward INTEGER,
        action TEXT NOT NULL,
        FOREIGN KEY (game_id) REFERENCES game_results(id)
        FOREIGN KEY (user_id) REFERNCES user(id))
""")

    connection.commit()
    connection.close()


def signupadd(username, password):
    """
    Adds a new user to the users table.
    Returns (True, message) on success and (False, message) on failure.
    """

    if username == "" or password == "":
        return False, "Username and password cannot be empty."

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
        INSERT INTO users(username, password)
        VALUES (?, ?)
        """, (username, password))
        connection.commit()
        return True, "Successfully signed up, please now log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        connection.close()


def loginadd(username, password):
    """
    Checks whether the supplied username/password combination exists.
    Returns (True, user_id, username) if valid, otherwise (False, None, None).
    """
    username = username.strip()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username
        FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()
    connection.close()

    if user:
        return True, user[0], user[1]

    return False, None, None


def create_or_get_player(user_id, username):
    """
    Creates a player record for a logged-in user if one does not already exist.
    The user_id is kept as the player id when possible so game results can
    be connected to the logged-in account.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM players WHERE id = ?", (user_id,))
    player = cursor.fetchone()

    if player is None:
        cursor.execute("""
            INSERT INTO players(id, name)
            VALUES (?, ?)
        """, (user_id, username))
        player_id = user_id
    else:
        player_id = player[0]

    connection.commit()
    connection.close()
    return player_id


def save_game_result(player_id, word_id, won, guesses_used):
    """
    Saves the result of a completed game and updates the player's statistics.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO game_results(player_id, word_id, won, guesses_used)
        VALUES (?, ?, ?, ?)
    """, (player_id, word_id, int(won), guesses_used))

    cursor.execute("""
        UPDATE players
        SET games_played = games_played + 1,
            games_won = games_won + ?
        WHERE id = ?
    """, (int(won), player_id))

#function for saving mdp decisions 

def mdp_decision(game_id, user_id, attempts_used, hints_remaining, correct_letters, reward, action ):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO mdp_decision(game_id, user_id, attempts_used, hints_remaining, correct_letters, reward, action) VALUES (?,?,?,?,?,?,?)
    """, (game_id, user_id, attempts_used, hints_remaining, correct_letters, reward, action))



    connection.commit()
    connection.close()

create_database()

print("Database ready")

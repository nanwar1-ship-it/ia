import sqlite3
import os

from databasesetup import create_database, DATABASE_NAME

# CHANGE:
# WHY:
# The old code used "words.txt" directly.
# Python searched for the file in the current working directory,
# which is the Rumi IB folder, while words.txt is inside the IA folder.
#
# OLD:
# with open("words.txt", "r", encoding="utf-8") as spanish:
#
# NEW:
# Build the path relative to this Python file so the program
# always finds words.txt inside the IA folder.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_FILE = os.path.join(BASE_DIR, "words.txt")

create_database()

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

with open(WORDS_FILE, "r", encoding="utf-8") as spanish:
    # rest of your code...
    imported_count = 0

    for line_number, line in enumerate(spanish, start=1):
        parts = line.strip().split(":")

        if len(parts) != 3:
            print(f"Skipping invalid line {line_number}: {line.strip()}")
            continue

        spanish_word = parts[0].strip()
        translation = parts[1].strip()
        difficulty_text = parts[2].strip()

        if spanish_word == "" or translation == "":
            print(f"Skipping empty word/translation on line {line_number}")
            continue

        # CHANGE 3
        # WHY: difficulty must be stored as an integer because the game searches
        # using difficulty numbers such as 4.
        # OLD:
        #     difficulty = parts[2]
        # NEW:
        try:
            difficulty = int(difficulty_text)
        except ValueError:
            print(f"Skipping invalid difficulty on line {line_number}: {difficulty_text}")
            continue

        cursor.execute("""
            INSERT INTO words (spanish_word, translation, difficulty)
            VALUES (?, ?, ?)
        """, (spanish_word, translation, difficulty))

        imported_count += 1

connection.commit()
connection.close()

print(f"Words imported: {imported_count}")

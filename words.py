import sqlite3

connection = sqlite3.connect("internalassessment.db")
cursor = connection.cursor()

with open("words.txt", "r", encoding = "utf-8") as spanish:
    for line in spanish:
        parts = line.strip().split(":")

        parts = line.split(":")

        if len(parts) == 3:
            spanish_word=parts[0]
            translation = parts[1]
            difficulty = parts[2]

        cursor.execute("""
            INSERT INTO words (spanish_word, translation, difficulty)
            VALUES (?, ?, ?)
            """, (spanish_word, translation, difficulty))

connection.commit()
connection.close()

print("Words imported")

import sqlite3
import re

title = 'WarAndPeace'

with open(f"{title}.txt") as f:
    book = f.read()

connection = sqlite3.connect('/Users/halleypark/PycharmProjects/Word Counter.db')

cursor = connection.cursor()


def create_table():
    #cursor.execute('DROP TABLE IF EXISTS Books')
    cursor.execute('CREATE TABLE Books(Word TEXT NOT NULL, Title TEXT NOT NULL, Count INTEGER, UNIQUE (Word, Title))')


def count(words, title):
    counts = {}
    for w in words:
        w = w.lower()
        if w in counts:
            counts[w] += 1
        else:
            counts[w] = 1
    for key in counts:
        cursor.execute("INSERT INTO Books (Word, Title, Count) VALUES(?, ?, ?)", (key, title, counts[key]))


filtered = re.sub("[.<>?”—/;:'“_!()]", " ", book)
filtered = filtered.replace("--", " ")
filtered = filtered.replace(",", "")
words = filtered.split()
print(set(words))
#create_table()
count(words, title)

connection.commit()
cursor.close()
connection.close()
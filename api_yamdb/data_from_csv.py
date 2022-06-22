import csv
import sqlite3

con = sqlite3.connect('Database.db')
cur = con.cursor()
cur.execute("CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " name TEXT, slug TEXT);")
with open('category.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['id'], i['name'], i['slug']) for i in dr]

cur.executemany("INSERT INTO category (id, name, slug) VALUES (?, ?, ?);",
                to_db)
con.commit()
con.close()

con = sqlite3.connect('Database.db')
cur = con.cursor()
cur.execute("CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " review_id INTEGER, text TEXT, author INTEGER, pub_date TEXT);")

with open('comments.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['id'], i['review_id'], i['text'], i['author'], i['pub_date'])
             for i in dr]

cur.executemany("INSERT INTO comments (id, review_id, text, author, pub_date)"
                "VALUES (?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('Database.db')
cur = con.cursor()
cur.execute("CREATE TABLE genre_title (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " title_id INTEGER, genre_id INTEGER);")

with open('genre_title.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['id'], i['title_id'], i['genre_id']) for i in dr]

cur.executemany("INSERT INTO genre_title (id, title_id, genre_id) VALUES"
                " (?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('Database.db')
cur = con.cursor()
cur.execute("CREATE TABLE genre (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " name TEXT, slug TEXT);")

with open('genre.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['id'], i['name'], i['slug']) for i in dr]

cur.executemany("INSERT INTO genre (id, name, slug) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('Database.db')
cur = con.cursor()
cur.execute("CREATE TABLE review (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title_id INTEGER, text TEXT, author INTEGER, score INTEGER,"
            " pub_date TEXT);")

with open('review.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['id'], i['title_id'], i['text'], i['author'], i['score'],
             i['pub_date']) for i in dr]

cur.executemany("INSERT INTO review (id, title_id, text, author, "
                "score, pub_date) VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('Database.db')
cur = con.cursor()
cur.execute("CREATE TABLE titles (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            " name TEXT, year INTEGER, category INTEGER);")

with open('titles.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['id'], i['name'], i['year'], i['category']) for i in dr]

cur.executemany("INSERT INTO titles (id, name, year, category) VALUES "
                "(?, ?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('Database.db')
cur = con.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "username TEXT, email TEXT, role TEXT, bio TEXT, first_name TEXT, "
            "last_name TEXT);")

with open('users.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=";")
    to_db = [(i['id'], i['username'], i['email'], i['role'], i['bio'],
             i['first_name'], i['last_name']) for i in dr]

cur.executemany("INSERT INTO users (id, username, email, role, bio, "
                "first_name, last_name) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()

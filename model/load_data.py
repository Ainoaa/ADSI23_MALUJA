import hashlib
import sqlite3
import json
from model import Connection


salt = "library"


con = sqlite3.connect("datos.db")
cur = con.cursor()


### Create tables
cur.execute("""
	CREATE TABLE Author(
		id integer primary key AUTOINCREMENT,
		name varchar(40)
	)
""")

cur.execute("""
	CREATE TABLE Book(
		id integer primary key AUTOINCREMENT,
		title varchar(50),
		author integer,
		cover varchar(50),
		description TEXT,
		FOREIGN KEY(author) REFERENCES Author(id)
	)
""")

cur.execute("""
	CREATE TABLE User(
		id integer primary key AUTOINCREMENT,
		name varchar(20),
		email varchar(30),
		password varchar(32),
		admin boolean
	)
""")

cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		user_id integer,
		last_login float,
		FOREIGN KEY(user_id) REFERENCES User(id)
	)
""")

cur.execute("""
	CREATE TABLE Erreseina(
		eraId integer,
		libId integer,
		data Date,
		Nota integer,
		Iruzkina varchar(200),
		PRIMARY KEY (eraId, libId, data)
		FOREIGN KEY(eraId) REFERENCES User(id),
		FOREIGN KEY(libId) REFERENCES Book(id)
	)
""")

cur.execute("""
    CREATE TABLE ForumTopic(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title VARCHAR(255),
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES User(id)
    )
""")

### Insert users

with open('usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
	dataBase_password = user['password'] + salt
	hashed = hashlib.md5(dataBase_password.encode())
	dataBase_password = hashed.hexdigest()
	cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}', {user['admin']})""")
	con.commit()


#### Insert books
with open('libros.tsv', 'r') as f:
	libros = [x.split("\t") for x in f.readlines()]

for author, title, cover, description in libros:
	res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	if res.rowcount == -1:
		cur.execute(f"""INSERT INTO Author VALUES (NULL, \"{author}\")""")
		con.commit()
		res = cur.execute(f"SELECT id FROM Author WHERE name=\"{author}\"")
	author_id = res.fetchone()[0]

	cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
		            (title, author_id, cover, description.strip()))

	con.commit()
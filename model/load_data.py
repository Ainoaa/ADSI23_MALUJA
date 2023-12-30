import hashlib
import sqlite3
import json

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
	CREATE TABLE Lagunak(
		lagun1Id integer,
		lagun2Id integer,
		FOREIGN KEY(lagun1Id) REFERENCES User(id),
		FOREIGN KEY(lagun2Id) REFERENCES User(id)
	)
""")

cur.execute("""
	CREATE TABLE ErreserbenHistoriala(
		userId integer,
		bookId integer,
		FOREIGN KEY(userId) REFERENCES User(id),
		FOREIGN KEY(bookId) REFERENCES Book(id)
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

### Insert lagunak

cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (1, 4))
con.commit()
cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (1, 2))
con.commit()
cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (1, 3))
con.commit()
cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (3, 4))
con.commit()

### Insert Erreserben Historiala

cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (0, 1))
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (0, 2))
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (0, 3))
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (0, 4))
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (1, 1))
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (2, 7))
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (3, 9))
con.commit()
#cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (1, 2))
#con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (1, 3))
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (0, 6))
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (0, 8))
con.commit()







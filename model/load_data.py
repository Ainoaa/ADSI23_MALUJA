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
		author int,
		cover varchar(50), --la ruta o el nombre de archivo de la portada
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
		PRIMARY KEY (eraId, libId, data),
		FOREIGN KEY(eraId) REFERENCES User(id),
		FOREIGN KEY(libId) REFERENCES Book(id)
	)
""")

cur.execute("""
    CREATE TABLE ForumTopic (
        id         INTEGER  PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER,
        username   TEXT,
        title      TEXT,
        content    TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (
            user_id
        )
        REFERENCES User (id) 
    )
""")

cur.execute("""
	CREATE TABLE forum_posts (
        id         INTEGER  PRIMARY KEY AUTOINCREMENT,
        topic_id   INTEGER  REFERENCES ForumTopic (id),
        user_id    INTEGER,
        content    TEXT,
        username   TEXT,
        created_at DATETIME DEFAULT (CURRENT_TIMESTAMP),
        FOREIGN KEY (
            topic_id
        )
        REFERENCES ForumTopic (id),
        FOREIGN KEY (
            user_id
        )
        REFERENCES User (id) 
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



cur.execute("""
	CREATE TABLE Mailegatu(
		eraId integer,
		libId integer,
		hasieraData Date,
		bukaeraData Date Null,
		PRIMARY KEY (eraId, libId, hasieraData),
		FOREIGN KEY(eraId) REFERENCES User(id),
		FOREIGN KEY(libId) REFERENCES Book(id)
	)
""")

cur.execute("""
	CREATE TABLE Eskaerak(
		eskBidali integer,
		eskJaso integer,
		FOREIGN KEY(eskBidali) REFERENCES User(id),
		FOREIGN KEY(eskJaso) REFERENCES User(id)
	)
""")

### Insert users

with open('usuarios.json', 'r') as f:
	usuarios = json.load(f)['usuarios']

for user in usuarios:
    dataBase_password = user['password'] + salt
    hashed = hashlib.md5(dataBase_password.encode())
    dataBase_password = hashed.hexdigest()
    cur.execute(
        f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}', {user['admin']})""")
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

cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (1, 4)) # no tocar
con.commit()
cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (1, 2))# no tocar
con.commit()
cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (1, 3))# no tocar
con.commit()
#cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (3, 4))
con.commit()
cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (3, 1))
con.commit()
#cur.execute("INSERT INTO Lagunak VALUES (?, ?)", (3, 2))
con.commit()
#al usuario con id=4 no le añadáis amigos 		#importante


### Insert Erreserben Historiala

cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (1, 1))# no tocar
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (2, 7))# no tocar
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (3, 9))# no tocar
con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (2, 9))# no tocar
con.commit()
#cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (1, 2))
#con.commit()
cur.execute("INSERT INTO ErreserbenHistoriala VALUES (?, ?)", (1, 3))# no tocar
con.commit()
#al usuario con id=4 no le pongáis que ha leido libros		#importante


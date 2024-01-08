import datetime
from .Connection import Connection
from .tools import hash_password
from model import Book

db = Connection()

class Session:
	def __init__(self, hash, time):
		self.hash = hash
		self.time = time

	def __str__(self):
		return f"{self.hash} ({self.time})"

class User:
	def __init__(self, id, name, email, admin):
		self.id = id
		self.name = name
		self.email = email
		print(admin, type(admin))
		self.admin = admin
		
	def __eq__(self, other):
		return isinstance(other, User) and self.id == other.id

	def __str__(self):
		return f"{self.name} ({self.email})"

	def new_session(self):
		now = float(datetime.datetime.now().time().strftime("%Y%m%d%H%M%S.%f"))
		session_hash = hash_password(str(self.id)+str(now))
		db.insert("INSERT INTO Session VALUES (?, ?, ?)", (session_hash, self.id, now))
		return Session(session_hash, now)

	def validate_session(self, session_hash):
		s = db.select("SELECT * from Session WHERE user_id = ? AND session_hash = ?", (self.id, session_hash))
		if len(s) > 0:
			now = float(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f"))
			session_hash_new = hash_password(str(self.id) + str(now))
			db.update("UPDATE Session SET session_hash = ?, last_login=? WHERE session_hash = ? and user_id = ?", (session_hash_new, now, session_hash, self.id))
			return Session(session_hash_new, now)
		else:
			return None

	def delete_session(self, session_hash):
		db.delete("DELETE FROM Session WHERE session_hash = ? AND user_id = ?", (session_hash, self.id))
	
	def get_books_read(self):
		# Obtener la lista de libros leídos por el usuario desde la base de datos
		books_read = db.select("SELECT book_id FROM UserBooks WHERE user_id = ?", (self.id,))
		return [book[0] for book in books_read]

	def get_book_topics(self, book_id):
		# Obtener los temas del libro desde la base de datos
		topics = db.select("SELECT topic FROM BookTopics WHERE book_id = ?", (book_id,))
		return [topic[0] for topic in topics]

	def get_lagunen_zerrenda(self, name="", email=""):
		lagunak = db.select("SELECT T2.* FROM Lagunak T, User T2 WHERE T.lagun1Id = ? AND T2.id = T.lagun2Id AND T2.name LIKE ? AND T2.email LIKE ?", (self.id,f"%{name}%", f"%{email}%"))
		lagun_zerrenda = list(set(
			User(b[0],b[1],b[2],b[4])
			for b in lagunak
		))
		return lagun_zerrenda

	def __hash__(self):
		return hash(self.id)
	
	def get_irakurritako_liburuak(self, title="", author=""):
		books_read = db.select("SELECT T2.* FROM ErreserbenHistoriala T, Book T2, Author T3 WHERE T.userId = ? AND T2.id = T.bookId AND T2.title LIKE ? AND T2.author = T3.id And T3.name LIKE ? ", (self.id,f"%{title}%", f"%{author}%"))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in books_read
		]
		return books
		
	def get_liburua_irakurri_dutenek(self, ida, name="", email=""):
		usuarios = db.select("SELECT T2.* FROM ErreserbenHistoriala T, User T2 WHERE T.userId = T2.id AND T.bookId = ? AND T2.name LIKE ? AND T2.email LIKE ?", (ida,f"%{name}%", f"%{email}%"))
		user_lista = [
			User(b[0],b[1],b[2],b[4])
			for b in usuarios
			if b[0] != self.id
		]
		return user_lista

	def getLagunak(self):
		lagunak = db.select( "SELECT DISTINCT us.* FROM User us, Lagunak l WHERE (l.lagun1Id = ? AND us.id = l.lagun2Id) OR (l.lagun2Id = ? AND us.id = l.lagun1Id)", (self.id, self.id))
		lagun_zerrenda = [
			User(b[0],b[1],b[2],b[4])
			for b in lagunak
		]
		return lagun_zerrenda

	def getIzena(self):
		return self.name

	def getJasotakoEskaerak(self):
		jaso = db.select("SELECT us.* FROM Eskaerak es, User us WHERE es.eskJaso = ? AND us.id = es.eskBidali", self.id)
		jasoZerrenda = [
			User(b[0],b[1],b[2],b[4])
			for b in jaso
		]
		return jasoZerrenda

	def getBidalitakoEskaerak(self):
		bidali = db.select("SELECT us.* FROM Eskaerak es, User us WHERE es.eskBidali = ? AND us.id = es.eskJaso", self.id)
		bidaliZerrenda = [
			User(b[0], b[1], b[2], b[4])
			for b in bidali
		]
		return bidaliZerrenda

	def eskaeraEzabatu(self, email):
		# Bidalitako eskaera ezabatu
		db.delete("DELETE FROM Eskaerak es, User us WHERE es.eskBidali = ? AND us.email = ? AND us.id = es.eskJaso", self.id, email)

	def eskaeraOnartu(self, email):
		# Jasotako eskaera onartu
		idBestea = db.select("SELECT id FROM User WHERE email = ? ", email)
		db.delete("DELETE FROM Eskaerak WHERE eskBidali = ? AND eskJaso = ?", idBestea, self.id,)
		db.insert("INSERT INTO Lagunak l VALUES ?, ? ", (self.id, idBestea))

	def eskaeraEzeztatu(self, email):
		# Jasotako eskaera ezeztatu
		idBestea = db.select("SELECT id FROM User WHERE email = ? ", email)
		db.delete("DELETE FROM Eskaerak WHERE eskBidali = ? AND eskJaso = ?", idBestea, self.id)

	def lagunaEzabatu(self, email):
		# Lagun bat ezabatu
		idBestea = db.select("SELECT id FROM User WHERE email = ? ", email)
		db.delete("DELETE FROM Lagunal WHERE (lagun1Id = ? AND lagun2Id =?) OR (lagun2Id = ? AND lagun1Id = ?)", self.id, idBestea, idBestea, self.id)

	def gehituEskaera(self, email):
		# Eskaera bidali
		idBestea = db.select("SELECT id FROM User WHERE email = ? ", email)
		db.insert("INSERT INTO Eskaerak VALUES (?, ?) ", self.id, idBestea)

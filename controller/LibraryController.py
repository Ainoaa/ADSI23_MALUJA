from model import Connection, Book, User
from model.tools import hash_password
import datetime 

db = Connection()

class LibraryController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_books(self, title="", author="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count

	def search_people(self, name="", email="", limit=4, page=0):
		count = db.select("""
		    SELECT count()
		    FROM User u
		    WHERE u.name LIKE ? 
		        AND u.email LIKE ? 
		""", (f"%{name}%", f"%{email}%"))[0][0]
		
		res = db.select("""
				SELECT u.*
				FROM Lagunak L, User U
				WHERE L.lagun1Id LIKE ? 
					AND L.Lagun2Id LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{name}%", f"%{email}%", limit, limit * page))

		people = [
		    User(u[0], u[1], u[2], u[4])
		    for u in res
		]
		return people, count

	def get_user(self, email, password):
		user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][4])
		else:
			return None

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][4])
		else:
			return None
			
	def liburua_dago(self, titulua, autorea):
		a = db.select("SELECT * FROM Author WHERE name = ?", (autorea,))
		if len(a)>0:
			autore_id = db.select("SELECT id FROM Author WHERE name = ?", (autorea,))[0][0]
			emaitza = db.select("SELECT * FROM BOOK WHERE title = ? AND author = ?", (titulua, autore_id))
			if len(emaitza)>0:
				return True
			else:
				return False
		else:
			return False
			
	def liburua_gehitu(self, titulua, autorea, azala, deskribapena):
		resultado = db.select("SELECT * FROM Author WHERE name = ?", (autorea,))
		#print(resultado)
		if len(resultado) > 0:
			autoreaa = resultado[0][0]
		#	print(autorea)
		else:
			db.insert("INSERT INTO Author VALUES (NULL, ?)", (autorea,))
			resultado1 = db.select("SELECT id FROM Author WHERE name = ?", (autorea,))
			autoreaa = resultado1[0][0]
		db.insert("INSERT INTO Book VALUES (null, ?, ?, ?, ?)", (titulua, autoreaa, azala, deskribapena))
		b = db.select("SELECT * FROM BOOK WHERE title = ? AND author = ?", (titulua, autoreaa))[0]
		liburua = Book(b[0],b[1],b[2],b[3],b[4])
		return liburua

	def liburua_ezabatu(self, titulua, autorea):
		#print(titulua, autorea)
		autoreId = db.select("SELECT id FROM Author WHERE name = ?", (autorea,))[0][0]
		db.delete("DELETE FROM Book WHERE title = ? AND author = ?", (titulua, autoreId))
		#print (autoreId)
		lista = db.select("SELECT * FROM Book WHERE author = ?", (autoreId,))
		if len(lista) == 0:
			db.delete("DELETE FROM Author WHERE id = ? OR name = ?", (autoreId, autorea))
			
				
	def get_autore_baten_liburuak(self,author,autore="",title=""):
		autorearen_liburuak = db.select("SELECT T.* FROM Book T, Author T2 WHERE T2.name = ? AND T2.id = T.author AND T.title LIKE ? AND T2.name LIKE ?",(author.name,f"%{title}%", f"%{autore}%"))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in autorearen_liburuak
		]
		return books
		
		
		
	def info_liburu(self, bookId):
    		book_info = db.select("SELECT * FROM Book WHERE id = ?", (bookId,))

    		if book_info:
        		return Book(book_info[0][0], book_info[0][1], book_info[0][2], book_info[0][3], book_info[0][4])
    		else:
        		return None
        			
        		
	def erreserbatu(self, bookId, userId):
    		book_info = self.info_liburu(bookId)

    		# Marcar el libro como reservado en la base de datos
    		hasiera_data = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    		db.insert("INSERT INTO Mailegatu (eraId, libId, hasieraData) VALUES (?, ?, ?)", (userId, bookId, hasiera_data))
    		return book_info


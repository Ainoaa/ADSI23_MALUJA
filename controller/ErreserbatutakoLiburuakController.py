from model import Connection

db = Connection()

class ErreserbatutakoLiburuakController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(ErreserbatutakoLiburuakController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance
		
		
	def __init__(self):
        if not self.__initialized:
            self.__initialized = True


	def bueltatu_liburua(self, hasiData, bukatuData, erabId, bookId):
		db.delete("DELETE FROM Mailegatu WHERE hasiData = ? AND bukatuData = ? AND erabId = ? AND bookId = ?", (hasiData, bukatuData, erabId, bookId))


	def erreserbatu_liburua(self, userId, bookId):
        # Verificar si el usuario ya tiene reservado el libro
        erreserbatuta_dauka = db.select("SELECT * FROM Mailegatu WHERE userId = ? AND bookId = ?", (userId, bookId))

        if erreserbatuta_dauka:
            # El usuario ya tiene reservado este libro
            return False
        else:
            # Reservar el libro para el usuario
            db.insert("INSERT INTO Mailegatu (userId, bookId, hasiData) VALUES (?, ?, CURRENT_TIMESTAMP)", (userId, bookId))
            return True
	
	
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
		
		
	def jadaMailegatuZuen(self, eraId, libId):
		zenbakia = db.select("SELECT count(*) FROM Mailegatu M WHERE M.eraId= ? AND M.libId= ? And bukaeraData is not Null", (eraId, libId))
		if zenbakia[0][0] >=1:
			return True
		else:
			return False


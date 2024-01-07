from model import Connection

db = Connection()

class ErreserbatutakoLiburuakController:
    __instance = None
  
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ErreserbatutakoLiburuakController, cls).__new__(cls)
            cls.__instance.__initialized = False
            cls.__instance.libros_reservados = []
        return cls.__instance
        
    def get_liburu_by_id(self, book_id):
        emaitza = db.select("SELECT * FROM Book WHERE id = ?", (book_id,))
        if emaitza:
            book_id, title, author, description, cover = result[0]
            return {
                'id': book_id,
                'title': title,
                'author': author,
                'description': description,
                'cover': cover
            }
        else:
            return None

    def get_user_id(self, userId):
    	user_id = db.select("SELECT userId FROM ErreserbenHistoriala WHERE id = ?", (userId,))[0][0]
    	return user_id


    def get_book_id(self, bookId):
    	book_id = db.select("SELECT bookId FROM ErreserbenHistoriala WHERE bookId = ?", (bookId,))[0][0]
    	return book_id

    	

    def info_liburu_erreserbatuta(self, bookId):
    	book_info = db.select("SELECT * FROM Book WHERE id = ?", (bookId,))

    	if book_info:
        	return Book(book_info[0][0], book_info[0][1], book_info[0][2], book_info[0][3], book_info[0][4])
    	else:
        	return None
        	

    def liburua_bueltatu(self, eraId, libId):
        if self.jada_mailegatuta_dago(eraId, libId):
            db.update("UPDATE Mailegatu SET bukaeraData = CURRENT_TIMESTAMP WHERE eraId = ? AND libId = ? AND bukaeraData IS NULL", (eraId, libId))
            self.libros_reservados.remove(libId)
            return True
        else:
            return False


    def erreserben_historialera_gehitu(self, userId, bookId):
        badago = db.select("SELECT * FROM ErreserbenHistoriala WHERE userId = ? AND bookId = ?", (userId, bookId))

        if not badago:
            db.insert("INSERT INTO ErreserbenHistoriala (userId, bookId) VALUES (?, ?)", (userId, bookId))
            return True
        else:
            return False

    
    def erreserbatu_liburua(self, userId, bookId):
    	booka = db.select("SELECT * FROM Mailegatu")
    
    	for fila in booka:
        	print(fila)
    
    	db.insert("INSERT INTO Mailegatu (eraId, libId, hasieraData) VALUES (?, ?, CURRENT_TIMESTAMP)", (userId, bookId))
    	self.libros_reservados.append(bookId)



    def jada_mailegatuta_dago(self, eraId, libId):
        num = db.select("SELECT count(*) FROM Mailegatu M WHERE M.eraId = ? AND M.libId = ? AND bukaeraData IS NULL", (eraId, libId))

        return num[0][0] >= 1
        

    def jadaMailegatuZuen(self, eraId, libId):
        zenbakia = db.select("SELECT count(*) FROM Mailegatu M WHERE M.eraId= ? AND M.libId= ? And bukaeraData is not Null", (eraId, libId))
        
        
        if zenbakia[0][0] >= 1:
            return True
        else:
            return False
         
         

    def get_liburu_erreserbatuak(self, user):
    	reserved_books = db.select("""
    	    SELECT T.* 
    	    FROM Book T, Mailegatu T2
    	    WHERE T2.libId = T.id AND T2.eraId = ?
    	""", (user.id,))
    	
    	books = [
    	    Book(b[0],b[1],b[2],b[3],b[4])
    	    for b in reserved_books
    	]
    	
    	for book in books:
    	    print(book.title)
    	    
    	return books




    def liburua_dago(self, titulua, autorea):
        autore_id = db.select("SELECT id FROM Author WHERE name = ?", (autorea,))
    
        if autore_id:
            autore_id = autore_id[0][0]
            emaitza = db.select("SELECT * FROM BOOK WHERE title = ? AND author = ?", (titulua, autore_id))
            return len(emaitza) > 0

        return False
        
        
        
        
##################### ERLAZIOAK EZABATZEKO ######################


    def erreseinakEzabatu(self, libId):
    	db.delete("DELETE FROM Erreseina WHERE libID = ?", (libId,))

    def erreserbenHistorialaEzabatu(self, libId):
        db.delete("DELETE FROM ErreserbenHistoriala WHERE bookId = ?", (libId,))

    def mailegatuakEzabatu(self, libId):
        db.delete("DELETE FROM Mailegatu WHERE libId = ?", (libId,))

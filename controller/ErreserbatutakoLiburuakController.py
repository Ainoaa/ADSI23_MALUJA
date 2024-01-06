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
        # Verificar si el usuario ya ha tenido reservado el libro
        if self.jada_mailegatuta_dago(eraId, libId):
            # Actualizar la fecha de finalización para indicar que el libro ha sido devuelto
            db.update("UPDATE Mailegatu SET bukaeraData = CURRENT_TIMESTAMP WHERE eraId = ? AND libId = ? AND bukaeraData IS NULL", (eraId, libId))
            # Eliminar el libro de la lista de libros reservados
            self.libros_reservados.remove(libId)
            return True
        else:
            return False


    def erreserben_historialera_gehitu(self, userId, bookId):
        # Verificar si ya existe una entrada para este libro y usuario en el historial
        badago = db.select("SELECT * FROM ErreserbenHistoriala WHERE userId = ? AND bookId = ?", (userId, bookId))

        if not badago:
            # Si no existe, agregar una nueva entrada al historial
            db.insert("INSERT INTO ErreserbenHistoriala (userId, bookId) VALUES (?, ?)", (userId, bookId))
            return True
        else:
            # Ya existe una entrada para este libro y usuario
            return False

    
    def erreserbatu_liburua(self, userId, bookId):
        # Reservar el libro para el usuario
        db.insert("INSERT INTO Mailegatu (eraId, libId, hasiData) VALUES (?, ?, CURRENT_TIMESTAMP)", (userId, bookId))
        # Agregar el libro a la lista de libros reservados
        self.libros_reservados.append(bookId)


    def jada_mailegatuta_dago(self, eraId, libId):
        # Verificar si el usuario ya tiene reservado el libro
        num = db.select("SELECT count(*) FROM Mailegatu M WHERE M.eraId = ? AND M.libId = ? AND bukaeraData IS NULL", (eraId, libId))
        
        # Si el recuento es mayor o igual a 1, significa que el libro ya está reservado
        return num[0][0] >= 1
        

    def jadaMailegatuZuen(self, eraId, libId):
        # Verificar si el usuario ya ha tenido reservado el libro
        zenbakia = db.select("SELECT count(*) FROM Mailegatu M WHERE M.eraId= ? AND M.libId= ? And bukaeraData is not Null", (eraId, libId))
        
        
        if zenbakia[0][0] >= 1:
            return True
        else:
            return False
         
         

    def get_liburu_erreserbatuak(self):
    	self.libros_reservados = []  
    
    	lista = db.select("SELECT * FROM ErreserbenHistoriala")
    	for row in lista:
            user_id, book_id = row
            libro = self.get_book_id(book_id)    
            if libro:
                self.libros_reservados.append(libro)

    	return self.libros_reservados




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

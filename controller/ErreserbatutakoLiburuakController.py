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


    def liburua_bueltatu(self, eraId, libId):
        # Verificar si el usuario ya ha tenido reservado el libro
        if self.jada_mailegatuta_dago(eraId, libId):
            # Actualizar la fecha de finalización para indicar que el libro ha sido devuelto
            db.update("UPDATE Mailegatu SET bukaeraData = CURRENT_TIMESTAMP WHERE eraId = ? AND libId = ? AND bukaeraData IS NULL", (eraId, libId))
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
        # Verificar si el usuario ya tiene reservado el libro
        erreserbatuta_dauka = db.select("SELECT * FROM Mailegatu WHERE eraId = ? AND libId = ?", (userId, bookId))

        if erreserbatuta_dauka:
            # El usuario ya tiene reservado este libro
            return False
        else:
            # Reservar el libro para el usuario
            db.insert("INSERT INTO Mailegatu (eraId, libId, hasiData) VALUES (?, ?, CURRENT_TIMESTAMP)", (userId, bookId))
            # Agregar el libro a la lista de libros reservados
            self.libros_reservados.append(bookId)
            return True


    def get_liburu_erreserbatuak(self):
    	katalogo_erreserbatuak = db.select("SELECT * FROM Book WHERE id IN (?)", (",".join(map(str, self.libros_reservados)),))
    	return katalogo_erreserbatuak


    def jada_mailegatuta_dago(self, eraId, libId):
        # Verificar si el usuario ya ha tenido reservado el libro
        count_result = db.select("SELECT count(*) FROM Mailegatu M WHERE M.eraId = ? AND M.libId = ? AND bukaeraData IS NULL", (eraId, libId))
        
        # Si el recuento es mayor o igual a 1, significa que el libro ya está reservado
        return count_result[0][0] >= 1
        

    def jadaMailegatuZuen(self, eraId, libId):
    	# Verificar si el usuario ya ha tenido reservado el libro
        zenbakia = db.select("SELECT count(*) FROM Mailegatu M WHERE M.eraId= ? AND M.libId= ? And bukaeraData is not Null", (eraId, libId))
        
        
        if zenbakia[0][0] >= 1:
            return True
        else:
            return False
            

    def liburua_dago(self, titulua, autorea):
    	autore_id = db.select("SELECT id FROM Author WHERE name = ?", (autorea,))
    
    	if autore_id:
        	autore_id = autore_id[0][0]
        	emaitza = db.select("SELECT * FROM BOOK WHERE title = ? AND author = ?", (titulua, autore_id))
        	return len(emaitza) > 0

    	return False

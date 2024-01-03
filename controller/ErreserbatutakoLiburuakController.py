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


    def bueltatu_liburua(self, hasiData, bukatuData, erabId, bookId):
        db.delete("DELETE FROM Mailegatu WHERE hasiData = ? AND bukatuData = ? AND erabId = ? AND bookId = ?", (hasiData, bukatuData, erabId, bookId))



    def erreserbatu_liburua(self, userId, bookId):
        # Verificar si el usuario ya tiene reservado el libro
        erreserbatuta_dauka = db.select("SELECT * FROM Mailegatu WHERE eraId = ? AND libId = ?", (userId, bookId))

        if erreserbatuta_dauka:
            # El usuario ya tiene reservado este libro
            return False
        else:
            # Reservar el libro para el usuario
            db.insert("INSERT INTO Mailegatu (eraId, libId, hasiData) VALUES (?, ?, CURRENT_TIMESTAMP)", (userId, bookId))
            return True


    def add_liburu_erreserbatua(self, bookId):
        self.libros_reservados.append(bookId)


    def get_liburu_erreserbatuak(self, title="", author=""):
    	# Utiliza los parámetros title y author en la consulta SQL
    	kontsulta = """
        	SELECT b.*
        	FROM Mailegatu M
        	INNER JOIN Book b ON M.libId = b.id
        	WHERE M.bukaeraData IS NULL
    	"""
    
    	if title:
        	kontsulta += " AND b.title LIKE ?"
    	if author:
        	kontsulta += " AND b.author LIKE ?"

    	# Usa los parámetros de búsqueda en la consulta
    	params = ()
    	if title:
        	params += (f"%{title}%",)
    	if author:
        	params += (f"%{author}%",)

        #Ejecuta la consulta y retorna la lista de libros reservados
    	lista = db.select(kontsulta, params)
    	return lista
    

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

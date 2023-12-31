from model import Connection

db = Connection()

class ErreserbatutakoLiburuakController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(ErreserbatutakoLiburuakController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance

	def bueltatu_liburua(self, hasiData, bukatuData, erabId, bookId):
		db.delete("DELETE FROM Mailegatu WHERE hasiData = ? AND bukatuData = ? AND erabId = ? AND bookId = ?", (hasiData, bukatuData, erabId, bookId))

	def erreserbatu_liburua(self, erabId, bookId, data):
		db = tools.hash_password(pasahitza)
		if admin == "true":
			admin_balioa = 1
		else:
			admin_balioa = 0
		db.insert("INSERT INTO Mailegatu VALUES (NULL, ?, ?, ?, ?)", (izena, emaila, hp, admin_balioa))
	
	
	
	
	
	def jadaMailegatuZuen(self, eraId, libId):
		zenbakia = db.select("SELECT count(*) FROM Mailegatu M WHERE M.eraId= ? AND M.libId= ? And bukaeraData is not Null", (eraId, libId))
		if zenbakia[0][0] >=1:
			return True
		else:
			return False


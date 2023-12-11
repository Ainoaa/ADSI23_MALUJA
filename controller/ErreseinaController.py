from model import Connection, Erreseina
from model.tools import hash_password

db = Connection()

class ErreseinaController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(ErreseinaController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance

	def erreseinaSortu(self, eraId, libId, data, nota, iruzkina):
		db.insert("INSERT INTO ERRESEINA VALUES(?, ?, ?, ?, ?)", (eraId, libId, data, nota, iruzkina))
		erreseina = Erreseina(eraId, libId, data, nota, iruzkina);
		self.lista.append(erreseina)
		
	def jadaErreseinaZuen(self, eraId, libId):
		emaitza = db.select("SELECT * FROM ERRESEINA WHERE eraID = ? AND libId = ?", (eraId, libId))
		if emaitza:
			return True
		else:
			return False
			
	def erreseinaEditatudef(self, eraId, libId, data, nota, iruzkina):
		db.update("UPDATE ERRESEINA SET data = ?, nota = ?, iruzkina = ? WHERE eraId = ? AND libId = ?", (data, nota, iruzkina, eraId, libId))
		erreseina = next((item for item in self.lista if item.geteraId() == eraId and item.getlibId() == libId), None)
		if erreseina:
			erreseina.erreseinaEditatu(eraId, libId, data, nota, iruzkina)
		else:
			print("Ez da erreseina aurkitu")
			
			

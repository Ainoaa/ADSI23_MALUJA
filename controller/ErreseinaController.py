from model import Connection, Erreseina
from model.tools import hash_password

db = Connection()

class ErreseinaController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(ErreseinaController, cls).__new__(cls)
			cls.__instance.__initialized = False
			cls.__instance.lista = []
		return cls.__instance

	def gehituErreseina(self, erreseina):
		self.lista.append(erreseina)
		
		
	def erreseinaSortu(self, eraId, libId, data, nota, iruzkina):
		db.insert("INSERT INTO ERRESEINA VALUES(?, ?, ?, ?, ?)", (eraId, libId, data, nota, iruzkina))
		erreseina = Erreseina(eraId, libId, data, nota, iruzkina)
		gehituErreseina(erreseina)
		
		
	def jadaErreseinaZuen(self, eraId, libId, data):
		emaitza = db.select("SELECT count(*) FROM ERRESEINA WHERE eraID = ? AND libId = ? AND data = ?", (eraId, libId, data))
		if emaitza >=1:
			return True
		else:
			return False
			
	def erreseinaEditatu(self, eraId, libId, lehenData, nota, iruzkina, orainData):
		db.update("UPDATE ERRESEINA SET data = ?, nota = ?, iruzkina = ? WHERE eraId = ? AND libId = ? AND data = ?", (orainData, nota, iruzkina, eraId, libId, lehenData))
		erreseina = bilatuErreseina(eraId, libId, lehenData)
		if erreseina:
			erreseina.erreseinaEditatu(orainData, nota, iruzkina)
		else:
			print("Ez da erreseina aurkitu")
			
			
	def bilatuErreseina(self, eraId, libId, lehenData):
		erreseina = next((item for item in self.lista if item.getEraId() == eraId and item.getLibId() == libId and item.getData() == lehenData), None)
		return erreseina
			
			

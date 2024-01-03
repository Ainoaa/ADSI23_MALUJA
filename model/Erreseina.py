from .Connection import Connection

db = Connection()

class Erreseina:
	def __init__(self, eraId, libId, data, nota, iruzkina):
		self.eraId = eraId
		self.libId = libId
		self.data = data
		self.nota = nota
		self.iruzkina = iruzkina
		
	def __str__(self):
		return f"{self.eraId} {self.libId} {self.data} {self.nota} {self.iruzkina} "
		
		
	def erreseinaEditatu(self, orainData, nota, iruzkina):
		self.data = orainData
		self.nota = nota
		self.iruzkina = iruzkina
		
	def getEraId(self):
		return self.eraId
		
	def getLibId(self):
		return self.libId
		
	def getData(self):
		return self.data
		

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
		return f"{self.id} {self.iruzkina} {self.nota} {self.data}"
		
		
	def erreseinaEditatu(self, orainData, nota, iruzkina):
		self.data = orainData
		self.nota = nota
		self.iruzkina = iruzkina
		
	def getEraId():
		return self.eraId
		
	def getLibId():
		return self.libId
		
	def getData():
		return self.data
		

from .Connection import Connection

db = Connection()

class Erreseina:
	def __init__(self, eraId, libId, data, nota, iruzkin):
		self.eraId = eraId
		self.libId = libId
		self.data = data
		self.nota = nota
		self.iruzkin = iruzkin
		
	def __str__(self):
		return f"{self.id} {self.iruzkin} {self.nota} {self.data}"
		
		
	def erreseinaEditatu(self, eraId, libId, data, nota, iruzkin):
		self.eraId = eraId
		self.libId = libId
		self.data = data
		self.nota = nota
		self.iruzkin = iruzkin
		
	def getEraId():
		return self.eraId
		
	def getlibId():
		return self.libId
		

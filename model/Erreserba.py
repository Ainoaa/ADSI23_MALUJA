from .Connection import Connection

db = Connection()

class Erreserba:
	def __init__(self, eraId, libId, hasieraData, bukaeraData):
		self.eraId = eraId
		self.libId = libId
		self.hasieraData = hasieraData
		self.bukaeraData = bukaeraData
		
	def __str__(self):
		return f"{self.eraId} {self.libId} {self.hasieraData} {self.bukaeraData} "
		
		
	def getEraId(self):
		return self.eraId
		
	def getLibId(self):
		return self.libId
		
	def getHasieraData(self):
		return self.hasieraData
		
	def getBukaeraData(self):
		return self.bukaeraData

from model import Connection

db = Connection()

class ErreserbatutakoLiburuakController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(ErreserbatutakoLiburuakController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance

	def bueltatu_liburua(self, izena, idazlea, data):


	def erreserbatu_liburua(self, izzena, idazlea, data):


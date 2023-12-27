from model import Connection

db = Connection()

class ErabiltzaileController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(ErabiltzaileController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance	

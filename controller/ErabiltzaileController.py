from model import Connection

db = Connection()

class ErabiltzaileController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(ErabiltzaileController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance	
		
	def erabiltzailea_gehitu(self, izena, emaila, pasahitza, admin):
		hp = tools.hash_password(pasahitza)
		if admin == "true":
			admin_balioa = 1
		else:
			admin_balioa = 0
		db.insert("INSERT INTO User VALUES (NULL, ?, ?, ?, ?)", (izena, emaila, hp, admin_balioa))
		#e = db.select("SELECT * FROM User WHERE name = ? AND email = ?", (izena, emaila))[0]
		#erabiltzailea = User (e[0],e[1],e[2],e[3]),e[4])
		#return erabiltzailea

	def erabiltzailea_ezabatu(self, izena, emaila):
		db.delete("DELETE FROM User WHERE name = ? AND email = ?", (izena, emaila))

	def erabiltzailea_dago(self, emaila):
		e = db.select("SELECT * FROM User WHERE email = ?", (emaila,))
		return len(e)>0

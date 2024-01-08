from model import Connection, User
from model import tools
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
		e = db.select("SELECT * FROM User WHERE name = ? AND email = ?", (izena, emaila))[0]
		erabiltzailea = User(e[0],e[1],e[2],e[3])
		return erabiltzailea

	def erabiltzailea_ezabatu(self, eraId):
		e = db.select("SELECT * FROM User WHERE id = ?", (eraId,))[0]
		erabiltzailea = User(e[0],e[1],e[2],e[3])
		db.delete("DELETE FROM User WHERE id = ?", (eraId,))
		return erabiltzailea

	def erabiltzailea_dago(self, emaila):
		e = db.select("SELECT * FROM User WHERE email = ?", (emaila,))
		return len(e)>0

	def lagunakBilatu(self, id):
		lagunak = db.select("SELECT DISTINCT us.* FROM User us, Lagunak l WHERE (l.lagun1Id = ? AND us.id = l.lagun2Id) OR (l.lagun2Id = ? AND us.id = l.lagun1Id)", (id, id))
		return lagunak

	def eskaeraOnartu(self, idB, idJ):
		db.delete("DELETE FROM Eskaerak WHERE idBidali = ? AND idJaso = ?", (idB, idJ))
		db.insert("INSERT INTO Lagunak(lagun1Id, lagun2Id) VALUES (?,?)", (idB, idJ))

	def eskaeraEzeztatu(self, idB, idJ):
		db.delete("DELETE FROM Eskaerak WHERE idBidali = ? AND idJaso = ?", (idB, idJ))

	def lagunaEzabatu(self, idN, idL):
		db.delete("DELETE FROM Lagunak WHERE (lagun1Id = ? AND lagun2Id = ?) OR (lagun1Id = ? AND lagun2Id = ?)", (idN, idL, idL, idN))

	def get_erabiltzaileId(self, izena, emaila):
		eraId = db.select("SELECT id FROM User WHERE name = ? AND email = ?", (izena, emaila))[0][0]
		return eraId
##################### ERLAZIOAK EZABATZEKO ######################
	def lagunakEzabatu(self, eraId):
		db.delete("DELETE FROM Lagunak WHERE lagun1Id = ? OR lagun2Id = ?", (eraId, eraId))
	def erreseinakEzabatu(self, eraId):
		db.delete("DELETE FROM Erreseina WHERE eraId = ?", (eraId,))
	def forumTopicEzabatu(self, eraId):
		db.delete("DELETE FROM ForumTopic WHERE user_id = ?", (eraId,))
	def forum_posts_ezabatu(self, eraId):
		db.delete("DELETE FROM forum_posts WHERE user_id = ?", (eraId,))
	def erreserbenHistorialaEzabatu(self, eraId):
		db.delete("DELETE FROM ErreserbenHIstoriala WHERE userid = ?", (eraId,))
	def mailegatuakEzabatu(self, eraId):
		db.delete("DELETE FROM Mailegatu WHERE eraId = ?", (eraId,))

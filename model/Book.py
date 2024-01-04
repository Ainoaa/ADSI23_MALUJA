from .Connection import Connection
from .Author import Author

db = Connection()

class Book:
	def __init__(self, id, title, author, cover, description):
		self.id = id
		self.title = title
		self.author = author
		self.cover = cover
		self.description = description

	@property
	def author(self):
	    if isinstance(self._author, int):
	        result = db.select("SELECT * FROM Author WHERE id=?", (self._author,))
	        if result:
	            em = result[0]
	            self._author = Author(em[0], em[1])
	        else:
	            self._author = None  # O puedes asignar cualquier otro valor por defecto
	    return self._author


	@author.setter
	def author(self, value):
		self._author = value

	def __str__(self):
		return f"{self.title} ({self.author})"
	
	def __eq__(self,obj):
		if type(obj) != type(self):
			return False
		return self.id == obj.id

	def __neq__(self,obj):
		if type(obj) != type(self):
			return True
		return self.id != obj.id

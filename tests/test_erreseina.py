	
from . import BaseTestClass
from bs4 import BeautifulSoup
from model import Connection
from controller.ErreseinaController import ErreseinaController

erreseinak = ErreseinaController()
db = Connection()

class TestErreseina(BaseTestClass):

	@classmethod
	def setUpClass(cls):
		db.insert("Insert into Mailegatu (eraId, libId, hasieraData, bukaeraData) Values (?, ?, ?, ?)", (1, 1, "2023/04/10", "2023/04/12"))
		db.insert("Insert into Mailegatu (eraId, libId, hasieraData, bukaeraData) Values (?, ?, ?, ?)", (1, 2, "2023/04/10", "2023/04/12"))
		db.insert("Insert into Erreseina (eraId, libId, data, nota, iruzkina) Values (?, ?, ?, ?, ?)", (1, 1, "2023-08-10 19:13:12", 5, "Oso ona: Test"))
		eraId = 1
		libId = 2
		nota = 4
		erreseinak.erreseinaSortu(eraId, libId, "2023-08-15 15:13:12", nota, "Oso ona: Test")
	
	def test_erreseina_sortzeko_leihoa_agertzea_mailegatu_gabe(self):
		params = {
			'eraId' : 2,
			'libId' : 2
		}
		res = self.client.get('/erreseina_sortu', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina sortzerakoan/editatzerakoan errore bat gertatu da!!", title_tag.text)
	
	def test_erreseina_sortzeko_leihoa_agertzea_mailegatuta(self):
		params = {
			'eraId' : 1,
			'libId' : 1
		}
		res = self.client.get('/erreseina_sortu', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina", title_tag.text)
	
		
	def test_erreseina_gorde_mailegatu_gabe(self):
		params = {
			'eraId' : 2,
			'libId' : 2,
			'data' : "2023-09-10 15:13:12",
			'nota' : 4,
			'iruzkina' : "Ona: Test"
		}
		res = self.client.get('/erreseina_sortuta', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina sortzerakoan/editatzerakoan errore bat gertatu da!!", title_tag.text)
		zenbat = db.select("Select count(*) From Erreseina Where eraId = ? And libId = ? And data = ? And nota = ? And iruzkina = ?", (2, 2, "2023-09-10 15:13:12", 4, "Ona: Test"))
		self.assertEqual(0, zenbat[0][0])
		
	def test_erreseina_gorde_mailegatuta(self):
		params = {
			'eraId' : 1,
			'libId' : 1,
			'data' : "2023-09-10 15:13:12",
			'nota' : 4,
			'iruzkina' : "Ona: Test"
		}
		res = self.client.get('/erreseina_sortuta', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina modu egoki batean sortu/editatu da!!", title_tag.text)
		zenbat = db.select("Select count(*) From Erreseina Where eraId = ? And libId = ? And data = ? And nota = ? And iruzkina = ?", (1, 1, "2023-09-10 15:13:12", 4, "Ona: Test"))
		self.assertEqual(1, zenbat[0][0])
	
	def test_erreseina_editatzeko_leihoa_agertzea_mailegatu_gabe(self):
		params = {
			'eraId' : 2,
			'libId' : 2,
			'data' : "2023-09-09 15:10:10",
			'nota' : 2,
			'iruzkina' : "Txarra: Test"
		}
		res = self.client.get('/erreseina_editatu', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina sortzerakoan/editatzerakoan errore bat gertatu da!!", title_tag.text)
		
	def test_erreseina_editatzeko_leihoa_agertzea_mailegatuta_baina_erreseina_sortu_gabe(self):
		params = {
			'eraId' : 1,
			'libId' : 2,
			'data' : "2023-09-09 15:10:10",
			'nota' : 2,
			'iruzkina' : "Txarra: Test"
		}
		res = self.client.get('/erreseina_editatu', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina sortzerakoan/editatzerakoan errore bat gertatu da!!", title_tag.text)
		
	
	def test_erreseina_editatzeko_leihoa_agertzea_mailegatuta_eta_erreseina_sortuta(self):
		params = {
			'eraId' : 1,
			'libId' : 1,
			'data' : "2023-08-10 19:13:12",
			'nota' : 5,
			'iruzkina' : "Oso ona: Test"
		}
		res = self.client.get('/erreseina_editatu', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina", title_tag.text)

	
	def test_erreseina_editatu_klikatu_mailegatu_gabe(self):
		params = {
			'eraId' : 2,
			'libId' : 2,
			'data' : "2023-09-09 15:10:10",
			'nota' : 2,
			'iruzkina' : "Txarra: Test"
		}
		res = self.client.get('/erreseina_editatuta', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina sortzerakoan/editatzerakoan errore bat gertatu da!!", title_tag.text)
		zenbat = db.select("Select count(*) From Erreseina Where eraId = ? And libId = ? And nota = ? And iruzkina = ?", (2, 2, 2, "Txarra: Test"))
		self.assertEqual(0, zenbat[0][0])
	
	def test_erreseina_editatu_klikatu_mailegatuta_baina_erreseina_sortu_gabe(self):
		params = {
			'eraId' : 1,
			'libId' : 2,
			'data' : "2023-09-09 15:10:10",
			'nota' : 2,
			'iruzkina' : "Txarra: Test"
		}
		res = self.client.get('/erreseina_editatuta', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina sortzerakoan/editatzerakoan errore bat gertatu da!!", title_tag.text)
		zenbat = db.select("Select count(*) From Erreseina Where eraId = ? And libId = ? And nota = ? And iruzkina = ?", (1, 2, 2, "Txarra: Test"))
		self.assertEqual(0, zenbat[0][0])
	
	def test_erreseina_editatu_klikatu_mailegatuta_eta_erreseina_sortuta(self):
		params = {
			'eraId' : 1,
			'libId' : 2,
			'data' : "2023-08-15 15:13:12",
			'nota' : 3,
			'iruzkina' : "Oso ona: Test2"
		}
		zenbat1 = db.select("Select count(*) From Erreseina Where eraId = ? And libId = ? And nota = ? And iruzkina = ?", (1, 2, 3, "Oso ona: Test2"))
		res = self.client.get('/erreseina_editatuta', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, 'html.parser')
		title_tag = soup.find('h1')
		self.assertEqual("Erreseina modu egoki batean sortu/editatu da!!", title_tag.text)
		zenbat2 = db.select("Select count(*) From Erreseina Where eraId = ? And libId = ? And nota = ? And iruzkina = ?", (1, 2, 3, "Oso ona: Test2"))
		self.assertEqual(zenbat1[0][0]+1, zenbat2[0][0])

	

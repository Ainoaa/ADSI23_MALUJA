from . import BaseTestClass
from bs4 import BeautifulSoup
from controller.ErreseinaController import ErreseinaController

erreseinak = ErreseinaController()

class TestLibErreseinaKatalogoa(BaseTestClass):

	@classmethod
	def setUpClass(cls):
		eraId = 1
		libId = 9
		nota = 5
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-10 19:13:12", nota, "Oso ona--> Test")
		nota = 4
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-11 19:13:12", nota, "Oso--> Test")
		nota = 3
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-12 19:13:12", nota, "Kili kolo--> Test")
		eraId = 2
		libId = 5
		nota = 3
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-07 19:13:12", nota, "Kili kolo--> Test")
		eraId = 1
		nota = 5
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-09 19:13:12", nota, "Oso ona--> Test")
		nota = 4
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-22 19:13:12", nota, "Oso--> Test")
		nota = 3
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-26 19:13:12", nota, "Kili kolo--> Test")
	
	def test_zero_erreseinako_liburua(self):
		params = {
				'eraId' : 2,
				'libId' : 8
			}
		res = self.client.get('/liburuko_erreseina_katalogoa', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		title_tag = soup.find('h1')
		self.assertEqual("Erreseinen Lista", title_tag.text)
		items = soup.find_all('li')
		self.assertEqual(4, len(items))	#Gutxienez, beti 4 liv egongo dira
		
	
	def test_bakarrik_pertsona_bateko_erreseinak_daukan_liburua(self):
		params = {
				'eraId' : 1,
				'libId' : 9
			}
		res = self.client.get('/liburuko_erreseina_katalogoa', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		title_tag = soup.find('h1')
		self.assertEqual("Erreseinen Lista", title_tag.text)
		items = soup.find_all('li')
		self.assertEqual(7, len(items))
	
	def test_pertsona_askoko_erreseinak_dauzkan_liburua(self):
		params = {
				'eraId' : 1,
				'libId' : 5
			}
		res = self.client.get('/liburuko_erreseina_katalogoa', query_string = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		title_tag = soup.find('h1')
		self.assertEqual("Erreseinen Lista", title_tag.text)
		items = soup.find_all('li')
		self.assertEqual(8, len(items))

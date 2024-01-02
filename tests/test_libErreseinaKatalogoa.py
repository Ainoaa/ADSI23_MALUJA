from . import BaseTestClass
from bs4 import BeautifulSoup
from controller.ErreseinaController import ErreseinaController

erreseinak = ErreseinaController()

class TestLibErreseinaKatalogoa(BaseTestClass):

	@classmethod
	def setUpClass(cls):
		eraId = 1
		libId = 1
		nota = 5
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-10 19:13:12", nota, "Oso ona--> Test")
		nota = 4
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-11 19:13:12", nota, "Oso--> Test")
		nota = 3
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-12 19:13:12", nota, "Kili kolo--> Test")
	
	def test_zero_erreseinako_liburua(self):
		params = {
				'eraId' : 2,
				'libId' : 2
			}
		res = self.client.get('/liburuko_erreseina_katalogoa', data = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		items = soup.find_all('li')
		self.assertEqual(0, len(items))
		
	
	def test_bakarrik_pertsona_bateko_erreseinak_daukan_liburua(self):
		params = {
				'eraId' : 1,
				'libId' : 1
			}
		res = self.client.get('/liburuko_erreseina_katalogoa', data = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		items = soup.find_all('li')
		self.assertEqual(3, len(items))
	
	def test_pertsona_askoko_erreseinak_dauzkan_liburua(self):
		eraId = 2
		libId = 1
		nota = 3
		erreseinak.erreseinaSortu(eraId, libId, "2023-09-12 19:13:12", nota, "Kili kolo--> Test")
		params = {
				'eraId' : "1",
				'libId' : "1"
			}
		res = self.client.get('/liburuko_erreseina_katalogoa', data = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		items = soup.find_all('li')
		self.assertEqual(4, len(items))

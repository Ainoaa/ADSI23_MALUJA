from . import BaseTestClass
from bs4 import BeautifulSoup
from controller.ErreseinaController import ErreseinaController

erreseinak = ErreseinaController()

class TestLibErreseinaKatalogoa(BaseTestClass):

	@classmethod
	def setUpClass(cls):
		erreseinak.erreseinaSortu("1", "1", "2023-09-10 19:13:12", "5", "Oso ona--> Test")
		erreseinak.erreseinaSortu("1", "1", "2023-09-11 19:13:12", "4", "Oso--> Test")
		erreseinak.erreseinaSortu("1", "1", "2023-09-12 19:13:12", "3", "Kili kolo--> Test")
	
	def test_zero_erreseinako_liburua(self):
		params = {
				'eraId' : "2",
				'libId' : "2"
			}
		res = self.client.post('/liburuko_erreseina_katalogoa', data = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		items = soup.find_all('li')
		self.assertEqual(0, len(items))
		
	
	def test_bakarrik_pertsona_bateko_erreseinak_daukan_liburua(self):
		params = {
				'eraId' : "1",
				'libId' : "1"
			}
		res = self.client.post('/liburuko_erreseina_katalogoa', data = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		items = soup.find_all('li')
		self.assertEqual(3, len(items))
	
	def test_pertsona_askoko_erreseinak_dauzkan_liburua(self):
		erreseinak.erreseinaSortu("2", "1", "2023-09-12 19:13:12", "3", "Kili kolo--> Test")
		params = {
				'eraId' : "1",
				'libId' : "1"
			}
		res = self.client.post('/liburuko_erreseina_katalogoa', data = params)
		self.assertEqual(200, res.status_code)
		soup = BeautifulSoup(res.data, features="html.parser")
		items = soup.find_all('li')
		self.assertEqual(4, len(items))

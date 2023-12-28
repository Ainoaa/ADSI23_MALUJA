from . import BaseTestClass
from bs4 import BeautifulSoup

class TestErreseina(BaseTestClass):
	
	def test_erreseina_bat_gehitu_mailegatu_gabe(self):
		params = {
			'eraId' : "1"
			'libId' : "1"
			'data' : "2023-09-10 15:13:12"
		}
		res = self.client.get('e/rreseina_idatzi', query_string = params)
		self.assertEqual(200, res.status_code)
	
	
	def test_erreseina_bat_gehitu_mailegatuta(self):
	
	
	
	def test_erreseina_bat_editatu_jada_erreseina_sortuta(self):
	
	
	
	def test_erreseina_bat_editatu_erreseina_sortu_gabe(self):

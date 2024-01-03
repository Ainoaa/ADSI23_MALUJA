from . import BaseTestClass
from bs4 import BeautifulSoup

class TestLagunenGomendioak(BaseTestClass):
	
	def test_redirect(self):
		res = self.client.get('/LagunenGomendioak')
		self.assertEqual(302, res.status_code)
		self.assertEqual('/', res.location)

	def test_sartu_ondo(self):
		self.login('ejemplo@gmail.com', '123456')
		res = self.client.get('/LagunenGomendioak')
		self.assertEqual(200, res.status_code)
		
	def test_izandako_gomendioak_lagunen_arabera_lagunik_izan_gabe(self):
		self.login('ejemplo2@gmail.com', '123456')
		res = self.client.get('/LagunenGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		lagunen_lagunak = page.find_all('div', {'class': 'card', 'data-section': 'Zure lagunen lagunak'})
		self.assertEqual(len(lagunen_lagunak), 0)
		
	def test_izandako_gomendioak_lagunen_arabera_lagunak_izaten(self):
		self.login('ejemplo@gmail.com', '123456')
		res = self.client.get('/LagunenGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		lagunen_lagunak = page.find_all('div', {'class': 'card', 'data-section': 'Zure lagunen lagunak'})
		self.assertGreater(len(lagunen_lagunak), 0)
	
	def test_besteek_irakurritako_liburuen_arabera_irakurri_gabe(self):
		self.login('ejemplo2@gmail.com', '123456')
		res = self.client.get('/LagunenGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		irakurritako_liburuak = page.find_all('div', {'class': 'card', 'data-section': 'Irakurritako liburuen arabera'})
		self.assertEqual(len(irakurritako_liburuak), 0)
		
	def test_besteek_irakurritako_liburuen_arabera_besteek_liburu_hori_irakurri_gabe(self):
		self.login('james@gmail.com', '123456')
		res = self.client.get('/LagunenGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		irakurritako_liburuak = page.find_all('div', {'class': 'card', 'data-section': 'Irakurritako liburuen arabera'})
		self.assertEqual(len(irakurritako_liburuak), 0)

	def test_besteek_irakurritako_liburuen_arabera_besteek_liburu_hori_irakurrita(self):
		self.login('ejemplo@gmail.com', '123456')
		res = self.client.get('/LagunenGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		irakurritako_liburuak = page.find_all('div', {'class': 'card', 'data-section': 'Irakurritako liburuen arabera'})
		self.assertGreater(len(irakurritako_liburuak), 0)
		
	def test_bilaketa_parametro_gabe(self):
    		self.login('ejemplo@gmail.com', '123456')
    		res = self.client.get('/LagunenGomendioak')
    		self.assertEqual(200, res.status_code)
    		page = BeautifulSoup(res.data, features="html.parser")
    		cards = page.find_all('div', class_='card')
    		self.assertGreater(len(cards), 0)

	def test_bilaketa_txarto(self):
		params = {
			'name': "Federico Valverde"
		}
		self.login('ejemplo@gmail.com', '123456')
		res = self.client.get('/LagunenGomendioak', query_string=params)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		lagunak = page.find_all('div', class_='card')
		self.assertEqual(len(lagunak), 0)

	def test_bilaketa_ondo(self):
		params = {
			'name': "juan"
		}
		self.login('ejemplo@gmail.com', '123456')
		res = self.client.get('/LagunenGomendioak', query_string=params)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		lagunak = page.find_all('div', class_='card')
		self.assertGreater(len(lagunak), 0)
		for lagun in lagunak:
			self.assertIn(params['name'].lower(), lagun.find(class_='card-title').get_text().lower())
			
			

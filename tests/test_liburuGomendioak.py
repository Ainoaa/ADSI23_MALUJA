from . import BaseTestClass
from bs4 import BeautifulSoup

class TestLiburuGomendioak(BaseTestClass):
	
	def test_redirect(self):
		res = self.client.get('/liburuGomendioak')
		self.assertEqual(302, res.status_code)
		self.assertEqual('/', res.location)

	def test_sartu_ondo(self):
		self.login('james@gmail.com', '123456')
		res = self.client.get('/liburuGomendioak')
		self.assertEqual(200, res.status_code)

	def test_irakurritako_liburuen_arabera_irakurritako_liburuak_izan_gabe(self):
		self.login('ejemplo2@gmail.com', '123456')
		res = self.client.get('/liburuGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		cards_amigos = page.find_all('div', {'class': 'card', 'data-section': 'liburuen arabera'})
		self.assertEqual(len(cards_amigos), 0)
	
	def test_irakurritako_liburuen_arabera_irakurritako_liburuak_izaten(self):
		self.login('james@gmail.com', '123456')
		res = self.client.get('/liburuGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		cards_amigos = page.find_all('div', {'class': 'card', 'data-section': 'liburuen arabera'})
		self.assertGreater(len(cards_amigos), 0)
	
	def test_lagunek_irakurritako_liburuen_arabera_lagunak_izan_gabe(self):
		self.login('jhon@gmail.com', '123')
		res = self.client.get('/liburuGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		cards_amigos = page.find_all('div', {'class': 'card', 'data-section': 'lagunen arabera'})
		self.assertEqual(len(cards_amigos), 0)
	
	def test_lagunek_irakurritako_liburuen_arabera_lagunak_izaten(self):
		self.login('james@gmail.com', '123456')
		res = self.client.get('/liburuGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		cards_amigos = page.find_all('div', {'class': 'card', 'data-section': 'lagunen arabera'})
		self.assertGreater(len(cards_amigos), 0)
	
	def test_lagunek_irakurritako_liburuen_arabera_lagunak_izaten_baina_liburuak_irakurri_gabe(self):
		self.login('ejemplo@gmail.com', '123456')
		res = self.client.get('/liburuGomendioak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		cards_amigos = page.find_all('div', {'class': 'card', 'data-section': 'lagunen arabera'})
		self.assertEqual(len(cards_amigos), 0)
	
		
	def test_bilaketa_parametro_gabe(self):
    		self.login('james@gmail.com', '123456')
    		res = self.client.get('/liburuGomendioak')
    		self.assertEqual(200, res.status_code)
    		page = BeautifulSoup(res.data, features="html.parser")
    		cards = page.find_all('div', class_='card')
    		self.assertGreater(len(cards), 0)

	def test_bilaketa_txarto(self):
		params = {
			'title': "Este libro no existe"
		}
		self.login('james@gmail.com', '123456')
		res = self.client.get('/liburuGomendioak', query_string=params)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		cards = page.find_all('div', class_='card')
		self.assertEqual(len(cards), 0)

	def test_bilaketa_ondo(self):
		params = {
			'title': "Forbiden boy"
		}
		self.login('james@gmail.com', '123456')
		res = self.client.get('/liburuGomendioak', query_string=params)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		cards = page.find_all('div', class_='card')
		self.assertGreater(len(cards), 0)
		for card in cards:
			self.assertIn(params['title'].lower(), card.find(class_='card-title').get_text().lower())
			
			

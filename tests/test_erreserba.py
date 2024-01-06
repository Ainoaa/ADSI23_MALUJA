from . import BaseTestClass
from bs4 import BeautifulSoup
from model import Connection
from Book import Book

class TestErreserba(BaseTestClass):
	
	def test_sin_parametros_de_busqueda(self):
		res = self.client.get('/erreserbatutakoLiburuak')
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(6,len(page.find('div', class_='row').find_all('div', class_='card')))


	def test_busquedaFallida(self):
		params = {
			'title': "Este libro no ha sido reservado nunca."
		}
		res = self.client.get('/erreserbatutakoLiburuak', query_string = params)
		self.assertEqual(200, res.status_code)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))


	def test_busquedaPorTitulo(self):
		params = {
			'title': Book.title
		}
		res = self.client.get('/erreserbatutakoLiburuak', query_string = params)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(6, len(page.find('div', class_='row').find_all('div', class_='card')))
		for card in page.find('div', class_='row').find_all('div', class_='card'):
			self.assertIn(params['title'].lower(), card.find(class_='card-title').get_text().lower())
		self.assertEqual(2, len(page.find('ul', class_='pagination').find_all('li', class_='page-item')))
		
		
	def test_busquedaPorAutor(self):
		params = {
			'author': Book.author
		}
		res = self.client.get('/erreserbatutakoLiburuak', query_string = params)
		page = BeautifulSoup(res.data, features="html.parser")
		self.assertEqual(6, len(page.find('div', class_='row').find_all('div', class_='card')))
		for card in page.find('div', class_='row').find_all('div', class_='card'):
			self.assertIn(params['title'].lower(), card.find(class_='card-title').get_text().lower())
		self.assertEqual(2, len(page.find('ul', class_='pagination').find_all('li', class_='page-item')))
		
		
	def test_reserva_exitosa(self):
		# Suponemos que hemos reservado el libro con id 1
		book_id = 1
        	res = self.client.post(f'/liburuaErreserbatu/{book_id}')
        	self.assertEqual(302, res.status_code) 

        	self.assertTrue(res.location.endswith(f'/liburuaErreserbatuDa/{book_id}'))

        	# Simular una segunda reserva del mismo libro
        	res = self.client.post(f'/liburuaErreserbatu/{book_id}')
        	self.assertEqual(200, res.status_code)

        	page = BeautifulSoup(res.data, features="html.parser")
        	self.assertIn("liburuaErreserbatutaZegoenJada.html", page.find("template").get("name"))
        	
        	
       	def test_devolucion_exitosa(self):
    		# Suponemos que hemos reservado el libro con id 1
    		book_id = 1

    		self.client.post(f'/liburuaErreserbatu/{book_id}')
    		res = self.client.post(f'/liburuaBueltatu/{book_id}')
    		self.assertEqual(302, res.status_code) 
    		
    		self.assertTrue(res.location.endswith(f'/liburuaBueltatuDa/{book_id}'))

    		# Intentamos devolver el mismo libro nuevamente
    		res = self.client.post(f'/liburuaBueltatu/{book_id}')
    		self.assertEqual(200, res.status_code)

    		page = BeautifulSoup(res.data, features="html.parser")
    		self.assertIn("ezDagoLiburua.html", page.find("template").get("name"))

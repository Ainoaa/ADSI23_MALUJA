import unittest
from controller import webServer
from model import Connection
class BaseTestClass(unittest.TestCase):
	def setUp(self):
		self.app = webServer.app
		self.client = self.app.test_client()
		self.db = Connection()
		
	def tearDown(self):
		pass

	def login(self, email, password):
		return self.client.post('/login', data=dict(
			email=email,
			password=password
		))
	def liburuaGehitu(self, titulua, autorea, azala, deskribapena):
		return self.client.post('/liburuaGehitu', data=dict(
			titulua=titulua,
			autorea=autorea,
			azala=azala,
			deskribapena=deskribapena
			))

	def liburua_dago(self, titulua, autorea):
		return self.client.post('/liburuaGehitu', data=dict(
			titulua=titulua,
			autorea=autorea,
			))

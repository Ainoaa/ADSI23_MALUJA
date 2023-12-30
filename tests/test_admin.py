from . import BaseTestClass
from bs4 import BeautifulSoup
from model import Connection
db = Connection()
class TestAdmin(BaseTestClass):


    def test_liburua_Gehitu(self):
        #Liburua ez dagoela konprobatuko dugu:
            # Liburua ez dagoela konprobatuko dugu:
        params = {
            'title': "Liburu Berria"
        }
        res = self.client.get('/catalogue', query_string=params)
        self.assertEqual(200, res.status_code)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))
        print(f"Orain 'Liburu Berria' ez dago gure katalogoan")

        # liburua gehitu egiten da
        data = {
            'titulo': 'Liburu Berria',
            'autor': 'Mercedes Abad',
            'cover': 'A',
            'descripcion': 'B'
        }
        res = self.client.post('/liburuaGehitu', data=data)
        print(f"Orain 'Liburu Berria' gure katalogora gehitu dugu")
        # Liburua gehitu dela ziurtatzeko, katalogoan bilatzen dugu eta true 
        # itzuliko du, baldin eta katalogoan badago.
        params = {
            'title': "Liburu Berria"
        }
        res = self.client.get('/catalogue', query_string=params)
        page = BeautifulSoup(res.data, features="html.parser")
        self.assertEqual(1, len(page.find('div', class_='row').find_all('div', class_='card')))
        for card in page.find('div', class_='row').find_all('div', class_='card'):
            self.assertIn(params['title'].lower(), card.find(class_='card-title').get_text().lower())
        self.assertEqual(1, len(page.find('ul', class_='pagination').find_all('li', class_='page-item')))
        print(f"Orain 'Liburu Berria' katalogoan agertzen dela konprobatu dugu")

        # Sartutako liburua borratuko dut, hurrengorako arazorik ez egoteko.
        # Hala ere, liburu hori sartuta egongo balitz eta berriz ere saiakera
        # egiten badugu, sinpleki ez da ezer gertatuko, horretarako konfiguratuta 
        # baitago. Eta gure pantailan normalean mezu bat agertuko litzateke.
        # self.db.delete("DELETE FROM Book WHERE author='Jon' and title='Ezabatzeko liburua'")

        data = {
            'titulo': 'Liburu Berria',
            'autor': 'Mercedes Abad',
        }
        res = self.client.post('/liburuaEzabatu', data=data)


    def test_liburuaEzabatu(self):
    	#Beste liburu bat gehitzen dut
    	    # Beste liburu bat gehitzen dut
	    data = {
	        'titulo': 'Ezabatzeko liburua',
	        'autor': 'Jon',
	        'cover': 'A',
	        'descripcion': 'B'
	    }
	    res = self.client.post('/liburuaGehitu', data=data)

	    # Orain begiratzen dugu ziurtatzeko liburua dagoela
	    params = {
	        'title': "Ezabatzeko liburua"
	    }
	    res = self.client.get('/catalogue', query_string=params)
	    page = BeautifulSoup(res.data, features="html.parser")
	    self.assertEqual(1, len(page.find('div', class_='row').find_all('div', class_='card')))
	    for card in page.find('div', class_='row').find_all('div', class_='card'):
	        self.assertIn(params['title'].lower(), card.find(class_='card-title').get_text().lower())
	    self.assertEqual(1, len(page.find('ul', class_='pagination').find_all('li', class_='page-item')))
	    print(f"'Ezabatzeko liburua' existitzen dela konprobatu dugu")

	    # Orain liburu hori ezabatuko dugu
	    data = {
	        'titulo': 'Ezabatzeko liburua',
	        'autor': 'Jon'
	    }
	    res = self.client.post('/liburuaEzabatu', data=data)
	    print(f"'Ezabatzeko liburua' ezabatu dugu gure katalogotik")

	    # Orain katalogoan begiratuko dugu ea beneta ezabatu den ala ez
	    params = {
	        'title': "Ezabatzeko liburua"
	    }
	    res = self.client.get('/catalogue', query_string=params)
	    self.assertEqual(200, res.status_code)
	    page = BeautifulSoup(res.data, features="html.parser")
	    self.assertEqual(0, len(page.find('div', class_='row').find_all('div', class_='card')))
	    print(f"'Ezabatzeko liburua' gure katalogoan ez dela agertzen konprobatu dugu")


    def test_liburua_Gehitu_bazegoen(self):
        #Liburua gure katagora igotzen saiatuko gara
        
        data = {
            'titulo': 'Vuelo con turbulencias',
            'autor': 'Mercedes Abad',
            'cover': '-',
            'descripcion': '¡La vida es un viaje con turbulencias! Y eso es lo que reflexiona en este libro Mercedes Abad, con un estilo divertido y lleno de anécdotas que invita al lector a disfrutar de su propio viaje con turbulencias. A lo largo de este libro, Mercedes Abad nos presenta una reflexión sobre la vida que abarca todos los aspectos: el amor, la amistad, la familia, el trabajo, el dinero, la salud, el éxito, la felicidad... Y todo ello desde una perspectiva positiva. ¡Un viaje con mucho humor!'
        }
        res = self.client.post('/liburuaGehitu', data=data)
        print(f"Ez da ezer gertatu, eta liburu hori soilik behin dago gordeta")
        # Nahiz eta guk ez ikusi, gure programa pentsatuta dago horrelako kasuetarako,
        #liburua errepikatu beharrean, soilik behin agertuko da, hau da, aurretik zegoen
        #moduan utziko da, eta web orrialdetik eginez gero, mezu bat agertuko litzateke
        #adieraziz liburu hori bazegoela.

    def test_liburua_ez_da_exititzen_ezabatu(self):
        #Liburua gure katagora igotzen saiatuko gara
        
        data = {
            'titulo': 'asñldfjasñldjfas',
            'autor': 'asdjañfldsjfañl',
            'cover': '-',
            'descripcion': 'adfasd'
        }
        res = self.client.post('/liburuaEzabatu', data=data)
        print(f"Ez da ezer gertatu, gordeta ez dagoena ezin da ezabatu")

    def test_erabiltzailea_ezabatu(self):
        data = {
            'name': 'Julio',
            'email': 'julio@gmail.com'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)
        print(f"Erabiltzailea gehitu da!")

        data = {
            'name': 'Julio',
            'email': 'julio@gmail.com',
            'password': '123',
            'admin': 'false'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
    def test_erabiltzailea_gehitu(self):
        data = {
            'name': 'Javi',
            'email': 'javi@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
        print(f"Erabiltzailea ezabatu da!")
        data = {
            'name': 'Javi',
            'email': 'javi@gmail.com'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)
        


    
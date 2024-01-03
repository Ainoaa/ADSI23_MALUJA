from . import BaseTestClass
from bs4 import BeautifulSoup
from model import Connection
db = Connection()
class TestAdmin(BaseTestClass):

    def test_liburua_gehitu(self):
        data = {
            'titulo': 'Liburu Berria',
            'autor': 'Mercedes Abad',
        }
        res = self.client.post('/liburuaEzabatu', data=data)
        #Liburua ez dagoela konprobatuko dugu:
            # Liburua ez dagoela konprobatuko dugu:
        autoreId = self.db.select("SELECT id FROM Author WHERE name = 'Mercedes Abad'")[0][0]
        emaitza = self.db.select("SELECT * FROM Book WHERE title = 'Liburu Berria' and author = ?", (autoreId,))
        self.assertTrue(len(emaitza)==0)

        # liburua gehitu egiten da
        data = {
            'titulo': 'Liburu Berria',
            'autor': 'Mercedes Abad', #BERE ID-a 1 DA!
            'cover': 'A',
            'descripcion': 'B'
        }
        res = self.client.post('/liburuaGehitu', data=data)
        self.assertEqual(200, res.status_code)
        emaitza1 = self.db.select("SELECT * FROM Book WHERE title = 'Liburu Berria' and author = ?", (autoreId,))
        self.assertTrue(len(emaitza1)>0)
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
            'autor': 'Mercedes Abad',
            'cover': 'A',
            'descripcion': 'B'
        }
        res = self.client.post('/liburuaGehitu', data=data)
        autoreId = self.db.select("SELECT id FROM Author WHERE name = 'Mercedes Abad'")[0][0]
        emaitza = self.db.select("SELECT * FROM Book WHERE title = 'Ezabatzeko liburua' and author = ?", (autoreId,))
        # Orain begiratzen dugu ziurtatzeko liburua dagoela
        self.assertTrue(len(emaitza) > 0) 

        # Orain liburu hori ezabatuko dugu
        data = {
            'titulo': 'Ezabatzeko liburua',
            'autor': 'Mercedes Abad'
        }
        res = self.client.post('/liburuaEzabatu', data=data)
        self.assertEqual(200, res.status_code)
        # Orain katalogoan begiratuko dugu ea beneta ezabatu den ala ez
        emaitza1 = self.db.select("SELECT * FROM Book WHERE title = 'Ezabatzeko liburua' and author = ?", (autoreId,))
        self.assertTrue(len(emaitza1) == 0)



    def test_bazegoen_liburua_gehitu(self):
        #Liburua gure katagora igotzen saiatuko gara
        autoreId = self.db.select("SELECT id FROM Author WHERE name = 'Mercedes Abad'")[0][0]
        lib = self.db.select("SELECT * FROM Book WHERE author = ?", (autoreId,))
        self.assertTrue(len(lib)>0)
        data = {
            'titulo': 'Vuelo con turbulencias',
            'autor': 'Mercedes Abad',
            'cover': '-',
            'descripcion': '¡La vida es un viaje con turbulencias! Y eso es lo que reflexiona en este libro Mercedes Abad, con un estilo divertido y lleno de anécdotas que invita al lector a disfrutar de su propio viaje con turbulencias. A lo largo de este libro, Mercedes Abad nos presenta una reflexión sobre la vida que abarca todos los aspectos: el amor, la amistad, la familia, el trabajo, el dinero, la salud, el éxito, la felicidad... Y todo ello desde una perspectiva positiva. ¡Un viaje con mucho humor!'
        }
        res = self.client.post('/liburuaGehitu', data=data)
        self.assertEqual(200, res.status_code)
        lib1 = self.db.select("SELECT * FROM Book WHERE author = ?", (autoreId,))
        self.assertTrue(len(lib1)>0)
        self.assertEqual(lib,lib1)

        # Nahiz eta guk ez ikusi, gure programa pentsatuta dago horrelako kasuetarako,
        #liburua errepikatu beharrean, soilik behin agertuko da, hau da, aurretik zegoen
        #moduan utziko da, eta web orrialdetik eginez gero, mezu bat agertuko litzateke
        #adieraziz liburu hori bazegoela.

    def test_ez_zegoen_liburua_ezabatu(self):
        #Liburua gure katagora igotzen saiatuko gara
        lib = self.db.select("SELECT * FROM BOOK WHERE author = 'asdjañfldsjfañl' and title = 'asñldfjasñldjfas'")
        self.assertTrue(len(lib)==0)
        data = {
            'titulo': 'asñldfjasñldjfas',
            'autor': 'asdjañfldsjfañl',
            'cover': '-',
            'descripcion': 'adfasd'
        }
        res = self.client.post('/liburuaEzabatu', data=data)
        self.assertEqual(200, res.status_code)

    def test_liburua_gehitu_eta_autorea_ere(self):
        data = {
            'titulo': 'kaixo',
            'autor': 'amadeo',
        }
        res = self.client.post('/liburuaEzabatu', data=data)
        autoreId = self.db.select("SELECT id FROM Author WHERE name = 'amadeo'")
        self.assertTrue(len(autoreId)==0)
        emaitza = self.db.select("SELECT * FROM Book WHERE title = 'kaixo'")
        self.assertTrue(len(emaitza) == 0)
        data = {
            'titulo': 'kaixo',
            'autor': 'amadeo',
        }
        res = self.client.post('/liburuaGehitu', data=data)
        self.assertEqual(200, res.status_code)
        autoreId = self.db.select("SELECT id FROM Author WHERE name = 'amadeo'")[0][0]
        emaitza1 = self.db.select("SELECT * FROM Book WHERE title = 'kaixo' and author = ?", (autoreId,))
        self.assertFalse(len(emaitza1)==0)
        data = {
            'titulo': 'kaixo',
            'autor': 'amadeo',
        }
        res = self.client.post('/liburuaEzabatu', data=data)
        

##################################ERABILTZAILEA################################

    def test_bazegoen_erabiltzailea_ezabatu(self):
        data = {
            'name': 'Jaime',
            'email': 'jaime@gmail.com',
            'password': '123',
            'admin': 'false'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)

        era = self.db.select("SELECT * FROM USER WHERE email = 'jaime@gmail.com'")
        self.assertTrue(len(era)>0)
        data = {
            'name': 'Jaime',
            'email': 'jaime@gmail.com'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)
        self.assertEqual(200, res.status_code)
        era = self.db.select("SELECT * FROM USER WHERE email = 'jaime@gmail.com'")
        self.assertTrue(len(era)==0)

        

    def test_ez_zegoen_erabiltzailea_ezabatu(self):
        era = self.db.select("SELECT * FROM USER WHERE email = 'asdfasdfasdf@gmail.com'")
        self.assertTrue(len(era)==0)
        data = {
            'name': 'Francisco',
            'email': 'asdfasdfasdf@gmail.com'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)
        era = self.db.select("SELECT * FROM USER WHERE email = 'asdfasdfasdf@gmail.com'")
        self.assertTrue(len(era)==0)



    def test_ez_zegoen_erabiltzailea_gehitu(self):
        era = self.db.select("SELECT * FROM USER WHERE email = 'mamadu@gmail.com'")
        self.assertFalse(len(era)>0)
        data = {
            'name': 'Mamadu',
            'email': 'mamadu@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
        era = self.db.select("SELECT * FROM USER WHERE email = 'mamadu@gmail.com'")
        self.assertTrue(len(era)>0)
        
        data = {
            'name': 'Mamadu',
            'email': 'mamadu@gmail.com'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)


    def test_bazegoen_erabiltzailea_gehitu(self):
        data = {
            'name': 'Fernando',
            'email': 'fernando@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
        era = self.db.select("SELECT * FROM USER WHERE email = 'fernando@gmail.com'")
        self.assertTrue(len(era)>0)

        data = {
            'name': 'Fernando',
            'email': 'fernando@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
        era2 = self.db.select("SELECT * FROM USER WHERE email = 'fernando@gmail.com'")
        self.assertTrue(len(era2)>0)
        self.assertEqual(era, era2)

    def test_true_edo_false_ez_den_zerbait_jarri_erabiltzaileari(self):
        data = {
            'name': 'Tom',
            'email': 'tom@gmail.com',
            'password': '123',
            'admin': 'asdfasdf'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
        era = self.db.select("SELECT admin FROM USER WHERE email = 'tom@gmail.com'")[0][0]
        self.assertEqual(era, 0)
        #O false adierazten du, eta 1 true
        #Adierazita dago, "true" ez den zerbait jartzen baldin bada, "false" jartzeko automatikoki
        data = {
            'name': 'Tom',
            'email': 'tom@gmail.com'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)

    
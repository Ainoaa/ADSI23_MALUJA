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
        autoreId = self.db.select("SELECT id FROM Author WHERE name = 'Mercedes Abad'")[0][0]
        emaitza = self.db.select("SELECT * FROM Book WHERE title = 'Liburu Berria' and author = ?", (autoreId,))
        self.assertTrue(len(emaitza)==0)
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
        data = {
            'titulo': 'Ezabatzeko liburua',
            'autor': 'Mercedes Abad',
            'cover': 'A',
            'descripcion': 'B'
        }
        res = self.client.post('/liburuaGehitu', data=data)
        autoreId = self.db.select("SELECT id FROM Author WHERE name = 'Mercedes Abad'")[0][0]
        emaitza = self.db.select("SELECT * FROM Book WHERE title = 'Ezabatzeko liburua' and author = ?", (autoreId,))
        self.assertTrue(len(emaitza) > 0) 
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

    def test_erreseinak_erreserbenHistoriala_mailegatuak_dituen_liburua_ezabatu(self):
        data = {
            'name': 'Jaime1',
            'email': 'jaime1@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
        data = {
            'titulo': 'Liburua',
            'autor': 'Jon', 
            'cover': 'A',
            'descripcion': 'B'
        }
        res = self.client.post('liburuaGehitu', data=data)

        id1 = self.db.select("SELECT id FROM USER WHERE email = 'jaime1@gmail.com'")[0][0]
        idlib = self.db.select("SELECT id FROM Book WHERE title = 'Liburua'")[0][0]
        self.db.insert("INSERT INTO Erreseina VALUES (?,?,'2024-01-03','hola','iepa!')", (id1, idlib))
        self.db.insert("INSERT INTO ErreserbenHistoriala VALUES (?,?)", (id1, idlib))
        self.db.insert("INSERT INTO Mailegatu VALUES (?,?,'2024-01-04',NULL)", (id1, idlib))
        
        erreseinak = self.db.select("SELECT * FROM Erreseina WHERE eraId = ?", (id1,))
        self.assertTrue(len(erreseinak)>0)
        erreserbaHistoriala = self.db.select("SELECT * FROM ErreserbenHistoriala WHERE userId = ?", (id1,))
        self.assertTrue(len(erreserbaHistoriala)>0)
        mailegatuak = self.db.select("SELECT * FROM Mailegatu WHERE eraId = ?", (id1,))
        self.assertTrue(len(mailegatuak)>0)

        data = {
            'titulo': 'Liburua',
            'autor': 'Jon', 
            'cover': 'A',
            'descripcion': 'B'
        }
        res = self.client.post('/liburuaEzabatu', data=data)
        data = {
            'name': 'Jaime1',
            'email': 'jaime1@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        erreseinak = self.db.select("SELECT * FROM Erreseina WHERE eraId = ?", (id1,))
        self.assertFalse(len(erreseinak)>0)
        erreserbaHistoriala = self.db.select("SELECT * FROM ErreserbenHistoriala WHERE userId = ?", (id1,))
        self.assertFalse(len(erreserbaHistoriala)>0)
        mailegatuak = self.db.select("SELECT * FROM Mailegatu WHERE eraId = ?", (id1,))
        self.assertFalse(len(mailegatuak)>0)






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
        data = {
            'name': 'Tom',
            'email': 'tom@gmail.com'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)

    def test_lagunak_Erreseinak_ForumTopic_ForumPosts_ErreserbenHistoriala_Mailegatuak_dituen_erabiltzailea_ezabatu(self):
        data = {
            'name': 'Jaime1',
            'email': 'jaime1@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
        data = {
            'name': 'Jaime2',
            'email': 'jaime2@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaGehitu', data=data)
        data = {
            'titulo': 'Liburua',
            'autor': 'Jon', 
            'cover': 'A',
            'descripcion': 'B'
        }
        res = self.client.post('/liburuaGehitu', data=data)
        id1 = self.db.select("SELECT id FROM USER WHERE email = 'jaime1@gmail.com'")[0][0]
        id2 = self.db.select("SELECT id FROM USER WHERE email = 'jaime2@gmail.com'")[0][0]
        idlib = self.db.select("SELECT id FROM Book WHERE title = 'Liburua'")[0][0]
        self.db.insert("INSERT INTO Lagunak VALUES (?,?)", (id1, id2))
        self.db.insert("INSERT INTO Erreseina VALUES (?,?,'2024-01-03','hola','iepa!')", (id1, idlib))
        self.db.insert("INSERT INTO ForumTopic VALUES (NULL,?,'kaixo','polita',null)", (id1,))
        topicid = self.db.select("SELECT id FROM ForumTopic WHERE user_id = ?", (id1,))[0][0]
        self.db.insert("INSERT INTO forum_posts VALUES (null,?,?,'kaixo')", (topicid, id1))
        self.db.insert("INSERT INTO ErreserbenHistoriala VALUES (?,?)", (id1, idlib))
        self.db.insert("INSERT INTO Mailegatu VALUES (?,?,'2024-01-04',NULL)", (id1, idlib))
        
        jaime1Lagunak = self.db.select("SELECT * FROM Lagunak WHERE lagun1Id = ?", (id1,))
        self.assertTrue(len(jaime1Lagunak) > 0)
        jaime2Lagunak = self.db.select("SELECT * FROM Lagunak WHERE lagun2Id = ?", (id2,))
        self.assertTrue(len(jaime2Lagunak) > 0)
        erreseinak = self.db.select("SELECT * FROM Erreseina WHERE eraId = ?", (id1,))
        self.assertTrue(len(erreseinak)>0)
        forumtopic = self.db.select("SELECT * FROM ForumTopic WHERE user_id = ?", (id1,))
        self.assertTrue(len(forumtopic)>0)
        erreserbaHistoriala = self.db.select("SELECT * FROM ErreserbenHistoriala WHERE userId = ?", (id1,))
        self.assertTrue(len(erreserbaHistoriala)>0)
        mailegatuak = self.db.select("SELECT * FROM Mailegatu WHERE eraId = ?", (id1,))
        self.assertTrue(len(mailegatuak)>0)

        
        data = {
            'name': 'Jaime1',
            'email': 'jaime1@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)
        data = {
            'name': 'Jaime2',
            'email': 'jaime2@gmail.com',
            'password': '123',
            'admin': 'true'
        }
        res = self.client.post('erabiltzaileaEzabatu', data=data)
        data = {
            'titulo': 'Liburua',
            'autor': 'Jon', 
            'cover': 'A',
            'descripcion': 'B'
        }
        res = self.client.post('/liburuaEzabatu', data=data)
        

        jaime1Lagunak = self.db.select("SELECT * FROM Lagunak WHERE lagun1Id = ?", (id1,))
        self.assertFalse(len(jaime1Lagunak) > 0)
        jaime2Lagunak = self.db.select("SELECT * FROM Lagunak WHERE lagun2Id = ?", (id2,))
        self.assertFalse(len(jaime2Lagunak) > 0)
        erreseinak = self.db.select("SELECT * FROM Erreseina WHERE eraId = ?", (id1,))
        self.assertFalse(len(erreseinak)>0)
        forumtopic = self.db.select("SELECT * FROM ForumTopic WHERE user_id = ?", (id1,))
        self.assertFalse(len(forumtopic)>0)
        erreserbaHistoriala = self.db.select("SELECT * FROM ErreserbenHistoriala WHERE userId = ?", (id1,))
        self.assertFalse(len(erreserbaHistoriala)>0)
        mailegatuak = self.db.select("SELECT * FROM Mailegatu WHERE eraId = ?", (id1,))
        self.assertFalse(len(mailegatuak)>0)

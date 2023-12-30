from .LibraryController import LibraryController
from .ErreseinaController import ErreseinaController
from controller.ForumController import ForumController
from .ErabiltzaileController import ErabiltzaileController
from flask import Flask, render_template, request, redirect, make_response, url_for

from model import Connection
app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')
db = Connection()

library = LibraryController()
erreseinak = ErreseinaController()
erabiltzaileak = ErabiltzaileController()
#erreserbatuak = ErreserbatutakoLiburuakController()
forum_controller = ForumController()


@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
	                       total_pages=total_pages, max=max, min=min)



@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp
	
@app.route('/erreseina_sortu')
def jadaMailegatuZuen():
	eraId = request.values.get("eraId")
	libId = request.values.get("libId")
	if erreserbatuak.jadaMailegatuZuen(eraId, libId):
		dataOrain = datetime.datetime.now()
		dataFormatua = dataOrain("%Y-%m-%d %H:%M:%S")
		return render_template('erreseina.html', eraId = eraId, libId = libId, data = dataFormatua, nota = None, iruzkina = None)
	else:
		return None
		
@app.route('/erreseina_sortuta')
def erreseinaSortu():
	eraId = request.values.get("eraId")
	libId = request.values.get("libId")
	data = request.values.get("data")
	nota = request.values.get("nota")
	iruzkina = request.values.get("iruzkina")
	if erreserbatuak.jadaMailegatuZuen(eraId, libId):
		erreseinak.erreseinaSortu(eraId, libId, data, nota, iruzkina)
	return render_template('mailegatu.html', eraId=eraId, libId=libId)	#Volver a otro sitio
		
@app.route('/erreseina_editatu')
def jadaErreseinaZuen():
	eraId = request.values.get("eraId")
	libId = request.values.get("libId")
	data = request.values.get("data")
	nota = request.values.get("nota")
	iruzkina = request.values.get("iruzkina")
	if erreserbatuak.jadaMailegatuZuen(eraId, libId):
		if erreseinak.jadaErreseinaZuen(eraId, libId):
			#Conseguir datos de la erreseina
			return render_template('erreseina.html', eraId=eraId, libId=libId, data=data, nota=nota, iruzkina=iruzkina)
		else:
			return None
	else:
		return None

@app.route('/erreseina_editatuta')
def erreseinaEditatu():
	eraId = request.values.get("eraId")
	libId = request.values.get("libId")
	data = request.values.get("data")
	nota = request.values.get("nota")
	iruzkina = request.values.get("iruzkina")
	if erreserbatuak.jadaMailegatuZuen(eraId, libId):
		if erreseinak.jadaErreseinaZuen(eraId, libId):
			dataOrain = datetime.datetime.now()
			dataFormatua = dataOrain("%Y-%m-%d %H:%M:%S")
			erreseinak.erreseinaEditatu(eraId, libId, data, nota, iruzkina, dataFormatua)
	return render_template('mailegatu.html', eraId=eraId, libId=libId)	#Volver a otro sitio
			
			

@app.route('/liburuko_erreseina_katalogoa')
def liburuko_erreseina_katalogoa():
	eraId = request.values.get("eraId")
	libId = request.values.get("libId")
	lista = erreseinak.bilatuErreseinak(libId)
	return render_template('libErreseinaKatalogo.html', lista, eraId)



@app.route('/admin')
def admin():
	return render_template('admin.html')


###############################################################################################################

@app.route('/liburuaGehitu', methods=['GET','POST'])
def liburuaGehitu():
	if request.method == 'POST':
		titulua = request.values.get("titulo")
		autorea = request.values.get("autor")
		azala = request.values.get("cover")
		deskribapena = request.values.get("descripcion")
		if library.liburua_dago(titulua, autorea):
			return render_template('liburuaGehitutaDagoJada.html')
		else:
			liburua = library.liburua_gehitu(titulua, autorea, azala, deskribapena)
			return render_template('liburuaGehituDa.html')
	else:
		return render_template('liburuaGehitu.html')




@app.route('/liburuaEzabatu', methods=['GET', 'POST'])
def liburuaEzabatu():
	if request.method == 'POST':
		titulua = request.values.get("titulo")
		autorea = request.values.get("autor")
		if library.liburua_dago(titulua, autorea):
			library.liburua_ezabatu(titulua, autorea)
			return render_template('liburuaEzabatuDa.html')
		else:
			return render_template('ezDagoLiburua.html')
	else:
		return render_template('liburuaEzabatu.html')

@app.route('/erabiltzaileaGehitu', methods=['GET', 'POST'])
def erabiltzaileaGehitu():
	if request.method == 'POST':
		izena = request.form.get('name')
		emaila = request.form.get('email')
		pasahitza = request.form.get('password')
		admin = request.form.get('admin')
		if erabiltzaileak.erabiltzailea_dago(emaila,):
			return render_template('erabiltzaileaDagoJada.html')
		else:
			erabiltzaileak.erabiltzailea_gehitu(izena, emaila, pasahitza, admin)
			return render_template('erabiltzaileaGehituDa.html')
	else:
		return render_template('erabiltzaileaGehitu.html')

@app.route('/erabiltzaileaEzabatu', methods=['GET', 'POST'])
def erabiltzaileaEzabatu():
	if request.method == 'POST':
		izena = request.form.get('name')
		emaila = request.form.get('email')
		if erabiltzaileak.erabiltzailea_dago(emaila,):
			erabiltzaileak.erabiltzailea_ezabatu(izena, emaila)
			return render_template('erabiltzaileaEzabatuDa.html')
		else:
			return render_template('erabiltzaileaEzDago.html')
	return render_template('erabiltzaileaEzabatu.html')
##############################################################################################################

@app.route('/LagunenGomendioak')
def LagunenGomendioak():
	if not('user' in dir(request) and request.user and request.user.token):
		return redirect("/")
	name = request.values.get("name", "")
	email = request.values.get("email", "")
	page_lagunak = int(request.values.get("page_lagunak", 1))
	page_zure_lag = int(request.values.get("page_zure_lag", 1))


	lagun_zerrenda = request.user.get_lagunen_zerrenda()
	irakurritako_liburuak = request.user.get_irakurritako_liburuak()
	gomendatutako_lagunak = []
	for User in lagun_zerrenda:
		lista = User.get_lagunen_zerrenda()
		for user in lista:
			print(user.name)
		gomendatutako_lagunak = [
			user
			for user in lista
			if user not in irakurritako_lagunak and
			user not in gomendatutako_lagunak
		]
	total_pages_lagunak = (len(gomendatutako_lagunak)//4) +1
	lagunen_lagunak = gomendatutako_lagunak
	for book in lagunen_lagunak:
			print(user.name)

	people, nb_people = library.search_people(name=name, email=email, page=page - 1)
	total_pages_zure_lagunak = (nb_people // 4) + (1 if nb_people % 4 > 0 else 0)

	return render_template('LagunenGomendioak.html', lagunen_lagunak=lagunen_lagunak, current_page_lagunak=page_lagunak, total_pages_lagunak=total_pages_lagunak, people=people,
                       		current_page_zure_lag=page_zure_lag, total_pages_zure_lagunak=total_pages_zure_lagunak,
				name=name, email=email, max=max, min=min)



@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'POST':
        user_id = request.user.id
        title = request.form.get('title')
        content = request.form.get('content')
        forum_controller.create_forum_topic(user_id, title, content)
        return redirect(url_for('list_topics'))

    return render_template('create_topic.html')


@app.route('/list_topics')
def list_topics():
    # Lógica para obtener y mostrar la lista de temas del foro
    topics = forum_controller.get_forum_topics()
    return render_template('foroa.html', topics=topics)

@app.route('/foroa')
def foroa():
	topics = forum_controller.get_forum_topics()
	return render_template('foroa.html',topics=topics)

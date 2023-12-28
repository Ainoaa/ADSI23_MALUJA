from .LibraryController import LibraryController
from .ErreseinaController import ErreseinaController
from .ErabiltzaileController import ErabiltzaileController
#from .ErreserbatutakoLiburuakController import ErreserbatutakoLiburuakController
from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = LibraryController()
erreseinak = ErreseinaController()
erabiltzaileak = ErabiltzaileController()
#erreserbatuak = ErreserbatutakoLiburuakController()

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


@app.route('/LagunenGomendioak')
def LagunenGomendioak():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('LagunenGomendioak.html', books=books, title=title, author=author, current_page=page,
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
	
@app.route('/erreseina_idatzi')
def jadaMailegatuZuen():
	eraId = request.values.get("eraId")
	libId = request.values.get("libId")
	if erreserbatuak.jadaMailegatuZuen(eraId, libId):
		dataOrain = datetime.datetime.now()
		dataFormatua = dataOrain("%Y-%m-%d %H:%M:%S")
		return render_template('erreseina.html', eraId = eraId, libId = libId, data = dataFormatua, nota = None, iruzkina = None)
	else:
		return None
		
@app.route('/mailegatu')	
def erreseinaSortu():
	eraId = request.values.get("eraId")
	libId = request.values.get("libId")
	data = request.values.get("data")
	nota = request.values.get("nota")
	iruzkina = request.values.get("iruzkina")
	if erreserbatuak.jadaMailegatuZuen(eraId, libId):
		erreseinak.erreseinaSortu(eraId, libId, data, nota, iruzkina)
	return render_template('mailegatu.html', eraId=eraId, libId=libId)	#Volver a otro sitio
		
@app.route('/erreseina_idatzi')
def jadaErreseinaZuen():
	eraId = request.values.get("eraId")
	libId = request.values.get("libId")
	data = request.values.get("data")
	nota = request.values.get("nota")
	iruzkina = request.values.get("iruzkina")
	if erreserbatuak.jadaMailegatuZuen(eraId, libId):
		if erreseinak.jadaErreseinaZuen(eraId, libId):
			return render_template('erreseina.html', eraId=eraId, libId=libId, data=data, nota=nota, iruzkina=iruzkina)
		else:
			return None
	else:
		return None

@app.route('/mailegatu')		
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
	page = int(request.values.get("page", 1))
	erreseinak, nb_erreseinak = erreseinak.search_erreseinak(eraId=eraId, libId=libId, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('libErreseinaKatalogo.html', erreseinak=erreseinak, eraId=eraId, libId=libId, current_page=page,
	                       total_pages=total_pages, max=max, min=min)



@app.route('/admin')      
def admin():
	return render_template('admin.html')
	


	

@app.route('/liburuaGehitu', methods=['GET','POST'])      
def liburuaGehitu():
	if request.method == 'POST':
		titulua = request.values.get("titulo")
		autorea = request.values.get("autor")
		azala = request.values.get("cover")
		deskribapena = request.values.get("descripcion")
		#print(liburu_id)
		#if library.liburuaGehitutaZegoen(liburu_id):
		#return render_template('liburuaGehitutaZegoen.html', liburu_id=liburu_id)
		#	else:
		liburua = library.liburua_gehitu(titulua, autorea, azala, deskribapena)
	return render_template('liburuaGehitu.html')
	
	                
	                
	                
@app.route('/liburuaEzabatu', methods=['GET', 'POST'])      
def liburuaEzabatu():
	if request.method == 'POST':
		titulua = request.values.get("titulo")
		autorea = request.values.get("autor")
		library.liburua_ezabatu(titulua, autorea)


	#if library.liburuaGehitutaZegoen(libId):
	#	return render_template('liburuaEzabatu.html')
	#else:
	return render_template('liburuaEzabatu.html')
	
@app.route('/erabiltzaileaGehitu')      
def erabiltzaileaGehitu():
	name = request.form.get('name')
	email = request.form.get('email')
	password = request.form.get('password')
	admin = request.form.get('admin')
	db.insert("INSERT INTO USER (name, email, password, admin) VALUES (?, ?, ?, ?)",(name, email, password, admin))
	return render_template('erabiltzaileaGehitu.html')
    	                
@app.route('/erabiltzaileaEzabatu')      
def erabiltzaileaEzabatu():
	return render_template('erabiltzaileaEzabatu.html')	                	                
		                

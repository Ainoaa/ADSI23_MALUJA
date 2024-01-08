from .LibraryController import LibraryController
from .ErreseinaController import ErreseinaController
from controller.ForumController import ForumController
from .ErabiltzaileController import ErabiltzaileController
from .ErreserbatutakoLiburuakController import ErreserbatutakoLiburuakController
from flask import Flask, render_template, request, redirect, make_response, url_for
from datetime import datetime
from model import Connection
app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')
db = Connection()

library = LibraryController()
erreseinak = ErreseinaController()
erabiltzaileak = ErabiltzaileController()
erreserbatuak = ErreserbatutakoLiburuakController()
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
    return render_template('catalogue.html', books=books, title=title, author=author, current_page=page, total_pages=total_pages, max=max, min=min)



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
        dataOrain = datetime.now()
        dataFormatua = dataOrain.strftime("%Y-%m-%d %H:%M:%S")
        return render_template('erreseina.html', eraId = eraId, libId = libId, data = dataFormatua, nota = None, iruzkina = None)
    else:
        return render_template('erroreaErreseina.html')

@app.route('/erreseina_sortuta')
def erreseinaSortu():
    eraId = request.values.get("eraId")
    libId = request.values.get("libId")
    data = request.values.get("data")
    nota = request.values.get("nota")
    iruzkina = request.values.get("iruzkina")
    if erreserbatuak.jadaMailegatuZuen(eraId, libId):
        erreseinak.erreseinaSortu(eraId, libId, data, nota, iruzkina)
        return render_template('erreseinaEginda.html')
    else:
         return render_template('erroreaErreseina.html')

@app.route('/erreseina_editatu')
def jadaErreseinaZuen():
    eraId = request.values.get("eraId")
    libId = request.values.get("libId")
    data = request.values.get("data")
    nota = request.values.get("nota")
    iruzkina = request.values.get("iruzkina")
    if erreserbatuak.jadaMailegatuZuen(eraId, libId):
        if erreseinak.jadaErreseinaZuen(eraId, libId, data):
            return render_template('erreseina.html', eraId=eraId, libId=libId, data=data, nota=nota, iruzkina=iruzkina)
        else:
            return render_template('erroreaErreseina.html')
    else:
        return render_template('erroreaErreseina.html')

@app.route('/erreseina_editatuta')
def erreseinaEditatu():
    eraId = request.values.get("eraId")
    libId = request.values.get("libId")
    data = request.values.get("data")
    nota = request.values.get("nota")
    iruzkina = request.values.get("iruzkina")
    if erreserbatuak.jadaMailegatuZuen(eraId, libId):
        if erreseinak.jadaErreseinaZuen(eraId, libId, data):
            dataOrain = datetime.now()
            dataFormatua = dataOrain.strftime("%Y-%m-%d %H:%M:%S")
            erreseinak.erreseinaEditatu(eraId, libId, data, nota, iruzkina, dataFormatua)
            return render_template('erreseinaEginda.html')
        else:
            return render_template('erroreaErreseina.html')
    else:
        return render_template('erroreaErreseina.html')



@app.route('/liburuko_erreseina_katalogoa')
def liburuko_erreseina_katalogoa():
    eraId = request.values.get("eraId", -1)
    libId = request.values.get("libId", -1)
    lista = erreseinak.bilatuErreseinak(libId)
    return render_template('libErreseinaKatalogo.html', lista=lista, eraId=eraId)


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
            return render_template('liburuaGehituDa.html', liburua=liburua)
    else:
        return render_template('liburuaGehitu.html')




@app.route('/liburuaEzabatu', methods=['GET', 'POST'])
def liburuaEzabatu():
    if request.method == 'POST':
        titulua = request.values.get("titulo")
        autorea = request.values.get("autor")
        if library.liburua_dago(titulua, autorea):
            autoreId = library.get_autoreId(autorea)
            libId = library.get_libId(titulua, autorea)
            library.erreseinakEzabatu(libId)
            library.erreserbenHistorialaEzabatu(libId)
            library.mailegatuakEzabatu(libId)
            liburua = library.liburua_ezabatu(libId, autoreId)
            return render_template('liburuaEzabatuDa.html',liburua=liburua)
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
            erabiltzailea = erabiltzaileak.erabiltzailea_gehitu(izena, emaila, pasahitza, admin)
            return render_template('erabiltzaileaGehituDa.html', erabiltzailea=erabiltzailea)
    else:
        return render_template('erabiltzaileaGehitu.html')

@app.route('/erabiltzaileaEzabatu', methods=['GET', 'POST'])
def erabiltzaileaEzabatu():
    if request.method == 'POST':
        izena = request.form.get('name')
        emaila = request.form.get('email')
        if erabiltzaileak.erabiltzailea_dago(emaila,):
            eraId = erabiltzaileak.get_erabiltzaileId(izena, emaila)
            erabiltzaileak.lagunakEzabatu(eraId)
            erabiltzaileak.erreseinakEzabatu(eraId)
            erabiltzaileak.forumTopicEzabatu(eraId)
            erabiltzaileak.forum_posts_ezabatu(eraId)
            erabiltzaileak.erreserbenHistorialaEzabatu(eraId)
            erabiltzaileak.mailegatuakEzabatu(eraId)
            erabiltzailea = erabiltzaileak.erabiltzailea_ezabatu(eraId)
            return render_template('erabiltzaileaEzabatuDa.html', erabiltzailea=erabiltzailea)
        else:
            return render_template('erabiltzaileaEzDago.html')
    return render_template('erabiltzaileaEzabatu.html')

##############################################################################################################

@app.route('/LagunenGomendioak')
def LagunenGomendioak():
    if not('user' in dir(request) and request.user and request.user.token):
        return redirect("/")
    name = request.values.get("name", "")
    email = request.values.get("user_email", "")
    page_lagunen_lagunak = int(request.values.get("page_lagunen_lagunak", 1))
    page_zure_lag_lib = int(request.values.get("page_zure_lag_lib", 1))

    #Lagunen lagunak gomendatu
    lagun_zerrenda = request.user.get_lagunen_zerrenda()
    gomendatutako_lagunen_lagunak = []
    for User in lagun_zerrenda:
        lista = User.get_lagunen_zerrenda(name,email)
        gomendatutako_lagunen_lagunak.extend(
            user
            for user in lista
            if user != request.user and
            user not in lagun_zerrenda and
            user not in gomendatutako_lagunen_lagunak
        )
    gomendatutako_lagunen_lagunak = [user for user in gomendatutako_lagunen_lagunak if user.id != request.user.id]
    total_pages_lagunen_lagunak = (len(gomendatutako_lagunen_lagunak)//4) +1
    lagunen_lagunak = gomendatutako_lagunen_lagunak

    #Irakurritako liburuen araberako lagunak gomendatu
    irakurritako_liburuak = request.user.get_irakurritako_liburuak()
    gomendatutako_lagunak_liburuekiko = []
    for book in irakurritako_liburuak:
        liburua_irakurri_dutenek = request.user.get_liburua_irakurri_dutenek(book.id,name,email)
        gomendatutako_lagunak_liburuekiko.extend(
            user
            for user in liburua_irakurri_dutenek
            if user not in lagun_zerrenda and
            user not in gomendatutako_lagunak_liburuekiko
        )

    irakurritako_liburuen_lagunak = gomendatutako_lagunak_liburuekiko
    total_pages_zure_lag_lib = (len(gomendatutako_lagunak_liburuekiko)//4) +1

    #if "eskaera" in request.values:
    #    User.gehituEskaera(request.values.get("mail"))
    #elif "eskaera1" in request.values:
    #    User.gehituEskaera(request.values.get("mail1"))

    return render_template('LagunenGomendioak.html', lagunen_lagunak=lagunen_lagunak, current_page_lagunen_lagunak=page_lagunen_lagunak, total_pages_lagunen_lagunak=total_pages_lagunen_lagunak,
                irakurritako_liburuen_lagunak=irakurritako_liburuen_lagunak, current_page_zure_lag_lib=page_zure_lag_lib, total_pages_zure_lag_lib=total_pages_zure_lag_lib,
                name=name, email=email, max=max, min=min)


#########################################################################################################################################################################################################################################################################

@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'POST':
        user_id = request.user.id
        username = request.user.name
        title = request.form.get('title')
        content = request.form.get('content')
        forum_controller.create_forum_topic(user_id, username, title, content)
        return redirect(url_for('foroa'))

    return render_template('foroa.html')


@app.route('/foroa')
def foroa():
    topics = ForumController().get_forum_topics_with_posts()
    return render_template('foroa.html', topics=topics)

@app.route('/create_reply', methods=['POST'])
def create_reply():
    if 'user' in dir(request) and request.user and request.user.token:
        user_id = request.user.id
        topic_id = request.form.get('topic_id')
        content = request.form.get('reply_content')
        # Erantzuna sortu:
        forum_controller.create_reply(user_id, topic_id, content)
        return redirect(url_for('foroa'))
    # Identifikatuta ez badago, login orrira bidali
    return redirect(url_for('login'))


@app.route('/get_forum_posts_for_topic/<int:topic_id>', methods=['GET'])
def get_forum_posts_for_topic(topic_id):
    forum_controller = ForumController()
    posts = forum_controller.get_forum_posts_for_topic(topic_id)
    if posts is not None:
        return redirect(url_for('foroa'))
    else:
        print('Error al obtener mensajes del tema')
        return redirect(url_for('foroa'))


@app.route('/liburuGomendioak')
def liburuGomendioak():
    if not('user' in dir(request) and request.user and request.user.token):
        return redirect("/")
    title = request.values.get("title", "")
    author = request.values.get("author", "")
    page_lagunak = int(request.values.get("page_lagunak", 1))
    page_zure_lib = int(request.values.get("page_zure_lib", 1))
    #Lagunak irakurritakoaren araberako gomendioak
    lagun_zerrenda = request.user.get_lagunen_zerrenda()
    irakurritako_liburuak = request.user.get_irakurritako_liburuak()
    gomendatutako_liburuak_lagunak = []
    for User in lagun_zerrenda:
        lista = User.get_irakurritako_liburuak(title,author)
        gomendatutako_liburuak_lagunak.extend(
            book
            for book in lista
            if book not in irakurritako_liburuak and
            book not in gomendatutako_liburuak_lagunak
        )
    total_pages_lagunak = (len(gomendatutako_liburuak_lagunak)//6) +1
    books_lagunak = gomendatutako_liburuak_lagunak
    #Erabiltzailearen irakurritakoaren araberako gomendioak
    irakurritako_liburuak = request.user.get_irakurritako_liburuak()
    gomendatutako_liburuak = []
    for book in irakurritako_liburuak:
        autorearen_liburuak = library.get_autore_baten_liburuak(book.author,author,title)
        gomendatutako_liburuak.extend(
            book
            for book in autorearen_liburuak
            if book not in irakurritako_liburuak and
            book not in gomendatutako_liburuak
        )
    books_zure_lib = gomendatutako_liburuak
    total_pages_zure_lib = (len(gomendatutako_liburuak)//6) + 1
    if "eskaera" in request.values:
        User.gehituEskaera(request.values.get("mail"))
    elif "eskaera1" in request.values:
        User.gehituEskaera(request.values.get("mail1"))
    return render_template('liburuGomendioak.html', books_lagunak=books_lagunak, current_page_lagunak=page_lagunak, total_pages_lagunak=total_pages_lagunak,
                books_zure_lib=books_zure_lib, current_page_zure_lib=page_zure_lib, total_pages_zure_lib=total_pages_zure_lib,
                title=title, author=author, max=max, min=min)



@app.route('/ErreserbatutakoLiburuak')
def historialErreserba():
    libros_reservados = erreserbatuak.get_liburu_erreserbatuak()
    return render_template('erreserbatutakoLiburuak.html', libros_reservados=libros_reservados)


@app.route('/liburuaBueltatu', methods=['GET', 'POST'])
def liburuaBueltatu():
    if request.method == 'POST':
        liburu_id = request.values.get("bookId")
        user_id = request.values.get("userId")
        
        if erreserbatuak.jada_mailegatuta_dago(liburu_id, user_id):
            eraId = erreserbatuak.get_user_id(user_id)
            libId = erreserbatuak.get_book_id(liburu_id)
            erreserbatuak.erreseinakEzabatu(libId)
            erreserbatuak.erreserbenHistorialaEzabatu(libId)
            erreserbatuak.mailegatuakEzabatu(libId)
            liburua = erreserbatuak.liburua_bueltatu(libId, eraId)
            return render_template('liburuaBueltatuDa.html',liburua=liburua)
        else:
            return render_template('liburuaEzDago.html')
    else:
        return render_template('liburuaBueltatu.html')
       
 
 
@app.route('/liburuaErreserbatu', methods=['GET', 'POST'])
def liburuaErreserbatu():
    if request.method == 'POST':
        libId = request.values.get("libId")
        eraId = request.values.get("eraId")

        if erreserbatuak.jada_mailegatuta_dago(eraId, libId):
            return render_template('liburuaErreserbatutaZegoenJada.html')
        else:
            liburua = erreserbatuak.erreserbatu_liburua(libId, eraId)
            return render_template('liburuaErreserbatuDa.html')
    else:
        return render_template('liburuaErreserbatu.html')


@app.route('/infoLiburuErreserbatuta/<int:bookId>') 
def info_liburu_erreserbatuta(bookId):
    book_info = erreserbatuak.info_liburu_erreserbatuta(bookId)
    if 'user' in dir(request) and request.user and request.user.token:
        eraId = request.user.id
    else:
    	eraId = -1
    return render_template('info_liburu_erreserbatuta.html', book_info=book_info, eraId=eraId, libId=book_info.id)

        
@app.route('/infoLiburuCatalogo/<int:bookId>') 
def info_liburu_catalogo(bookId):
    book_info = library.info_liburu_catalogo(bookId)
    if 'user' in dir(request) and request.user and request.user.token:
        eraId = request.user.id
    else:
    	eraId = -1
    return render_template('info_liburu_catalogo.html', book_info=book_info, eraId=eraId, libId=book_info.id)


# *****************************************************************************************        Lagunak        *****************************************************************************************
@app.route('/nireLagunak', methods=['GET', 'POST'])
def nireLagunak():
    if not ('user' in dir(request) and request.user and request.user.token):
        return redirect("/")

    #eraId = request.values.get("eraId", "")
    lagun_zerrenda = request.user.getLagunak()
    lagunak = []
    for User in lagun_zerrenda:
        lagunak.extend(
            lagun
            for lagun in lagun_zerrenda
        )
    lagunak = list(set(lagunak))

    if "ezabatu" in request.values:
        User.lagunaEzabatu(request.values.get("mail"))
    return render_template('nireLagunak.html', lagunak=lagunak)


@app.route('/jasotakoEskaerak', methods=['GET', 'POST'])
def jasotakoEskaerak():
    if not ('user' in dir(request) and request.user and request.user.token):
        return redirect("/")

    eskaera_zerrenda = request.user.getJasotakoEskaerak()
    eskaerak = []
    for User in eskaera_zerrenda:
        eskaerak.extend(
            eskaera
            for eskaera in eskaerak
        )
    eskaerak = list(set(eskaerak))

    if "onartu" in request.values:
        User.eskaeraOnartu(request.values.get("mail"))
    elif "ezeztatu" in request.values:
        User.eskaeraEzeztatu(request.values.get("mail"))
    return render_template('jasotakoEskaerak.html', eskaerak=eskaerak)

@app.route('/bidalitakoEskaerak', methods=['GET', 'POST'])
def bidalitakoEskaerak():
    if not ('user' in dir(request) and request.user and request.user.token):
        return redirect("/")

    eskaera_zerrenda = request.user.getBidalitakoEskaerak()
    eskaerak = []
    for User in eskaera_zerrenda:
        eskaerak.extend(
            eskaera
            for eskaera in eskaerak
        )
    eskaerak = list(set(eskaerak))
    if "ezabatu" in request.values:
        User.eskaeraEzabatu(request.values.get("mail"))
    return render_template('bidalitakoEskaerak.html', eskaerak=eskaerak)

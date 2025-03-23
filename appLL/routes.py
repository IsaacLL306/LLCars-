from flask import Flask, render_template, url_for, request, make_response, session, redirect, flash, g, jsonify, send_from_directory
import os
from appLL import app, db
from appLL.models import carros_normales, Vehiculos_premium, Users, Posts, db, news, creditos, Motos, motos_altoCC
from requests import get
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

#____________________________________________Variables___________________________________

app.secret_key = "LL_Proyecto306"

#____________________________________________Vistas Generales___________________________________

@app.route("/ruta_nolose")
def nolose():
    return "QLQ, estamos probando el modulo de routes.py"

@app.route("/")
def index():
    ultimas_noticias = news.query.order_by(news.id.desc()).limit(4).all()
    seguridad_vial = "Recuerda que tu seguridad esta en tus propias manos, conduce prudentemente y alejate del peligro vial"
    return render_template("index.html", tituloH = "LL consesionaria", H1_LL = "LL Cars@", seguridad = seguridad_vial, ultimas_noticias=ultimas_noticias)

@app.route("/catalogo")
def catalogo():    
    return render_template("catalogo.html", titulo = "Tu carro!!!", PremiumH = Vehiculos_premium, carros_normales = carros_normales, motos_ofertas = Motos, superbikes = motos_altoCC)

@app.route('/vehiculo/<modelo>')
def ver_vehiculo(modelo):
    # Combinar todas las listas de vehículos
    vehiculos = Vehiculos_premium + carros_normales + Motos + motos_altoCC

    # Buscar el vehículo por su modelo
    vehiculo = next((v for v in vehiculos if v["Modelo"].lower() == modelo.lower()), None)

    # Manejar el caso en que no se encuentre el vehículo
    if not vehiculo:
        return "Vehículo no encontrado", 404

    # Renderizar la página con los datos del vehículo
    return render_template('carros.html', vehiculo=vehiculo, Motos=Motos, motos_altoCC=motos_altoCC)

@app.route('/vitrina')
def vitrina():
    nombre_user = ""
    if "username" in session:
        user = g.user
        nombre_user = g.auth2
    else:
        nombre_user= ""
        user = None
    return render_template("vitrinaLL.html", nombre_user = nombre_user, user = user, carros = carros_normales, premium_carros = Vehiculos_premium, motos = Motos, superbikes = motos_altoCC )

#____________________________________________Vistas Usuario___________________________________

@app.before_request
def auth():
    if "username" in session:
        user = Users.query.filter_by(username=session["username"]).first()
        g.user = user
        g.auth2 = user.username
        g.auth3 = user.role
        if user.role == "admin":
            print(f"Admin logeado: {g.user.username}")
        else:
            print(f"logeado {g.auth2} {g.auth3}")
    else:
        g.auth2 = None
        g.auth3 = None
        print(f"Sin sesion activa {g.auth2} {g.auth3}")

@app.route("/sign", methods = ["GET", "POST"]) #CREAR_USUARIOs
def Sign_up():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"])
        new_user = Users(
            email=request.form["email"],
            username=request.form["username"],
            password=hashed_pw,
            role='user' 
        )
        if not Users.query.filter_by(email=new_user.email).first():
            db.session.add(new_user)
            db.session.commit()
            flash("Te has registrado exitosamente", "success")            
            return redirect(url_for('login'))        
        flash("El correo electrónico ya está registrado", "error")    
    return render_template("signup.html")


@app.route("/login", methods = ["GET", "POST"]) #ENTRAR_PERFIL
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username = request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["username"] = user.username
            
            flash("Logeado correctamente", "succes")
            return redirect(url_for('perfil_vista'))
        flash("Credenciales invalidas", "error")
        
    return render_template("login.html")
 
@app.route("/profile") #VISTA_PERFIL
def perfil_vista():
    if "username" in session:
        user = Users.query.filter_by(username=session["username"]).first()
        nombre_perfil = user.username
        return render_template('profile.html', nombre_title = nombre_perfil, user = user)
    else:
        flash('Por favor, inicia sesión para acceder a tu perfil.', 'succes')
        return redirect(url_for('login'))
    
@app.route("/logout") #DESCONECTAO
def logout():
    session.pop("username", None)
    return f"""
    <html>
        <body style="text-align: center; margin-top: 20vh;">
            <div style="border: 1px solid black; padding: 20px; border-radius: 10px; width: fit-content; margin-left:auto;margin-right:auto;">
                Adiós
            </div>
            <p><a href="{ url_for('index') }">Volver al inicio</a></p>
            <p><a href="{ url_for('login') }">logear</a></p>
        </body>
    </html>
    """

@app.route("/user_share")
def share_vehicle():
    return render_template("userVehicle.html")


#________________Formularios de subir imagenes___________________

save_image = os.path.abspath("./appLL/static/uploads")
app.config["UPLOAD_FOLDER"] = save_image

if not os.path.exists(save_image):
    os.makedirs(save_image)

save_news = os.path.abspath("./appLL/static/uploads/news")
app.config["NEWS_IMAGE_FOLDER"] = save_news

if not os.path.exists(save_news):
    os.makedirs(save_news)

@app.route("/uploads/<filename>")
def get_file(filename):    
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/get_image/<filename>')
def get_image(filename):
    return send_from_directory(save_news, filename)

@app.route("/upload", methods = ["GET", "POST"])
def subir_archivo():
    if request.method == "POST":
        f = request.files["ourfile"]
        filename = f.filename
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return redirect(url_for("get_file", filename = filename))
    return render_template("files.html")

@app.route("/Configuracion", methods=["GET", "POST"])
def noticia_admin():
    if "username" in session:
        user = Users.query.filter_by(username=session["username"]).first()
        ultimas_noticias = news.query.order_by(news.id.desc()).limit(4).all()
        if user and user.role == 'admin':
            if request.method == "POST":
                if 'archivo' in request.files:
                    # Subir noticia
                    f = request.files["archivo"]
                    filename_secure_filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config["NEWS_IMAGE_FOLDER"], filename_secure_filename))  # Usar el nombre consistente

                    new_noticia = news(
                        titulo=request.form.get("titulo"),
                        descripcion=request.form.get("descripcion"),
                        fotoUrl=filename_secure_filename
                    )
                    db.session.add(new_noticia)
                    db.session.commit()
                    flash("Noticia creada correctamente.")

                elif 'noticia_id' in request.form:
                    # Eliminar noticia
                    noticia_id = request.form.get('noticia_id')
                    noticia = news.query.get(noticia_id)

                    if noticia:
                        # Eliminar la imagen si existe
                        if noticia.fotoUrl and os.path.exists(os.path.join(app.config["NEWS_IMAGE_FOLDER"], noticia.fotoUrl)):
                            os.remove(os.path.join(app.config["NEWS_IMAGE_FOLDER"], noticia.fotoUrl))

                        db.session.delete(noticia)
                        db.session.commit()
                        flash("Noticia eliminada correctamente")
                    else:
                        flash("No se encontró la noticia")

                else:
                    flash("Acción no válida")
            return render_template("files.html", ultimas_noticias = ultimas_noticias, Var = 'news', noticias = True)  # Renderizar el mismo template
        else:
            flash("No tienes permisos para acceder a esta sección.")
            return render_template("index.html") #Redireccion a la vista del user
    else:
        flash('Por favor, inicie sesión para acceder a esta sección.')
        return redirect(url_for('login'))

@app.route("/Configuracion/promociones", methods=["GET", "POST"])
def promover_usuario():
    if "username" in session:
        user = Users.query.filter_by(username=session["username"]).first()
        if user and user.role == 'admin':
            if request.method == "POST":
                username_to_change = request.form.get('username')
                action = request.form.get('action') # "promover" o "revertir"

                if username_to_change and action:
                    user_to_change = Users.query.filter_by(username=username_to_change).first()

                    if user_to_change:
                        if action == "promover":
                            if user_to_change.role != 'admin':
                                user_to_change.role = 'admin'
                                db.session.commit()
                                flash(f"Usuario {username_to_change} promovido correctamente.")
                            else:
                                flash(f"Usuario {username_to_change} ya es administrador.")
                        elif action == "revertir":
                            if user_to_change.role == 'admin':
                                user_to_change.role = 'user'
                                db.session.commit()
                                flash(f"Usuario {username_to_change} revertido correctamente.")
                            else:
                                flash(f"Usuario {username_to_change} no es administrador.")
                        else:
                            flash("Acción no válida.")
                    else:
                        flash(f"Usuario {username_to_change} no encontrado.")

            return render_template("files.html", Var='promo')
        else:
            flash("No tienes permisos para acceder a esta sección.")
            return render_template("index.html")
    else:
        flash('Por favor, inicie sesión para acceder a esta sección.')
        return redirect(url_for('login'))
    


#________________Definir___________________

@app.route("/insert/defautl")
def insert():
    new_post = Posts(title = "LL Consesionaria")
    db.session.add(new_post)
    db.session.commit()
    var = new_post.title
    return f"Fino mano se registro {var}"

@app.route("/select/default")
def select():
    post = Posts.query.filter_by(id_user=3).first()
    nombre = post.title
    print(post, nombre)

    retorno = f"""Query done  // Fino <br>
    nombre del Query: {nombre}<br><br><br>
    <a href="{url_for('index')}">Ir a base</a>
    """
    return retorno

#Cookies

@app.route("/Cookies/set")
def Cookies():
    resp = make_response(render_template("cookies.html"))
    resp.set_cookie("usernames", "Consesio")
    return resp

@app.route("/Cookies/read")
def leer_cookie():
    username = request.cookies.get("username", None)
    if username == None:
        return "No existe"
    return f"{username}"

@app.route("/home")
def home():
    if g.user:
        return "Tu eres %s " % g.user
    
    return "Conectate primero"
    

#Jasons
motos =[
    {
        "id": 1,
        "modelo": "New Owen",
        "serial": 2025
    },
    {
        "id": 2,
        "modelo": "Leon",
        "serial": 2024
    }
]
Vehiculos =[
    {
        "marca": "Chevrolet",
        "modelo": "Aveo",
        "serial": 2025
    },
    {
        "marca": "Honda",
        "modelo": "Civic",
        "serial": 2024
    }
]

@app.route("/jason/vehiculos")
def jason_luis():
    return jsonify({"Ofertas de Vehiculos":{"Motos": motos, "Carros": Vehiculos}})

@app.route("/jason/creditos")
def creditos_f():
    return jsonify(creditos)

@app.route("/jason/2xD")
def j():
    return jsonify({"Carros": carros_normales, "Carros Premium":Vehiculos_premium})

#____________________________Funciones de admin_______________________________--

@app.route("/admin_configLL")
def secret():
    if "username" in session:
        user = Users.query.filter_by(username=session["username"]).first()
        g.usuario_verificacion = user
        if user and user.role != 'user':
            g.hola = session["username"]
            return render_template('admin_config.html', usuario=g.hola, user = user)
        else:
            flash('No tienes permiso para acceder a esta sección.', 'error')
            return redirect(url_for('index'))
        
    else:
        flash('Por favor, inicia sesión para acceder a tu perfil.', 'succes')
        return redirect(url_for('login'))

@app.route("/host")
def host():
    if "username" in session:
        user = Users.query.filter_by(username=session["username"]).first()
        versace = "Cambiar cuenta"
        auto = "no eres admin"
        if user and user.role == 'admin':
            return render_template("host.html", userH = session["username"])
    if "username" not in session:
        versace = "logear"
        auto = "No estas logeado"
    return f"""
    <html>
        <body style="text-align: center; margin-top: 20vh;">
            <div style="border: 1px solid black; padding: 20px; border-radius: 10px; width: fit-content; margin-left:auto;margin-right:auto;">
                {auto}
            </div>
            <p><a href="{ url_for('index') }">Volver al inicio</a></p>
            <p><a href="{ url_for('login') }">{versace}</a></p>
        </body>
    </html>
    """

Up_Car = 'static/uploads/LLCars'  # Carpeta para guardar las imágenes
app.config['Up_Car'] = Up_Car
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/dato_de_vitrina", methods=['GET', 'POST'])
def admin_vitrina():
    if request.method == 'POST':
        print("Formulario recibido")  # Verifica si la función se ejecuta
        marca = request.form['marca']
        modelo = request.form['modelo']
        año = request.form['año']
        precio = request.form['precio']
        imagen = request.files['imagen']
        premium = 'premium' in request.form
        emblema = request.files['emblema'] if premium and 'emblema' in request.files else None

        print(f"Marca: {marca}, Modelo: {modelo}, Año: {año}, Precio: {precio}") # Imprime los datos del formulario
        print(f"Imagen: {imagen}, Premium: {premium}, Emblema: {emblema}") # Imprime las imagenes

        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['Up_Car'], filename))

            if premium and emblema and allowed_file(emblema.filename):
                emblema_filename = secure_filename(emblema.filename)
                emblema.save(os.path.join(app.config['UPLOAD_FOLDER_EMBLEMAS'], emblema_filename))
            else:
                emblema_filename = None

            return redirect(url_for('index'))

    return render_template('db.html')

@app.route("/DocLL")
def Documentacion_LLConsesionaria():
    return render_template("DocLL.html")

@app.route("/politicaLL")
def politicas_condiciones():
    return render_template("cookies.html")
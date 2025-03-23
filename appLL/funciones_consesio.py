def hola():
  print("Hola")

from flask_script import Manager
from appLL import app, db, Users # Importa la aplicación y la base de datos
from werkzeug.security import generate_password_hash, check_password_hash

manager = Manager(app)

@manager.command
def create_admin():
    usuario = {
        "username": input("Usuario: "),
        "email": input("Email: "),
        "password": getpass.getpass("Password: ")
    }
    
    new_user = Users(
        username=usuario['username'],
        email=usuario['email'],
        password=generate_password_hash(usuario['password']),
        role='admin'  # Establece el rol a 'admin'
    )
    
    db.session.add(new_user)
    db.session.commit()


@app.route("/Configuracion/<Var>", methods=["GET", "POST"])  # Esto será para promover al admin
def search(Var):
    if "username" in session:
        user = Users.query.filter_by(username=session["username"]).first()
        if user and user.role == 'admin':
            if request.method == "POST":
                if Var == 'promo':
                    username = request.form.get('username')
                    if username:
                        # Aquí deberías agregar la lógica para promover al usuario en tu base de datos
                        # Por ejemplo: 
                        user_to_promote = Users.query.filter_by(username=username).first()
                        if user_to_promote:
                            user_to_promote.role = 'admin'  # Promover al usuario
                            db.session.commit()  # Guardar cambios en la base de datos
                            flash(f"Usuario {username} promovido correctamente.")
                        else:
                            flash(f"Usuario {username} no encontrado.")
                
                # Redirigir para evitar reenvío del formulario
                return redirect(url_for('search', Var=Var))  
            
            return render_template("files.html", Var=Var)  # Renderizar el mismo template con Var

        else:
            flash("No tienes permisos para acceder a esta sección.")
            return render_template("index.html")
    else:
        flash('Por favor, inicie sesión para acceder a esta sección.')
        return redirect(url_for('login'))
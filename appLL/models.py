from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#______________Modelos___________
class Posts(db.Model): #no me acuerdo que era esta clase
    id_user = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))

class Users(db.Model): #______________Usuarios___________
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    role = db.Column(db.String(20), default='user', nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.email}', '{self.nombre}', '{self.role}')"

    
class news(db.Model): #______________Noticias en index___________
    id = db.Column(db.Integer, primary_key = True)
    fotoUrl = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f'<Noticia {self.titulo}>'

#______________Vehiculos___________

#Base de los Vehiculos
class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    año = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50))  # 'normal', 'premium', 'bajo_cc', 'alto_cc'
    tipo = db.Column(db.String(50))  # 'carro', 'moto'
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    usuario = db.relationship('Users', backref='vehiculos')
    __mapper_args__ = {
        'polymorphic_identity': 'vehiculo',
        'polymorphic_on': tipo
    }

    def __repr__(self):
        return f'<Vehiculo {self.modelo}>'

#___________Vitrina
class Carro(Vehiculo):
    id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), primary_key=True)
    imagen = db.Column(db.String(255))
    __mapper_args__ = {
        'polymorphic_identity': 'carro',
        'polymorphic_on': Vehiculo.categoria, #Polimorfismo por categoria
    }

    def __repr__(self):
        return f'<Carro {self.modelo}>'

class Moto(Vehiculo):
    id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), primary_key=True)
    cilindraje = db.Column(db.Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'moto',
    }

    def __repr__(self):
        return f'<Moto {self.modelo}>'

class VehiculoUsuario(Vehiculo): #VehiculoUsuario hereda de Vehiculo
    id = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), primary_key=True)
    precio_venta = db.Column(db.Integer)  # Puede ser nulo si no está en venta
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_inicio_compartir = db.Column(db.DateTime)  # Puede ser nulo si no se comparte
    fecha_fin_compartir = db.Column(db.DateTime)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    usuario = db.relationship('Users', backref='vehiculos_usuarios')

    __mapper_args__ = {
        'polymorphic_identity': 'vehiculo_usuario',
    }

    def __repr__(self):
        return f'<VehiculoUsuario {self.modelo}>'

class CarroNormal(Carro):
    id = db.Column(db.Integer, db.ForeignKey('carro.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'normal',
    }

    def __repr__(self):
        return f'<CarroNormal {self.modelo}>'

class CarroPremium(Carro):
    id = db.Column(db.Integer, db.ForeignKey('carro.id'), primary_key=True)
    emblema = db.Column(db.String(255))
    __mapper_args__ = {
        'polymorphic_identity': 'premium',
    }

    def __repr__(self):
        return f'<CarroPremium {self.modelo}>'





#___________________Json______________________-

carros_normales = [ # Parametros:  Marca - Modelo - año - precio -- imagen
    { "Marca": "Chevrolet", "Modelo": "Aveo", "año" :2007, "precio": "3.200$", "imagen":"Aveo.jpeg"},
    { "Marca": "Honda", "Modelo": "CiviC", "año" :2016, "precio": "5.600$", "imagen":"Civic.jpeg"},
    { "Marca": "Chevrolet", "Modelo": "Camaron", "año": 2020, "precio": "55.000$", "imagen": "Camaro.jpeg" },
    { "Marca": "Ford", "Modelo": "Fusion", "año": 2017, "precio": "7.200$", "imagen": "Ffusion.jpeg" },
    { "Marca": "Ford", "Modelo": "F150", "año": 2002, "precio": "9.770$", "imagen": "f150.jpeg" }
]

Vehiculos_premium = [ # Parametros: Marca - Modelo - año - precio -- imagen -- Frase emblema
    {"Marca": "Mecedes Benz", "Modelo": "Kompressor", "año": 2024, "imagen": "AMG3.jpg", "precio": "88.000$", "Emblema": "-- Elegancia y comodidad", "id": "AMG3"},
    {"Marca": "Lamborghini", "Modelo": "Murcielago", "año": 2011, "imagen": "murcielago.jpeg","precio": "110.000$","Emblema": "-- Presencia y estatus", "id": "Lambo"},
    {"Marca": "Ford", "Modelo": "Mustang", "año" : 2021, "imagen": "LoveMustang.jpg", "precio": "75.000$", "Emblema": "-- Virtud y Poder", "id": "Mustang3"},
    {"Marca": "BMW", "Modelo": "I7 Sedan", "año" : 2022, "imagen": "BMWSedan.jpg", "precio": "91.000$", "Emblema": "-- Belleza Italica", "id": "Sedan3"}
]

Motos = [ # Parametros: Marca - Modelo - cc - año - precio -- imagen
    {"Marca":"EK", "Modelo":"OwenLL", "cc":150, "año":2025, "precio":"1.250$", "imagen":"OwenLL.jpg"},
    {"Marca":"MD", "Modelo":"Lechuza", "cc":200, "año":2024, "precio":"1660$", "imagen":"HawkMD.jpeg"},
    {"Marca":"HaoJue", "Modelo":"Sx1", "cc":200, "año":2024, "precio":"1.880$", "imagen":"Sx1HJ.jpeg"},
    {"Marca":"EK", "Modelo":"RK", "cc":200, "año":2024, "precio":"1.660$", "imagen":"RK200.jpeg"},
    {"Marca":"Toro", "Modelo":"REX", "cc":250, "año":2025, "precio":"1.920$", "imagen":"ToroRex.jpeg"}

]
motos_altoCC = [ # Parametros: Marca - Modelo - CC - año - precio - Categoria -- imagen
    {"Marca":"Yamaha", "Modelo":"MT 09", "cc":900, "año":2018, "precio":"13.500$", "Categoria":"Naked", "imagen":"MT09.jpeg"},
    {"Marca":"Susuki", "Modelo":"Vstrom", "cc":1000, "año":2023, "precio":"14.950$", "Categoria":"Turismo", "imagen":"Elenfoque.jpg"},
    {"Marca":"Kawasaki", "Modelo":"z900rs", "cc":900, "año":2023, "precio":"20.000$", "Categoria":"Naked classic", "imagen":"z900rs.jpeg"},
    {"Marca":"BMW", "Modelo":"R18", "cc":1800, "año":2025, "precio":"22.980€", "Categoria":"Cruisser", "imagen":"chopperBM.jpg"},
    {"Marca":"BMW", "Modelo":"GS", "cc":1200, "año":2025, "precio":"33.000$", "Categoria":"Adventure", "imagen":"Elenfoque2.jpg"}
]






creditos = [
    {
        "Ref": "Login",
        "Aplicado":"Modelo de Login y Singup",
        "link_ref": "https://codingstella.com/how-to-make-cool-glowing-login-form-using-html-css/#google_vignette"
    },
    {
        "Ref": "Footer",
        "Aplicado":"Modelo de footer",
        "link_ref": "https://www.youtube.com/watch?v=nkZz9DOBzBI"
    },
    {
        "Ref": "Curso Flask",
        "Aplicado": "LL Consesionaria",
        "link_ref": "https://www.youtube.com/playlist?list=PLBO4apWPK7b7K6c-jpEI0zflZYDjVp7cd"
    }
]


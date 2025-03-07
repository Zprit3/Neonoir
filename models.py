from extensions import db
from wtforms.validators import DataRequired
import bcrypt

class Jugador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False, info={'validators': [DataRequired()]})
    contrasena = db.Column(db.String(128), nullable=False)
    puntaje = db.Column(db.Integer, default=0)
    inventario = db.relationship('Inventario', backref='jugador', uselist=False)

    def set_password(self, password):
        self.contrasena = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.contrasena.encode('utf-8'))

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    vida = db.Column(db.Integer, default=100)
    estadistica_principal = db.Column(db.Integer, default=10)
    oro = db.Column(db.Integer, default=0)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))
    objetos_victoria = db.Column(db.Integer, default=0)

class JugadorPersonaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugador.id'), nullable=False)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'), nullable=False)
    activo = db.Column(db.Boolean, default=False)

class Casilla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)

class Tarjeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200))
    tipo = db.Column(db.String(50), nullable=False)
    efecto = db.Column(db.String(200))
    duracion = db.Column(db.Integer)
    unica = db.Column(db.Boolean, default=False)
    valor = db.Column(db.Integer, default=0)
    enemigos = db.relationship('Enemigo', secondary='enemigo_tarjetas', back_populates='tarjetas')

class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tablero_id = db.Column(db.Integer, db.ForeignKey('tablero.id'), nullable=False)
    estado = db.Column(db.String(50), default='en curso')

class Enemigo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    vida = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    ataque = db.Column(db.Integer, default=10)
    oro_drop = db.Column(db.Integer, default=0)
    tarjetas = db.relationship('Tarjeta', secondary='enemigo_tarjetas', back_populates='enemigos')
    es_jefe = db.Column(db.Boolean, default=False)

class EnemigoTarjetas(db.Model):
    enemigo_id = db.Column(db.Integer, db.ForeignKey('enemigo.id'), primary_key=True)
    tarjeta_id = db.Column(db.Integer, db.ForeignKey('tarjeta.id'), primary_key=True)

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200))
    avance_casillas = db.Column(db.Integer, default=0)
    modificacion_oro = db.Column(db.Integer, default=0)
    modificacion_vida = db.Column(db.Integer, default=0)
    debuff_estadistica = db.Column(db.String(50))
    duracion_debuff_casillas = db.Column(db.Integer, default=0)
    npc_id = db.Column(db.Integer, db.ForeignKey('npc.id'))

class Zona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_zona = db.Column(db.String(20), nullable=False)

    recuperacion_vida = db.Column(db.Integer, default=0)
    limpiar_debuffs = db.Column(db.Boolean, default=False)
    probabilidad_objeto_victoria = db.Column(db.Integer, default=0)

    modificacion_vida = db.Column(db.Integer, default=0)
    debuff_estadistica = db.Column(db.String(50))
    retorno_zona_descanso = db.Column(db.Boolean, default=False)

    descripcion = db.Column(db.String(200))

class Npc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    dialogo = db.Column(db.Text)

class ObjetoVictoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200))
    cantidad_necesaria = db.Column(db.Integer, default=5)
    probabilidad_caida = db.Column(db.Float, default=0.0)
    probabilidad_caida_zona = db.Column(db.Float, default=0.0)

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugador.id'))
    fragmentos = db.relationship('FragmentoInventario', backref='inventario', lazy=True)

    def contar_fragmentos(self):
        return len(self.fragmentos)

class FragmentoInventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))
    objeto_victoria_id = db.Column(db.Integer, db.ForeignKey('objeto_victoria.id'))

class CasillaEstado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partida_id = db.Column(db.Integer, db.ForeignKey('partida.id'), nullable=False)
    casilla_id = db.Column(db.Integer, db.ForeignKey('casilla.id'), nullable=False)
    contenido_id = db.Column(db.Integer)
    contenido_tipo = db.Column(db.String(50))

class PersonajePartida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partida_id = db.Column(db.Integer, db.ForeignKey('partida.id'), nullable=False)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'), nullable=False)
    posicion = db.Column(db.Integer, default=0)
    vida = db.Column(db.Integer)
    debuffs = db.Column(db.JSON, default={})
    zonas_visitadas = db.Column(db.JSON, default=[])
    probabilidad_objeto_victoria = db.Column(db.Integer, default=1)

class PersonajeTarjetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'), nullable=False)
    tarjeta_id = db.Column(db.Integer, db.ForeignKey('tarjeta.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)

class Tablero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    casillas = db.Column(db.Text, nullable=False)

class CasillaContenido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    casilla_id = db.Column(db.Integer, db.ForeignKey('casilla.id'), nullable=False)
    contenido_id = db.Column(db.Integer)
    contenido_tipo = db.Column(db.String(50))

class Tienda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    tarjetas_venta = db.Column(db.JSON, default=[])

class InventarioTarjetas(db.Model):
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'), primary_key=True)
    tarjeta_id = db.Column(db.Integer, db.ForeignKey('tarjeta.id'), primary_key=True)
    cantidad = db.Column(db.Integer, default=1)
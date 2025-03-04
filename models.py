from extensions import db

class Jugador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasena = db.Column(db.String(120), nullable=False)
    puntaje = db.Column(db.Integer, default=0)

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jugadorId = db.Column(db.Integer, db.ForeignKey('jugador.id'), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    vida = db.Column(db.Integer, default=100)
    estadisticaPrincipal = db.Column(db.Integer, default=10)
    oro = db.Column(db.Integer, default=0)

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


class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tableroId = db.Column(db.Integer, db.ForeignKey('tablero.id'), nullable=False)
    estado = db.Column(db.String(50), default='en curso')

class Enemigo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    vida = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    oroDrop = db.Column(db.Integer, default=0)
    tarjetaDropId = db.Column(db.Integer, db.ForeignKey('tarjeta.id'))

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200))
    avanceCasillas = db.Column(db.Integer, default=0)
    modificacionOro = db.Column(db.Integer, default=0)
    modificacionVida = db.Column(db.Integer, default=0)
    debuffEstadistica = db.Column(db.String(50))
    duracionDebuffCasillas = db.Column(db.Integer, default=0)
    npcId = db.Column(db.Integer, db.ForeignKey('npc.id'))

class Zona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipoZona = db.Column(db.String(20), nullable=False) # "positiva", "negativa", "neutra"

    # Campos para Zonas Positivas
    recuperacionVida = db.Column(db.Integer, default=0)
    limpiarDebuffs = db.Column(db.Boolean, default=False)
    probabilidadObjetoVictoria = db.Column(db.Integer, default=0)

    # Campos para Zonas Negativas
    modificacionVida = db.Column(db.Integer, default=0)
    debuffEstadistica = db.Column(db.String(50))
    retornoZonaDescanso = db.Column(db.Boolean, default=False)

    # Campos para Zonas Neutras
    descripcion = db.Column(db.String(200))

class Npc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    dialogo = db.Column(db.Text)

class ObjetoVictoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200))

class CasillaEstado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partidaId = db.Column(db.Integer, db.ForeignKey('partida.id'), nullable=False)
    casillaId = db.Column(db.Integer, db.ForeignKey('casilla.id'), nullable=False)
    contenidoId = db.Column(db.Integer)
    contenidoTipo = db.Column(db.String(50))

class PersonajePartida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partidaId = db.Column(db.Integer, db.ForeignKey('partida.id'), nullable=False)
    personajeId = db.Column(db.Integer, db.ForeignKey('personaje.id'), nullable=False)
    posicion = db.Column(db.Integer, default=0)
    vida = db.Column(db.Integer)

class PersonajeTarjetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personajeId = db.Column(db.Integer, db.ForeignKey('personaje.id'), nullable=False)
    tarjetaId = db.Column(db.Integer, db.ForeignKey('tarjeta.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)

class Tablero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    casillas = db.Column(db.Text, nullable=False) # Guarda el tablero como JSON o texto

class CasillaContenido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    casillaId = db.Column(db.Integer, db.ForeignKey('casilla.id'), nullable=False)
    contenidoId = db.Column(db.Integer)
    contenidoTipo = db.Column(db.String(50))
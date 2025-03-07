import random
from models import Casilla, CasillaContenido, Zona, Enemigo, Evento, Npc, Tienda, Tablero, CasillaEstado
from extensions import db
from app import socketio

def generar_tablero(partida, tamano_tablero, dificultad):
    """Genera un tablero de juego con casillas aleatorias."""

    # Cálculo de porcentajes según dificultad
    dificultades = {
        "facil": {"neutras": 0.60, "eventos": 0.15, "enemigos": 0.15, "tiendas": 0.05, "npcs": 0.05, "positivas": 0.03, "negativas": 0.02, "enemigo_tipo": "debil"},
        "normal": {"neutras": 0.50, "eventos": 0.20, "enemigos": 0.20, "tiendas": 0.05, "npcs": 0.05, "positivas": 0.02, "negativas": 0.03, "enemigo_tipo": "normal"},
        "dificil": {"neutras": 0.40, "eventos": 0.25, "enemigos": 0.25, "tiendas": 0.03, "npcs": 0.02, "positivas": 0.01, "negativas": 0.04, "enemigo_tipo": "fuerte"},
    }

    if dificultad not in dificultades:
        dificultad = "normal"  # Dificultad por defecto

    config = dificultades[dificultad]

    cant_neutras = int(tamano_tablero * config["neutras"])
    cant_eventos = int(tamano_tablero * config["eventos"])
    cant_enemigos = int(tamano_tablero * config["enemigos"])
    cant_tiendas = int(tamano_tablero * config["tiendas"])
    cant_npcs = int(tamano_tablero * config["npcs"])
    cant_positivas = int(tamano_tablero * config["positivas"])
    cant_negativas = int(tamano_tablero * config["negativas"])
    enemigo_tipo = config["enemigo_tipo"]

    # Crear y guardar las casillas
    casillas = []
    for _ in range(tamano_tablero):
        casilla = Casilla()  # creamos la casilla
        db.session.add(casilla)  # agregamos la casilla a la base de datos
        db.session.flush()  # fuerzo el autoincremento
        casillas.append(casilla)

    # Crear una instancia de Tablero
    nuevo_tablero = Tablero()
    db.session.add(nuevo_tablero)
    db.session.flush()

    # Casilla de inicio
    casilla_inicio = CasillaContenido(casillaId=casillas[0].id, contenidoTipo="inicio")
    db.session.add(casilla_inicio)
    db.session.flush()
    casilla_estado = CasillaEstado(partidaId=partida.id, casillaId=casillas[0].id, contenidoId=casilla_inicio.id, contenidoTipo="inicio")
    db.session.add(casilla_estado)
    casillas.pop(0)

    # Casilla de descanso
    casilla_descanso = CasillaContenido(casillaId=casillas[-1].id, contenidoTipo="descanso")
    db.session.add(casilla_descanso)
    db.session.flush()
    casilla_estado = CasillaEstado(partidaId=partida.id, casillaId=casillas[-1].id, contenidoId=casilla_descanso.id, contenidoTipo="descanso")
    db.session.add(casilla_estado)
    casillas.pop()

    # Generar contenido de casillas de forma aleatoria según porcentajes
    casillas_disponibles = casillas
    random.shuffle(casillas_disponibles)  # randomizamos las casillas disponibles

    # Obtener datos de la base de datos
    zonas_neutras = Zona.query.filter_by(tipoZona="neutra").all()
    eventos = Evento.query.all()
    enemigos = Enemigo.query.filter_by(tipo=enemigo_tipo).all()  # filtrar por dificultad
    tiendas = Tienda.query.all()
    npcs = Npc.query.all()
    zonas_positivas = Zona.query.filter_by(tipoZona="positiva").all()
    zonas_negativas = Zona.query.filter_by(tipoZona="negativa").all()

    contenidos = {
        "zona_neutra": (zonas_neutras, "zona", cant_neutras),
        "evento": (eventos, "evento", cant_eventos),
        "enemigo": (enemigos, "enemigo", cant_enemigos),
        "tienda": (tiendas, "tienda", cant_tiendas),
        "npc": (npcs, "npc", cant_npcs),
        "zona_positiva": (zonas_positivas, "zona", cant_positivas),
        "zona_negativa": (zonas_negativas, "zona", cant_negativas),
    }

    for tipo, (lista_contenidos, tipo_contenido, cantidad) in contenidos.items():
        for _ in range(min(cantidad, len(casillas_disponibles), len(lista_contenidos))):
            casilla = casillas_disponibles.pop()
            contenido = random.choice(lista_contenidos)
            casilla_contenido = CasillaContenido(casillaId=casilla.id, contenidoTipo=tipo_contenido, contenidoId=contenido.id)
            db.session.add(casilla_contenido)
            db.session.flush()
            casilla_estado = CasillaEstado(partidaId=partida.id, casillaId=casilla.id, contenidoId=casilla_contenido.id, contenidoTipo=tipo_contenido)
            db.session.add(casilla_estado)

    # Guardar el tablero en la partida
    partida.tableroId = nuevo_tablero.id
    nuevo_tablero.casillas = [casilla.id for casilla in casillas]

    db.session.commit()
    socketio.emit('tablero_generado', {'partida_id': partida.id, 'tablero_id': nuevo_tablero.id}, room=partida.id) #emitir tablero generado.
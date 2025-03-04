import random
from models import Casilla, CasillaContenido, Zona, Enemigo, Evento, Npc, Tienda
from extensions import db

def generar_tablero(tamano_tablero, dificultad):
    tablero = []
    #calculo de porcentajes segun dificultad
    if dificultad == "facil":
        cant_neutras = int(tamano_tablero * 0.60)
        cant_eventos = int(tamano_tablero * 0.15)
        cant_enemigos = int(tamano_tablero * 0.15)
        cant_tiendas = int(tamano_tablero * 0.05)
        cant_npcs = int(tamano_tablero * 0.05)
        cant_positivas = int(tamano_tablero * 0.03)
        cant_negativas = int(tamano_tablero * 0.02)
        enemigo_vida = 8
        enemigo_tipo = "debil"
    elif dificultad == "dificil":
        cant_neutras = int(tamano_tablero * 0.40)
        cant_eventos = int(tamano_tablero * 0.25)
        cant_enemigos = int(tamano_tablero * 0.25)
        cant_tiendas = int(tamano_tablero * 0.03)
        cant_npcs = int(tamano_tablero * 0.02)
        cant_positivas = int(tamano_tablero * 0.01)
        cant_negativas = int(tamano_tablero * 0.04)
        enemigo_vida = 15
        enemigo_tipo = "fuerte"
    else: #dificultad normal
        cant_neutras = int(tamano_tablero * 0.50)
        cant_eventos = int(tamano_tablero * 0.20)
        cant_enemigos = int(tamano_tablero * 0.20)
        cant_tiendas = int(tamano_tablero * 0.05)
        cant_npcs = int(tamano_tablero * 0.05)
        cant_positivas = int(tamano_tablero * 0.02)
        cant_negativas = int(tamano_tablero * 0.03)
        enemigo_vida = 10
        enemigo_tipo = "normal"

    #generar casillas
    for i in range(tamano_tablero):
        casilla = Casilla(id=i)
        tablero.append(casilla)

    #casilla de inicio
    casilla_inicio = CasillaContenido(casillaId = 0, contenidoTipo = "inicio")
    db.session.add(casilla_inicio)

    #generar contenido de casillas de forma aleatoria segun porcentajes
    casillas_disponibles = list(range(1, tamano_tablero)) #excluimos la primera casilla que es de inicio
    random.shuffle(casillas_disponibles) #randomizamos las casillas disponibles

    #obtener datos de la base de datos
    zonas_neutras = Zona.query.filter_by(tipoZona="neutra").all()
    eventos = Evento.query.all()
    enemigos = Enemigo.query.filter_by(tipo=enemigo_tipo).all() #filtrar por dificultad
    tiendas = Tienda.query.all()
    npcs = Npc.query.all()
    zonas_positivas = Zona.query.filter_by(tipoZona="positiva").all()
    zonas_negativas = Zona.query.filter_by(tipoZona="negativa").all()

    #generar zonas neutras
    for i in range(cant_neutras):
        if casillas_disponibles and zonas_neutras:
            casilla_id = casillas_disponibles.pop()
            zona = random.choice(zonas_neutras) #seleccionar zona aleatoria
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "zona", contenidoId = zona.id)
            db.session.add(casilla_contenido)

    #generar eventos
    for i in range(cant_eventos):
        if casillas_disponibles and eventos:
            casilla_id = casillas_disponibles.pop()
            evento = random.choice(eventos)
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "evento", contenidoId = evento.id)
            db.session.add(casilla_contenido)

    #generar enemigos
    for i in range(cant_enemigos):
        if casillas_disponibles and enemigos:
            casilla_id = casillas_disponibles.pop()
            enemigo = random.choice(enemigos)
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "enemigo", contenidoId = enemigo.id)
            db.session.add(casilla_contenido)

    #generar tiendas
    for i in range(cant_tiendas):
        if casillas_disponibles and tiendas:
            casilla_id = casillas_disponibles.pop()
            tienda = random.choice(tiendas)
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "tienda", contenidoId = tienda.id)
            db.session.add(casilla_contenido)

    #generar npcs
    for i in range(cant_npcs):
        if casillas_disponibles and npcs:
            casilla_id = casillas_disponibles.pop()
            npc = random.choice(npcs)
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "npc", contenidoId = npc.id)
            db.session.add(casilla_contenido)

    #generar zonas positivas
    for i in range(cant_positivas):
        if casillas_disponibles and zonas_positivas:
            casilla_id = casillas_disponibles.pop()
            zona = random.choice(zonas_positivas)
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "zona", contenidoId = zona.id)
            db.session.add(casilla_contenido)

    #generar zonas negativas
    for i in range(cant_negativas):
        if casillas_disponibles and zonas_negativas:
            casilla_id = casillas_disponibles.pop()
            zona = random.choice(zonas_negativas)
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "zona", contenidoId = zona.id)
            db.session.add(casilla_contenido)

    db.session.commit()
    return tablero
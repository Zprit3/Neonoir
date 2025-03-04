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

    #generar zonas neutras
    for i in range(cant_neutras):
        if casillas_disponibles:
            casilla_id = casillas_disponibles.pop()
            zona = Zona(tipoZona = "neutra", descripcion = "Zona neutra")
            db.session.add(zona)
            db.session.flush() #obtener el id de la zona recien creada
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "zona", contenidoId = zona.id)
            db.session.add(casilla_contenido)

    #generar eventos
    for i in range(cant_eventos):
        if casillas_disponibles:
            casilla_id = casillas_disponibles.pop()
            evento = Evento(nombre = "Evento aleatorio", descripcion = "Descripcion aleatoria")
            db.session.add(evento)
            db.session.flush()
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "evento", contenidoId = evento.id)
            db.session.add(casilla_contenido)

    #generar enemigos
    for i in range(cant_enemigos):
        if casillas_disponibles:
            casilla_id = casillas_disponibles.pop()
            enemigo = Enemigo(nombre = "Enemigo aleatorio", vida = enemigo_vida, tipo = enemigo_tipo) #agregar dificultad
            db.session.add(enemigo)
            db.session.flush()
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "enemigo", contenidoId = enemigo.id)
            db.session.add(casilla_contenido)

    #generar tiendas
    for i in range(cant_tiendas):
        if casillas_disponibles:
            casilla_id = casillas_disponibles.pop()
            tienda = Tienda(nombre = "Tienda aleatoria", tarjetas_venta = []) #agregar tarjetas a la venta
            db.session.add(tienda)
            db.session.flush()
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "tienda", contenidoId = tienda.id)
            db.session.add(casilla_contenido)

    #generar npcs
    for i in range(cant_npcs):
        if casillas_disponibles:
            casilla_id = casillas_disponibles.pop()
            npc = Npc(nombre = "Npc aleatorio", dialogo = "Dialogo aleatorio")
            db.session.add(npc)
            db.session.flush()
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "npc", contenidoId = npc.id)
            db.session.add(casilla_contenido)

    #generar zonas positivas
    for i in range(cant_positivas):
        if casillas_disponibles:
            casilla_id = casillas_disponibles.pop()
            zona = Zona(tipoZona = "positiva", recuperacionVida = 10, probabilidadObjetoVictoria = 1)
            db.session.add(zona)
            db.session.flush()
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "zona", contenidoId = zona.id)
            db.session.add(casilla_contenido)

    #generar zonas negativas
    for i in range(cant_negativas):
        if casillas_disponibles:
            casilla_id = casillas_disponibles.pop()
            zona = Zona(tipoZona = "negativa", modificacionVida = -10, retornoZonaDescanso = True)
            db.session.add(zona)
            db.session.flush()
            casilla_contenido = CasillaContenido(casillaId = casilla_id, contenidoTipo = "zona", contenidoId = zona.id)
            db.session.add(casilla_contenido)

    db.session.commit()
    return tablero
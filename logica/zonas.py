from extensions import db
from models import PersonajePartida, Zona, CasillaContenido, Casilla
import random

def aplicar_efecto_zona(personaje, zona, partida_id):
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje.id).first()

    if zona.tipoZona == 'positiva':
        # Recuperación de vida
        personaje_partida.vida += zona.recuperacionVida

        # Limpieza de debuffs
        personaje_partida.debuffs = {}  # Elimina todos los debuffs

        # Objeto de victoria
        if zona.probabilidadObjetoVictoria > 0:
            if random.randint(1, 100) <= personaje_partida.probabilidad_objeto_victoria:
                # Lógica para otorgar el objeto de victoria
                pass
            else:
                # Aumentar la probabilidad
                personaje_partida.probabilidad_objeto_victoria += 5  # Aumenta un 5%

        # Agregar zona a la lista de zonas visitadas
        personaje_partida.zonas_visitadas.append(zona.id)

    elif zona.tipoZona == 'negativa':
        # Modificación de vida (negativa)
        personaje_partida.vida += zona.modificacionVida

        # Debuff de estadística
        if zona.debuffEstadistica:
            personaje_partida.debuffs[zona.debuffEstadistica] = 3  # Duración de 3 casillas

        # Retorno a zona de descanso
        if zona.retornoZonaDescanso and personaje_partida.zonas_visitadas:
            zona_descanso_id = personaje_partida.zonas_visitadas[-1]  # Última zona visitada
            zona_descanso = Zona.query.get(zona_descanso_id)
            if zona_descanso:
                # Mover al personaje a la casilla de la zona de descanso
                casilla_descanso = CasillaContenido.query.filter_by(contenidoId=zona_descanso_id, contenidoTipo='zona').first()
                if casilla_descanso:
                    personaje_partida.posicion = casilla_descanso.casillaId - 1 # se resta 1 para que al moverse, caiga en la casilla.
                    personaje_partida.zonas_visitadas.pop() # elimina la ultima zona visitada
            else:
                print('Zona de descanso no encontrada')

    elif zona.tipoZona == 'neutra':
        print(zona.descripcion)

    db.session.commit()
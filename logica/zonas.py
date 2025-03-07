from extensions import db
from logica.condiciones_victoria import verificar_condiciones_victoria
from models import FragmentoInventario, Inventario, PersonajePartida, Zona, CasillaContenido, ObjetoVictoria
import random
from app import socketio

def aplicar_efecto_zona(personaje, zona, partida_id):
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje.id).first()

    if zona.tipoZona == 'positiva':
        # Recuperación de vida
        personaje_partida.vida += zona.recuperacionVida

        # Limpieza de debuffs
        personaje_partida.debuffs = {}  # Elimina todos los debuffs

        # Objeto de victoria
        objeto_victoria = ObjetoVictoria.query.first()
        if objeto_victoria:
            if random.random() < objeto_victoria.probabilidad_caida_zona:
                print("¡Has encontrado un fragmento de Neonoir en la zona!")
                # Agregar fragmento al inventario del jugador
                inventario = Inventario.query.filter_by(jugador_id=personaje.jugadorId).first()
                if inventario:
                    fragmento = FragmentoInventario(inventario_id=inventario.id, objeto_victoria_id=objeto_victoria.id)
                    db.session.add(fragmento)
                verificar_condiciones_victoria(partida_id, personaje.id) # llamada corregida
            else:
                print("No has encontrado nada en la zona.")
            objeto_victoria.probabilidad_caida_zona += 0.001 #aumenta en 0.1% la probabilidad por zona positiva visitada.

        # Agregar zona a la lista de zonas visitadas
        personaje_partida.zonas_visitadas.append(zona.id)
        socketio.emit('zona_positiva_visitada', {'personaje_id': personaje.id, 'zona_id': zona.id}, room=partida_id) #emitir visita a zona positiva.

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
                    personaje_partida.zonas_visitadas.pop()  # elimina la ultima zona visitada
            else:
                print('Zona de descanso no encontrada')
        socketio.emit('zona_negativa_visitada', {'personaje_id': personaje.id, 'zona_id': zona.id}, room=partida_id) #emitir visita a zona negativa.

    elif zona.tipoZona == 'neutra':
        objeto_victoria = ObjetoVictoria.query.first()
        if objeto_victoria:
            if random.random() < objeto_victoria.probabilidad_caida_zona:
                print("¡Has encontrado un fragmento de Neonoir en la zona!")
                # Agregar fragmento al inventario del jugador
                inventario = Inventario.query.filter_by(jugador_id=personaje.jugadorId).first()
                if inventario:
                    fragmento = FragmentoInventario(inventario_id=inventario.id, objeto_victoria_id=objeto_victoria.id)
                    db.session.add(fragmento)
                verificar_condiciones_victoria(partida_id, personaje.id) # llamada corregida
            else:
                print("No has encontrado nada en la zona.")
            objeto_victoria.probabilidad_caida_zona += 0.001 #aumenta en 0.1% la probabilidad por zona neutra visitada.
        socketio.emit('zona_neutra_visitada', {'personaje_id': personaje.id, 'zona_id': zona.id}, room=partida_id) #emitir visita a zona neutra.

    db.session.commit()
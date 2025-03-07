from extensions import db
from logica.condiciones_victoria import verificar_condiciones_victoria
from models import FragmentoInventario, Inventario, Personaje, Enemigo, PersonajePartida, ObjetoVictoria
import random
from logica.dados import lanzar_dados  # Importar la función
from app import socketio

def iniciar_combate(partida_id, personaje_id, enemigo_id):
    personaje_partida = PersonajePartida.query.filter_by(partidaId=partida_id, personajeId=personaje_id).first()
    personaje = Personaje.query.get(personaje_id)
    enemigo = Enemigo.query.get(enemigo_id)

    # Ataque del personaje
    dado1_personaje, dado2_personaje, total_dados_personaje = lanzar_dados()
    dano_personaje = personaje.estadisticaPrincipal + total_dados_personaje
    if dado1_personaje == 6 and dado2_personaje == 6:
        dano_personaje = int(dano_personaje * 1.3)  # Daño crítico
    enemigo.vida -= dano_personaje

    # Ataque del enemigo
    dado1_enemigo, dado2_enemigo, total_dados_enemigo = lanzar_dados()
    dano_enemigo = enemigo.ataque + total_dados_enemigo #utilizar la estadistica de ataque
    if dado1_enemigo == 6 and dado2_enemigo == 6:
        dano_enemigo = int(dano_enemigo * 1.3)  # Daño crítico
    personaje_partida.vida -= dano_enemigo

    if enemigo.es_jefe and enemigo.vida <= 0:
        objeto_victoria = ObjetoVictoria.query.first()
        if objeto_victoria:
            if random.random() < objeto_victoria.probabilidad_caida:
                print("¡Has obtenido un fragmento de Neonoir!")
                # Agregar fragmento al inventario del jugador
                inventario = Inventario.query.filter_by(jugador_id=personaje.jugadorId).first()
                if inventario:
                    fragmento = FragmentoInventario(inventario_id=inventario.id, objeto_victoria_id=objeto_victoria.id)
                    db.session.add(fragmento)
                verificar_condiciones_victoria(inventario)
            else:
                print("El jefe no ha soltado el fragmento de Neonoir.")
            objeto_victoria.probabilidad_caida += 0.05
    db.session.commit()

    socketio.emit('combate_resultado', {
        "daño_personaje": dano_personaje,
        "dados_personaje": (dado1_personaje, dado2_personaje),
        "daño_enemigo": dano_enemigo,
        "dados_enemigo": (dado1_enemigo, dado2_enemigo),
        "vida_personaje": personaje_partida.vida,
        "vida_enemigo": enemigo.vida,
        "enemigo_id": enemigo_id,
        "personaje_id": personaje_id
    }, room=partida_id) #emitir resultado del combate.

    return {
        "daño_personaje": dano_personaje,
        "dados_personaje": (dado1_personaje, dado2_personaje),
        "daño_enemigo": dano_enemigo,
        "dados_enemigo": (dado1_enemigo, dado2_enemigo),
        "vida_personaje": personaje_partida.vida,
        "vida_enemigo": enemigo.vida,
    }